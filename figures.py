import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

'''add for loop to repeat and plot for all mice - look at psychometric photometry figures'''

df = pd.read_pickle('/home/mwisdom/Documents/data_analysis/analysed_data/One_Second_Hold/SNL_photo36/AllSessionsDataframe/SNL_photo36_all_sessions.pkl')

df = df.set_index('CueDelay')

x_values = df.index.unique()
y_values = []

for x in x_values:
    y = df.loc[x, 'NumberOfCentrePokes'].mean()
    y_values.append(y)

fig, ax = plt.subplots()
ax.plot(x_values, y_values)
fig.show()

