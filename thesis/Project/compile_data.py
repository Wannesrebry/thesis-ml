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

"""
        Receives a path with all the data archives, lists the path to get a list of all filenames and then iterates through
    all the files in the path creating a dataframe of each one. Then gets a CSV file with data about the samples
    in each files name, CSV file that was manualy formated to separate months, days, etc. Creates another dataframe with
    this filename data and last joins both file dataframe and filename dataframe to have all the info for the samples.
"""


def create_filenames_df(path):
    files = os.listdir(path)
    months = []
    days = []
    hours = []
    sample_numbers = []
    modes = []

    for file in files:
        parts = file.split('_')
        datetime = parts[0]
        month = parts[0].split('-')[0]
        day = parts[0].split('-')[1].split('T')[0]
        hour = parts[0].split('-')[1].split('T')[1][:2]
        sample_number = parts[1]
        mode = parts[2].split('.')[0]

        months.append(month)
        days.append(day)
        hours.append(hour)
        sample_numbers.append(sample_number)
        modes.append(mode)

    data = {'month': months,
            'day': days,
            'hour': hours,
            'sample_Number': sample_numbers,
            'mode': modes}
    df = pd.DataFrame(data, columns=['month', 'day', 'hour', 'sample_Number', 'mode'])
    df.to_csv('datasets//filename.csv', index=False)


def compile_data(path):
    # Lists the files in path
    files = os.listdir(path)

    # Creates a dataframe for the data in each files name, then labeling the data columns
    try:
        filename_df = pd.read_csv('datasets\\filename.csv', names=['month', 'day', 'hour', 'sample_Number', 'mode'])
    except Exception:
        create_filenames_df(path)
        filename_df = pd.read_csv('datasets\\filename.csv', names=['month', 'day', 'hour', 'sample_Number', 'mode'])

    # Initialize our big main dataframe that will join everything
    main_df = pd.DataFrame()

    filename_df.describe()
    # Iterates through all files in file path and counts each file
    for count, file in enumerate(files):
        print(file)
        sample_number = file.split('_')[1]

        # Passing each csv data file in path to a individual dataframe
        file_df = pd.read_csv("{}\\{}".format(path, file))

        """
            Each row in the filename dataframe refers to a single data file in the given path, so we grab that single
        row that refers to the current file by counting each file and grabing its respective row.
        """
        # Join each file dataframe with its filename dataframe
        file_df = file_df.join(filename_df.query("sample_Number == '{}'".format(sample_number)), how='left')

        # Since we grab only a row, we will have NaNs. Wich we fill with the same info of that single row
        file_df.fillna(method='ffill', inplace=True)

        file_df.describe()

        # Joins each file dataframe into one
        if main_df.empty:
            main_df = file_df
            main_df.fillna(method='ffill', inplace=True)
        else:
            main_df = main_df.append(file_df)
            main_df.fillna(method='ffill', inplace=True)

    print('Compile done')
    return main_df


#   Calls the compile_data then saves the main dataframe into a csv file
def save_compiled_data(path):
    main_df = compile_data(path)

    # create path to the main_df csv file if it doesnt exist
    if not os.path.exists('compiled_df'):
        os.makedirs('compiled_df')
    # Saves dataframe to a csv file, removes a index
    main_df.to_csv('compiled_df//One_year_compiled.csv', index=False)
    print('Compiled and saved')


if __name__ == '__main__':
    save_compiled_data('Datasets\\initial_datasets')
