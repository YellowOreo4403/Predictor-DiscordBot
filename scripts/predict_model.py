import os
import pickle
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model_prediksi.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def predict_price(luas_rumah, luas_tanah, kamar, kamar_mandi, usia, lantai):
    data = np.array([[luas_rumah, luas_tanah, kamar, kamar_mandi, usia, lantai]])
    return model.predict(data)[0]