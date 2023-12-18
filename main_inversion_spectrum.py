from procosine_library import *
import numpy as np
from scipy import optimize as opt
import scipy.io
import os
import glob
import scipy.interpolate
import matplotlib.pyplot as plt
from uncertainties import ufloat 
import json


"""Loading inversion parameters"""

with open("inversion_parameters.json", 'r') as f:
            inversion_param  = json.load(f) 

path_spectra=inversion_param["path_spectra"]
path_wl=inversion_param["path_wl"]

# P0=[N,Cab,Car,Cbrown,Cw,Cm,Thetai,Bspec]
P0=np.array(inversion_param["P0"])
LB=np.array(inversion_param["LB"])
UB=np.array(inversion_param["UB"])

gtol=inversion_param["gtol"]
xtol=inversion_param["xtol"]
ftol=inversion_param["ftol"]

spectre=np.load(path_spectra)
spectre=0.6*spectre[0,:]
wl=np.load(path_wl)

Thetas=int(inversion_param["Thetas"])
data= dataSpec_P5B()
spline=scipy.interpolate.CubicSpline(data[:,0],data) # Resampling to the actual spectral sampling interval of the measurement
data = np.squeeze(spline(wl))

"""Apply Procosine inversion """
# The "TolFun" parameter has to be tuned depending on signal SNR (low
# tolerance for low SNRs and vice versa)
func=Procosine(Thetas,data)
popt,pcov=opt.curve_fit(func.procosine,xdata=wl,ydata=spectre,p0=P0,bounds=(LB,UB),method='trf',gtol=gtol,xtol=xtol,ftol=ftol)
rsim=procosine([wl,Thetas,data],*popt)


"""Plotting Result"""
sigma_sol=np.sqrt(np.diagonal(pcov))


# format parameter errors
N = ufloat(popt[0], sigma_sol[0])
Cab = ufloat(popt[1], sigma_sol[1])
Ccx = ufloat(popt[2], sigma_sol[2])
Cbp = ufloat(popt[3], sigma_sol[3])
Cw = ufloat(popt[4], sigma_sol[4])
Cdm = ufloat(popt[5], sigma_sol[5])
Thetai = ufloat(popt[6], sigma_sol[6])
bspec = ufloat(popt[7], sigma_sol[7])
text_res = "Best fit parameters:\nN = {}\nCab = {}\nCcx = {}\nCbp = {}\nCw = {}\nCdm = {}\nThetai = {}\nbspec = {}".format(N,Cab,Ccx,Cbp,Cw,Cdm,Thetai,bspec)
print(text_res)


plt.figure()
line1,=plt.plot(wl,spectre,linewidth=2.5,color=[0.75,0.75,0.99],label='Measured Pseudo-BRF')
line2,=plt.plot(wl,rsim,':',linewidth=1.5,color=[0,0,0.7],label='Inverted Pseudo-BRF')
plt.legend(handles=[line1,line2])   
plt.xlabel('Wavelength (nm)',fontsize=16,weight='bold')
plt.ylabel('Pseudo Bidirectional Reflectance Factor',fontsize=16,weight='bold')
plt.title('N = '+'{:04.2f}'.format(popt[0])+'; '+'  $C_{ab}$ ='+'{:04.1f}'.format(popt[1])+'; '+\
    '  $C_{cx}$ = '+'{:04.2f}'.format(popt[2])+'; '+'  $C_{bp}$ ='+'{:04.1f}'.format(popt[3])+'; '+\
    '  $C_{w}$ ='+'{:07.5f}'.format(popt[4])+'; '+'  $C_{dm}$ = '+'{:07.5f}'.format(popt[5])+'; '+\
    '  $\u03B8_{i}$ ='+'{:04.1f}'.format(popt[6])+'; '+'  $b_{spec}$ ='+'{:04.2f}'.format(popt[7]),weight='bold')

plt.axis([min(wl),max(wl),0,1])
plt.show()




