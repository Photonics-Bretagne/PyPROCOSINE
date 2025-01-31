
import os
import sys
import json
from flask import Flask, render_template, request, redirect, url_for

# Définition du chemin du projet depuis la racine
current_dir = os.path.dirname(__file__)
root_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(root_path)

INVERSION_CONFIG_FILE_PATH = os.path.join(root_path, 'conf', 'inversion_parameters.json')
SIMULATION_CONFIG_FILE_PATH = os.path.join(root_path, 'conf', 'simulation_parameters.json')

# Initialisation de l'application Flask
app = Flask(__name__)

# Fonction pour charger la configuration JSON
def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Fonction pour sauvegarder la configuration JSON
def save_config(config, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/inversion-parameter', methods=['GET', 'POST'])
def inversion_parameter():
    if request.method == 'POST':
        config = load_config(INVERSION_CONFIG_FILE_PATH)
        for key in config.keys():
            if key in request.form:
                config[key] = request.form[key]
        save_config(config, INVERSION_CONFIG_FILE_PATH)
        return redirect(url_for('inversion_parameter'))

    config = load_config(INVERSION_CONFIG_FILE_PATH)
    return render_template('inversion_parameter.html', config=config)

@app.route('/simulation-parameter', methods=['GET', 'POST'])
def simulation_parameter():
    if request.method == 'POST':
        config = load_config(SIMULATION_CONFIG_FILE_PATH)
        for key in config.keys():
            if key in request.form:
                config[key] = request.form[key]
        save_config(config, SIMULATION_CONFIG_FILE_PATH)
        return redirect(url_for('simulation_parameter'))

    config = load_config(SIMULATION_CONFIG_FILE_PATH)
    return render_template('simulation_parameter.html', config=config)

if __name__ == '__main__':
    app.run(debug=True)
