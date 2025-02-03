import os
import sys
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Utilisation du backend sans interface graphique

from spectrum_loader import load_spectrum_route
from spectrum_loader import get_loaded_wavelengths, get_loaded_reflectances




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

def create_sim_plot(wl, inv_spectrum):
    if inv_spectrum is None:
        return None
    fig, ax = plt.subplots()
    ax.plot(wl, inv_spectrum, label="Simulated Spectrum", color='blue')
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

app.add_url_rule('/load-spectrum', 'load_spectrum_route', load_spectrum_route, methods=['POST'])

# Fonction pour créer une image pour l'inversion
def create_inversion_plot(proco):
    fig, ax = plt.subplots()
    
    ax.plot(proco.wl, proco.spectrum, linewidth=2.5, color=(0.75, 0.75, 0.99), label='Measured Pseudo-BRF')
    ax.plot(proco.wl, proco.inversion_spectrum, linestyle=':', linewidth=1.5, color=(0, 0, 0.7), label='Inverted Pseudo-BRF')
    
    ax.set_xlabel('Wavelength (nm)', fontsize=16, weight='bold')
    ax.set_ylabel('Pseudo Bidirectional Reflectance Factor', fontsize=16, weight='bold')
    ax.set_title(str(proco.inversion_result)[1:-1].replace("'", ""), weight='bold')

    ax.set_xlim(min(proco.wl), max(proco.wl))
    ax.set_ylim(0, 1)
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)

    return image_base64


@app.route('/')
def home():
    return render_template('home.html', plot_url=None)  # Aucune simulation au démarrage

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
        return redirect(url_for('home'))  # Ne lance pas la simulation automatiquement

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
        return redirect(url_for('home'))  # Ne lance pas la simulation automatiquement

    config = load_config(SIMULATION_CONFIG_FILE_PATH)
    return render_template('simulation_parameter.html', config=config)

app.add_url_rule('/load-spectrum', 'load_spectrum_route', load_spectrum_route, methods=['POST'])

@app.route('/run-simulation', methods=['POST'])
def run_simulation():
    try:
        pro = proco.Procosine()
        pro.loading_simulation_paramaters(SIMULATION_CONFIG_FILE_PATH)
        pro.procosine_simulation()

        plot_url = create_sim_plot(pro.data[:, 0], pro.simulated_spectrum)
        return jsonify({'plot_url': plot_url})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/run-inversion', methods=['POST'])
def run_inversion():
    try:
        loaded_wavelengths = get_loaded_wavelengths()
        loaded_reflectances = get_loaded_reflectances()

        if loaded_wavelengths is None or loaded_reflectances is None:
            return jsonify({'error': "No spectrum loaded"})

        pro = proco.Procosine()
        pro.loading_inversion_parameters(INVERSION_CONFIG_FILE_PATH)
        pro.wl = loaded_wavelengths
        pro.spectrum = loaded_reflectances
        pro.procosine_inversion()

        plot_url = create_inversion_plot(pro)
        return jsonify({'plot_url': plot_url})

    except Exception as e:
        return jsonify({'error': str(e)})






if __name__ == '__main__':
    app.run(debug=True)
