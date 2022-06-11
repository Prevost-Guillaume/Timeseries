import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Mult:
    """Example class : Multiply signal"""

    def __init__(self, n):
        self.n = n


    def fit(self, data, memory=None, context='out'):
        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):
        d = data.copy()
        out = data * self.n

        return (out, memory) if context == 'pipeline' else out




class UpdateMemory:
    """Update memory"""

    def __init__(self, update):
        self.update = update


    def fit(self, data, memory=None, context='out'):
     
        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):
        for k in self.update:
            memory[k] = self.update[k]

        return (data, memory) if context == 'pipeline' else data


class SetSeasons:
    def __init__(self, seasons):
        self.seasons = seasons


    def fit(self, data, memory=None, context='out'):
        return self.execute(data, memory=memory, context=context)


    def execute(self, data, memory=None, context='out'):
        memory["seasons"] = self.seasons
        return (data, memory) if context == 'pipeline' else data


    