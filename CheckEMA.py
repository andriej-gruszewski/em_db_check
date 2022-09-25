#!/usr/bin/env python
# coding: utf-8

# In[14]:


import streamlit as st 
import pandas as pd
import datetime as dt
import numpy as np
import pandas_ta as ta


# In[15]:


from sqlalchemy import create_engine
engine = create_engine('sqlite:///CryptoDB.db')


# In[16]:


symbols = pd.read_sql('SELECT name FROM sqlite_master WHERE type="table"', engine).name.to_list()


# In[ ]:


st.title('Welcome to live TA platform')


# In[17]:


def applytechnicals(df):
    df["EMA_5"] = ta.ema(df['c'], length=5)
    df["EMA_20"] = ta.ema(df['c'], length=20)
    df.dropna(inplace=True)


# In[30]:


def qry(symbol):
    now = dt.datetime.utcnow()
    before = now - dt.timedelta(minutes=120)
    qry_str = f"""SELECT E,c FROM '{symbol}' WHERE E >= '{before}'"""
    df = pd.read_sql(qry_str,engine)
    df.E = pd.to_datetime(df.E)
    df = df.set_index('E')
    df = df.resample('5min').last() # 5 min charts
    applytechnicals(df)
    df['position'] = np.where(df["EMA_5"] > df["EMA_20"], 1, 2)
    return df


# In[144]:


def check():
    for symbol in symbols:
        if len(qry(symbol).position) > 1:
            #if qry(symbol).position[-1] and qry(symbol).position.diff()[-1]:
            if qry(symbol).position[-1] == 1 and qry(symbol).position[-1] - qry(symbol).position[-2] == -1:
                st.write(symbol+" LONG")
            elif qry(symbol).position[-1] == 2 and qry(symbol).position[-1] - qry(symbol).position[-2] == 1:
                st.write(symbol+" SHORT")
            


# In[ ]:


st.button('Get EMA Cross', on_click=check())

