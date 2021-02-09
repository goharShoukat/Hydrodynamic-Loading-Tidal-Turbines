#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 15:44:10 2021

@author: goharshoukat
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#The data file was cleaned to remove the first couple of lines. 
df = pd.read_csv('run001.txt', sep = '\t')
df = df.drop([0])

#all column heads are stored to recreate proper columns
col_head = list(df.columns)
#the data series is throwing an exception that the data is not numeric
#the following for loop converts the entire dataframe to numeric which 
#can then be plotted
for i in range(len(df.columns)):
    x = pd.to_numeric(df[col_head[i]])
    df = df.drop(columns=[col_head[i]])
    df.insert(i, col_head[i], x)


