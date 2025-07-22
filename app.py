import streamlit as st
import pickle
import json
import numpy as np

# Load model
with open("bengaluru_house_prices.pickle", "rb") as f:
    model = pickle.load(f)

# Load column data
with open("columns.json", "r") as f:
    data_columns = json.load(f)['data_columns']

# Extract locations from column names
locations = data_columns[3:]  # first 3 columns are total_sqft, bath, bhk

# Streamlit UI
st.title("🏠 Bengaluru House Price Predictor")

# User Inputs
st.write("#### Enter the house details below:")
total_sqft = st.number_input("Total Square Feet", min_value=300, max_value=10000, step=50)
bath = st.slider("Number of Bathrooms", 1, 10, 2)
bhk = st.slider("Number of BHK", 1, 10, 3)
location = st.selectbox("Location", sorted(locations))

# Prediction logic
def predict_price(location, sqft, bath, bhk):
    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(model.predict([x])[0], 2)

# Predict button
if st.button("Predict Price"):
    predicted_price = predict_price(location, total_sqft, bath, bhk)
    st.success(f"🏡 Estimated Price: ₹ {predicted_price} Lakhs")
