import google.generativeai as genai
from tqdm import tqdm
import pandas as pd
import re
import json
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from numpy.lib.stride_tricks import sliding_window_view
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import TimeSeriesSplit
from skopt import BayesSearchCV
from sklearn.metrics import mean_squared_error, make_scorer, mean_absolute_error
from sklearn.neural_network import MLPRegressor

knn_bs = joblib.load("modelo_knn_bs.pkl") # Para cargar el modelo

def knn_predict(data):
    # Preprocess the data
    data = pd.DataFrame(data)
    data = data.dropna()
    data = data.reset_index(drop=True)

    # Normalize the data
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    predictions = knn_bs.predict(data_scaled)

    # Inverse transform the predictions to get the original scale
    predictions = scaler.inverse_transform(predictions)

    return predictions.tolist()  # Convert to list for JSON serialization
