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

'''
    basic Heatmap/Correlation matrix with all columns
'''


def plot_heatmap_v1(df):
    plt.subplots(figsize=(10, 5))
    # heatmap of correlations from -1 to 1
    sns.heatmap(df.corr(), vmin=-1, vmax=1,
                cbar=True, square=False, fmt='.2f',
                annot=True, annot_kws={'size': 10}, cmap='Reds')
    plt.show()


'''
    Heatmap/Correlation matrix with dropped columns and inverse Torque
'''


def plot_heatmap_v2(df):
    df = df.drop(['day', 'hour', 'sample_Number', 'month', 'timestamp'], axis=1)
    # Flipping column values
    df['pCut::Motor_Torque'] = df['pCut::Motor_Torque'] * -1
    # Heatmap
    plt.subplots(figsize=(10, 5))
    sns.heatmap(df.corr(), vmin=-1, vmax=1,
                cbar=True, square=False, fmt='.2f',
                annot=True, annot_kws={'size': 10}, cmap='Reds')
    plt.show()


if __name__ == '__main__':
    main_df = pd.read_csv('compiled_df//One_year_compiled.csv')
    main_df.describe()
    # plot_heatmap_v1(main_df)
    plot_heatmap_v2(main_df)
