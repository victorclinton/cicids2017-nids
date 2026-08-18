import numpy as np


def assign_risk(confidence):

    if confidence >= 90:
        return "High"

    if confidence >= 70:
        return "Medium"

    return "Low"


def safe_divide(a, b):

    if b == 0:
        return 0

    return a / b


def replace_inf(df):

    return df.replace(
        [np.inf, -np.inf],
        np.nan
    )