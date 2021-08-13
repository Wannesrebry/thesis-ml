import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import regularizers
from sklearn import preprocessing
from sklearn.svm import OneClassSVM
from numpy.random import seed
from scipy.special import softmax
from tensorflow_core.python import set_random_seed

from thesis.Project.data import handle_non_numeric_data


def plot_tl_vl_epoch(history):
    plt.subplots(figsize=(15, 7))

    plt.plot(history.history['loss'], 'b', label='Training loss')
    plt.plot(history.history['val_loss'], 'r', label='Validation loss')
    plt.legend(loc='upper right')
    plt.xlabel('Epochs')
    plt.ylabel('Loss, [mse]')

    plt.show()


def distribution_loss_traindata(model):
    # Reconstructing train data
    X_pred = model.predict(np.array(X_train))

    # Creating dataframe for reconstructed data
    X_pred = pd.DataFrame(X_pred, columns=main_df.columns)
    X_pred.index = pd.DataFrame(X_train).index

    # Dataframe to get the difference of predicted data and real data.
    scored = pd.DataFrame(index=pd.DataFrame(X_train).index)
    # Returning the mean of the loss for each column
    scored['Loss_mae'] = np.mean(np.abs(X_pred - X_train), axis=1)

    # plot
    plt.subplots(figsize=(15, 7))
    sns.distplot(scored['Loss_mae'],
                 bins=15,
                 kde=True,
                 color='blue')
    plt.show()


def loss_time_alldata(model):
    # Reconstructing full data
    X_pred = model.predict(np.array(X))
    X_pred = pd.DataFrame(X_pred, columns=main_df.columns)
    X_pred.index = pd.DataFrame(X).index

    # Returning mean of the losses for each column and putting it in a dataframe
    scored = pd.DataFrame(index=pd.DataFrame(X).index)
    scored['Loss_mae'] = np.mean(np.abs(X_pred - X), axis=1)

    # Plot size
    plt.subplots(figsize=(15, 7))

    # Saving dataframe
    scored.to_csv('..//compiled_df//AutoEncoder_loss.csv')

    # Plot
    plt.plot(scored['Loss_mae'], 'b', label='Prediction Loss')

    plt.legend(loc='upper right')
    plt.xlabel('Sample')
    plt.ylabel('Loss, [mse]')
    plt.show()


if __name__ == '__main__':
    # ------------------------- Preparing data for training ---------------------------
    main_df = pd.read_csv('..//compiled_df//One_year_compiled.csv')
    main_df = main_df.drop(['day', 'hour', 'sample_Number', 'month', 'timestamp'], axis=1)
    main_df = handle_non_numeric_data(main_df)
    X = main_df

    scaler = preprocessing.MinMaxScaler()

    X = pd.DataFrame(scaler.fit_transform(X),
                     columns=X.columns,
                     index=X.index)

    X = preprocessing.scale(X)

    train_percentage = 0.15
    train_size = int(len(main_df.index) * train_percentage)

    X_train = X[:train_size]
    # ----------------------------------------------------------------------------------

    # Seed for random batch validation and training
    seed(10)
    set_random_seed(10)

    # Elu activatoin function
    act_func = 'elu'

    # Input layer
    model = Sequential()

    # First hidden layer, connected to input vector X.
    model.add(Dense(50, activation=act_func,
                    kernel_initializer='glorot_uniform',
                    kernel_regularizer=regularizers.l2(0.0),
                    input_shape=(X_train.shape[1],)
                    )
              )
    # Second hidden layer
    model.add(Dense(10, activation=act_func,
                    kernel_initializer='glorot_uniform'))
    # Thrid hidden layer
    model.add(Dense(50, activation=act_func,
                    kernel_initializer='glorot_uniform'))

    # Input layer
    model.add(Dense(X_train.shape[1],
                    kernel_initializer='glorot_uniform'))

    # Loss function and Optimizer choice
    model.compile(loss='mse', optimizer='adam')

    # Train model for 50 epochs, batch size of 200
    NUM_EPOCHS = 50
    BATCH_SIZE = 200

    # Grabbing validation and training loss over epochs
    history = model.fit(np.array(X_train), np.array(X_train),
                        batch_size=BATCH_SIZE,
                        epochs=NUM_EPOCHS,
                        validation_split=0.1,
                        verbose=1)

    #plot_tl_vl_epoch(history)
    #distribution_loss_traindata
    loss_time_alldata(model)
