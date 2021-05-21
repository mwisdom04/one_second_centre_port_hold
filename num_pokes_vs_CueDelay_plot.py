import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12.0, 6.0))
# create figure into which you plot your graph
fig1 = fig.add_subplot(1, 1, 1)
# add a subplot into the figure

animalIDs = ['SNL_photo36', 'SNL_photo38', 'SNL_photo39', 'SNL_photo40']

for animalID in animalIDs:
    df = pd.read_pickle('/home/mwisdom/Documents/data_analysis/analysed_data/One_Second_Hold/' + animalID + '/AllSessionsDataframe/' + animalID + '_all_sessions.pkl')
    CueDelayTimes = df['CueDelay'].unique()
    CueDelayTimes.sort()

    num_pokes_at_cue_delay = {}

    for CueDelay in CueDelayTimes[1:]:
        filt = df['CueDelay'] == CueDelay
        filtered_df = df[filt]
        filtered_df = filtered_df.reset_index(drop=True)
        first_15_NumPokes_at_CueDelay = filtered_df.loc[0:14, ['NumberOfCentrePokes', 'CueDelay']]
        if first_15_NumPokes_at_CueDelay.size == 30:
            num_pokes_at_cue_delay[CueDelay] = first_15_NumPokes_at_CueDelay
        else:
            continue

    df_NumCentrePokes_CueDelay = pd.DataFrame()

    for k, v in num_pokes_at_cue_delay.items():
        df_to_append = pd.DataFrame.from_dict(v)
        df_NumCentrePokes_CueDelay = df_NumCentrePokes_CueDelay.append(df_to_append)

    x_values = df_NumCentrePokes_CueDelay['CueDelay'].unique()
    y_values = []

    for x in x_values:
        filt = df_NumCentrePokes_CueDelay['CueDelay'] == x
        filtered_df = df_NumCentrePokes_CueDelay.loc[filt]
        CueDelayTime_mean = filtered_df['NumberOfCentrePokes'].mean()
        y_values.append(CueDelayTime_mean)

    plt.plot(x_values, y_values, label= animalID)

fig1.legend()
# add legend to figure using the relevant AnimalIDs
fig1.set(title='graph', ylabel='Mean centre pokes per trial',
         xlabel='Cue delay times (s)')

fig.tight_layout()


