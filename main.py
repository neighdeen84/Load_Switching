import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Enter in the CSVs you want to process:
df_primary = pd.read_csv('Dryer_7loads_5min.csv', header=None)
df_secondary = pd.read_csv('EV5_5min.csv', header=None)

# Creating a new dataframe for the merged primary & secondary:
df_primary_and_secondary = pd.DataFrame() # Create empty dataframe

# Set first column equal to the same ones of the primary's timestamp, and the second and third equal to the power cols:
df_primary_and_secondary['Time'] = df_primary.iloc[:,0]
df_primary_and_secondary['Power_1'] = df_primary.iloc[:,1]
df_primary_and_secondary['Power_2'] = df_secondary.iloc[:,1]

# Replacing NaN values with zeroes:
#df_primary_and_secondary.fillna(0)
df_primary_and_secondary.replace(np.nan, 0, inplace=True)

#print(df_primary_and_secondary)
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

# Setting the initial conditions:
place_holder = []
deferred_count = 0

for i, row in df_primary_and_secondary.iterrows():
    # Smooth brain variables
    power_1_on = row['Power_1'] > 100
    power_2_on = row['Power_2'] > 100
    store_power_1 = row['Power_1']
    store_power_2 = row['Power_2']
    ########################################################## Conditions

    # save power 2 unconditionally - if we want to use it now cool, or derfer it to later, that's cool too
    if power_2_on:
        place_holder.append(store_power_2)

    # always output power 1 if it's on
    if power_1_on:
        df_switching_output.iloc[i, 1] = store_power_1
        if power_2_on:
            deferred_count += 1
            print("Deferred at", row['Time'])
    # if we have power 2 to run, output that
    elif len(place_holder) > 0:
        df_switching_output.iloc[i, 1] = place_holder.pop(0)
    # otherwise, output nuttin'
    else:
        df_switching_output.iloc[i, 1] = 0.0


print("The NeoCharge deferred the secondary power", str(deferred_count), "times")

# Plotting to verify switching:
df_switching_output.plot()
plt.title('Switched Output')
plt.show()

# Printing out the final output CSV: :D
#df_switching_output.to_csv('switched_output.csv', index=False)

# Kinda want another CSV with all 3 power values to see if the switching is happening:
df_all = pd.DataFrame() # Create empty dataframe
df_all['Time'] = df_primary_and_secondary.iloc[:,0]
df_all['Power_1'] = df_primary_and_secondary.iloc[:,1]
df_all['Power_2'] = df_primary_and_secondary.iloc[:,2]
df_all['Power_Switched'] = df_switching_output.iloc[:,1]
#print(df_all)
df_all.to_csv('primary_and_secondary_and_switched_output_5.csv', index=False)

# Removing column labels for easier gridlabbing:
df_switching_output.columns = [''] * len(df_switching_output.columns)
#print(df_switching_output)
df_switching_output.to_csv('switch5.csv', index=False, header=None)