import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.collections as clt
import ptitprince as pt

sns.set(style='whitegrid', font_scale=2)

df = pd.read_pickle('/home/mwisdom/Documents/data_analysis/analysed_data/One_Second_Hold/SNL_photo36' + '/AllSessionsDataframe/' animal + '_all_sessions.pkl')

'''SessionDates = df['SessionDate'].unique()'''

Cue_Delay_bin_filts = {'0.02-0.05': (df['CueDelay'] > 0.02) & (df['CueDelay'] < 0.05) & (df['TrainingLevel'] == 3),
'0.05 - 0.1': (df['CueDelay'] > 0.05) & (df['CueDelay'] < 0.1) & (df['TrainingLevel'] == 3),
'0.1 - 0.2': (df['CueDelay'] > 0.1) & (df['CueDelay'] < 0.2) & (df['TrainingLevel'] == 3),
'0.2 - 0.4': (df['CueDelay'] > 0.2) & (df['CueDelay'] < 0.4) & (df['TrainingLevel'] == 3),
'0.4 - 0.7': (df['CueDelay'] > 0.4) & (df['CueDelay'] < 0.7) & (df['TrainingLevel'] == 3),
'0.7 - 0.99': (df['CueDelay'] > 0.4) & (df['CueDelay'] < 0.99) & (df['TrainingLevel'] == 3)}

CentrePortHoldTimes_by_CueDelay = {}

for k, v in Cue_Delay_bin_filts.items():
    CueDelay_filtered_df = df.loc[v]
    array_CentrePortHoldTimes = np.hstack(CueDelay_filtered_df['CentrePortHoldTimes'])
    CentrePortHoldTimes_by_CueDelay[k] = array_CentrePortHoldTimes

df_CentrePortHoldTimes_by_CueDelay = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in CentrePortHoldTimes_by_CueDelay.items() ]))

f, ax = plt.subplots(figsize= (7, 7))
ax = sns.violinplot( data = df_CentrePortHoldTimes_by_CueDelay)





