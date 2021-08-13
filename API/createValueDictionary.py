import pandas as pd


def createDataFrame(df):
    dictor = {}
    for column in df.columns:
        if df[column].dtype != 'int64' and df[column].dtype != 'float64':
            # print(createDistinctIndexFor(df, column))
            dictor[column] = createDistinctIndexFor(df, column)
        else:
            dictor[column] = None
    # Make dictor a DataFrame
    return dictor


def createDistinctIndexFor(df, column):
    columnDataDF = df[column]
    values = getDistinctFunctions(columnDataDF.values)
    dict_item = {}
    for i in range(len(values)):
        dict_item[values[i]] = i
    return dict_item


def getDistinctFunctions(values):
    output = []
    for x in values:
        if x not in output:
            output.append(x)
    return output


def valueRef(df):
    return createDataFrame(df)
