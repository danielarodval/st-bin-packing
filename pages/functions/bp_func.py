import pandas as pd
import streamlit as st

class Item:
    def __init__(self, name, length, width, height, weight, volume, conditions, size, count=1):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.volume = volume
        self.conditions = conditions
        self.size = size
        self.count = count  # New attribute to hold the count of items
        self.packed_count = 0

class Bin:
    _id_counter = 0  # Class variable to keep track of bin IDs

    def __init__(self, max_length, max_width, max_height, max_volume, max_weight, bin_type, name):
        self.id = Bin._id_counter  # Unique ID for each bin instance
        Bin._id_counter += 1  # Increment the ID counter

        self.max_length = max_length
        self.max_width = max_width
        self.max_height = max_height
        self.max_volume = max_volume
        self.max_weight = max_weight
        self.Type = bin_type
        self.name = name
        self.items = []  # List of items
        self.stacks = []  # List of stacks, each stack is a list of items
        self.current_volume = 0
        self.current_weight = 0
    def can_fit(self, item):
        # Check if the item fits within the bin's remaining dimensions and weight
        if (self.current_volume + item.volume <= self.max_volume and
            self.current_weight + item.weight <= self.max_weight and
            self.max_length >= item.length and
            self.max_width >= item.width and
            self.max_height >= item.height):
            return True
        return False

    def add_item(self, item):
        max_packs = item.count if item.size != 'large' else min(item.count, 2)

        # Attempt to add the item based on its count and if it fits
        while self.can_fit(item) and item.packed_count < max_packs:
            self.items.append(item)
            self.current_volume += item.volume
            self.current_weight += item.weight
            item.packed_count += 1  # Increment the packed count

            # Manage stacks (if applicable)
            added_to_stack = False
            for stack in self.stacks:
                if stack[-1].size == item.size:
                    stack.append(item)
                    added_to_stack = True
                    break
            if not added_to_stack:
                self.stacks.append([item])

            # If the item's count is fully packed, break
            if item.packed_count == item.count:
                break
            
        return item.packed_count > 0  # Return True if at least one of the item was packed

def classify_size(volume):
    if volume < 1000:
        return 'small'
    elif volume < 5000:
        return 'medium'
    else:
        return 'large'

def generate_orientations(item):
    # Generate all possible orientations based on length, width, and height
    orientations = [
        (item.length, item.width, item.height),
        (item.length, item.height, item.width),
        (item.width, item.height, item.length),
        (item.width, item.length, item.height),
        (item.height, item.length, item.width),
        (item.height, item.width, item.length)
    ]
    return [Item(item.name, l, w, h, item.weight, item.volume, item.conditions, item.size) for l, w, h in orientations]

def sort_items(items):
    # Prioritize items based on length, width, height, and then volume
    items.sort(key=lambda x: (-x.length, -x.width, -x.height, -x.volume))

def pack_items(items, bins):
    unloaded_items = []
    sort_items(items)  # Sort items based on the new criteria

    for item in items:
        for _ in range(item.count):
            item_fitted = False
            for orientation in generate_orientations(item):
                for bin in bins:
                    if bin.can_fit(orientation) and bin.add_item(orientation):
                        item_fitted = True
                        break  # Stop trying other orientations if item is fitted
                if item_fitted:
                    break  # Move to the next item if this orientation is fitted

            if not item_fitted:
                unloaded_items.append(item)  # Log item if it couldn't be fitted
                break  # Break if we can't fit an item to move to the next

    return bins, unloaded_items

def print_bins(packed_bins):
    for i, bin in enumerate(packed_bins, start=1):
        st.write(f"##### Bin {i}:")
        for stack in bin.stacks:
            #concatenate a list of items into a string
            st.write(f"* Stack {bin.stacks.index(stack) + 1}:")
            if len(stack) > 100:
                st.write(f"Item Count: {len(stack)}")
            else:
                items = ', '.join([item.name for item in stack])
                st.write(f"{items}")
            
            for item in stack:
                #st.write(f"  {item.name} (Size: {item.size}, Volume: {item.volume})")
                st.write()
        #print bin volume left
        st.write(f"Volume Left: {(bin.max_volume - bin.current_volume).round(2)}")
        st.divider()