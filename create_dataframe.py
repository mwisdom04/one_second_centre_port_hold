from load_bpod_raw_events import load_bpod_file
from load_nested_structs import loadmat
import pandas as pd
import numpy as np
import glob
import os

animalID = 'SNL_photo40'
BehaviouralTask = '/Two_Alternative_Choice_CentrePortHold/'

inputDir = '/mnt/winstor/sjones/data/bpod_raw_data/'
outputDir = '/home/mwisdom/Documents/data_analysis/analysed_data/One_Second_Hold/' + animalID
if not os.path.isdir(outputDir):
    os.mkdir(outputDir)

filenames_bpod_data = sorted(glob.glob(inputDir + animalID + BehaviouralTask + 'Session Data/' + '*.mat'))
filenames_bpod_settings = sorted(glob.glob(inputDir + animalID + BehaviouralTask + 'Session Settings/' + '*.mat'))

if len(filenames_bpod_settings) != len(filenames_bpod_data) + 1:
    print('error: number of settings files does not match data files')


for count, bpod_file in enumerate(filenames_bpod_data):

    mat_and_RawEvents = load_bpod_file(bpod_file)
    mat = mat_and_RawEvents[0]
    RawEvents = mat_and_RawEvents[1]

    mat_settings = loadmat(filenames_bpod_settings[count])

    SessionData = mat['SessionData']
    nTrials = SessionData['nTrials']

    TrialSequence = SessionData['TrialSequence'][0:nTrials]
    TrialSide = SessionData['TrialSide'][0:nTrials]
    TrialHighPerc = SessionData['TrialHighPerc'][0:nTrials]
    ChosenSide = SessionData['ChosenSide'][0:nTrials]
    Outcomes = SessionData['Outcomes'][0:nTrials]
    ResponseTime = SessionData['ResponseTime'][0:nTrials]
    FirstPoke = SessionData['FirstPoke'][0:nTrials]
    FirstPokeCorrect = SessionData['FirstPokeCorrect'][0:nTrials]


    RawData = SessionData['RawData']
    RawEvents = SessionData['RawEvents']

    OriginalStateNamesByNumber = RawData['OriginalStateNamesByNumber'][0:nTrials]
    OriginalStateData = RawData['OriginalStateData'][0:nTrials]
    OriginalStateTimestamps = RawData['OriginalStateTimestamps'][0:nTrials]
    OriginalEventData = RawData['OriginalEventData'][0:nTrials]
    OriginalEventTimestamps = RawData['OriginalEventTimestamps'][0:nTrials]

    TrialStartTimestamps = SessionData['TrialStartTimestamp'][0:nTrials]
    TrialEndTimestamps = SessionData['TrialEndTimestamp'][0:nTrials]

    TrainingLevel = mat_settings['TrialSettings']['GUI']['TrainingLevel']
    RewardAmount = mat_settings['TrialSettings']['GUI']['RewardAmount']

    df = pd.DataFrame(TrialSequence, columns=['TrialSequence'])
    df['TrialSide'] = TrialSide
    df['TrialHighPerc'] = TrialHighPerc
    df['ChosenSide'] = ChosenSide
    df['Outcomes'] = Outcomes
    df['ResponseTime'] = ResponseTime
    df['FirstPoke'] = FirstPoke
    df['FirstPokeCorrect'] = FirstPokeCorrect
    df['OriginalStateNamesByNumber'] = OriginalStateNamesByNumber
    df['OriginalStateData'] = OriginalStateData
    df['OriginalStateTimestamps'] = OriginalStateTimestamps
    df['OriginalEventData'] = OriginalEventData
    df['OriginalEventTimestamps'] = OriginalEventTimestamps
    df['TrialStartTimestamps'] = TrialStartTimestamps
    df['TrialEndTimestamps'] = TrialEndTimestamps
    df['TrainingLevel'] = TrainingLevel
    df['RewardAmount'] = RewardAmount

    CueDelay = []
    #NumberOfCentrePokes = []

    for trial in df.index:
        Relevant_Trial_Loc = df['OriginalStateData'].iloc[trial]
        # input the relevant filter corresponding to the state you are interested in
        Loc_of_CueDelay_in_sequence = np.where(Relevant_Trial_Loc == 3)
        #CentrePokes = len(Loc_of_CueDelay_in_sequence[0])
        #NumberOfCentrePokes.append(CentrePokes)
        Loc_of_WaitForPortOut_in_sequence = np.where(Relevant_Trial_Loc == 4)

        Relevant_Trial_Loc_2 = df['OriginalStateTimestamps'].iloc[trial]
        StateTimestamp_CueDelay = Relevant_Trial_Loc_2[Loc_of_CueDelay_in_sequence[0][-1]]
        StateTimestamp_WaitForPortOut = Relevant_Trial_Loc_2[Loc_of_WaitForPortOut_in_sequence[0][0]]
        TrialCueDelay = StateTimestamp_WaitForPortOut - StateTimestamp_CueDelay
        CueDelay.append(TrialCueDelay)

    CueDelay = np.asarray(CueDelay)
    CueDelay = np.around(CueDelay, decimals= 3)

    df['CueDelay'] = CueDelay

    SessionDate = []
    for trial in df.index:
        SessionDate.append(SessionData['Info']['SessionDate'])
    SessionDate = np.asarray(SessionDate)

    df['SessionDate'] = SessionDate

    CentrePortHoldTimes = []
    NumberOfCentrePokes = []

    for n in range(0, nTrials):
        TrialEvents = RawEvents['Trial'][n]['Events']
        Port2In = TrialEvents['Port2In']
        Port2Out = TrialEvents['Port2Out']
        if isinstance(Port2In, np.ndarray):
            if len(Port2In) == len(Port2Out):
                TrialCentrePortHoldTimes = Port2Out - Port2In
            else:
                TrialCentrePortHoldTimes = Port2Out[-1] - Port2In
        else:
            TrialCentrePortHoldTimes = Port2Out - Port2In
        if isinstance(TrialCentrePortHoldTimes, float):
            TrialCentrePortHoldTimes = np.asarray(TrialCentrePortHoldTimes)
            CentrePortHoldTimes.append(TrialCentrePortHoldTimes)
        else:
            TrialCentrePortHoldTimes = np.asarray(TrialCentrePortHoldTimes)
            CentrePortHoldTimes.append(TrialCentrePortHoldTimes)
        NumberOfCentrePokes.append(TrialCentrePortHoldTimes.size)

    df['CentrePortHoldTimes'] = CentrePortHoldTimes
    df['NumberOfCentrePokes'] = NumberOfCentrePokes




    extract_start = bpod_file.find('Session Data/') + len('Session Data/')
    extract_end = bpod_file.find('.mat')

    df.to_pickle(outputDir + '/' + bpod_file[extract_start:extract_end] + '.pkl')

    print(outputDir + '/' + bpod_file[extract_start:extract_end] + '.pkl')



'''read in dataframes, create list, concatenate'''

pkl_files = sorted(glob.glob(outputDir + '/*.pkl'))

df_to_concat = []

for pkl_file in pkl_files:
    df_to_concat.append(pd.read_pickle(pkl_file))

df_concat = pd.concat(df_to_concat, ignore_index=True)

df_concat_output_dir = outputDir + '/AllSessionsDataframe'
if not os.path.isdir(df_concat_output_dir):
    os.mkdir(df_concat_output_dir)

df_concat.to_pickle(df_concat_output_dir + '/' + animalID + '_all_sessions' + '.pkl')
