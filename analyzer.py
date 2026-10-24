
import pandas as pd
import numpy as np

def analyze_dataframe(df):
    """Calculate deterministic statistics and data-quality metrics."""

    rows, columns = df.shape

    missing = df.isnull().sum()
    missing_cells = int(missing.sum())

    duplicate_rows = int(df.duplicated().sum())

    numeric_df = df.select_dtypes(include="number")

    numeric_summary = {}
    for col in numeric_df.columns:
        series = numeric_df[col].dropna()

        if len(series) == 0:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        outliers = int(
            ((series < q1 - 1.5 * iqr) |
             (series > q3 + 1.5 * iqr)).sum()
        )

        numeric_summary[col] = {
            "mean": round(float(series.mean()), 2),
            "median": round(float(series.median()), 2),
            "min": float(series.min()),
            "max": float(series.max()),
            "outliers": outliers
        }

    missing_pct = (missing_cells / (rows * columns) * 100) if rows * columns else 0
    duplicate_pct = (duplicate_rows / rows * 100) if rows else 0

    health_score = max(
        0,
        min(100, round(100 - 2 * missing_pct - 1.5 * duplicate_pct))
    )

    return {
        "rows": rows,
        "columns": columns,
        "missing_cells": missing_cells,
        "missing_by_column": missing[missing > 0].to_dict(),
        "duplicate_rows": duplicate_rows,
        "missing_percentage": round(missing_pct, 2),
        "duplicate_percentage": round(duplicate_pct, 2),
        "health_score": health_score,
        "numeric_summary": numeric_summary,
        "column_types": df.dtypes.astype(str).to_dict()
    }
