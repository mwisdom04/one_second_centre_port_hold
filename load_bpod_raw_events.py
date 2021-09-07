import load_nested_structs as load_ns

def load_bpod_file(main_session_file):
    # gets the Bpod data out of MATLAB struct and into python-friendly format
    loaded_bpod_file = load_ns.loadmat(main_session_file)
    # as RawEvents.Trial is a cell array of structs in MATLAB, we have to loop through the array and convert the structs to dicts
    trial_raw_events = loaded_bpod_file['SessionData']['RawEvents']['Trial']
    for trial_num, trial in enumerate(trial_raw_events):
        trial_raw_events[trial_num] = load_ns._todict(trial)
    loaded_bpod_file['SessionData']['RawEvents']['Trial'] = trial_raw_events
    return loaded_bpod_file, trial_raw_events