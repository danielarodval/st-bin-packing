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
    selected_containers[container] = st.number_input(f"Number of {container}", min_value=0, max_value=12, step=1)

total_containers = sum(selected_containers.values())
if total_containers > 12:
    st.error("The total number of containers cannot exceed 12. Please adjust your selections.")

#%% Select Mission Type
mission_types = items.loc[items['utilization'] != 'General', 'utilization'].unique()
selected_mission_types = st.multiselect("Select Mission Types", mission_types)
if 'General' in selected_mission_types or not selected_mission_types:
    mission_items = items.copy()
else:
    mission_items = pd.concat([items.loc[items['utilization'] == 'General'], items.loc[items['utilization'].isin(selected_mission_types)]])

#%% Initialize Bins based on selected containers
bins = []
for container, count in selected_containers.items():
    for _ in range(count):
        container_specs = containers.loc[containers['item'] == container].iloc[0]
        bins.append(bf.Bin(
            max_volume=container_specs['volume'],
            max_weight=container_specs['weight'],
            max_height=container_specs['height'],
            max_length=container_specs['length'],
            max_width=container_specs['width']))
        
#%% Pack Items
packed_bins, missing_items = bf.pack_items([bf.Item(row['item'], row['length'], row['width'], row['height'], row['weight'], row['volume'], row['utilization'], row['size'], row['count']) for index, row in mission_items.iterrows()], bins)

# Display results
if missing_items:
    st.write("#### Missing Items")
    for item in missing_items:
        st.write(f"* {item.name} {item.packed_count}/{item.count}")

bf.print_bins(packed_bins)
