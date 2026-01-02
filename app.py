from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load ML model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# ---------------- STATE ----------------
prediction_count = 0
chat_count = 0
# --------------------------------------

@app.route("/")
def home():
    return {
        "message": "🏠 House Price Prediction API with Chatbot",
        "total_predictions": prediction_count,
        "total_chat_messages": chat_count
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
    prediction_count += 1

    return jsonify({
        "predicted_price": round(price, 2),
        "prediction_number": prediction_count
    })

# ---------------- CHATBOT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    global chat_count
    chat_count += 1

    user_message = request.get_json().get("message", "").lower()

    if "price" in user_message:
        reply = "House price is predicted using area, bedrooms, bathrooms, and parking."

    elif "how" in user_message or "work" in user_message:
        reply = "I use a trained Linear Regression model to estimate house prices."

    elif "input" in user_message or "feature" in user_message:
        reply = "Please provide area, number of bedrooms, bathrooms, and parking spaces."

    elif "hello" in user_message or "hi" in user_message:
        reply = "Hello! 👋 I can help you predict house prices."

    else:
        reply = "I'm here to assist with house price prediction. Ask me about inputs or pricing."

    return jsonify({
        "reply": reply,
        "chat_number": chat_count
    })
