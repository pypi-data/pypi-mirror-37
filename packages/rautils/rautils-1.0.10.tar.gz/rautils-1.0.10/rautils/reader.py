import openpyxl as xl
import pandas as pd


def readCsv(*args, **kwargs):
    return pd.read_csv(*args, **kwargs)


def readXlsx(*args, **kwargs):
    return xl.load_workbook(*args, **kwargs)
