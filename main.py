import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Enter in the CSVs you want to process:
df_primary = pd.read_csv('Neocharge_log_1_24_2021_MDF2_GLD_24H.csv', header=None)
df_secondary = pd.read_csv('converted0_MDF_EV.csv', header=None)

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
power_2_status = False
place_holder = [0]

for i in range(len(df_primary_and_secondary)):
    # Smooth brain variables
    power_1_on = df_primary_and_secondary.iloc[i,df_primary_and_secondary.columns.get_loc('Power_1')] > 100
    power_2_on = df_primary_and_secondary.iloc[i,df_primary_and_secondary.columns.get_loc('Power_2')] > 100
    store_power_1 = df_primary_and_secondary.iloc[i,df_primary_and_secondary.columns.get_loc('Power_1')]
    store_power_2 = df_primary_and_secondary.iloc[i, df_primary_and_secondary.columns.get_loc('Power_2')]
    store_power_2_deferral = df_primary_and_secondary.iloc[place_holder[0],df_primary_and_secondary.columns.get_loc('Power_2')]
    ########################################################## Conditions

    # Power 1 on and power 2 off
    ## OUTPUT: power 1
    if power_1_on and not power_2_on:
        df_switching_output.iloc[i, 1] = store_power_1

    # Power 1 on and power 2 on
    ## OUTPUT: power 1
    if power_1_on and power_2_on:
        df_switching_output.iloc[i, 1] = store_power_1
        ### Power 2 status is not saved
        if power_2_status is not True:
            #### SAVE: power 2 place
            power_2_status = True
            place_holder.append(i)

    # Power 1 off and power 2 on
    if not power_1_on and power_2_on:
        ## No saved power 2
        if power_2_status is False:
            ### OUTPUT: power 2
            df_switching_output.iloc[i, 1] = store_power_2
        ## Power 2 is saved
        if power_2_status is True:
            place_holder.append(i)
            ### OUTPUT: power 2 deferral
            df_switching_output.iloc[i, 1] = store_power_2_deferral
            place_holder.insert(1,place_holder[0]+1)
            place_holder = place_holder[1:]
            store_power_2_deferral = df_primary_and_secondary.iloc[place_holder[0], df_primary_and_secondary.columns.get_loc('Power_2')]


    # Power 1 off and power 2 off
    if not power_1_on and not power_2_on:
        ## Power 2 is saved
        if power_2_status is True:
            ### OUTPUT: power 2 deferral
            df_switching_output.iloc[i, 1] = store_power_2_deferral
            place_holder.insert(1, place_holder[0] + 1)
            place_holder = place_holder[1:]
            store_power_2_deferral = df_primary_and_secondary.iloc[place_holder[0], df_primary_and_secondary.columns.get_loc('Power_2')]
            # check next value for place_holder
            if store_power_2_deferral < 100:
                power_2_status = False
                if len(place_holder[1:]) != 0:
                    place_holder = place_holder[1:]
                    store_power_2_deferral = df_primary_and_secondary.iloc[place_holder[0], df_primary_and_secondary.columns.get_loc('Power_2')]
                    power_2_status = True
        '''
        ########################################################## Check
        if df_primary_and_secondary.iloc[i,df_primary_and_secondary.columns.get_loc('Time')] == '2021-01-24 14:00:58':
        print('power 1')
        print(power_1_on)

        print('power 2')
        print(power_2_on)

        print('power_1_storage')
        print(power_1_storage)

        print('power_2_status')
        print(power_2_status)

        print('place_holder')
        print(place_holder)

        print('i')
        print(i)
        '''

#print(df_switching_output)

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
