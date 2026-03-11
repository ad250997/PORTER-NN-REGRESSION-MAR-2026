from fastapi import FastAPI
from tensorflow.keras.models import load_model
import pandas as pd

from preprocessing import preprocess
from schemas import OrderData

app = FastAPI(
    title="Delivery Time Prediction API",
    description="Neural Network regression model for delivery time prediction",
    version="1.0"
)

model = load_model("model/porter_best_model.keras")


@app.get("/")
def root():
    return {"message": "Delivery Time Prediction API running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def predict(order: OrderData):

    # convert API input → dataframe
    df = pd.DataFrame([order.model_dump()])

    # preprocessing pipeline
    model_inputs = preprocess(df)

    # prediction
    prediction = model.predict(model_inputs)

    return {
        "predicted_delivery_time": float(prediction[0][0])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)