#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 15:44:10 2021

@author: goharshoukat
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv('run001.txt', sep = '\t')
df = df.drop([0])
