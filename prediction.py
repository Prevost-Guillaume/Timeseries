import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler




class BasicPrediction:
    def __init__(self, n=1, degree=1, model=LinearRegression()):
        self.n = n
        self.degree = degree
        self.model = model
        self.regressor = None
    

    def fit(self, data, memory=None, context='out'):
        self.regressor = make_pipeline(PolynomialFeatures(degree=self.degree), StandardScaler(), self.model)
        x = [[i] for i in range(len(list(data.dropna())))]
        self.regressor.fit(x,data.dropna())

        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):
        x = [[i] for i in range(len(data)+self.n)]
        pred = self.regressor.predict(x)
        memory['pred'] = pred

        return (data, memory) if context == 'pipeline' else data




class PredictTrend:

    def __init__(self, n=1, degree=1, model=LinearRegression()):
        self.window = None
        self.predictor = BasicPrediction(n=n, degree=degree, model=model)


    def fit(self, data, memory=None, context='out'):
        self.window = max(memory['seasons'])

        memory['trend'] = data.rolling(self.window).mean()
        
        self.predictor.fit(memory['trend'], memory)

        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):

        _, memory = self.predictor.execute(memory['trend'], memory, context='pipeline')
        memory['pred_trend'] = memory['pred'].copy()

        return (data, memory) if context == 'pipeline' else data






class PredictVariance:

    def __init__(self, n=1, degree=1, model=LinearRegression()):
        self.window = None
        self.predictor = BasicPrediction(n=n, degree=degree, model=model)


    def fit(self, data, memory=None, context='out'):
        self.window = max(memory['seasons'])

        memory['variance'] = data.rolling(self.window).std()
        
        self.predictor.fit(memory['variance'], memory)

        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):

        _, memory = self.predictor.execute(memory['variance'], memory, context='pipeline')
        memory['pred_variance'] = memory['pred'].copy()

        return (data, memory) if context == 'pipeline' else data





class PredictSeason:

    def __init__(self, n=1, model=RandomForestRegressor()):
        self.n = n
        self.model = model


    def fit(self, data, memory=None, context='out'):

        t = data.rolling(max(memory['seasons'])).mean()
        v = (data-t).rolling(max(memory['seasons'])).std()
        
        data_normalized = ((data-t)/v).dropna()
        startindex = len(data)-len(data_normalized)

        x = [[(i+startindex)%s for s in memory['seasons']] for i in range(len(data_normalized))]
        self.model.fit(x, data_normalized)

        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):

        x = [[i%s for s in memory['seasons']] for i in range(len(data)+self.n)]
        memory['pred_season'] = self.model.predict(x)

        return (data, memory) if context == 'pipeline' else data




class MergePredictions:

    def __init__(self):
        pass


    def fit(self, data, memory=None, context='out'):

        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):
        pt = 0 
        pv = 1
        ps = 0
        if 'pred_trend' in memory.keys():
            pt = memory['pred_trend']
        if 'pred_variance' in memory.keys():
            pv = memory['pred_variance']
        if 'pred_season' in memory.keys():
            ps = memory['pred_season']
        p = pt+(ps*pv)
        memory['pred'] = p

        return (p, memory) if context == 'pipeline' else p
