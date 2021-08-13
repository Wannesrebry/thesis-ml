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
    # Grabbing the entire dataset
    main_df = pd.read_csv('..//compiled_df//One_year_compiled.csv')
    # Dropping columns with unwanted/irrelevant info for the algorithm
    main_df = main_df.drop(['day', 'hour', 'sample_Number', 'month', 'timestamp'], axis=1)
    # Convert non numeric data
    main_df = handle_non_numeric_data(main_df)

    # Passing our dataframe as our features
    X = main_df
    # Defining preprocessor for the data
    scaler = preprocessing.MinMaxScaler()
    # Preprocessing
    X = pd.DataFrame(scaler.fit_transform(X),
                     columns=X.columns,
                     index=X.index)

    # Scaling
    X = preprocessing.scale(X)
    # Splitting the feature data for training data. First 200.000 rows.
    X_train = X[:200000]

    # Creating a fitting OneClass SVM
    ocsvm = OneClassSVM(nu=0.25, gamma=0.05)
    ocsvm.fit(X_train)


    df = main_df.copy()
    df['anomaly'] = pd.Series(ocsvm.predict(X))

    # Saving Dataframe.
    df.to_csv('..//compiled_df//Labled_df.csv')

    # Reading into dataframe
    df = pd.read_csv('..//compiled_df/Labled_df.csv', index_col=0)
    df.head()

