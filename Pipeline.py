import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Pipeline:

    def __init__(self, *functions):
        self.functions = functions



    def fit(self, data, memory={}, context='out'):
        d = data.copy()
        memory['data'] = data.copy()

        for f in self.functions:
            d, memory = f.fit(d, memory=memory, context='pipeline')

        return (d, memory) if context == 'pipeline' else d





    def execute(self, data, memory={}, context='out'):
        d = data.copy()
        memory['data'] = data.copy()

        for f in self.functions:
            d, memory = f.execute(d, memory=memory, context='pipeline')

        
        return (d, memory) if context == 'pipeline' else d

    




class Pipeline_:
    # ATTENTION A LA MEMORY : NE PAS UTILISER self.memory MAIS JUSTE LA VARIABLE MEMORY

    def __init__(self, *functions):
        self.functions = functions
        self.memory = {}    # Dict containing all vars ??



    def fit(self, data, memory=None, context='out'):
        d = data.copy()
        self.memory['data'] = data.copy()

        for f in self.functions:
            d, self.memory = f.fit(d, memory=self.memory, context='pipeline')
        
        return d, self.memory if context == 'pipeline' else None




    def execute(self, data, memory=None, context='out'):
        d = data.copy()
        self.memory['data'] = data.copy()

        for f in self.functions:
            d, self.memory = f.execute(d, memory=self.memory, context='pipeline')

        
        return d, self.memory if context == 'pipeline' else d

    
