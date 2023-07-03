from fastapi import APIRouter, status
from models.demand_forecasting.demand_forecasting import forecast

from dtypes.request import Request
from utils.feature_generator import generate_features

router = APIRouter(prefix="/api/v1")


@router.get("/")
async def home():
    return {"status_code": status.HTTP_200_OK, "results": "Pong!"}


@router.post("/forecast")
async def forecast_demand(request: Request):
    try:
        menu_group = request.menu_group
        n_weeks = request.n_weeks
        include_deals = request.include_deals

        features_df = generate_features(menu_group, n_weeks, include_deals)
        result = forecast(features_df)

        return {"status_code": status.HTTP_200_OK, "results": result}
    except Exception as e:
        return {
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "results": f"Error, reason: {e}",
        }
