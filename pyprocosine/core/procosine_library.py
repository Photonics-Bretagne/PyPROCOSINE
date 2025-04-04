# -*- coding: utf-8 -*-
"""
Python library for PROCOSINE inversion
Created on Thu Mar 26 14:40:12 2020
@author: Mathieu Ribes
"""

# _______________________________________________________________________
#
# procosine.py (march, 27th 2020)
# _______________________________________________________________________

import sys 
import os 
import importlib

import numpy as np
import scipy
import os 
import json
from scipy import optimize as opt
from uncertainties import ufloat 
import matplotlib.pyplot as plt
import importlib.resources as pkg_resources
import pyprocosine.core as core
from pyprocosine.core import procosine_src as src

import pandas as pd




class Procosine():

    def __init__(self):
        # working_path=os.getcwd()
        # self.actual_path= os.path.dirname(os.path.realpath(__file__))
        # os.chdir(self.actual_path)
        # os.chdir('..')
        # self.root_path=os.getcwd()
        # os.chdir(working_path)
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.dataSpec_P5B() 

    def dataSpec_P5B(self):
        """ 
        ***********************************************************************
        Adapted from dataSpec_P5B.m -  (october, 20th 2009)
        ***********************************************************************
        [0] = wavelength (nm)
        [1] = refractive index of leaf material
        [2] = specific absorption coefficient of chlorophyll (a+b) (cm2.microg-1)
        [3] = specific absorption coefficient of carotenoids (cm2.microg-1)
        [4] = specific absorption coefficient of brown pigments (arbitrary units)
        [5] = specific absorption coefficient of water (cm-1)
        [6] = specific absorption coefficient of dry matter (cm2.g-1)
        Féret et al. (2008), PROSPECT-4 and 5: Advances in the Leaf Optical
        Properties Model Separating Photosynthetic Pigments, Remote Sensing of
        Environment
        The specific absorption coefficient corresponding to brown pigment is
        provided by Frederic Baret (EMMAH, INRA Avignon, baret@avignon.inra.fr)
        and used with his autorization.
        ***********************************************************************
        """
        #path_conf=os.path.join(self.root_path,"conf","dataSpec_P5B.npy")
        with pkg_resources.files(core).joinpath("dataSpec_P5B.npy").open("rb") as f:
            self.data=np.load(f)


    def loading_inversion_parameters(self,parameter_path):
        """
        This function allows to load inversion parameters stored in json file. The json file need to be stored  in the conf directory !

        Parameters
        ----------
        parameter_path : str
            the path of the json file containing inversion parameters. The json file need to be stored in the conf directory !!

        """
        
        with open(parameter_path, 'r') as f:
            self.inversion_param  = json.load(f)
        self.inversion_param["P0"]=np.array(self.inversion_param["P0"])
        self.inversion_param["LB"]=np.array(self.inversion_param["LB"])
        self.inversion_param["UB"]=np.array(self.inversion_param["UB"])
        self.inversion_param["Thetas"]=int(self.inversion_param["Thetas"])


    def loading_simulation_paramaters(self,parameter_path):
        """
        This function allows to load simulation parameters stored in json file. The json file need to be stored  in the conf directory !

        Parameters
        ----------
        parameter_path : str
            the path of the json file containing simulation parameters. The json file need to be stored in the conf directory !!

        """

        with open(parameter_path, 'r') as f:
            self.simulation_param  = json.load(f) 



           

    
    def load_spectrum(self,spectrum_path,wavelength_path):
        """
        This function allows to load spectrum and wavelengths stored in .npy format . npy files need to be stored  in the spectra_example directory !

        Parameters
        ----------
        sectrum_file_name : str
            the title of the npy file containing spectrum reflectance values. The npy file need to be stored in the spectra_example directory !!

        wavelength_file_name : str
            the title of the npy file containing corresponding vwavelngths of the spectrum reflectance values. The npy file need to be stored in the spectra_example directory !!
        """
        
        self.spectrum=np.load(spectrum_path)
        self.wl=np.load(wavelength_path)

    def procosine_inversion(self):

        """
        This function allows to run a prcosine inversion on a preloaded spectrum (see load_spectrum function) with preloaded inversion parameters (see loading_inversion_parameters)
        """


        P0=self.inversion_param["P0"]
        LB=self.inversion_param["LB"]
        UB=self.inversion_param["UB"]
        gtol=self.inversion_param["gtol"]
        xtol=self.inversion_param["xtol"]
        ftol=self.inversion_param["ftol"]
        Thetas=self.inversion_param["Thetas"]

        spline=scipy.interpolate.CubicSpline(self.data[:,0],self.data) # Resampling to the actual spectral sampling interval of the measurement
        self.data = np.squeeze(spline(self.wl))

        func=src.Procosine_function(Thetas,self.data)
        print(np.shape(self.spectrum))
        popt,pcov=opt.curve_fit(func.procosine_function,xdata=self.wl,ydata=self.spectrum,p0=P0,bounds=(LB,UB),method='trf',gtol=gtol,xtol=xtol,ftol=ftol)
        sigma_sol=np.sqrt(np.diagonal(pcov))
        self.inversion_spectrum=src.procosine([self.wl,Thetas,self.data],*popt)

        #self.inversion_result={"N":popt[0],"Cab":popt[1],"Ccx":popt[2],"Cbp":popt[3],"Cw":popt[4],"Cdm":popt[5],"Thetai":popt[6],"bspec":popt[7]}
        self.inversion_result={}
        self.inversion_result["N"]= ufloat(popt[0], sigma_sol[0])
        self.inversion_result["Cab"] = ufloat(popt[1], sigma_sol[1])
        self.inversion_result["Ccx"] = ufloat(popt[2], sigma_sol[2])
        self.inversion_result["Cbp"] = ufloat(popt[3], sigma_sol[3])
        self.inversion_result["Cw"] = ufloat(popt[4], sigma_sol[4])
        self.inversion_result["Cdm"] = ufloat(popt[5], sigma_sol[5])
        self.inversion_result["Thetai"] = ufloat(popt[6], sigma_sol[6])
        self.inversion_result["bspec"] = ufloat(popt[7], sigma_sol[7])

    def procosine_simulation(self):
        """
        This function allow to run a simulation of spectrum from preloaded simulation paramaters( see teh function loading_simulation_paramaters)
        """
        leaf_parameters=np.asarray(list(self.simulation_param.values()))
        Thetas = 0
        self.simulated_spectrum = src.procosine([self.data[:,0],Thetas,self.data],*leaf_parameters)
         

    def show_inversion_result(self):
        """
        this function allow to plot the spectrum in matplotlib figure which the procosine inversion was run (see procosine_inversion fucntion) and the spectrum results from the fitting.
        the best parameters of the procosin inversion are print and appear with their associated uncertainties on the title of the figure.
        """
        print("best fit parameters :",self.inversion_result)
        plt.figure()
        line1,=plt.plot(self.wl,self.spectrum,linewidth=2.5,color=[0.75,0.75,0.99],label='Measured Pseudo-BRF')
        line2,=plt.plot(self.wl,self.inversion_spectrum,':',linewidth=1.5,color=[0,0,0.7],label='Inverted Pseudo-BRF')
        plt.legend(handles=[line1,line2])   
        plt.xlabel('Wavelength (nm)',fontsize=16,weight='bold')
        plt.ylabel('Pseudo Bidirectional Reflectance Factor',fontsize=16,weight='bold')

        plt.title(str(self.inversion_result)[1:-1].replace("'",""),weight='bold')

        plt.axis([min(self.wl),max(self.wl),0,1])
        plt.show()
        
    def show_simulation_result(self):
        """
        This function allow to plot the spectrum comes from the procosine simulation (see procosine_simulation function) in a matplotlib figure.
        The simulations paramaters used appear on the title of the figure. 
        """
        plt.figure()
        plt.plot(self.data[:,0],self.simulated_spectrum,linewidth=2.5,color=[0.75,0.75,0.99]);
        plt.xlabel('Wavelength (nm)',fontsize=11,weight='bold')
        plt.ylabel('Pseudo Bidirectional Reflectance Factor',fontsize=12,weight='bold')
        plt.title(str(self.simulation_param)[1:-1].replace("'",""),weight='bold')
        plt.axis([400,2500,0,1])
        plt.show()







