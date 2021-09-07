import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

animalIDs = ['CPH01', 'CPH02', 'CPH03', 'CPH04', 'CPH05', 'CPH06', 'CPH07', 'CPH08', 'CPH09', 'CPH10', 'CPH11', 'CPH12'] #'SNL_photo38', 'SNL_photo39', 'SNL_photo40']

InputDir = '/home/mwisdom/Documents/data/analysed_data/one_second_centre_port_hold/'
OutputDir = '/home/mwisdom/Documents/figures/one_second_centre_port_hold/CPH01-12/'

fig, ax = plt.subplots(len(animalIDs), 1, figsize=(15, (len(animalIDs)*5)), sharex=True)
fig.subplots_adjust(hspace=0.3)

VariableCueStart = {}
ReachedOneSec = {}

for n, animalID in enumerate(animalIDs):
    df = pd.read_pickle(InputDir + animalID + '/AllSessionsDataframe/' + animalID + '_all_sessions.pkl')

    df['TrainingLevel'].replace({1: 'Habituation', 3: 'Auditory'}, inplace=True)

    ax[n].axhline(0.1, ls='--', alpha=0.4, color='k')
    ax[n].axhline(1, ls='--', alpha=0.4, color='k')

    sns.lineplot(ax=ax[n], x=df.index, y='CueDelay', data=df, hue='SessionDate',
                 marker=".", alpha=0.15, markeredgewidth=0, linewidth=0)
    ax[n].set_title('Cue Delay Transition ' + animalID)

plt.savefig(OutputDir + 'CueDelayTransitionsAllAnimals.pdf',
            transparent=True, bbox_inches='tight')