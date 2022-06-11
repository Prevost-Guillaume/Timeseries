import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



class ShowPlot:
    def __init__(self, title=None):
        self.title=title


    def fit(self, data, memory=None, context='out'):
        return self.execute(data, memory=memory, context=context)



    def execute(self, data, memory=None, context='out'):
        plt.legend()
        if self.title is not None:
            plt.title(self.title)
        plt.show()

        return (data, memory) if context == 'pipeline' else data



class PlotSerie:
    def __init__(self, label=None):
        self.label=label


    def fit(self, data, memory=None, context='out'):
        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):
        if self.label is None:
            pd.Series(data).plot()
        else:
            pd.Series(data).plot(label=self.label)
        return (data, memory) if context == 'pipeline' else data



class PlotAnomalies:
    def __init__(self, label=None):
        self.label=label


    def fit(self, data, memory=None, context='out'):
        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):
        memory['data'].plot(label='data')
        x = memory['anomaly']
        y = [memory['data'][i] for i in x]
        plt.scatter(x,y,c='red',label=self.label)

        return (data, memory) if context == 'pipeline' else data



