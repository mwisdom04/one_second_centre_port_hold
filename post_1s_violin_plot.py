import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.collections as clt
import ptitprince as pt
from scipy import stats

animalIDs = ['SNL_photo40']            #['SNL_photo36', 'SNL_photo38', 'SNL_photo39', 'SNL_photo40']

df_to_concat = []

for animalID in animalIDs:
    df = pd.read_pickle('/home/mwisdom/Documents/data_analysis/analysed_data/One_Second_Hold/' + animalID + '/AllSessionsDataframe/' + animalID + '_all_sessions.pkl')

    post_1s_TrialNum_bins = {'0-49': [0, 49], '50-99': [50, 99], '100-149': [100, 149], '150-199': [150, 199], '200-249': [200, 249], '250-299': [250, 299]}

    '''{'0-99': [0, 99],
    '100-199': [100, 199],
    '200-299': [200, 299],
    '300-399': [300, 399],
    '400-499': [400, 499],
    '500-599': [500, 599],
    '600-699': [600, 699]}'''

    post_1s_CentrePortHoldTimes = {}

    for k, v in post_1s_TrialNum_bins.items():
        filt = (df['CueDelay'] == 1) & (df['TrainingLevel'] == 3)
        filtered_df = df.loc[filt]
        filtered_df = filtered_df.reset_index(drop=True)
        array_CentrePortHoldTimes = np.hstack(filtered_df.loc[v[0]:v[1], 'CentrePortHoldTimes'])
        array_CentrePortHoldTimes = np.delete(array_CentrePortHoldTimes, np.where(array_CentrePortHoldTimes < 0))
        post_1s_CentrePortHoldTimes[k] = array_CentrePortHoldTimes

    df_post_1s_CentrePortHoldTimes = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in post_1s_CentrePortHoldTimes.items()]))
    df_to_concat.append(df_post_1s_CentrePortHoldTimes)

df_all_post1s_CPHT_TrialBinned = pd.concat(df_to_concat, ignore_index=True)

f, ax = plt.subplots(figsize= (7, 7))
ax = sns.violinplot( data = df_all_post1s_CPHT_TrialBinned)