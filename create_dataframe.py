from load_bpod_raw_events import load_bpod_file
from load_nested_structs import loadmat
import pandas as pd
import numpy as np
import glob
import os

'''additions: 
    - add comments to make code easy to interpret
    - only create new dataframes for those sessions which dataframes haven't previously been created
    - check number of trials in a session and discard if under (x) no trials'''

# do you want to overwrite pkl files previously created for the mouse? write True if yes and False if no
overwrite_old_files = False

animalIDs = ['SNL_photo45'] #'SNL_photo50','SNL_photo52', 'SNL_photo53', 'SNL_photo54']         #'SNL_photo45', 'SNL_photo47', 'SNL_photo48', 'SNL_photo49', 'SNL_photo50',

for animalID in animalIDs:

    print('Curating dataframe for ' + animalID)

    BehaviouralTask = '/Two_Alternative_Choice_CentrePortHold/'

    inputDir = '/home/matthew/Documents/transferred_files/'
    outputDir = '/home/matthew/Documents/data/analysed_data/one_second_centre_port_hold/' + animalID
    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)

    filenames_bpod_data = sorted(glob.glob(inputDir + animalID + BehaviouralTask + 'Session Data/' + '*.mat'))
    #filenames_bpod_settings = sorted(glob.glob(inputDir + animalID + BehaviouralTask + 'Session Settings/' + '*.mat'))

    #if len(filenames_bpod_settings) != len(filenames_bpod_data) + 1:
        #print('error: number of settings files does not match data files')


    for count, bpod_file in enumerate(filenames_bpod_data):

        extract_start = bpod_file.find('Session Data/') + len('Session Data/')
        extract_end = bpod_file.find('.mat')
        outputFileName = outputDir + '/' + bpod_file[extract_start:extract_end] + '.pkl'

        Session_time_date = bpod_file.split("Session Data/", 1)[1]

        if overwrite_old_files == False:
            if (os.path.isfile(outputFileName)):
                print('Session already analysed: ' + Session_time_date)
                continue
            else:
                pass

        mat = loadmat(bpod_file)

        SessionData = mat['SessionData']

        try:
            SessionData['nTrials']
        except:
            print('Session is invalid: ' + Session_time_date)
            continue
        else:
            pass

        nTrials = SessionData['nTrials']

        if nTrials < 10:
            print('Session ignored as less then 10 trials: ' + Session_time_date)
            continue
        else:
            pass

        print('Analysing session: ' + Session_time_date)

        mat_and_RawEvents = load_bpod_file(bpod_file)
        mat = mat_and_RawEvents[0]
        RawEvents = mat_and_RawEvents[1]

        #mat_settings = loadmat(filenames_bpod_settings[count])

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

        #TrainingLevel = mat_settings['TrialSettings']['GUI']['TrainingLevel']
        #RewardAmount = mat_settings['TrialSettings']['GUI']['RewardAmount']

        TrainingLevel = SessionData['SettingsFile']['GUI']['TrainingLevel']
        TrainingLevel = [TrainingLevel] * nTrials
        RewardAmount = SessionData['SettingsFile']['GUI']['RewardAmount']
        RewardAmount = [RewardAmount] * nTrials
        Punish = SessionData['SettingsFile']['GUI']['Punish']
        Punish = [Punish] * nTrials
        VariableCueDelay = SessionData['SettingsFile']['GUI']['VariableCueDelay']
        VariableCueDelay = [VariableCueDelay] * nTrials

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
        df['Punish'] = Punish
        df['VariableCueDelay'] = VariableCueDelay
        df['RollingMean'] = df['FirstPokeCorrect'].rolling(50, min_periods=1).sum() * 2

        CumPer = df['FirstPokeCorrect'].cumsum()
        CumPer = (100 * CumPer)/(df.index + 1)
        df['CumulativePerformance'] = CumPer

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
            if isinstance(Port2In, float):
                Port2In_list = []
                Port2In_list.append(Port2In)
                Port2In = np.asarray(Port2In_list)
            elif isinstance(Port2Out, float):
                Port2Out_list = []
                Port2Out_list.append(Port2Out)
                Port2Out = np.asarray(Port2Out_list)
            else:
                pass
            if isinstance(Port2In, np.ndarray) & isinstance(Port2Out, np.ndarray):
                if len(Port2In) == len(Port2Out):
                    TrialCentrePortHoldTimes = Port2Out - Port2In
                elif len(Port2In) == len(Port2Out) + 1:
                    TrialCentrePortHoldTimes = Port2Out - Port2In[:-1]
                elif len(Port2In) + 1 == len(Port2Out):
                    TrialCentrePortHoldTimes = Port2Out[1:] - Port2In
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

        df.to_pickle(outputFileName)

        print('dataframe saved as: ' + outputFileName)



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
