import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_values(df, target_column, periods=5):
    df = df.dropna(subset=[target_column])

    # Create time index
    df["time_index"] = np.arange(len(df))

    X = df[["time_index"]]
    y = df[target_column]

    model = LinearRegression()
    model.fit(X, y)

    future_index = np.arange(len(df), len(df) + periods).reshape(-1, 1)
    predictions = model.predict(future_index)

    return predictions
