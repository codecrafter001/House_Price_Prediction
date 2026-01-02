import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load dataset
df = pd.read_csv("housing_price_data.csv")

# Features and target
X = df[["area", "bedrooms", "bathrooms", "parking"]]
y = df["price"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save trained model
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("✅ model.pkl generated successfully")
