from unittest import result
import pandas as pd
from xgboost import XGBRegressor

from utils.feature_generator import drop_derived_features
from typing import List


def forecast(features_df: pd.DataFrame) -> List[int]:
    xgb = XGBRegressor()
    xgb.load_model("assets/model.json")

    pred_features = drop_derived_features(features_df)

    result_df = pd.DataFrame(
        {"dates": features_df["dates"].dt.date, "forecast": xgb.predict(pred_features)}
    )
    result_df["dates"] = pd.to_datetime(result_df["dates"], format="%Y-%m-%d")
    result_df = result_df.groupby([pd.Grouper(key="dates", freq="W")]).sum()

    forecast_result = result_df["forecast"].to_list()
    forecast_result = [round(forecast) for forecast in forecast_result]

    return forecast_result
