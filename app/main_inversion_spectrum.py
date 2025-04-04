import pyprocosine.core.procosine_library as proco
import os 
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) 
conf_path = os.path.join(ROOT_DIR, "conf", "inversion_parameters.json")
spectrum_path=os.path.join(ROOT_DIR,"spectra_example","example_spectrum.npy")
wl_path=os.path.join(ROOT_DIR,"spectra_example","example_wavelengths.npy")

pro=proco.Procosine() # create a Procosine Class 
pro.loading_inversion_parameters(conf_path) # load inversion paraametrs from the json file in conf folder
pro.load_spectrum(spectrum_path,wl_path) # load spectrum and wavelengths from the spectrum_example folder

"""Apply Procosine inversion """
# The "TolFun" parameter has to be tuned depending on signal SNR (low
# tolerance for low SNRs and vice versa)

pro.procosine_inversion() # run the procosine inversion 
pro.show_inversion_result() #plot and print the procosine inversion results 


