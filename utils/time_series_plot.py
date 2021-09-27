#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 21:23:21 2019

@author: aneesh
"""

import pandas as pd
from matplotlib import pyplot

df = pd.read_csv("Tasks.csv")
df['time stamp'] = df['time stamp'] - df['time stamp'][0]
df = df.loc[0:]
df2 = df[['x_acc', 'y_acc', 'z_acc']]
df3 = df2[:885]
series = pd.Series(df['x_acc'].values, index=df['time stamp'])
#df4 = df['time stamp'][:175]
series.plot()
pyplot.show()

df2 = pd.DataFrame(df2.values, index = df['time stamp'], columns= ["Accelerometer X", "Accelerometer Y", "Accelerometer Z" ])
pyplot.figure()
ax = df2.plot(color = ['#1570BF', 'g', '#BF0404'], linewidth = 1)
ax.legend(loc='best', fancybox=True, framealpha=0)
ax.set_facecolor("#F2F2F2")
ax.grid()
ax.set_ylabel("Accelerometer")
pyplot.suptitle("Accelerometer Readings")
pyplot.savefig('time-series.pdf', dpi=1200)

ax.plot()
