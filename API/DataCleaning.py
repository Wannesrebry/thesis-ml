import pandas as pd
from createValueDictionary import valueRef


def createColumnValues(column, trainData, dictor):
    trainDataLength = trainData.shape[0]
    columnDataDF = trainData[column]
    values = columnDataDF.values
    res = []
    for index in range(trainDataLength):
        value = values[index]
        index_value = dictor[column].get(value)
        res.append(index_value)
    return res


def createDataFrame(df, dictor, ignore=None):
    if ignore is None:
        ignore = []
    result = {}
    print(dictor)
    for column in list(dictor.keys()):
        if (df[column].dtype != 'int64' or df[column].dtype != 'float64') and dictor[column] is not None \
                and not ignore.__contains__(column):
            result[column] = createColumnValues(column, df, dictor)
        else:
            result[column] = df[column].values
    res = pd.DataFrame(result)
    return res


def createTrainDataCleanData():
    dictor = createDataFrame(pd.read_csv("../files/train.csv"))
    # Take means of columns with NAN values
    averageLotFrontage = dictor.LotFrontage.mean()
    averageMasVnrArea = dictor.MasVnrArea.mean()
    averageGarageYrBlt = dictor.GarageYrBlt.mean()

    # Fill nan values with their means
    dictor.LotFrontage.fillna(averageLotFrontage, inplace=True)
    dictor.MasVnrArea.fillna(averageMasVnrArea, inplace=True)
    dictor.GarageYrBlt.fillna(averageGarageYrBlt, inplace=True)

    # Test if the missing values are filled in
    assert dictor.LotFrontage.notnull().all()
    assert dictor.MasVnrArea.notnull().all()
    assert dictor.GarageYrBlt.notnull().all()
    assert dictor.isnull().sum().sum() == 0
    return dictor


def createTestDataCleanData():
    return createDataFrame(pd.read_csv("../files/test.csv"))


if __name__ == '__main__':
    trainDataClean = createTrainDataCleanData()
    # If all tests are passed, next line will be executed and a new file will be saved
    trainDataClean.to_csv("../files/cleanTrainData.csv", index=False)

    testDataClean = createTestDataCleanData()
    testDataClean.to_csv("../files/cleanTestData.csv", index=False)