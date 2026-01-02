from flask import Flask, request, jsonify, render_template_string
import pickle

app = Flask(__name__)

# -------- Load ML Model --------
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# -------- State --------
prediction_count = 0
chat_count = 0

# -------- Home / Health Check --------
@app.route("/")
def home():
    return {
        "status": "running",
        "predictions": prediction_count,
        "chat_messages": chat_count
    }

# -------- Prediction (GET + POST) --------
@app.route("/predict", methods=["GET", "POST"])
def predict():
    global prediction_count

    # Browser-friendly form
    if request.method == "GET":
        return render_template_string("""
        <h2>🏠 House Price Prediction</h2>
        <form method="post">
            Area: <input name="area" type="number" required><br><br>
            Bedrooms: <input name="bedrooms" type="number" required><br><br>
            Bathrooms: <input name="bathrooms" type="number" required><br><br>
            Parking: <input name="parking" type="number" required><br><br>
            <button type="submit">Predict</button>
        </form>
        <hr>
        <h3>🤖 Need help?</h3>
        <p>Go to <code>/chat</code> endpoint for chatbot assistance</p>
        """)

    # POST (JSON or form)
    try:
        data = request.get_json(silent=True)

        if data:
            area = float(data["area"])
            bedrooms = int(data["bedrooms"])
            bathrooms = int(data["bathrooms"])
            parking = int(data["parking"])
        else:
            area = float(request.form["area"])
            bedrooms = int(request.form["bedrooms"])
            bathrooms = int(request.form["bathrooms"])
            parking = int(request.form["parking"])

        price = model.predict([[area, bedrooms, bathrooms, parking]])[0]
        prediction_count += 1

        return {
            "predicted_price": round(price, 2),
            "prediction_number": prediction_count
        }

    except Exception as e:
        return {"error": "Invalid input"}, 400

# -------- Chatbot Assistance --------
@app.route("/chat", methods=["GET", "POST"])
def chat():
    global chat_count

    # Browser help page
    if request.method == "GET":
        return render_template_string("""
        <h2>🤖 House Prediction Assistant</h2>
        <form method="post">
            Ask a question:<br><br>
            <input name="message" type="text" required style="width:300px"><br><br>
            <button type="submit">Ask</button>
        </form>
        """)

    chat_count += 1
    data = request.get_json(silent=True)

    if data:
        message = data.get("message", "").lower()
    else:
        message = request.form.get("message", "").lower()

    if "price" in message:
        reply = "House price depends on area, bedrooms, bathrooms, and parking."
    elif "how" in message:
        reply = "I use a trained Machine Learning model (Linear Regression)."
    elif "input" in message or "feature" in message:
        reply = "You need area, bedrooms, bathrooms, and parking."
    elif "hello" in message or "hi" in message:
        reply = "Hello 👋 I can help you predict house prices."
    else:
        reply = "Ask me about house price prediction or required inputs."

    return {
        "reply": reply,
        "chat_number": chat_count
    }
