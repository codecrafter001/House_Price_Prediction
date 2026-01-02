from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# ---------------- LOAD MODEL SAFELY ----------------
try:
    with open("model.pkl", "rb") as file:
        model = pickle.load(file)
except Exception as e:
    model = None
    print("Model loading failed:", e)

# ---------------- STATE ----------------
prediction_count = 0
chat_count = 0
# -------------------------------------

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "predictions": prediction_count,
        "chat_messages": chat_count
    })

# ---------------- PREDICTION ----------------
@app.route("/predict", methods=["POST"])
def predict():
    global prediction_count

    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    try:
        area = float(data["area"])
        bedrooms = int(data["bedrooms"])
        bathrooms = int(data["bathrooms"])
        parking = int(data["parking"])
    except Exception:
        return jsonify({"error": "Invalid input values"}), 400

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

    data = request.get_json(silent=True)
    if not data or "message" not in data:
        return jsonify({"reply": "Please send a message"}), 400

    chat_count += 1
    user_message = str(data["message"]).lower()

    if "price" in user_message:
        reply = "House price is predicted using area, bedrooms, bathrooms, and parking."
    elif "how" in user_message:
        reply = "I use a trained Linear Regression model to estimate house prices."
    elif "input" in user_message:
        reply = "You need area, bedrooms, bathrooms, and parking to predict a price."
    elif "hello" in user_message or "hi" in user_message:
        reply = "Hello 👋 I can help you with house price prediction."
    else:
        reply = "Ask me about price prediction or required inputs."

    return jsonify({
        "reply": reply,
        "chat_number": chat_count
    })
