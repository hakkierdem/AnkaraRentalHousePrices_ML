from src.data_processing import FeatureEngineering

import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import numpy as np


pipeline = joblib.load("ankara_house_rent_pipeline_simple.pkl")

st.title("🏠 Ankara House Prices Prediction")

st.write("""
Bu uygulama, girdiğiniz ev özelliklerine göre Ankara'daki ev fiyatını tahmin eder.
""")


st.sidebar.header("Ev Özellikleri")

county_coords = {
    'Akyurt': {'latitude': 40.123403769999996, 'longitude': 33.06471565},
    'Altındağ': {'latitude': 39.96369218214286, 'longitude': 32.89223272142857},
    'Etimesgut': {'latitude': 39.93201155869565, 'longitude': 32.6155145},
    'Gölbaşı': {'latitude': 39.80639137714286, 'longitude': 32.75467427142857},
    'Keçiören': {'latitude': 39.989206893893126, 'longitude': 32.84398646641222},
    'Mamak': {'latitude': 39.92237966694215, 'longitude': 32.91080730247934},
    'Polatlı': {'latitude': 39.58011607291667, 'longitude': 32.13985315625},
    'Pursaklar': {'latitude': 40.049855990322584,'longitude': 32.908875483870965},
    'Sincan': {'latitude': 39.966589574257426, 'longitude': 32.56716298118812},
    'Yenimahalle': {'latitude': 39.970875757499996, 'longitude': 32.765185521875},
    'Çankaya': {'latitude': 39.89420821053922, 'longitude': 32.81809600098039},
    'Çubuk': {'latitude': 40.16099275714286, 'longitude': 32.996489864285714}
}


county = st.selectbox("İlçe seçiniz", list(county_coords.keys()))

m2 = st.sidebar.number_input("Metrekare", min_value=10, max_value=300, value=100)
room = st.sidebar.number_input("Oda Sayısı", min_value=1, max_value=5, value=3)
saloon = st.sidebar.number_input("Salon Sayısı", min_value=0, max_value=3, value=1)


input_df = pd.DataFrame({
    "m2": [m2],
    "Room": [room],
    "Saloon": [saloon],
    "County": [county]
})

prediction = pipeline.predict(input_df)[0]
st.subheader(f"Tahmini fiyat: {prediction:,.0f} TL",)


feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
importances = pipeline.named_steps["model"].feature_importances_

indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10,6))
plt.bar(range(len(importances)), importances[indices])
plt.xticks(range(len(importances)), np.array(feature_names)[indices], rotation=90)
plt.title("Feature Importances")
plt.savefig("feature_importance.png", dpi=300, bbox_inches="tight")


sorted_idx = np.argsort(importances)[::-1]

for idx in sorted_idx[:10]:
    print(feature_names[idx], importances[idx])


house_data = pd.read_csv("data/ankara_house_prices.csv")


model = pipeline.named_steps["model"]
importances = model.feature_importances_
print(importances)



