import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.svm import OneClassSVM
from numpy.random import seed
from tensorflow import keras
from scipy.special import softmax


main_df = pd.read_csv('../datasetsone-year-compiledcsv/One_year_compiled.csv')
main_df.describe()