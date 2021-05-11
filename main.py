import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import shutil



def iter_files(dryer_folder_path,EV_folder_path):
    # Create output folder then change working directory to the folder path:
    switched_dir = os.getcwd() + '\\data\\switched_data'

    # If output folder doesn't exist, create it:
    if os.path.isdir(switched_dir):
        shutil.rmtree(switched_dir)
        os.mkdir(switched_dir)
    else:
        os.mkdir(switched_dir)


    for dryer_file,EV_file in zip(os.listdir(dryer_folder_path),os.listdir(EV_folder_path)):
        print(dryer_file + ' and ' + EV_file + ' are being processed right now')

        # Enter in the CSVs you want to process:
        df_primary = pd.read_csv(dryer_folder_path +'\\'+ dryer_file, header=None)
        df_secondary = pd.read_csv(EV_folder_path + '\\' + EV_file, header=None)
        # Creating a new dataframe for the merged primary & secondary:
        df_primary_and_secondary = pd.DataFrame() # Create empty dataframe

        # Set first column equal to the same ones of the primary's timestamp, and the second and third equal to the power cols:
        df_primary_and_secondary['Time'] = df_primary.iloc[:,0]
        df_primary_and_secondary['Power_1'] = df_primary.iloc[:,1]
        df_primary_and_secondary['Power_2'] = df_secondary.iloc[:,1]

        # Replacing NaN values with zeroes:
        df_primary_and_secondary.replace(np.nan, 0, inplace=True)

        #print(df_primary_and_secondary)
        # Creating a new dataframe for the switched output:
        df_switching_output = pd.DataFrame() # Create empty dataframe

        # Set first columns equal to the same ones of the primary & secondary merged dataframe, zero out the power col:
        df_switching_output['Time'] = df_primary_and_secondary.iloc[:,0]
        df_switching_output['Power'] = df_primary_and_secondary.iloc[:,1]
        df_switching_output['Power'] = 0

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
            # Variables to make things easier:
            power_1_on = row['Power_1'] > 100
            power_2_on = row['Power_2'] > 100
            store_power_1 = row['Power_1']
            store_power_2 = row['Power_2']


            ######### Conditions #########
            # Save power 2 unconditionally - if we want to use it now cool, or defer it to later, that's cool too
            if power_2_on:
                place_holder.append(store_power_2)

            # Always output power 1 if it's on
            if power_1_on:
                df_switching_output.iloc[i, 1] = store_power_1
                if power_2_on:
                    deferred_count += 1
                    # Uncomment to show deferrals & their times:
                    #print("Deferred at", row['Time'])
            # If we have power 2 to run, output that:
            elif len(place_holder) > 0:
                df_switching_output.iloc[i, 1] = place_holder.pop(0)
            # Otherwise, don't output anything:
            else:
                df_switching_output.iloc[i, 1] = 0.0

        # Uncomment line below to show how many deferrals occurred at what times:
        #print("The NeoCharge deferred the secondary power", str(deferred_count), "times")

        # Uncomment block of code below to plot and verify switching:
        '''
        # df_switching_output.plot()
        # plt.title('Switched Output')
        # plt.show()
        '''

        # Uncomment block of code to print out csv with dryer, EV and switched column to verify switching:
        '''
        # Kinda want another CSV with all 3 power values to see if the switching is happening:
        df_all = pd.DataFrame() # Create empty dataframe
        df_all['Time'] = df_primary_and_secondary.iloc[:,0]
        df_all['Power_1'] = df_primary_and_secondary.iloc[:,1]
        df_all['Power_2'] = df_primary_and_secondary.iloc[:,2]
        df_all['Power_Switched'] = df_switching_output.iloc[:,1]
        #print(df_all)
        df_all.to_csv('primary_and_secondary_and_switched_output_5.csv', index=False)
        '''

        # Removing column labels for easier gridLAB-D-ing:
        df_switching_output.columns = [''] * len(df_switching_output.columns)
        out_number = re.findall("\d+", dryer_file)[0]

        # Printing out the switched output csv:
        df_switching_output.to_csv( switched_dir + '\\switch'+ out_number+".csv", index=False, header=None)

cwd = os.getcwd()
data_dir = cwd + '\\data'
dryer_profiles_dir = data_dir + '\\dryer_profiles_feeder'
EV_profiles_dir = data_dir + '\\EV_profiles_feeder'

# Calling the function (use EV profiles directory as function input):
iter_files(dryer_profiles_dir, EV_profiles_dir)