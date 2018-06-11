import requests
from requests.auth import HTTPBasicAuth
#import simplejson as json
import json
import pandas as pd
from bokeh.io import output_notebook
import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
import bokeh

payload = ('bhavikaj@gmail.com','bhavikaj-di')
ticker = 'GOOG'
url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker='+ticker+'&api_key=BQR2bnRMkoJwe8QVn_6_'
req = requests.get(url, auth=HTTPBasicAuth('bhavikaj@gmail.com','bhavikaj-di'))

data_dict = req.json()
# temp = json.dumps(data_dict)
# ticker_data = json.dumps(temp)
columns = []
temp = data_dict['datatable']['columns']
for item in temp:
    columns.append(item['name'])

data = []
for i in range(len(data_dict['datatable']['data'])):
    data.append(data_dict['datatable']['data'][i])
    data_df = pd.DataFrame(data, columns=columns)
len(data_df)



def datetime(x):
    return np.array(x, dtype=np.datetime64)

p1 = figure(x_axis_type="datetime", title="Stock Closing Prices")
p1.grid.grid_line_alpha=0.3
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Price'

p1.line(datetime(data_df['date']), data_df['adj_close'], color='#A6CEE3', legend='GOOG')
p1.legend.location = "top_left"

show(p1)