from flask import Flask, render_template, request, redirect
import requests
import simplejson as json
import pandas as pd
import datetime as dt
import bokeh
from bokeh.plotting import figure
from bokeh.embed import components


#get ticker symbol, set date range, pull data from Quandl, and put in dataframe
def get_data(ticker):
	
	current_date = dt.datetime.now().date().strftime("%Y-%m-%d")
	begin_date = dt.datetime.now().date() + dt.timedelta(-30)
	begin_date = begin_date.strftime("%Y-%m-%d")

	#import data
	myURL = 'https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + '/data.json?api_key=Ny7LjkeNwh1aFxjHewmJ&start_date=' + begin_date + '&end_date=' + current_date

	r = requests.get(myURL)
	rawdata = r.json()['dataset_data']
	stock_df = pd.DataFrame(rawdata['data'], columns = rawdata['column_names'])
	stock_df['Date'] =pd.to_datetime(stock_df['Date'])
	return stock_df

#graph data
def plot_data(stock_df, data_sel):
	p = figure(title="Quandl Stock Prices", x_axis_label='Date', y_axis_label='Price')
	
	if 'closing' in data_sel:
		p.line(stock_df['Date'], stock_df['Close'], legend="Closing Price", line_width=2)
	if 'opening' in data_sel:
		p.line(stock_df['Date'], stock_df['Open'], legend="Opening Price", line_width=2, line_color = "red")
	if 'adj_opening' in data_sel:
		p.line(stock_df['Date'], stock_df['Adj. Open'], legend="Adjusted Opening Price", line_width=2, line_color = "black")
	if 'adj_closing' in data_sel:
		p.line(stock_df['Date'], stock_df['Adj. Close'], legend="Adjusted Closing Price", line_width=2, line_color = "purple")
	script, div = components(p)
	return script, div



#default Flask settings
app = Flask(__name__)

@app.route('/')
def main():
	return redirect('/index') #changed redirect

@app.route('/about')
def about():
	return render_template('about.html')

#code to use text box to get stock ticker info and check boxes for user input
@app.route('/index', methods=['GET','POST'])
def index():
	tick_str = request.form.get('ticker')
	data_sel =  request.form.getlist('features')
	return tick_str, data_sel
    return render_template('index.html')

@app.route('/plotpage', methods=['GET','POST'])
def plotpage():
	
	df = get_data(tick_str)
	script, div = plot_data(df, data_sel)
	return render_template('stock.html', script=script, div=div)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
	#app.run(port=33507)
  
