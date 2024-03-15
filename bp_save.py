"""
Attempting bin packing via Fractional Knapsack approach and Containers approach.

Plotly visualization will leverage sub containers to show the bin packing.

The app will include an interface to allow the user to select the container, select the mission type, then filter 
"""

import pandas as pd
import streamlit as st
import bp_func as bf
import numpy as np

st.set_page_config(layout="wide")

st.title("Bin Packing Test")
st.write("## USSF SPEC/Materials Testing")

#%% functions
class Item:
    def __init__(self, name, length, width, height, weight, volume, conditions, size):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.volume = volume
        self.conditions = conditions
        self.size = size
        self.packed_count = 0

class Bin:
    def __init__(self, max_length, max_width, max_height, max_volume, max_weight):
        self.stacks = []  # List of stacks, each stack is a list of items
        self.remaining_length = max_length
        self.remaining_width = max_width
        self.remaining_height = max_height
        self.max_volume = max_volume
        self.max_weight = max_weight
        self.current_volume = 0
        self.current_weight = 0

    def can_fit(self, item):
        return (item.length <= self.remaining_length and
                item.width <= self.remaining_width and
                item.height <= self.remaining_height)

    def add_item_to_stack(self, item):
        # Determine max_packs based on item size
        max_packs = 1 if item.size == 'large' else 2

        # Combined check for weight, volume, fit, and packed_count
        if (self.current_weight + item.weight > self.max_weight or
            self.current_volume + item.volume > self.max_volume or
            not self.can_fit(item) or
            item.packed_count >= max_packs):
            return False

        # If the item passes all checks, proceed to add it to the appropriate stack
        added = False
        for stack in self.stacks:
            if stack and stack[-1].size == item.size:
                stack.append(item)
                self.current_volume += item.volume
                self.current_weight += item.weight
                item.packed_count += 1  # Increment the packed count
                added = True
                break

        # If no suitable stack was found, create a new one
        if not added:
            self.stacks.append([item])
            self.current_volume += item.volume
            self.current_weight += item.weight
            item.packed_count += 1  # Increment the packed count

        return True

#%% Load Data

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
    st.write(mission_items)
#%% Pack Items
item_objects = [Item(row['item'], row['length'], row['width'], row['height'], row['weight'], row['volume'], row['utilization'], row['size']) for index, row in mission_items.iterrows()]
bins = [Bin(
    max_volume=container['volume'].values[0],
    max_weight=container['weight'].values[0],
    max_height=container['height'].values[0],
    max_length=container['length'].values[0],
    max_width=container['width'].values[0]) for _ in range(1)]  # Initialize bins

#%% Example usage
packed_bins = bf.pack_items(item_objects, bins)

# Output the packing result
for i, bin in enumerate(packed_bins, start=1):
    st.write(f"Bin {i}:")
    for stack in bin.stacks:
        for item in stack:
            st.write(f"  {item.name} (Size: {item.size}, Volume: {item.volume})")
    st.write(f"Remaining Volume: {bin.max_volume - bin.current_volume}, Remaining Weight: {bin.max_weight - bin.current_weight}")

    #st.write(f"Remaining Volume: {(bin.max_volume - bin.current_volume).round(2)}, Remaining Weight: {(bin.max_weight - bin.current_weight).round(2)}")
    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("Remaining Volume", value=(bin.max_volume - bin.current_volume).round(2))
    metric2.metric("Remaining Weight", value=(bin.max_weight - bin.current_weight).round(2))
