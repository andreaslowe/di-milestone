from flask import Flask, render_template, request, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests
import simplejson as json
import pandas as pd
import datetime as dt
from bokeh.plotting import figure, output_file, show

#get ticker symbol, set date range, pull data from Quandl, and put in dataframe
def get_data(ticker):
	
	current_date = dt.datetime.now().date().strftime("%Y-%m-%d")
	begin_date = dt.datetime.now().date() + dt.timedelta(-30)
	begin_date = begin_date.strftime("%Y-%m-%d")

	#import data
	myURL = 'https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + 
	'/data.json?api_key=Ny7LjkeNwh1aFxjHewmJ&start_date=' + begin_date + '&end_date=' + current_date

	r = requests.get(myURL)
	rawdata = r.json()['dataset_data']
	stock_df = df.DataFrame(rawdata['data'], columns = rawdata['column_names'])
	return stock_df

#graph data
def plot_data(stock_df, data_sel):
	p = figure(title="Quandl Stock Prices", x_axis_label='Date', y_axis_label='Price')
	if data_sel == 'closing':	
		p.line(stock_df['Date'], stock_df['Close'], legend="Selection", line_width=2)




#default Flask settings
app = Flask(__name__)

app.vars = {}

#ticker= 'FB'

#@app.route('/')
#def index():
#  return render_template('index.html')
@app.route('/')
def main():
	return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
	return render_template('index.html')

#@app.route('/about')
#def about():
#  return render_template('about.html')

 #code to use text box to get stock ticker info and check boxes for user input
@app.route('/', methods=['POST'])
def my_form_post():
    tickStr = request.form['tickerText']
	reqList = request.form['priceCheck'] # checkboxes

	app.vars['ticker'] = tickStr.upper()
	app.vars['priceReqs'] = reqList



if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
