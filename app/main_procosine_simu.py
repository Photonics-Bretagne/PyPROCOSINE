from pyprocosine.core.procosine_library import *

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) 
conf_path = os.path.join(ROOT_DIR, "conf", "simulation_parameters.json")
print()
pro=Procosine() # create a Procosine class
pro.loading_simulation_parameters(conf_path ) # Load simulation paraametrs from the json file in conf folder 
pro.procosine_simulation() # Run the procosine simulation 
pro.show_simulation_result() # plto teh results of teh simulation 



