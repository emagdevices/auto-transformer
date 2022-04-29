# Loading libraries
import pandas as pd
import numpy as np
import math 
from decimal import ROUND_DOWN, ROUND_UP
import data 

swg_data = data.swg_data
lamination_data = data.lamination_data

def area_product(K_f, K_u, B_ac, J, Frequency, apparent_power):
    """Input Arguments:
        Output power [watts]
        Efficiency in scale of 100%
        K_f
        K_u
        B_ac -> Operational flux density
        J
        Frequency -> in Hz
        Apparent power in watts
    """
    Area_product = (apparent_power*(10**4))/(K_f * K_u * B_ac * J * Frequency)
    return Area_product


def findSWG(Bare_area):
    '''
        Bare area in sqmm
        return variables: 
            required swg dataframe, 
            diameter of insulated wire, 
            bare area of selected swg
    '''
    # swg_data = pd.read_csv('../DATA/EMD - Sheet1.csv') # select the swg the data 
    swg_data = data.swg_data
    higer_data = swg_data[Bare_area < swg_data['Normal Conductor Area mm²']]
    required_swg_result = higer_data.iloc[(higer_data['Normal Conductor Area mm²'] - Bare_area).abs().argsort()[:1]]
    diameter_of_insulated_wire = required_swg_result['Medium Covering Max']
    A_wp = required_swg_result['Normal Conductor Area mm²'].max() / 100 # cm^2
    return required_swg_result, diameter_of_insulated_wire, A_wp 

def bare_area(input_current, current_density):
    '''
        arguments: 
            input current [amps], 
            current density [amp/]
        return variables: 
            Bare area in sqmm
    '''
    a_wp = input_current / current_density
    return a_wp* 100 

