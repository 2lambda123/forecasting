# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
This file contains utility functions for builing LightGBM model to
solve time series forecasting problems.
"""

import pandas as pd


def predict(df, model, target_col, idx_cols, integer_output=True):
    """Predict target variable with a trained LightGBM model.

    Args:
        df (pandas.DataFrame): Dataframe including all needed features
        model (lightgbm.Booster): Trained LightGBM booster model
        target_col (str): Name of the target column
        idx_col (list[str]): List of the names of the index columns, e.g. ["store", "brand", "week"]
        integer_output (bool): It it is True, the forecast will be rounded to an integer

    Returns:
        pandas.DataFrame including the predictions of the target variable
    """
    if target_col in df.columns:
        df = df.drop(target_col, axis=1)
    predictions = pd.DataFrame({target_col: model.predict(df)})
    if integer_output:
        predictions[target_col] = predictions[target_col].apply(lambda x: round(x))
    return pd.concat([df[idx_cols].reset_index(drop=True), predictions], axis=1)
