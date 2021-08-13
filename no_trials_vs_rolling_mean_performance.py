import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

animalIDs = ['SNL_photo45', 'SNL_photo47', 'SNL_photo48', 'SNL_photo49', 'SNL_photo50', 'SNL_photo52', 'SNL_photo53', 'SNL_photo54'] #'SNL_photo38', 'SNL_photo39', 'SNL_photo40']

ExpGroups = {'Weekdays only': ['SNL_photo45', 'SNL_photo47', 'SNL_photo48', 'SNL_photo49'], 'Weekdays & Weekends': ['SNL_photo50', 'SNL_photo52', 'SNL_photo53', 'SNL_photo54']}

InputDir = '/home/mwisdom/Documents/data/analysed_data/one_second_centre_port_hold/'
OutputDir = '/home/mwisdom/Documents/figures/one_second_centre_port_hold/weekdays_only_vs_weekday_&_weekend/'

fig, ax = plt.subplots(len(animalIDs), 1, figsize=(15, (len(animalIDs)*5)), sharex=True)
fig.subplots_adjust(hspace=0.3)

VariableCueStart = {}
ReachedOneSec = {}

for n, animalID in enumerate(animalIDs):
    df = pd.read_pickle(InputDir + animalID + '/AllSessionsDataframe/' + animalID + '_all_sessions.pkl')

    df['TrainingLevel'].replace({1: 'Habituation', 3: 'Auditory'}, inplace=True)

    for i, index in enumerate(df.index):
        if df.loc[i, 'CueDelay'] > 0.1:
            VariableCueStart[animalID] = i
            ax[n].axvline(VariableCueStart[animalID], ls='--', alpha=0.2, color='k') #label= 'Started CPH Increase')
            break

    if 1 in df['CueDelay'].unique():
        for i, index in enumerate(df.index):
            if df.loc[i, 'CueDelay'] == 1:
                ReachedOneSec[animalID] = i
                ax[n].axvline(ReachedOneSec[animalID], ls='--', alpha=0.2, color='k') #label= 'Reached 1s')
                break
    else:
        pass

    ax[n].axhline(50, ls='--', alpha=0.4, color='k')
    ax[n].axhline(75, ls='--', alpha=0.1, color='k')
    ax[n].set(ylim=(0, 100))
    ax[n].set_ylabel("Rolling Mean", fontsize=12)
    ax[n].set_xlabel('Trial number', fontsize=12)
    ax[n].tick_params(labelsize=12)

    df['rolling_mean'] = df['FirstPokeCorrect'].rolling(50, min_periods=1).sum()*2

    sns.lineplot(ax=ax[n], x=df.index, y='rolling_mean', data=df, hue='TrainingLevel',
                 marker=".", alpha=0.15, markeredgewidth=0, linewidth=0)
    ax[n].set_title('Rolling mean ' + animalID)

lgd = plt.legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0.)
for l in lgd.get_lines():
    l.set_alpha(1)
    l.set_linewidth(2)

#plt.show()

plt.savefig(OutputDir + 'CumulativePerformanceAllAnimals.pdf',
            transparent=True, bbox_inches='tight')



fig, ax = plt.subplots(2, 1, figsize=(15, 2*5), sharex=True)
fig.subplots_adjust(hspace=0.3)


for n, (k, v) in enumerate(ExpGroups.items()):

    df_2 = pd.DataFrame()

    for animalID in v:
        df = pd.read_pickle(InputDir + animalID + '/AllSessionsDataframe/' + animalID + '_all_sessions.pkl')

        df['TrainingLevel'].replace({1: 'Habituation', 3: 'Auditory'}, inplace=True)

        ax[n].axhline(50, ls='--', alpha=0.4, color='k')
        ax[n].axhline(75, ls='--', alpha=0.1, color='k')
        ax[n].set(ylim=(0, 100))
        ax[n].set(xlim=(0, 2000))
        ax[n].set_ylabel("Rolling Mean", fontsize=12)
        ax[n].set_xlabel('Trial number', fontsize=12)
        ax[n].tick_params(labelsize=12)

        df['rolling_mean'] = df['FirstPokeCorrect'].rolling(50, min_periods=1).sum()*2

        sns.lineplot(ax=ax[n], x=df.index, y='rolling_mean', data=df, color='grey',
                     marker=".", alpha=0.2, markeredgewidth=0, linewidth=0,) #label= animalID)

        df_2[animalID] = df.loc[0:1000, 'rolling_mean']

    df_2['mean_all_animals'] = df_2.mean(axis=1)

    sns.lineplot(ax=ax[n], x=df_2.index, y='mean_all_animals', data=df_2, color='orange',
                     marker=".", alpha=0.5, markeredgewidth=0, linewidth=0) #label='mean')


    ax[n].set_title(k)

    #leg = plt.legend()
    #for lh in leg.legendHandles:
        #lh.set_alpha(1)
    '''lgd = plt.legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0.)
    for l in lgd.get_lines():
        l.set_alpha(1)
        l.set_linewidth(2)'''

plt.savefig(OutputDir + 'CumulativePerformanceAllAnimalsByCohort.pdf',
            transparent=True, bbox_inches='tight')


