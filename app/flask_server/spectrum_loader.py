import os
import json
import numpy as np
import pandas as pd
from flask import Blueprint, request, jsonify

# Définition du dossier d'upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Variables globales pour stocker les spectres chargés
loaded_wavelengths = None
loaded_reflectances = None

# Création d'un blueprint Flask pour éviter l'importation circulaire
spectrum_loader = Blueprint('spectrum_loader', __name__)

# Fonction pour charger un spectre depuis différents formats
def load_spectrum(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".npy":
        data = np.load(file_path)
        if data.shape[1] != 2:
            raise ValueError("Fichier .npy invalide : doit contenir 2 colonnes (wavelengths, reflectances).")
        return data[:, 0].astype(float), data[:, 1].astype(float)  # Force en float
    
    elif ext in [".csv", ".txt", ".dat"]:
        df = pd.read_csv(file_path, delim_whitespace=True if ext != ".csv" else ",", header=None, dtype=float)
        if df.shape[1] != 2:
            raise ValueError(f"Fichier {ext} invalide : doit contenir 2 colonnes (wavelengths, reflectances).")
        print(np.size(df.iloc[:, 0].values.astype(float)))
        return df.iloc[:, 0].values.astype(float), df.iloc[:, 1].values.astype(float)  # Force en float
    
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path, header=None, dtype=float)
        if df.shape[1] != 2:
            raise ValueError("Fichier Excel invalide : doit contenir 2 colonnes (wavelengths, reflectances).")
        return df.iloc[:, 0].values.astype(float), df.iloc[:, 1].values.astype(float)  # Force en float
    
    elif ext == ".json":
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if "wavelengths" not in data or "reflectances" not in data:
            raise ValueError("Fichier JSON invalide : doit contenir 'wavelengths' et 'reflectances'.")
        return np.array(data["wavelengths"], dtype=float), np.array(data["reflectances"], dtype=float)  # Force en float
    
    else:
        raise ValueError(f"Format de fichier non supporté : {ext}")
    
    

# Route Flask pour gérer l'upload et chargement du spectre
@spectrum_loader.route('/load-spectrum', methods=['POST'])
def load_spectrum_route():
    global loaded_wavelengths, loaded_reflectances
    if 'file' not in request.files:
        return jsonify({"message": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    try:
        loaded_wavelengths, loaded_reflectances = load_spectrum(file_path)
        return jsonify({"message": f"File {file.filename} uploaded and loaded successfully!"})
    except Exception as e:
        return jsonify({"message": f"Error loading file: {str(e)}"}), 500
    
def get_loaded_wavelengths():
    return loaded_wavelengths

def get_loaded_reflectances():
    return loaded_reflectances
