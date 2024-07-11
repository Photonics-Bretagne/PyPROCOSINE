# define the root path of the repo in the sys path 
import sys
import os
sys.path.append(f'..{os.sep}..')

# import the core of procosine
from pyprocosine.core.procosine_library import *


pro=Procosine() # create a Procosine class
pro.loading_simulation_paramaters("simulation_parameters.json") # Load simulation paraametrs from the json file in conf folder 
pro.procosine_simulation() # Run the procosine simulation 
pro.show_simulation_result() # plto teh results of teh simulation 



