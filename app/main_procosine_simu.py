import sys
import os

current_dir = os.path.dirname(__file__)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# import the core of procosine
from core.procosine_library import *


pro=Procosine() # create a Procosine class
pro.loading_simulation_paramaters("simulation_parameters.json") # Load simulation paraametrs from the json file in conf folder 
pro.procosine_simulation() # Run the procosine simulation 
pro.show_simulation_result() # plto teh results of teh simulation 



