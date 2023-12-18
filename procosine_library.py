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

import numpy as np
import math
import scipy



def tav(teta,ref):
    """
    ***********************************************************************
     Adapted from tav.m     
    ***********************************************************************
    Stern F. (1964), Transmission of isotropic radiation across an
    interface between two dielectrics, Appl. Opt., 3(1):111-113.
    Allen W.A. (1973), Transmission of isotropic light across a
    dielectric surface in two and three dimensions, J. Opt. Soc. Am.,
    63(6):664-666.
    ***********************************************************************
    Féret et al. (2008), PROSPECT-4 and 5: Advances in the Leaf Optical
    Properties Model Separating Photosynthetic Pigments, Remote Sensing of
    Environment
    ***********************************************************************
    """

    s=np.size(ref)
    teta=teta*np.pi/180
    r2=ref**2
    rp=r2+1
    rm=r2-1
    a=((ref+1)**2)/2
    k=-((r2-1)**2)/4
    ds=np.sin(teta)
    
    k2=k**(2)
    rm2=rm**2
    
    if teta==0:
      f=4*ref/(ref+1)**2
    else:
      if teta==np.pi/2:
        b1=np.zeros(s)
      else:
        b1=np.sqrt((((ds**2)-rp/2)**2)+k)
     
      
      b2=(ds**2)-rp/2
      b=b1-b2
      ts=(k2/(6*b**3)+(k/b)-b/2)-(k2/(6*a**3)+(k/a)-a/2)
      tp1=-2*r2*(b-a)/(rp**2)
      tp2=-2*r2*rp*np.log(b/a)/rm2
      tp3=r2*(b**(-1)-a**(-1))/2
      tp4=16*(r2**2)*((r2**2)+1)*np.log((2*rp*b-rm2)/(2*rp*a-rm2))/((rp**3)*rm2)
      tp5=16*(r2**3)*(((2*rp*b-rm2)**(-1))-(2*rp*a-rm2)**(-1))/rp**3
      tp=tp1+tp2+tp3+tp4+tp5
      f=(ts+tp)/(2*ds**2)
      
      return f


 
def cosine(x,wl,DHR,Thetas):
    """
    ***********************************************************************
     Adapted from cosine.m     
    ***********************************************************************
    Jay, S., Bendoula, R., Hadoux, X., Féret, J.B. & Gorretta, N. (2016), A
    physically-based model for retrieving foliar biochemistry and leaf
    orientation using close-range imaging spectroscopy, Remote Sensing of 
    Environment, 177:220-236.
    ***********************************************************************
    """ 
    Thetai=x[0]
    Bspec=x[1]
    
    PBRF = (math.cos(Thetai*math.pi/180)/math.cos(Thetas*math.pi/180))*(DHR+Bspec)
    return PBRF


def procosine(Xdatas,*x):
    """
    ***********************************************************************
     Adapted from procosine.m     
    ***********************************************************************
    Jay, S., Bendoula, R., Hadoux, X., Féret, J.B. & Gorretta, N. (2016), A
    physically-based model for retrieving foliar biochemistry and leaf
    orientation using close-range imaging spectroscopy, Remote Sensing of 
    Environment, 177:220-236.

    Féret, J.B., François, C., Asner, G.P., Gitelson, A.A., Martin, R.E., 
    Bidel, L.P.R., Ustin, S.L., Le Maire, G. & Jacquemoud, S. (2008), PROSPECT-4 
    and 5: Advances in the Leaf Optical Properties Model Separating 
    Photosynthetic Pigments, Remote Sensing of Environment, 112:3030-3043.
    ***********************************************************************
    """
    wl=Xdatas[0]
    Thetas=Xdatas[1]
    data=Xdatas[2]
    
    N=x[0]
    Cab=x[1]
    Ccx=x[2]
    Cbp=x[3]
    Cw=x[4]
    Cm=x[5]
    Thetai=x[6]
    Bspec=x[7]
    
    RT = prospect_5B(N,Cab,Ccx,Cbp,Cw,Cm,data) 
    
    PBRF = cosine(np.array([Thetai,Bspec]),wl,RT[1,:],Thetas)
    
    return PBRF

class Procosine:
    def __init__(self,Thetas,data):
        self.Thetas=Thetas
        self.data=data
    
    def procosine(self,wl,*x):
        N=x[0]
        Cab=x[1]
        Ccx=x[2]
        Cbp=x[3]
        Cw=x[4]
        Cm=x[5]
        Thetai=x[6]
        Bspec=x[7]
        
        RT = prospect_5B(N,Cab,Ccx,Cbp,Cw,Cm,self.data) 
        
        PBRF = cosine(np.array([Thetai,Bspec]),wl,RT[1,:],self.Thetas)
        
        return PBRF
        


def prospect_5B(N,Cab,Car,Cbrown,Cw,Cm,data):
    """
    ***********************************************************************
     Adapted from prospect_5B.m 
     ***********************************************************************
     _______________________________________________________________________
    
     Plant leaf reflectance and transmittance are calculated from 400 nm to
     2500 nm (1 nm step) with the following parameters:
    
           - N     = leaf structure parameter
           - Cab   = chlorophyll a+b content in µg/cm²
           - Car   = carotenoids content in µg/cm²
           - Cbrown= brown pigments content in arbitrary units
           - Cw    = equivalent water thickness in g/cm² or cm
           - Cm    = dry matter content in g/cm²
    
     Here are some examples observed during the LOPEX'93 experiment on
     fresh (F) and dry (D) leaves :
    
     ---------------------------------------------
                    N     Cab     Cw        Cm    
     min          1.000    0.0  0.004000  0.001900
     max          3.000  100.0  0.040000  0.016500
     corn (F)     1.518   58.0  0.013100  0.003662
     rice (F)     2.275   23.7  0.007500  0.005811
     clover (F)   1.875   46.7  0.010000  0.003014
     laurel (F)   2.660   74.1  0.019900  0.013520
     ---------------------------------------------
     min          1.500    0.0  0.000063  0.0019
     max          3.600  100.0  0.000900  0.0165
     bamboo (D)   2.698   70.8  0.000117  0.009327
     lettuce (D)  2.107   35.2  0.000244  0.002250
     walnut (D)   2.656   62.8  0.000263  0.006573
     chestnut (D) 1.826   47.7  0.000307  0.004305
     ---------------------------------------------
     _______________________________________________________________________
    """
# ***********************************************************************
# Jacquemoud S., Baret F. (1990), PROSPECT: a model of leaf optical
# properties spectra, Remote Sens. Environ., 34:75-91.
# Féret et al. (2008), PROSPECT-4 and 5: Advances in the Leaf Optical
# Properties Model Separating Photosynthetic Pigments, Remote Sensing of
# Environment, 112:3030-3043
# The specific absorption coefficient corresponding to brown pigment is
# provided by Frederic Baret (EMMAH, INRA Avignon, baret@avignon.inra.fr)
# and used with his autorization.
# ***********************************************************************

    l=data[:,0]
    n=data[:,1]
    k=(Cab*data[:,2]+Car*data[:,3]+Cbrown*data[:,4]+Cw*data[:,5]+Cm*data[:,6])/N
    indices=np.where(k==0)[0]
    k[indices]=np.finfo(float).eps
    trans=(1-k)*np.exp(-k)+(k**2)*scipy.special.expn(1,k)

#***********************************************************************
# reflectance and transmittance of one layer
# ***********************************************************************
# Allen W.A., Gausman H.W., Richardson A.J., Thomas J.R. (1969),
# Interaction of isotropic ligth with a compact plant leaf, J. Opt.
# Soc. Am., 59(10):1376-1379.
# ***********************************************************************

# reflectivity and transmissivity at the interface
#-------------------------------------------------
    alpha=40
    t12=tav(alpha,n)
    t21=tav(90,n)/n**2
    r12=1-t12
    r21=1-t21
    x=tav(alpha,n)/tav(90,n)
    y=x*(tav(90,n)-1)+1-tav(alpha,n)

# reflectance and transmittance of the elementary layer N = 1
#------------------------------------------------------------

    ra=r12+(t12*t21*r21*(trans**2))/(1-(r21**2*trans**2))
    ta=(t12*t21*trans)/(1-(r21**2)*trans**2)
    r90=(ra-y)/x
    t90=ta/x

# ***********************************************************************
# reflectance and transmittance of N layers
# ***********************************************************************
# Stokes G.G. (1862), On the intensity of the light reflected from
# or transmitted through a pile of plates, Proc. Roy. Soc. Lond.,
# 11:545-556.
# ***********************************************************************
    delta=(((t90**2)-(r90**2)-1)**2)-4*r90**2
    beta=(1+r90**2-t90**2-np.sqrt(delta))/(2*r90)
    va=(1+(r90**2)-(t90**2)+np.sqrt(delta))/(2*r90)
    vb=np.sqrt(beta*(va-r90)/(va*(beta-r90)))
    vbNN = vb**(N-1)
    vbNNinv = 1/vbNN
    vainv = 1/va
    s1=ta*t90*(vbNN-vbNNinv)
    s2=ta*(va-vainv)
    s3=va*vbNN-vainv*vbNNinv-r90*(vbNN-vbNNinv)

    RN=ra+s1/s3
    TN=s2/s3;
    LRT=np.array([l,RN,TN])
    
    return LRT





def dataSpec_P5B():
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
    data=np.load('dataSpec_P5B.npy')
    return data