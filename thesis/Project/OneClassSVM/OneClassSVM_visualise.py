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

from thesis.Project.data import handle_non_numeric_data

if __name__ == '__main__':
    df = pd.read_csv('..//compiled_df//Labled_dftest.csv', index_col=0)

    # Getting labled groups
    scat_1 = df.groupby('anomaly').get_group(1)
    scat_0 = df.groupby('anomaly').get_group(-1)

    # Plot size
    plt.subplots(figsize=(15, 7))

    # Plot group 1 -labeled, color green, point size 1
    plt.plot(scat_1.index, scat_1['pCut::Motor_Torque'], 'g.', markersize=1)

    # Plot group -1 -labeled, color red, point size 1
    plt.plot(scat_0.index, scat_0['pCut::Motor_Torque'], 'r.', markersize=1)

    plt.show()
