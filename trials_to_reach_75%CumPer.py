import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

animalIDs = ['CPH01', 'CPH02', 'CPH03', 'CPH04', 'CPH05', 'CPH06', 'CPH07', 'CPH08', 'CPH09', 'CPH10', 'CPH11', 'CPH12'] #'SNL_photo38', 'SNL_photo39', 'SNL_photo40']

InputDir = '/home/mwisdom/Documents/data/analysed_data/one_second_centre_port_hold/'
OutputDir = '/home/mwisdom/Documents/figures/one_second_centre_port_hold/CPH01-12/'

VariableCueStart = {}
ReachedOneSec = {}

for n, animalID in enumerate(animalIDs):
    df = pd.read_pickle(InputDir + animalID + '/AllSessionsDataframe/' + animalID + '_all_sessions.pkl')

    df['TrainingLevel'].replace({1: 'Habituation', 3: 'Auditory'}, inplace=True)

    for i, index in enumerate(df.index):
        if df.loc[i, 'CueDelay'] > 0.1:
            VariableCueStart[animalID] = i
            #ax[n].axvline(VariableCueStart[animalID], ls='--', alpha=0.2, color='k') #label= 'Started CPH Increase')
            break

    if 1 in df['CueDelay'].unique():
        for i, index in enumerate(df.index):
            if df.loc[i, 'CueDelay'] == 1:
                ReachedOneSec[animalID] = i
                #ax[n].axvline(ReachedOneSec[animalID], ls='--', alpha=0.2, color='k') #label= 'Reached 1s')
                break
    else:
        pass

