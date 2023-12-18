from procosine_library import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import optimize as opt
import scipy.io
import os
import glob
import scipy.interpolate
import json


with open("simulation_parameters.json", 'r') as f:
            simu_param  = json.load(f) 

leaf_parameters=np.asarray([simu_param["N"],simu_param["Cab"],simu_param["Ccx"],simu_param["Cbp"],simu_param["Cw"],simu_param["Cdm"],simu_param["Theta_i"],simu_param["Bspec"],])
#leaf_parameters=np.loadtxt('leaf_parameters.txt')
data= dataSpec_P5B()
Thetas = 0

rsim = procosine([data[:,0],Thetas,data],*leaf_parameters)

plt.figure()
plt.plot(data[:,0],rsim,linewidth=2.5,color=[0.75,0.75,0.99]);
plt.xlabel('Wavelength (nm)',fontsize=11,weight='bold')
plt.ylabel('Pseudo Bidirectional Reflectance Factor',fontsize=12,weight='bold')
plt.title('N = '+'{:03.2f}'.format(leaf_parameters[0])+'; '+'  $C_{ab}$ ='+'{:03.2f}'.format(leaf_parameters[1])+'; '+\
    '  $C_{cx}$ = '+'{:03.2f}'.format(leaf_parameters[2])+'; '+'  $C_{bp}$ ='+'{:03.2f}'.format(leaf_parameters[3])+'; '+\
    '  $C_{w}$ ='+'{:03.2f}'.format(leaf_parameters[4])+'; '+'  $C_{dm}$ = '+'{:03.2f}'.format(leaf_parameters[5])+'; '+\
    '  $\u03B8_{i}$ ='+'{:03.2f}'.format(leaf_parameters[6])+'; '+'  $b_{spec}$ ='+'{:03.2f}'.format(leaf_parameters[7]),weight='bold')
plt.axis([400,2500,0,1])
plt.show()