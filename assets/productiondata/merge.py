from load import get_production_data
import pandas as pd

data = get_production_data()

if __name__ == "__main__":
    for key in data.keys():
        print(key, data[key].columns)

    pd.set_option('display.max_columns', None)

    print(data["items"].shape)
    print(data["productionOrderLines"].shape)
    # Merge Items and ProductionOrderLines together:
    # df = data["items"].merge(data["productionOrderLines"], how='left', left_on='AutoID', right_on='ItemID', indicator=True)
    print(" ---------------------------")

    df_join = data["items"].join(data["productionOrderLines"].set_index('ItemID'), on='AutoID', lsuffix='_item', rsuffix='_productionOrderLine')
    df_join1 = data["items"].join(data['productionOrderLines'], lsuffix='_item', rsuffix='_productionOrderLine')
    print(df_join.shape)
    print(df_join.columns)
    print(df_join[df_join['AutoID_item'] == 222].shape)

'''
    print(df.shape)
    print(df.describe())
    print(df[0:3])
    print(df.loc[df["AutoID"] == "406"])

'''