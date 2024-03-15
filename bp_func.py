import pandas as pd

def classify_size(volume):
    if volume < 1000:
        return 'small'
    elif volume < 5000:
        return 'medium'
    else:
        return 'large'