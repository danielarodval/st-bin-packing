import streamlit as st
import matplotlib.pyplot as plt
import pages.functions.nflow as nf
import networkx as nx
import pandas as pd
import pages.functions.bp_func as bf
import random

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
items['size'] = items['volume'].apply(bf.classify_size)  # Direct assignment without loc since it's a clean copy

#%% Display Data

with st.expander("View Imported Data"):
    st.write("#### Containers")
    st.dataframe(containers)
    st.write("#### Items")
    st.dataframe(items)
st.divider()
#%% Select Container

st.write("### Container Selection")
selected_containers = {}
for container in containers['item'].unique():
    selected_containers[container] = st.number_input(f"Number of {container}", min_value=0, max_value=12, step=1)

total_containers = sum(selected_containers.values())
if total_containers > 12:
    st.error("The total number of containers cannot exceed 12. Please adjust your selections.")
st.divider()
#%% Select Mission Type
st.write("### Item Selection")
rand_item_ct = st.checkbox("Randomize Item Counts")

if rand_item_ct:
    items['count'] = [random.randint(1, 20) for _ in range(len(items))]
else:
    items['count'] = 0  # Direct assignment without loc since it's a clean copy

mission_types = items.loc[items['utilization'] != 'General', 'utilization'].unique()
selected_mission_types = st.multiselect("Select Mission Types", mission_types)
if 'General' in selected_mission_types or not selected_mission_types:
    mission_items = items.copy()
else:
    mission_items = pd.concat([items.loc[items['utilization'] == 'General'], items.loc[items['utilization'].isin(selected_mission_types)]])
        
#%%  Create Item Selection

expand_items = st.expander("View Mission Items")
with expand_items:
    mission_items = st.data_editor(mission_items)
    dis_graph = False

#%% Initialize Bins based on selected containers & items
item_objects = [bf.Item(row['item'], row['length'], row['width'], row['height'], row['weight'], row['volume'], row['utilization'], row['size'], row['count']) for index, row in mission_items.iterrows()]

bins = []
for container, count in selected_containers.items():
    for _ in range(count):
        container_specs = containers.loc[containers['item'] == container].iloc[0]
        bins.append(bf.Bin(
            max_volume=container_specs['volume'],
            max_weight=container_specs['weight'],
            max_height=container_specs['height'],
            max_length=container_specs['length'],
            max_width=container_specs['width'],
            bin_type=container_specs['unit'],
            name=container_specs['item']))

#%% Create Network
st.divider()

nf_naming_convention = {
    'Source':'Ledger',
    'Sink':'TEU'
    }

# Create the network flow graph
G = nf.create_flow_network_binned(mission_items, bins, nf_naming_convention)

# Compute maximum flow
flow_value, flow_dict = nx.maximum_flow(G, nf_naming_convention['Source'], nf_naming_convention['Sink'])

# Display the graph
st.write("### Network Flow Graph")
dis_graph = st.checkbox("Display Graph")

if dis_graph:
    st.pyplot(nf.display_graph(G,nf_naming_convention, bins))
else:
    st.write("Click the checkbox to display the graph.")

with st.sidebar:
        st.write("### Network Flow Results")
        st.write("Maximum flow value (total loaded volume):", flow_value)
        st.write("Flow along each edge:")
        for node in flow_dict:
            for conn in flow_dict[node]:
                if flow_dict[node][conn] > 0:
                    st.write(f"{node} -> {conn}: {flow_dict[node][conn]}")

#%% Generated Code
st.divider()

st.write("### General Implementation")
with st.expander("View Code"):
    st.code("""
    # Define manifest and containers
    manifest = {
        'Item1': 10,
        'Item2': 20,
        'Item3': 15
    }
    containers = {
        'Container1': 20,
        'Container2': 25
    }

    # Create the network flow graph
    G = nf.create_flow_network(manifest, containers)

    # Compute maximum flow
    flow_value, flow_dict = nx.maximum_flow(G, 'Ledger', 'TEU')

    # Display the graph
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    dis_graph = False
    with btn_col1:
        
        if st.button('Display Graph'):
            dis_graph = True
        else:
            st.write("Click the button to display the graph.")

    with btn_col3:
        st.button("Hide Graph", type="primary")

    if dis_graph:
        st.pyplot(nf.display_graph(G))

    st.divider()

    # Display results
    with st.sidebar:
        st.write("### Network Flow Results")
        st.write("Maximum flow value (total loaded volume):", flow_value)
        st.write("Flow along each edge:")
        for node in flow_dict:
            for conn in flow_dict[node]:
                if flow_dict[node][conn] > 0:
                    st.write(f"{node} -> {conn}: {flow_dict[node][conn]}")
    """)