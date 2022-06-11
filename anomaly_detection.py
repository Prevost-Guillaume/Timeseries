import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats



class ProbabilisticAnomalyDetector:
    """Basic anomaly detection : often last layer"""

    def __init__(self, p=0.05):
        self.distribution = None
        self.p = p


    def fit(self, data, memory=None, context='out'):
        mean = data.mean()
        std = data.std()
        self.distribution = scipy.stats.norm(mean, std)

        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):
        prob = self.distribution.cdf(data)

        # On calcule l'aire à l'exterieur des valeurs
        prob = (prob<0.5)*prob + (prob>0.5)*(1-prob)    # prob if prob > 0.5 else 1-prob
        prob = 2*prob

        # On récupère les indexs 
        memory['anomaly'] = np.array([i for i in range(len(prob)) if prob[i]<self.p])

        return (data, memory) if context == 'pipeline' else data

