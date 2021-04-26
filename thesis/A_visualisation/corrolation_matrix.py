import os

from assets.productiondata.load import get_production_data
from assets.historydata.load import get_history_data
from datetime import datetime

import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt


data_production = get_production_data()
data_history = get_history_data()


if __name__ == "__main__":
    corrMatrix = data_production["items"].corr().abs()
    plt.subplots(figsize=(40, 20))
    sn.heatmap(corrMatrix, cbar=True, square=False, fmt='.2f', annot=True, annot_kws={'size': 10}, cmap='Reds')
    plt.title("Correlation Matrix")
    #plt.show()
    plt.savefig(
        './output/correlationMatrix/correlationMatrix-' + str(datetime.now()).replace(" ", "-").replace(".", "-").replace(":", "-") + '.png'
    )


