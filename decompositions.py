import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.fft import fft, fftfreq
from statsmodels.tsa.stattools import acf
from scipy.signal import argrelextrema


class FindSeasons:
    def __init__(self, mode='acf',maxseasons=2):
        self.mode = mode
        self.maxseasons = maxseasons
        self.seasons = None
    

    def fourrier(self, data):
        N = data.shape[0]
        yf = fft(np.array(data))
        yf = 2.0/N * np.abs(yf[0:N//2])
        xf = fftfreq(N, 1)[:N//2]
        return xf, yf


    def fit(self, data, memory=None, context='out'):
        d = acf(data, nlags=data.shape[0])  if self.mode == 'acf' else data
        x,f = self.fourrier(d)
        maxi = list(argrelextrema(f, np.greater, order=2)[0])
        maxi = [m for m in maxi if m != 0 and 1/x[m] < len(f)//2]
        sorted_maxs = sorted(maxi, key=lambda x:f[x], reverse=True)[:self.maxseasons]
        seasons = list(set([int(1/x[i]) for i in sorted_maxs]))
        
        self.seasons = seasons
        return self.execute(data, memory=memory, context=context)
    

    def execute(self, data, memory=None, context='out'):
        memory['seasons'] = self.seasons
        return (data, memory) if context == 'pipeline' else data





class Detrend:
    """Remove trend from signal"""

    def __init__(self):
        self.window = None


    def fit(self, data, memory=None, context='out'):
        self.window = max(memory['seasons'])
        memory['trend'] = data.rolling(self.window).mean()
        
        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):
        t = data.rolling(self.window).mean()
        memory['trend'] = t
        out = data-t

        return (out, memory) if context == 'pipeline' else out



class Devariance:
    """Remove variance from signal"""

    def __init__(self):
        self.window = None


    def fit(self, data, memory=None, context='out'):
        self.window = max(memory['seasons'])
        memory['variance'] = data.rolling(self.window).std()

        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):
        v = data.rolling(self.window).std()
        memory['variance'] = v
        out = data/v
        
        return (out, memory) if context == 'pipeline' else out




class Deseason:
    """Remove seasonnality from signal"""

    def __init__(self):
        pass


    def fit(self, data, memory=None, context='out'):

        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):
        n = data.shape[0]
        d = data.copy()
        s = sorted(memory['seasons'], reverse=True)
        for season in s:
            pattern = d.groupby(d.index%season).median()
            seasonnal_conponent = pd.Series((list(pattern)*(int(n/season)+1))[:n])
            d = d-seasonnal_conponent
        out = d
        return (out, memory) if context == 'pipeline' else out

