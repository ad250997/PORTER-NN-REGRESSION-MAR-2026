from pydantic import BaseModel

class OrderData(BaseModel):

    created_at: str
    actual_delivery_time: str

    total_items: int
    subtotal: float
    num_distinct_items: int

    min_item_price: float
    max_item_price: float

    total_onshift_dashers: int
    total_busy_dashers: int
    total_outstanding_orders: int

    estimated_store_to_consumer_driving_duration: float

    market_id: int
    store_primary_category: int
    order_protocol: int