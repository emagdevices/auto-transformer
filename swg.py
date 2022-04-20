import pandas as pd

def findSWG(Bare_area):
    # Bare area in sqmm
    swg_data = pd.read_csv('EMD - Sheet1.csv') # select the swg the data 
    higer_data = swg_data[Bare_area < swg_data['Normal Conductor Area mm²']]
    required_swg_result = higer_data.iloc[(higer_data['Normal Conductor Area mm²'] - Bare_area).abs().argsort()[:1]]
    diameter_of_insulated_wire = required_swg_result['Medium Covering Max']

    return required_swg_result

Input_current = 2000 / 230

A_wp = Input_current / 250

A_wp_sqmm = A_wp * 100 

if __name__ == '__main__':
    required_swg = findSWG(A_wp_sqmm)
    print(required_swg) 