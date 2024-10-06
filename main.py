import pandas as pd # for manipulating csv dataset
import numpy as np
import matplotlib.pyplot as plt # make plots
from scipy.stats import norm # We will use this for understanding significance



url ='https://ceos.org/gst/files/pilot_topdown_CO2_Budget_countries_v1.csv'
df_all = pd.read_csv(url, skiprows=52)
df_all.to_excel('data_mapping/data.xlsx')