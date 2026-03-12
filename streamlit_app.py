import streamlit as st
import requests
import joblib
from datetime import datetime

API_URL = "http://127.0.0.1:8000/predict"

st.title("Delivery Time Prediction")

order_date = st.date_input("Order Date")
order_time = st.time_input("Order Time")

created_at = datetime.combine(order_date, order_time)
created_at = str(created_at.strftime("%Y-%m-%d %H:%M:%S"))

total_items = st.number_input("Total Items", min_value=1)
subtotal = st.number_input("Subtotal", min_value=1)
num_distinct_items = st.number_input("Distinct Items",min_value=1)

min_item_price = st.number_input("Min Item Price", min_value=1)
max_item_price = st.number_input("Max Item Price", min_value=1)

total_onshift_dashers = st.number_input("Dashers On Shift", min_value=0)
total_busy_dashers = st.number_input("Busy Dashers", min_value=0, max_value=total_onshift_dashers)
total_outstanding_orders = st.number_input("Outstanding Orders", min_value=0)

estimated_store_to_consumer_driving_duration = st.number_input("Driving Duration", min_value=1)

cat_unique_values = joblib.load('cat_unique_values.pkl')
market_id = st.selectbox('Market ID', cat_unique_values['market_id'], 0)

store_primary_category = st.selectbox('Store Primary Category', cat_unique_values['store_primary_category'], 0)

order_protocol = st.selectbox('Order Protocol', cat_unique_values['order_protocol'], 0)

if st.button("Predict"):

    payload = {
        "created_at": created_at,
        "total_items": total_items,
        "subtotal": subtotal,
        "num_distinct_items": num_distinct_items,
        "min_item_price": min_item_price,
        "max_item_price": max_item_price,
        "total_onshift_dashers": total_onshift_dashers,
        "total_busy_dashers": total_busy_dashers,
        "total_outstanding_orders": total_outstanding_orders,
        "estimated_store_to_consumer_driving_duration": estimated_store_to_consumer_driving_duration,
        "market_id": market_id,
        "store_primary_category": store_primary_category,
        "order_protocol": order_protocol
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        prediction = response.json()["predicted_delivery_time"]
        st.success(f"Predicted Delivery Time: {prediction:.0f} minutes")
    else:
        st.error("Prediction failed. Please Check the Inputs again.")