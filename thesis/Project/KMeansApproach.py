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
    # ------ Preparing features for training and future prediction -----
    main_df = pd.read_csv('compiled_df//One_year_compiled.csv')
    main_df = main_df.drop(['day', 'hour', 'sample_Number', 'month', 'timestamp'], axis=1)
    main_df = handle_non_numeric_data(main_df)
    X = main_df

    scaler = preprocessing.MinMaxScaler()

    X = pd.DataFrame(scaler.fit_transform(X),
                     columns=X.columns,
                     index=X.index)

    X = preprocessing.scale(X)
    # -------------------------------------------------------------------

    # Percentage of the data that will be considered healthy condition
    train_percentage = 0.15
    # Integer value for the slice that will be considered healthy condition
    train_size = int(len(main_df.index) * train_percentage)
    # Grabbing slice for training data
    X_train = X[:train_size]

    # Defining KMeans with 1 cluster
    kmeans = KMeans(n_clusters=1)
    # Fitting the algorithm
    kmeans.fit(X_train)

    # Creating a copy of the main dataset
    k_anomaly = main_df.copy()

    # Dataframe now will receive the distance of each data sample from the cluster
    k_anomaly = pd.DataFrame(kmeans.transform(X))

    # Saving cluster distance into csv file
    k_anomaly.to_csv('compiled_df//KM_Distance.csv')

    # Plot
    plt.subplots(figsize=(15, 7))

    plt.plot(k_anomaly.index, k_anomaly[0], 'g', markersize=1)

    plt.show()
