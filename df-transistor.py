#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<Ross>
  Purpose: understand pandas array
  Created: 09/03/17
"""

import unittest

import pandas as pd
from matplotlib import pyplot as plt
import numpy

df = pd.read_csv('test.csv', sep=',')
volt = str(df.values)
print(volt)
#plt.plot(df['Gate Voltage [V]'].value, df['Channel Current [A]'].value)
#plt.show()





if __name__ == '__main__':
    unittest.main()