from flask import Flask, render_template, request, redirect
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
from bokeh.embed import components
from bokeh.palettes import Spectral11
from datetime import datetime
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)


app = Flask(__name__)
app.vars={}


#@app.route('/')
#def index():
#  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')


def create_hover_tool():
    """Generates the HTML for the Bokeh's hover data tool on the graph."""
    hover_html = """
      <div>
        <span class="hover-tooltip">@xs date</span>
      </div>
      <div>
        <span class="hover-tooltip">@ys stock price</span>
      </div>
    """
    return HoverTool(tooltips=hover_html)


def create_line_chart(data_df,ticker,args,width = 1200, height = 600,hover_tool=None):
        
    columns = args
    len_col = len(args)
    colors=['red', 'green', 'blue','black']
    leg = ["-".join([ticker,column]) for column in columns]
    dateX_str = ['2016-11-14','2016-11-15','2016-11-16']
    #conver the string of datetime to python  datetime object
    dateX = [datetime.strptime(i, "%Y-%m-%d") for i in data_df['date']]
    x_axis = dateX
    data = {'xs': [x_axis]*len_col,
            'ys': [data_df[column].values for column in columns],
            'labels': leg[:len_col],
            'color':colors[:len_col]}

    source = ColumnDataSource(data)
    
    tools = []
    if hover_tool:
        tools = [hover_tool,]
        
    p1 = figure(x_axis_type="datetime", title="Stock Prices",width=1200, height=600, tools=tools,
                  responsive=True, outline_line_color="#666666",toolbar_location="above")
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'
    
    
    #Add dashes
    p1.multi_line(xs='xs', ys='ys', legend='labels',line_color = 'color', source=source)
    
    #p1.line(datetime(data_df['date']), data_df[data_column], line_color=colors[:len_col], legend=ticker)
    #p1.multi_line(xs=[x_axis]*len_col,
    #            ys=[data_df[column].values for column in columns],
    #            line_color=colors[:len_col],
    #            line_width=3,
    #            legend = leg)
    p1.legend.location = "top_left"
    p1.toolbar.logo = None
#    hover = p1.select(dict(type=HoverTool))
#    hover.tooltips = [("date", "@xs"), ("price", "@ys")]
#    hover.mode = 'mouse'

    return p1

@app.route('/index_lulu',methods=['GET','POST'])
def index_lulu():
    variables = []
    if request.method == 'GET':
        return render_template('userinfo_lulu.html')
    else:
        #request was a POST
        app.vars['ticker_symbol'] = request.form['ticker_symbol_lulu']
        for checkbox in "close", "adj_close", "open","adj_open":
            value = request.form.get(checkbox)
            if value:
                app.vars[checkbox] = checkbox
                variables.append(checkbox)
    
    variables = list(set(variables))
    payload = ('bhavikaj@gmail.com','bhavikaj-di')
    ticker = app.vars['ticker_symbol']
    url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker='+ticker+'&api_key=BQR2bnRMkoJwe8QVn_6_'
    req = requests.get(url, auth=HTTPBasicAuth('bhavikaj@gmail.com','bhavikaj-di'))

    data_dict = req.json()
    columns = []
    temp = data_dict['datatable']['columns']
    for item in temp:
        columns.append(item['name'])

    data = []
    for i in range(len(data_dict['datatable']['data'])):
        data.append(data_dict['datatable']['data'][i])
        data_df = pd.DataFrame(data, columns=columns)

#    f = open('%s.txt'%(app.vars['ticker_symbol']),'w')
#    f.write('Name: %s\n'%(app.vars['ticker_symbol']))
#    f.write(" ".join(variables))
#    f.close()
        
    arguments = [app.vars[checkbox] for checkbox in variables]  
    hover = create_hover_tool()
    plot = create_line_chart(data_df,ticker,arguments,hover_tool = hover)
    script, div = components(plot)

    #return render_template("chart.html",
    return render_template("chart.html",the_div=div, the_script=script)


if __name__ == '__main__':
    app.run(port=33507,debug=True)
