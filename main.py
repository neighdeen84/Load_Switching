from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Enter in the CSVs you want to process:
df_dryer = pd.read_csv('TEST_dryer_profile_611_1.csv', header=None)
df_EV = pd.read_csv('converted0_MDF_EV.csv', header=None)

# Adding a new empty column to the dryer dataframe to merge it with the EV's dataframe:
df_dryer['newcol'] = ""

# Filling the third empty column of the dryer with the power values from the second column in the EV dataframe:
df_dryer.iloc[:,2]= df_EV.iloc[:,1]
df_dryer_and_EV = df_dryer

#Labeling the dryer and EV columns (will remove the labels at the end):
df_dryer_and_EV.columns = ['Time', 'Power_1', 'Power_2']

# Removing column labels for easier gridlabbing (might do this at the very end instead if it's easier for python):
#df_dryer_and_EV.columns = [''] * len(df_dryer_and_EV.columns)
#print (df_dryer_and_EV)

# Creating a new dataframe for the switched output:
# Just set it equal to the dryer and EV dataframe, pop out the last column and zero out the power column:
df_switching_output = df_dryer_and_EV
df_switching_output.pop("Power_2")
df_switching_output['Power_1'] = 0


print(df_switching_output)