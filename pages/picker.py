import streamlit as st
import yfinance as yf
#fast loading of th data
yf.pdr_override()
import warnings
warnings.filterwarnings('ignore')
#cache the data set
import requests_cache
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'
import requests
from bs4 import BeautifulSoup


st.set_page_config(
  page_title="Poly-Invest",
  layout="centered",
  page_icon="❤️",
  initial_sidebar_state="expanded",
)
st.header("Stock & Crypto Prediction App")

st.sidebar.subheader('Query parameters')
st.header("**Stock**")
# Stock Fear & Greed Index
page = requests.get('https://www.google.com/finance/markets/most-active?hl=en')
soup = BeautifulSoup(page.content, 'html.parser')
for i in range(0,min(5,len(soup.select('div.ZvmM7')))):
  data = soup.select('div.ZvmM7')
  st.write(data[i].text)

st.header("**Crypto**")

page = requests.get('https://www.google.com/finance/markets/cryptocurrencies?hl=en')
soup = BeautifulSoup(page.content, 'html.parser')
for i in range(0,min(5,len(soup.select('div.ZvmM7')))):
  data = soup.select('div.ZvmM7')
  st.write(data[i].text)

