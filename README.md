# demand-forecasting

Demand Forecasting Experiments

# Description

API service for retail demand forecasting application with `XGBoost` and `FastAPI`.

# Implementation

1. The notebook in `experiments` directory contains experiment with the demand forecasting problem. Data manipulation is mostly done using `Pandas` and `Scikit-Learn`.
2. Model used in the experiment is `XGBoost`, a gradient boosting algorithm that can be used for time-series problems, although it requires several preprocessing first. Done some research on another time-series models such as `ARIMA`, `SARIMAX`, `Prophet`, and `LSTM`, but decided to move with XGBoost, solely because of curiosity in purpose of making XGBoost work for time-series analysis.
3. Since we have daily time-series data, the implemented approach of the model itself is by doing daily forecast, and in the end, sum all of the demand forecasted to create a weekly forecast. Note that the forecast will always start at the starting date of the next week.
4. The services used to serve the model is built with `FastAPI` and `Uvicorn`. This is done as simple as saving all models needed for inferencing and mimicking the evaluation process on the notebook.
5. The functionality is then made into an API that can be accessed through HTTP network protocol.

**The model is uploaded into the repository for simplicity sake. Read [Improvements](#improvements).**

# Setup

## Local Environment

Run the `run.sh` script. This will install all dependencies of the program and immediately run an `Uvicorn` server at port `8000`.

## Dockerized

Use `docker-compose up [-d]` to build the image and run a container on the image built. Use `-d` flag to run it in detached mode. The specification of the container is as follows.

```
base: python:3.9
CPU: 2 cores
Memory: 8G
Exposed Port(s): 8000 -> 11005
```

# Endpoints

```
POST /api/v1/forecast
{
    "menu_group": str,
    "n_weeks": int,
    "include_deals": Optional[bool]
}
```

**Note: `include_deals` is used if for example, the user wants to forecast the demand while also planning deals / promotions for the menu group. Will default to `false` if not specified.**

```
Successful Response
{
    "status_code": 200,
    "results": List[int]
}

Error Response
{
    "status_code": 500,
    "results": <error_message>
}
```

# Improvements

1. More detailed experiments, such as more EDA to find the time-series type of the data (which is very fluential in determining the chosen model), removing outliers, finding correlation of generated features, data imputation / interpolation, etc.
2. Better features engineering, such as introduction of lag features (result of previous data is used as input to current data), detailed features regarding product state (regarding promotions or deals), proper data split, and encoding result.
3. Same item ID doesn't correspond to same item name, in my opinion, can be problematic in long run and should be handled since data generation phase if possible.
4. Benchmark and compare several models for the current implementation to find best algorithm / architecture.
5. Create a setup script to download the models as a setup phase, from Google Drive or GCP for example. This way, the model doesn't need to be uploaded to the repository.

# Interesting Reads

1. Modern Time Series Forecasting with Python by Manu Joseph
2. [A real-world example of predicting Sales volume using XGBoost with GridSearch on a JupyterNotebook](https://medium.com/@oemer.aslantas/a-real-world-example-of-predicting-sales-volume-using-xgboost-with-gridsearch-on-a-jupyternotebook-c6587506128d)
3. [XGBoost For Time Series Forecasting: Don’t Use It Blindly](https://towardsdatascience.com/xgboost-for-time-series-forecasting-dont-use-it-blindly-9ac24dc5dfa9)
4. [Predicting Electricity Consumption with XGBRegressor](https://towardsdatascience.com/predicting-electricity-consumption-with-xgbregressor-a11b71104754)
5. [https://towardsdatascience.com/predicting-electricity-consumption-with-xgbregressor-a11b71104754](https://machinelearningmastery.com/xgboost-for-time-series-forecasting/)
6. [A Guide to Time Series Forecasting in Python](https://builtin.com/data-science/time-series-forecasting-python)
7. [A Guide to Time Series Forecasting with ARIMA in Python 3](https://www.digitalocean.com/community/tutorials/a-guide-to-time-series-forecasting-with-arima-in-python-3)
8. [PT2: Time Series Forecasting with XGBoost](https://www.kaggle.com/code/robikscube/pt2-time-series-forecasting-with-xgboost/notebook#3.-Lag-Features)
9. [Store Item Demand forecasting](https://www.kaggle.com/code/salmaneunus/store-item-demand-forecasting/notebook)
10. [Store Item Demand Forecasting Challenge](https://www.kaggle.com/code/nafisur/store-item-demand-forecasting-challenge/notebook)
