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

