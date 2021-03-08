import pandas as pd
import matplotlib.pyplot as plt

# Enter in the CSVs you want to process:
df_primary = pd.read_csv('TEST_dryer_profile_611_1.csv', header=None)
df_secondary = pd.read_csv('converted0_MDF_EV.csv', header=None)

# Creating a new dataframe for the merged primary & secondary:
df_primary_and_secondary = pd.DataFrame() # Create empty dataframe

# Set first column equal to the same ones of the primary's timestamp, and the second and third equal to the power cols:
df_primary_and_secondary['Time'] = df_primary.iloc[:,0]
df_primary_and_secondary['Power_1'] = df_primary.iloc[:,1]
df_primary_and_secondary['Power_2'] = df_secondary.iloc[:,1]

# Creating a new dataframe for the switched output:
df_switching_output = pd.DataFrame() # Create empty dataframe

# Set first columns equal to the same ones of the primary & secondary merged dataframe, zero out the power col:
df_switching_output['Time'] = df_primary_and_secondary.iloc[:,0]
df_switching_output['Power'] = df_primary_and_secondary.iloc[:,1]
df_switching_output['Power'] = 0

# Double check that everything is working as it should:
#print(df_primary_and_secondary)
#print(df_switching_output)

# How do you get to a specific entry in a df with if you have dimensions?
#print(df_primary_and_secondary.iloc[0,1])

'''
Comparison process:
We want to first check if the primary is over 100 W, if it is, then we automatically turn it on
and whatever value that is is written into its corresponding df_switching_output index. If the primary is
lower than that, we can look at the secondary and see if it's above 100. If it is, then the corresponding
df_switching_output index is equal to the secondary. If both the primary & secondary are below the threshold
then we keep the power value is zero.
'''

#count = 0
for i in range(len(df_primary_and_secondary)):

    if df_primary_and_secondary.iloc[i,df_primary_and_secondary.columns.get_loc('Power_1')] > 100:
        df_switching_output.iloc[i,1] = df_primary_and_secondary.iloc[i,df_primary_and_secondary.columns.get_loc('Power_1')]

    elif df_primary_and_secondary.iloc[i,df_primary_and_secondary.columns.get_loc('Power_2')] > 100:
        df_switching_output.iloc[i,1] = df_primary_and_secondary.iloc[i,df_primary_and_secondary.columns.get_loc('Power_2')]

'''
# Handmade progress bar (to double check that the script is still running), don't forget to uncomment count if you uncomment this:
    if count == 100:
        print('Made it to 100!')
    if count % 10000 == 0:
        print('Made it to '+str(count) +'!')
    count += 1
    #print('This is count ' + str(count))
    #print(df_switching_output.iloc[i])
'''

# printing to see if it worked, but we still won't be able to tell till we see the CSV:
#print(df_switching_output)

# Plotting to verify switching:
df_switching_output.plot()
plt.title('Switched Output')
plt.show()

# Printing out the final output CSV: :D
df_switching_output.to_csv('switched_output.csv', index=False)

# Kinda want another CSV with all 3 power values to see if the switching is happening:
df_all = pd.DataFrame() # Create empty dataframe
df_all['Time'] = df_primary_and_secondary.iloc[:,0]
df_all['Power_1'] = df_primary_and_secondary.iloc[:,1]
df_all['Power_2'] = df_primary_and_secondary.iloc[:,2]
df_all['Power_Switched'] = df_switching_output.iloc[:,1]
#print(df_all)
df_all.to_csv('primary_and_secondary_and_switched_output.csv', index=False)

# Removing column labels for easier gridlabbing:
df_switching_output.columns = [''] * len(df_switching_output.columns)
#print(df_switching_output)
df_switching_output.to_csv('switched_output_GLD.csv', index=False)
