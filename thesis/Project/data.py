import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.svm import OneClassSVM
from numpy.random import seed
from scipy.special import softmax


def handle_non_numeric_data(df):
    # Values in each column for each column
    columns = df.columns.values

    for column in columns:

        # Dictionary with each numerical value for each text
        text_digit_vals = {}

        # Receives text to convert to a number
        def convert_to_int(val):

            # Returns respective numerical value for class
            return text_digit_vals[val]

        # If values in columns are not float or int
        if df[column].dtype != np.int64 and df[column].dtype != np.float64:

            # Gets values form current column
            column_contents = df[column].values.tolist()

            # Gets unique values from current column
            unique_elements = set(column_contents)

            # Classification starts at 0
            x = 0

            for unique in unique_elements:

                # Adds the class value for the text in dictionary, if it's not there
                if unique not in text_digit_vals:
                    text_digit_vals[unique] = x
                    x += 1

            # Maps the numerical values to the text values in columns
            df[column] = list(map(convert_to_int, df[column]))

    return df
