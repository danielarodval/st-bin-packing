"""
Attempting bin packing via Fractional Knapsack approach and Containers approach.

Plotly visualization will leverage sub containers to show the bin packing.

The app will include an interface to allow the user to select the container, select the mission type, then filter 

REFERENCE CODE
class Item:
    def __init__(self, name, length, width, height, conditions, size):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.volume = length * width * height
        self.conditions = conditions
        self.size = size
        self.packed_count = 0

class Bin:
    def __init__(self, max_length, max_width, max_height):
        self.items = []
        self.remaining_length = max_length
        self.remaining_width = max_width
        self.remaining_height = max_height
        self.packed_items = []  # New attribute to store the packed items

    def can_fit(self, item):
        return (item.length <= self.remaining_length and
                item.width <= self.remaining_width and
                item.height <= self.remaining_height)

    def add_item(self, item):
        max_packs = 1 if item.size == 'large' else 2
        if not self.can_fit(item) or item.packed_count >= max_packs:  # Only pack the item if it has been packed less than max_packs times
            return False
        self.items.append(item)
        self.remaining_length -= item.length
        self.remaining_width -= item.width
        self.remaining_height -= item.height
        self.packed_items.append(item)  # Add the item to the packed items
        item.packed_count += 1  # Increment the packed count of the item
        return True

def pack_items(items, max_bin_length, max_bin_width, max_bin_height, num_bins, conditions):
    # Separate items into necessary and general items
    necessary_items = [item for item in items if any(condition in item.conditions for condition in conditions)]
    general_items = [item for item in items if "General" in item.conditions]

    # Duplicate each necessary item, and create rotated versions of each item
    necessary_items = [Item(item.name, l, w, h, item.conditions, item.size)
             for item in necessary_items
             for _ in range(2 if item.size == 'small' and any(condition in item.conditions for condition in conditions) else 1)
             for l, w, h in [(item.length, item.width, item.height),
                              (item.height, item.length, item.width),
                              (item.width, item.height, item.length)]]

    # Sort necessary items by volume in decreasing order
    necessary_items.sort(key=lambda item: item.volume, reverse=True)

    # Create bins and pack necessary items first
    bins = [Bin(max_bin_length, max_bin_width, max_bin_height) for _ in range(num_bins)]
    for item in necessary_items:
        # Try to fit item into a bin
        for bin in bins:
            if bin.add_item(item):
                break

    # After packing necessary items, sort general items by volume in decreasing order
    general_items.sort(key=lambda item: item.volume, reverse=True)

    # Try to pack general items into remaining space
    for item in general_items:
        # Try to fit item into a bin
        for bin in bins:
            if bin.add_item(item):
                break

    return bins


# Define your items and their properties
items = [
    Item("MREs", 18, 12.75, 14, ["General"], 'small'),
    Item("Water Pouches", 13.4, 10, 7, ["General"], 'small'),
    Item("Water Purifier", 7.88, 7.88, 8.19, ["General"], 'small'),
    Item("Portable Hospital Setup", 102, 41, 49, ["Causalities"], 'large'),
    Item("Body Bags", 8.66, 3.93, 1, ["Causalities"], 'small'),
    Item("First Aid Kits", 11.5, 3.25, 13, ["General"], 'small'),
    Item("Mass Casualties Kit", 12.25, 18.5, 14, ["Causalities"], 'large'),
    Item("Arctic Survival Kit", 20, 12, 12, ["Cold"], 'small'),
    Item("Surgical Kit", 9, 5, 1, ["General"], 'small'),
    Item("LED Flashlights", 2, 4.6, 1.1, ["General"], 'small'),
    Item("Battery Packs", 7, 1.62, 1, ["General"], 'small'),
    Item("Backpacks", 17, 11, 5, ["General"], 'small'),
    Item("Sleeping Bags", 6, 3.25, 3.25, ["General"], 'small'),
    Item("Blankets", 3, 5, 1, ["General"], 'small'),
    Item("Shovel", 11.25, 8, 2, ["General"], 'small'),
    Item("Solar Tent", 22.8, 7.8, 7.8, ["Hot"], 'small'),
    Item("Portable LED Light Tower", 81.8, 45, 35.9, ["General"], 'large'),
    Item("Portable Chair", 15, 4, 4, ["General"], 'small'),
    Item("Portable Table", 24, 24, 36, ["General"], 'large'),
    Item("Portable Toilet", 14, 3, 16, ["General"], 'small'),
    Item("Walkie Talkie", 6.37, 2.75, 7.52, ["General"], 'small'),
    Item("Radio", 6.77, 3.7, 2.91, ["General"], 'small')
]

# Define the maximum dimensions of your bins (ISU 90 containers)
max_bin_length = 94.25  # Update with the correct dimensions
max_bin_width = 80.5
max_bin_height = 41.25

# Define the number of bins available
num_bins = 16  # Change this to the number of ISU 90 containers available

# Ask the user for the weather condition
weather = input("What is the current weather? (Hot/Cold/General): ")

# Ask the user if there are casualties
casualties = input("Are there casualties? (Yes/No): ")

# Define the conditions based on user input
conditions = ["General"]
if weather.lower() == "hot":
    conditions.append("Hot")
elif weather.lower() == "cold":
    conditions.append("Cold")
if casualties.lower() == "yes":
    conditions.append("Causalities")

# Pack the items into bins
bins = pack_items(items, max_bin_length, max_bin_width, max_bin_height, num_bins, conditions)

# Print out the packing solution
for i, bin in enumerate(bins, start=1):
    print(f"Bin {i}:")
    for item in bin.packed_items:
        print(f"  {item.name}")
    print(f"Remaining space: {bin.remaining_length} x {bin.remaining_width} x {bin.remaining_height}")

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
    def __init__(self, max_volume, max_weight):
        self.stacks = []  # List of stacks, each stack is a list of items
        self.max_volume = max_volume
        self.max_weight = max_weight
        self.current_volume = 0
        self.current_weight = 0

    def can_add_item(self, item):
        # Check if the item can be added based on weight and volume
        if self.current_weight + item.weight > self.max_weight or \
           self.current_volume + item.volume > self.max_volume:
            return False
        return True

    def add_item_to_stack(self, item):
        # Attempt to add item to an appropriate stack
        for stack in self.stacks:
            if stack[-1].size == item.size and self.can_add_item(item):
                stack.append(item)
                self.current_volume += item.volume
                self.current_weight += item.weight
                return True

        # If no suitable stack found, create a new one if possible
        if self.can_add_item(item):
            self.stacks.append([item])
            self.current_volume += item.volume
            self.current_weight += item.weight
            return True

        return False

def pack_items(items, bins):
    # Sort items by volume in descending order for packing efficiency
    items.sort(key=lambda item: item.volume, reverse=True)

    # Attempt to pack each item into the bins
    for item in items:
        for bin in bins:
            if bin.add_item_to_stack(item):
                break  # Item has been packed, move to the next item

    return bins

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

del df

items['size'] = items['volume'].apply(bf.classify_size)


#%% Display Data

expand_import = st.expander("View Imported Data")
with expand_import:
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
    st.write(mission_items)
#%% Pack Items
item_objects = [Item(row['item'], row['length'], row['width'], row['height'], row['weight'], row['volume'], row['utilization'], row['size']) for index, row in mission_items.iterrows()]
bins = [Bin(max_volume=container['volume'].values[0], max_weight=container['weight'].values[0]) for _ in range(1)]  # Initialize bins

# Example usage
packed_bins = pack_items(item_objects, bins)

# Output the packing result
for i, bin in enumerate(packed_bins, start=1):
    print(f"Bin {i}:")
    for stack in bin.stacks:
        for item in stack:
            print(f"  {item.name} (Size: {item.size}, Volume: {item.volume})")
    print(f"Remaining Volume: {bin.max_volume - bin.current_volume}, Remaining Weight: {bin.max_weight - bin.current_weight}")

    #st.write(f"Remaining Volume: {(bin.max_volume - bin.current_volume).round(2)}, Remaining Weight: {(bin.max_weight - bin.current_weight).round(2)}")
    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("Remaining Volume", value=(bin.max_volume - bin.current_volume).round(2))
    metric2.metric("Remaining Weight", value=(bin.max_weight - bin.current_weight).round(2))
