"""
Attempting bin packing via Fractional Knapsack approach and Containers approach.

Plotly visualization will leverage sub containers to show the bin packing.

The app will include an interface to allow the user to select the container, select the mission type, then filter 
"""

import pandas as pd
import streamlit as st
import numpy as np
import pages.functions.bp_func as bf

st.set_page_config(layout="wide")

st.title("📦 Bin Packing Test")
st.write("## Algorithm Centralized Approach")
st.write("Item ledger configuration for bin packing. The app will include an interface to allow the user to select the container, select the mission type, then filter the items to be packed. The app will then display the bin packing results.")

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

containers = df.loc[df['utilization'] == 'Container'].copy()  # Use copy here
items = df.loc[df['utilization'] != 'Container'].copy()  # Use copy here
items['count'] = 1  # Direct assignment without loc since it's a clean copy
items['size'] = items['volume'].apply(bf.classify_size)  # Direct assignment without loc since it's a clean copy


#%% Display Data

with st.expander("View Imported Data"):
    st.write("#### Containers")
    st.dataframe(containers)
    st.write("#### Items")
    st.dataframe(items)

#%% Select Container
container = st.selectbox("Select Container", containers['item'].unique())
container = containers.loc[containers['item'] == container]
st.write(container)

#%% Select Mission Type
mission_types = items.loc[items['utilization'] != 'General', 'utilization'].unique()
selected_mission_types = st.multiselect("Select Mission Types", mission_types)
if 'General' in selected_mission_types:
    mission_items = items.copy()
else:
    mission_items = pd.concat([items.loc[items['utilization'] == 'General'], items.loc[items['utilization'].isin(selected_mission_types)]])

expand_items = st.expander("View Mission Items")
with expand_items:
    mission_items = st.data_editor(mission_items)

#%% Number of Bins
num_bins = st.slider("Number of Bins", 1, 12, 1)

#%% Pack Items
item_objects = [bf.Item(row['item'], row['length'], row['width'], row['height'], row['weight'], row['volume'], row['utilization'], row['size'], row['count']) for index, row in mission_items.iterrows()]

bins = [bf.Bin(
    max_volume=container['volume'].values[0],
    max_weight=container['weight'].values[0],
    max_height=container['height'].values[0],
    max_length=container['length'].values[0],
    max_width=container['width'].values[0]) for _ in range(num_bins)]  # Initialize bins

#%% Example usage
st.write("## Modeling")

packed_bins, missing_items = bf.pack_items(item_objects, bins)

if(missing_items == []):
    st.write("All items packed")
else:
    st.write("#### Missing Items")
    for item in missing_items:
        st.write(f"* {item.name} {item.packed_count}/{item.count}")

st.write("#### Packed Bins")

num_bins = len(packed_bins)
num_columns = min(num_bins, 5)  # Maximum of 5 columns

bf.print_bins(packed_bins)