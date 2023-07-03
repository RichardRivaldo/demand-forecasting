import datetime
import holidays
import pandas as pd
from joblib import load


def generate_features(
    menu_group: str, n_weeks: int, include_deals: bool
) -> pd.DataFrame:
    today_date = datetime.datetime.today()
    nw_start_date = today_date + datetime.timedelta(days=7 - today_date.weekday())
    features_df = pd.DataFrame(
        {"dates": pd.date_range(nw_start_date, periods=n_weeks * 7)}
    )

    features_df = _add_time_features(features_df)
    features_df = _add_holiday_and_weekend(features_df)
    features_df = _fill_details(menu_group, include_deals, features_df)

    encoder = load("assets/encoder.joblib")
    encoded = encoder.transform(features_df[["menu_group"]])
    features_df[encoder.categories_[0]] = encoded.toarray()

    return features_df


def drop_derived_features(features_df: pd.DataFrame) -> pd.DataFrame:
    features_df = features_df.drop(["dates", "menu_group"], axis=1)
    return features_df


def _add_time_features(features_df: pd.DataFrame) -> pd.DataFrame:
    features_df["year"] = features_df["dates"].dt.year
    features_df["month"] = features_df["dates"].dt.month
    features_df["week"] = features_df["dates"].dt.isocalendar().week.astype("int64")
    features_df["day_of_month"] = features_df["dates"].dt.day
    features_df["day_of_week"] = features_df["dates"].dt.dayofweek
    features_df["day_of_year"] = features_df["dates"].dt.dayofyear

    return features_df


def _add_holiday_and_weekend(features_df: pd.DataFrame) -> pd.DataFrame:
    features_df["is_holiday"] = features_df.apply(
        lambda x: x["dates"] in holidays.country_holidays("ID"), axis=1
    )
    features_df["is_weekend"] = features_df.apply(
        lambda x: x["day_of_week"] in [5, 6], axis=1
    )
    return features_df


def _fill_details(
    menu_group: str, include_deals: bool, features_df: pd.DataFrame
) -> pd.DataFrame:
    features_df["include_deals"] = include_deals
    features_df["menu_group"] = menu_group

    return features_df
