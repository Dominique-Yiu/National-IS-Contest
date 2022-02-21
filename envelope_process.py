#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/21 8:39
# @Author  : Yiu
# @Site    : https://github.com/dominique-yiu
# @File    : envelope_process.py
# @Software: PyCharm
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.function_base import  append
from scipy.signal import argrelmax, argrelmin, argrelextrema
from scipy.optimize import leastsq
