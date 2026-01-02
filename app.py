from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Property Value Forecaster</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #6b6fd7, #7b3fe4);
            padding: 40px;
            color: #fff;
        }
        .card {
            background: white;
            color: #333;
            max-width: 900px;
            margin: auto;
            border-radius: 12px;
            padding: 30px;
        }
        h1 {
            text-align: center;
            color: #fff;
            margin-bottom: 20px;
        }
        h2 {
            text-align: center;
            color: #6a4df4;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #ccc;
        }
        button {
            margin-top: 20px;
            padding: 12px;
            width: 100%;
            background: #6a4df4;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        .result {
            margin-top: 30px;
            background: #0fb67a;
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
        }
    </style>
</head>

<body>
    <h1>🏠 Property Value Forecaster</h1>

    <div class="card">
        <h2>Property Details</h2>

        <form method="post">
            <div class="grid">
                <input type="number" name="area" placeholder="Area (sq ft)" required>
                <input type="number" name="bedrooms" placeholder="Bedrooms" required>
                <input type="number" name="bathrooms" placeholder="Bathrooms" required>

                <input type="number" name="stories" placeholder="Stories" required>
                <select name="mainroad">
                    <option value="1">Main Road: Yes</option>
                    <option value="0">Main Road: No</option>
                </select>
                <select name="guestroom">
                    <option value="1">Guest Room: Yes</option>
                    <option value="0">Guest Room: No</option>
                </select>

                <select name="basement">
                    <option value="1">Basement: Yes</option>
                    <option value="0">Basement: No</option>
                </select>
                <select name="aircon">
                    <option value="1">Air Conditioning: Yes</option>
                    <option value="0">Air Conditioning: No</option>
                </select>
                <input type="number" name="parking" placeholder="Parking Spaces" required>
            </div>

            <button type="submit">Predict Property Value</button>
        </form>

        {% if price %}
        <div class="result">
            Estimated Property Value<br>
            ₹{{ price }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    price = None

    if request.method == "POST":
        area = int(request.form["area"])
        bedrooms = int(request.form["bedrooms"])
        bathrooms = int(request.form["bathrooms"])
        stories = int(request.form["stories"])
        parking = int(request.form["parking"])

        mainroad = int(request.form["mainroad"])
        guestroom = int(request.form["guestroom"])
        basement = int(request.form["basement"])
        aircon = int(request.form["aircon"])

        # Simple price logic (demo purpose)
        price = (
            area * 3500 +
            bedrooms * 500000 +
            bathrooms * 300000 +
            stories * 400000 +
            parking * 200000 +
            (mainroad + guestroom + basement + aircon) * 250000
        )

        price = f"{price:,.0f}"

    return render_template_string(HTML_TEMPLATE, price=price)

if __name__ == "__main__":
    app.run(debug=True)
