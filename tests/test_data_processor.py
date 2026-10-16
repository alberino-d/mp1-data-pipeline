#tests/test_data_processor.py

import pandas as pd
import pytest

from src.data_processor import handle_missing, remove_duplicates, remove_outliers


def test_remove_duplicates(sample_df):
    df = remove_duplicates(sample_df)

    assert len(df) == 98


def test_handle_missing_rows(sample_df):
    # Arrange: use the existing rating column.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce") 
    # note: errors="coerce" converts invalid numeric strings to missing values.

    handled_df = handle_missing(df, "rows")

    assert len(handled_df) == 97


def test_remove_outliers_iqr(sample_df):
    # Arrange: use numeric ratings and exclude missing values.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce") 
    df = df.dropna()
    # note: errors="coerce" converts invalid numeric strings to missing values.

    returned_df = remove_outliers(df, ["rating"], "iqr", 1.5)

    assert len(returned_df) == 95

def test_remove_outliers_zscore(sample_df):
    # Arrange: use numeric ratings and exclude missing values.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce") 
    df = df.dropna()
    # note: errors="coerce" converts invalid numeric strings to missing values.

    returned_df = remove_outliers(df, ["rating"], "zscore", 3)

    assert len(returned_df) == 95

def test_remove_outliers_with_unsupported_method(sample_df):
    # Arrange: use numeric ratings and exclude missing values.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce") 
    df = df.dropna()
    # note: errors="coerce" converts invalid numeric strings to missing values.

    with pytest.raises(ValueError):
        remove_outliers(df, ["rating"], "unknown", 1.5)
