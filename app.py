from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load trained ML model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# ---------------- STATE ----------------
prediction_count = 0
last_prediction = None
# --------------------------------------

@app.route("/")
def home():
    return {
        "message": "🏠 Stateful House Price Prediction API",
        "total_predictions": prediction_count,
        "last_prediction": last_prediction
    }

@app.route("/predict", methods=["POST"])
def predict():
    global prediction_count, last_prediction

    data = request.get_json()

    area = data["area"]
    bedrooms = data["bedrooms"]
    bathrooms = data["bathrooms"]
    parking = data["parking"]

    price = model.predict([[area, bedrooms, bathrooms, parking]])[0]

    prediction_count += 1

    last_prediction = {
        "area": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "parking": parking,
        "predicted_price": round(price, 2)
    }

    return jsonify({
        "predicted_price": round(price, 2),
        "prediction_number": prediction_count
    })
