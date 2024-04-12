import pandas as pd
import streamlit as st
import bp_func as bf
import numpy as np

st.set_page_config(layout="wide")
st.title("Network Flow Test")
st.write("## User Oriented Approach")
st.write("Item ledger configuration for network flow. The app will include an interface to allow the user to select the container, select the mission type, then filter the items to be packed. The app will then display the network flow results.")

#%% Load Data
df = pd.read_csv('Cost Estimates.csv')

# Clean Data
df = df.dropna()
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
# turn all columns to lowercase
df.columns = df.columns.str.lower()
df.columns= df.columns.str.strip()

df = df.iloc[:, 6:]
df = df.drop(df.columns[[3, 5, 6, 14]], axis=1)

containers = df.loc[df['utilization'] == 'Container']
items = df.loc[df['utilization'] != 'Container']
items.insert(2, 'count', 1)