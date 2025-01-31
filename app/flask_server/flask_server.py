import os
import sys
import json
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Utilisation du backend sans interface graphique

# Définition du chemin du projet depuis la racine
current_dir = os.path.dirname(__file__)
root_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(root_path)

import core.procosine_library as proco

INVERSION_CONFIG_FILE_PATH = os.path.join(root_path, 'conf', 'inversion_parameters.json')
SIMULATION_CONFIG_FILE_PATH = os.path.join(root_path, 'conf', 'simulation_parameters.json')

# Initialisation de l'application Flask
app = Flask(__name__)

# Fonction pour charger la configuration JSON tout en conservant le bon format des nombres
def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config  # Ne pas modifier les types ici pour préserver le format d'origine

# Fonction pour sauvegarder la configuration JSON sans altérer le format d'origine
def save_config(config, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

# Fonction pour générer un graphique et retourner une image encodée en base64
def create_plot(data):
    fig, ax = plt.subplots()
    ax.plot(data, label="Simulated Spectrum")
    ax.set_title("Procosine Simulation")
    ax.set_xlabel("Wavelength")
    ax.set_ylabel("Intensity")
    ax.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return image_base64

@app.route('/')
def home():
    simulated_spectrum = None
    try:
        pro = proco.Procosine()
        pro.loading_simulation_paramaters("simulation_parameters.json")
        pro.procosine_simulation()
        simulated_spectrum = pro.simulated_spectrum
    except Exception as e:
        print(f"Erreur lors de la simulation : {e}")

    plot_url = create_plot(simulated_spectrum) if simulated_spectrum is not None else None
    return render_template('home.html', plot_url=plot_url)

@app.route('/inversion-parameter', methods=['GET', 'POST'])
def inversion_parameter():
    if request.method == 'POST':
        config = load_config(INVERSION_CONFIG_FILE_PATH)
        for key in config.keys():
            if key in request.form:
                try:
                    config[key] = json.loads(request.form[key])  # Convertir au bon format
                except ValueError:
                    config[key] = request.form[key]  # Garder la valeur brute si conversion impossible
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
                try:
                    config[key] = json.loads(request.form[key])  # Convertir au bon format
                except ValueError:
                    config[key] = request.form[key]  # Garder la valeur brute si conversion impossible
        save_config(config, SIMULATION_CONFIG_FILE_PATH)
        return redirect(url_for('simulation_parameter'))

    config = load_config(SIMULATION_CONFIG_FILE_PATH)
    return render_template('simulation_parameter.html', config=config)

@app.route('/run-simulation', methods=['POST'])
def run_simulation():
    pro = proco.Procosine()  # create a Procosine class
    pro.loading_simulation_paramaters("simulation_parameters.json")  # Load simulation parameters from the json file in conf folder
    pro.procosine_simulation()  # Run the Procosine simulation
    print(np.size(pro.simulated_spectrum))
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)