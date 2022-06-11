import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from pytrends.request import TrendReq
from meteostat import Point, Daily, Hourly, Monthly


def load_google_trend_data(word='raclette', timeframe='all'):
    """Return google trends data"""
    pytrends = TrendReq(hl='fr-FR', tz=360)
    kw_list = [word]
    pytrends.build_payload(kw_list, cat=0, timeframe='all', geo='', gprop='')
    data = pytrends.interest_over_time()
    return data[word]



def load_weather_data(start=datetime(2010, 1, 1), end=datetime.today(), location=None, sampling='day'):
    """Return weather data"""
    if location is None:
        location = Point(50.62925, 3.057256)

    if sampling == 'month':
        data = Monthly(location, start, end)
        col = ['tavg', 'prcp', 'wspd', 'pres']
    elif sampling == 'day':
        data = Daily(location, start, end)
        col = ['tavg', 'prcp', 'wdir', 'wspd', 'pres']
    elif sampling == 'hour':
        data = Hourly(location, start, end)
        col = ['temp', 'rhum', 'prcp', 'wdir', 'wspd', 'pres']

    data = data.fetch()

    return data[col]

    
def load_data(file):
    return pd.read_csv(file)

def save_data(data, filename):
    data.to_csv(filename)

if __name__ == '__main__':

    for s in ['hour','day','month']:
        data = load_weather_data(sampling=s)
        save_data(data, s+'_weather.csv')

    for word in ['raclette','location appartement','Jeux olympiques','foot']:
        data = load_google_trend_data(word=word, timeframe='all')
        save_data(data, word+'.csv')
    

    for word in ['raclette','location appartement','Jeux olympiques','foot']:
        data = load_data(word+'.csv')
        data.plot()
        plt.legend()
        plt.show()
