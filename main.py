from assets.productiondata.load import get_production_data
from assets.historydata.load import get_history_data

import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt


data_production = get_production_data()
data_history = get_history_data()
'''
Items,
productionOrderLines,
instructions,
productionOperations,
instructionList (history only)
'''

if __name__ == "__main__":
    print(data_production["items"].head())
    print(data_production["productionOrderLines"].head())
    print(data_production["instructions"].head())
    print(data_production["productionOperations"].head())

    print(data_history["items"].head())
    print(data_history["productionOrderLines"].head())
    print(data_history["instructions"].head())
    print(data_history["productionOperations"].head())
    print(data_history["instructionList"].head())
