import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

df = pd.read_csv("housing_price_data.csv")

X = df[["area", "bedrooms", "bathrooms", "parking"]]
y = df["price"]

model = LinearRegression()
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))
print("✅ model.pkl created")
