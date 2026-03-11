import joblib
import numpy as np
import pandas as pd

scaler = joblib.load("artifacts/scaler.pkl")
cat_maps = joblib.load("artifacts/categorical_mappings.pkl")

def preprocess(data):

    data = data.copy()

    data["created_at"] = pd.to_datetime(data["created_at"])
    data["actual_delivery_time"] = pd.to_datetime(data["actual_delivery_time"])

    data["hour_of_day"] = data["created_at"].dt.hour
    data["day_of_week"] = data["created_at"].dt.day_of_week

    data = data.drop(columns=["created_at","actual_delivery_time"])

    data["hour_of_day_sin"] = np.sin(2*np.pi*data["hour_of_day"]/24)
    data["hour_of_day_cos"] = np.cos(2*np.pi*data["hour_of_day"]/24)

    data["day_of_week_sin"] = np.sin(2*np.pi*data["day_of_week"]/7)
    data["day_of_week_cos"] = np.cos(2*np.pi*data["day_of_week"]/7)

    data = data.drop(columns=["hour_of_day","day_of_week"])

    num_cols = [
        'total_items','subtotal','num_distinct_items',
        'min_item_price','max_item_price',
        'total_onshift_dashers','total_busy_dashers',
        'total_outstanding_orders',
        'estimated_store_to_consumer_driving_duration',
        'hour_of_day_sin','hour_of_day_cos',
        'day_of_week_sin','day_of_week_cos'
    ]

    cat_cols = [
        'market_id',
        'store_primary_category',
        'order_protocol'
    ]

    data[num_cols] = scaler.transform(data[num_cols])

    for col in cat_cols:
        data[col] = data[col].map(cat_maps[col]).fillna(0).astype("int32")

    inputs = {
        "num_input": data[num_cols].values
    }

    for col in cat_cols:
        inputs[f"{col}_input"] = data[col].values.reshape(-1,1)

    return inputs