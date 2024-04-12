import pandas as pd
import streamlit as st
import pages.functions.bp_func as bf
import numpy as np

st.set_page_config(layout="wide")
st.title("🌐 Network Flow Test")
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
    
st.write("### Container Selection")
selected_containers = {}
for container in containers['item'].unique():
    selected_containers[container] = st.number_input(f"Number of {container}", min_value=1, max_value=12, step=1)

total_containers = sum(selected_containers.values())
if total_containers > 12:
    st.error("The total number of containers cannot exceed 12. Please adjust your selections.")