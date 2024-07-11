#define the root path on teh root of the repo
import sys
import os
sys.path.append(f'..{os.sep}..')
print(sys.path)

#import the core of procosine
import pyprocosine.core.procosine_library as proco

pro=proco.Procosine() # create a Procosine Class 
pro.loading_inversion_parameters("inversion_parameters.json") # load inversion paraametrs from the json file in conf folder
pro.load_spectrum("example_spectrum.npy","example_wavelengths.npy") # load spectrum and wavelengths from the spectrum_example folder

"""Apply Procosine inversion """
# The "TolFun" parameter has to be tuned depending on signal SNR (low
# tolerance for low SNRs and vice versa)

pro.procosine_inversion() # run the procosine inversion 
pro.show_inversion_result() #plot and print the procosine inversion results 


