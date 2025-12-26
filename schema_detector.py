import pandas as pd

def detect_schema(df: pd.DataFrame):
    schema = {}

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            schema[col] = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            schema[col] = "datetime"
        else:
            schema[col] = "categorical"

    return schema
