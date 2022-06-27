import streamlit as st
import yfinance as yf
#fast loading of th data
yf.pdr_override()
import pandas as pd
import cufflinks as cf
import datetime
from plotly import graph_objs as go
from datetime import date
# Ta
import numpy as np
import matplotlib.pyplot as plt
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator
#FB
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')
pd.core.common.is_list_like = pd.api.types.is_list_like
import seaborn as sns
import matplotlib.dates as mdates
import requests
from bs4 import BeautifulSoup
#cache the data set
import requests_cache
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'


st.set_page_config(
  page_title="Poly-Invest",
  layout="centered",
  page_icon="❤️",
  initial_sidebar_state="expanded",
)
st.header("Stock & Crypto Prediction App")


# Sidebar
st.sidebar.subheader('Query parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2021, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date.today())

#valid date checker
if start_date < end_date:
  st.sidebar.success('Start date: `%s`\n\nEnd date: `%s`' % (start_date, end_date))
else:
  st.sidebar.error('Error: End date must fall after start date.')

# Retrieving tickers data
ticker_list = pd.read_csv('data-stock.txt')
tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list) # Select ticker symbol
tickerDuration = st.sidebar.selectbox('Time', ('1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max'))
tickerData = yf.Ticker(tickerSymbol,session=session) # Get ticker data
tickerDf = tickerData.history(period=tickerDuration,interval="1d", start=start_date, end=end_date)
#get the historical prices for this ticker
df = yf.download(tickerSymbol,start=start_date, end=end_date)

st.header("**About Company**")

# Ticker information
string_logo = '<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

cmp_name = tickerData.info['longName']
st.header('**%s**' % cmp_name)

string_summary = tickerData.info['longBusinessSummary']
st.info(string_summary)

# Bollinger bands
st.header('**Bollinger Bands**')
qf=cf.QuantFig(df,title='First Quant Figure',legend='top',name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

# Moving Average Convergence Divergence
macd = MACD(df['Close']).macd()

# Resistence Strength Indicator
rsi = RSIIndicator(df['Close']).rsi()


# Plot MACD
st.header('Stock Moving Average Convergence Divergence (MACD)')
st.area_chart(macd)

# Plot RSI
st.header('Stock RSI ')
st.line_chart(rsi,use_container_width=True)




# forecast
st.header('**Stock Forecast**')
df.reset_index(inplace=True)
data=df[["Date","Adj Close"]]
data=data.rename(columns={"Date": "ds", "Adj Close": "y"})
n=len(data)
df_train=data[0:n//2]
df_test=data[n//2:n]

m = Prophet()
m.fit(data)
future = m.make_future_dataframe(periods=411)
forecast = m.predict(future)
fig1 = m.plot(forecast)
st.write(fig1)

# Crypto Fear & Greed Index
page = requests.get('https://alternative.me/crypto/fear-and-greed-index/')
soup = BeautifulSoup(page.content, 'html.parser')
st.write("**Crypto Fear & Greed Index: **"+soup.select('div.fng-circle')[0].text)

# Stock Fear & Greed Index
page = requests.get('https://www.tickertape.in/market-mood-index')
soup = BeautifulSoup(page.content, 'html.parser')
st.write("**Stock Fear & Greed Index: **"+soup.select('span.number')[0].text)


# News
st.header("**News About: " + cmp_name +"**")
for info in tickerData.news:
  st.write("<a target='_blank' href='"+info['link']+"'>"+info["title"]+"</a>",unsafe_allow_html=True)

st.write(df)

# Api
st.write('---')
# st.write(tickerData.info)
#TODO remover unwanted line

