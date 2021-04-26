import os

import pandas as pd


def get_items():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "csvfilesraw/Z_items.csv"), delimiter=';')


def get_production_order_lines():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "csvfilesraw/Z_productionorderlines.csv"), delimiter=';')


def get_instructies():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "csvfilesraw/Z_instructions.csv"), delimiter=';')


def get_production_operations():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "csvfilesraw/Z_productionoperations.csv"), delimiter=';')


def get_production_data():
    return {
        "items": get_items(),
        "productionOrderLines": get_production_order_lines(),
        "instructions": get_instructies(),
        "productionOperations": get_production_operations()
    }