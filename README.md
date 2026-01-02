## House Price Prediction (Stateful API)

A Flask + Machine Learning API that predicts house prices and keeps
server-side state (number of predictions made).

### Features
- Linear Regression model
- Stateful backend (in-memory counter)
- Production-ready (Gunicorn)

### Endpoint
POST /predict

Request JSON:
{
  "area": 1500,
  "bedrooms": 3,
  "bathrooms": 2,
  "parking": 1
}

Response:
{
  "predicted_price": 11800000.0,
  "prediction_number": 5
}
