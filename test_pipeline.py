import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


from Pipeline import Pipeline
from prediction import PredictSeason
from transformations import *
from data_functions import load_data


data = load_data('data/hour_weather.csv')['temp']
data = load_data('data/raclette.csv')['raclette']
data = pd.read_csv('data/AirPassengers.csv')['#Passengers']



# Normalize timeserie (remove trend and variance)
show_data_pip = Pipeline(PlotSerie(label='data'), ShowPlot(title='input timeserie'))
show_data_pip.fit(data)

normalize = Pipeline(UpdateMemory({"seasons" : [12]}), 
                     Detrend(), 
                     Devariance())

normalize = Pipeline(FindSeasons(maxseasons=1), 
                     Detrend(), 
                     Devariance())
normalize.fit(data)


# Anomaly detector
anomalypip = Pipeline(normalize,
                      Deseason(),
                      ProbabilisticAnomalyDetector(p=0.05),
                      PlotAnomalies(label='anomalies'),
                      ShowPlot(title='anomaly detection')
                      )
datapip = anomalypip.fit(data)



# Timeserie forecasting
predpip = Pipeline(FindSeasons(maxseasons=1),
                   PlotSerie('data'),
                   PredictTrend(n=50, degree=1),
                   PredictVariance(n=50, degree=1),
                   PredictSeason(n=50),
                   MergePredictions(),
                   PlotSerie('prediction'),
                   ShowPlot(title='forecasting')
                   )
datapip = predpip.fit(data)


