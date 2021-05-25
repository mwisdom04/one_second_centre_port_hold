import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.collections as clt
import ptitprince as pt
from scipy import stats

sns.set(style='whitegrid', font_scale=2)

animalIDs = ['SNL_photo36', 'SNL_photo38', 'SNL_photo39', 'SNL_photo40']

df_to_concat = []

for animalID in animalIDs:
    df = pd.read_pickle('/home/mwisdom/Documents/data_analysis/analysed_data/One_Second_Hold/' + animalID + '/AllSessionsDataframe/' + animalID + '_all_sessions.pkl')

    '''SessionDates = df['SessionDate'].unique()'''

    Cue_Delay_bin_filts = {'0.02-0.1': (df['CueDelay'] > 0.02) & (df['CueDelay'] < 0.1) & (df['TrainingLevel'] == 3),
    '0.1 - 0.2': (df['CueDelay'] > 0.1) & (df['CueDelay'] < 0.2) & (df['TrainingLevel'] == 3),
    '0.2 - 0.35': (df['CueDelay'] > 0.2) & (df['CueDelay'] < 0.35) & (df['TrainingLevel'] == 3),
    '0.35 - 0.55': (df['CueDelay'] > 0.35) & (df['CueDelay'] < 0.55) & (df['TrainingLevel'] == 3),
    '0.55 - 0.75': (df['CueDelay'] > 0.55) & (df['CueDelay'] < 0.75) & (df['TrainingLevel'] == 3)}
    #'0.75 - 0.99': (df['CueDelay'] > 0.75) & (df['CueDelay'] < 0.99) & (df['TrainingLevel'] == 3)}

    CentrePortHoldTimes_by_CueDelay = {}

    for k, v in Cue_Delay_bin_filts.items():
        CueDelay_filtered_df = df.loc[v]
        array_CentrePortHoldTimes = np.hstack(CueDelay_filtered_df['CentrePortHoldTimes'])
        CentrePortHoldTimes_by_CueDelay[k] = array_CentrePortHoldTimes

    df_CentrePortHoldTimes_by_CueDelay = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in CentrePortHoldTimes_by_CueDelay.items() ]))
    df_to_concat.append(df_CentrePortHoldTimes_by_CueDelay)

df_all_CPHT_by_CueDelay = pd.concat(df_to_concat, ignore_index=True)

for k in Cue_Delay_bin_filts.keys():
    df_all_CPHT_by_CueDelay[(np.abs(stats.zscore(df_all_CPHT_by_CueDelay[k])) < 3)]

f, ax = plt.subplots(figsize= (7, 7))
ax = sns.violinplot( data = df_all_CPHT_by_CueDelay)


'''filt = df_all_CPHT_by_CueDelay['0.02-0.1'].notna()
stats.zscore(df_all_CPHT_by_CueDelay['0.02-0.1'].loc[filt])'''



