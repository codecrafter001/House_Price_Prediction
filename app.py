from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load ML model
model = pickle.load(open("model.pkl", "rb"))

# -------- STATE (in-memory) --------
prediction_count = 0
# ----------------------------------

@app.route("/")
def home():
    return {
        "message": "🏠 House Price Prediction API is live",
        "total_predictions": prediction_count
    }

@app.route("/predict", methods=["POST"])
def predict():
    global prediction_count
    data = request.get_json()

    area = data["area"]
    bedrooms = data["bedrooms"]
    bathrooms = data["bathrooms"]
    parking = data["parking"]

    price = model.predict([[area, bedrooms, bathrooms, parking]])[0]

    # Update state
    prediction_count += 1

    return jsonify({
        "predicted_price": round(price, 2),
        "prediction_number": prediction_count
    })
