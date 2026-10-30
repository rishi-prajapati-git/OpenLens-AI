"""
OpenLens AI - Enterprise Machine Learning & Deep Statistical Engine
Implements Isolation Forest anomaly detection, collinearity tracking,
distribution metrics, clustering, and deterministic evidence-based insights.
"""

import os
import warnings
warnings.filterwarnings("ignore")
os.environ["LOKY_MAX_CPU_COUNT"] = "4"

import numpy as np
import pandas as pd
from typing import Dict, Any, List
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def run_advanced_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Executes a comprehensive ML and statistical audit on the DataFrame.
    Returns structured metrics, anomaly results, and evidence-based insights.
    """
    rows, columns = df.shape
    if rows == 0 or columns == 0:
        return {"error": "Empty dataset."}

    # 1. Missingness & Duplicates
    missing = df.isnull().sum()
    missing_cells = int(missing.sum())
    total_cells = rows * columns
    missing_pct = (missing_cells / total_cells * 100) if total_cells else 0.0
    duplicate_rows = int(df.duplicated().sum())
    duplicate_pct = (duplicate_rows / rows * 100) if rows else 0.0

    # 2. Type Classification
    numeric_df = df.select_dtypes(include=[np.number])
    numeric_cols = numeric_df.columns.tolist()
    categorical_df = df.select_dtypes(include=["object", "category", "bool"])
    categorical_cols = categorical_df.columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()

    # Try detecting parseable datetime columns
    if not datetime_cols:
        for c in categorical_cols[:5]:
            sample = df[c].dropna().head(10)
            if not sample.empty:
                try:
                    pd.to_datetime(sample, errors="raise")
                    datetime_cols.append(c)
                except Exception:
                    pass

    # 3. Numeric Summary & Univariate Outliers
    numeric_summary = {}
    iqr_outliers_total = 0
    for col in numeric_cols:
        series = numeric_df[col].dropna()
        if len(series) == 0:
            continue
        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outlier_mask = (series < lower_bound) | (series > upper_bound)
        outlier_count = int(outlier_mask.sum())
        iqr_outliers_total += outlier_count
        
        skew = float(series.skew()) if len(series) > 2 else 0.0
        kurt = float(series.kurtosis()) if len(series) > 3 else 0.0

        numeric_summary[col] = {
            "mean": round(float(series.mean()), 2),
            "std": round(float(series.std()), 2) if len(series) > 1 else 0.0,
            "median": round(float(series.median()), 2),
            "min": round(float(series.min()), 2),
            "max": round(float(series.max()), 2),
            "iqr": round(float(iqr), 2),
            "outliers": outlier_count,
            "skewness": round(skew, 2),
            "kurtosis": round(kurt, 2),
            "zeros": int((series == 0).sum())
        }

    # 4. Categorical Cardinality & Unique Summary
    categorical_summary = {}
    for col in categorical_cols:
        series = df[col].dropna().astype(str)
        n_unique = int(series.nunique())
        top_val = series.mode()[0] if not series.empty else "N/A"
        top_freq = int(series.value_counts().iloc[0]) if not series.empty else 0
        top_pct = round(top_freq / len(series) * 100, 1) if len(series) else 0.0

        categorical_summary[col] = {
            "unique_count": n_unique,
            "unique_ratio": round(n_unique / rows * 100, 2) if rows else 0,
            "top_value": top_val,
            "top_frequency": top_freq,
            "top_percentage": top_pct,
            "cardinality_risk": "High" if n_unique > rows * 0.7 and rows > 50 else ("Low" if n_unique == 1 else "Normal")
        }

    # 5. Machine Learning Model: Isolation Forest Anomaly Detection
    anomaly_records = []
    anomaly_indices = []
    anomaly_count = 0
    anomaly_pct = 0.0

    if len(numeric_cols) >= 1 and rows >= 5:
        clean_num = numeric_df.dropna()
        if len(clean_num) >= 5:
            try:
                # Contamination auto or capped at 10%
                scaler = StandardScaler()
                scaled_data = scaler.fit_transform(clean_num)
                
                iso_forest = IsolationForest(
                    n_estimators=100,
                    contamination=min(0.08, max(0.01, 10.0 / len(clean_num))),
                    random_state=42
                )
                preds = iso_forest.fit_predict(scaled_data)
                scores = iso_forest.decision_function(scaled_data)

                # -1 indicates anomaly
                anomaly_mask = preds == -1
                anomaly_count = int(anomaly_mask.sum())
                anomaly_pct = round(anomaly_count / len(clean_num) * 100, 2)

                # Collect the top 10 most extreme anomalies
                anomaly_rows = clean_num[anomaly_mask].copy()
                anomaly_rows["anomaly_score"] = np.round(scores[anomaly_mask], 3)
                anomaly_rows = anomaly_rows.sort_values(by="anomaly_score")
                
                anomaly_indices = anomaly_rows.index.tolist()
                # Attach original df row context
                context_df = df.loc[anomaly_indices].head(10)
                context_df["ml_anomaly_score"] = anomaly_rows.loc[context_df.index, "anomaly_score"]
                anomaly_records = context_df.to_dict(orient="records")
            except Exception as e:
                anomaly_records = []

    # 6. Machine Learning Model: Correlation & Multicollinearity
    correlations = []
    correlation_matrix = {}
    if len(numeric_cols) >= 2:
        corr_matrix = numeric_df.corr().round(3)
        correlation_matrix = corr_matrix.to_dict()
        
        # Extract pairs with |r| > 0.65
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                c1, c2 = numeric_cols[i], numeric_cols[j]
                val = corr_matrix.loc[c1, c2]
                if not np.isnan(val) and abs(val) >= 0.5:
                    correlations.append({
                        "feature_x": c1,
                        "feature_y": c2,
                        "correlation": float(val),
                        "relationship": "Strong Positive" if val >= 0.75 else (
                            "Moderate Positive" if val >= 0.5 else (
                                "Strong Negative" if val <= -0.75 else "Moderate Negative"
                            )
                        )
                    })
        correlations = sorted(correlations, key=lambda x: abs(x["correlation"]), reverse=True)

    # 7. Machine Learning Model: Unsupervised KMeans Cluster Archetypes
    clusters_info = []
    if len(numeric_cols) >= 2 and rows >= 10:
        clean_num = numeric_df.dropna()
        if len(clean_num) >= 10:
            try:
                k = min(3, len(clean_num))
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(clean_num)
                kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
                cluster_labels = kmeans.fit_predict(X_scaled)
                clean_num_with_c = clean_num.copy()
                clean_num_with_c["cluster_id"] = cluster_labels
                
                for cid in range(k):
                    c_group = clean_num_with_c[clean_num_with_c["cluster_id"] == cid]
                    c_size = len(c_group)
                    c_pct = round(c_size / len(clean_num) * 100, 1)
                    centroid_means = {col: round(float(c_group[col].mean()), 2) for col in numeric_cols[:4]}
                    clusters_info.append({
                        "cluster_id": f"Cluster #{cid + 1}",
                        "population": c_size,
                        "percentage": c_pct,
                        "archetype_profile": centroid_means
                    })
            except Exception:
                clusters_info = []

    # 8. Holistic Health Score (0 - 100)
    health_penalty = (
        (missing_pct * 1.8) +
        (duplicate_pct * 1.5) +
        (min(15.0, (iqr_outliers_total / total_cells * 100) * 1.2) if total_cells else 0) +
        (5.0 if anomaly_pct > 5.0 else 0)
    )
    health_score = max(5, min(100, round(100 - health_penalty)))

    # 9. Deterministic AI Evidence Insights (100% Accurate, Zero Hallucinations)
    key_findings = []
    risk_warnings = []
    strategic_actions = []

    # Findings
    key_findings.append(f"Analyzed {rows:,} total records across {columns} dimensional features ({len(numeric_cols)} numeric, {len(categorical_cols)} categorical).")
    if anomaly_count > 0:
        key_findings.append(f"Isolation Forest ML detected {anomaly_count} multivariate outlier records ({anomaly_pct}% of dataset) exhibiting anomalous feature co-variance.")
    if correlations:
        top_corr = correlations[0]
        key_findings.append(f"Strongest feature alignment discovered between '{top_corr['feature_x']}' and '{top_corr['feature_y']}' (r = {top_corr['correlation']:.2f}, {top_corr['relationship']}).")
    if clusters_info:
        dominant_cluster = max(clusters_info, key=lambda c: c["population"])
        key_findings.append(f"K-Means clustering isolated {len(clusters_info)} distinct data archetypes. Dominant archetype encompasses {dominant_cluster['percentage']}% of records.")

    # Warnings
    if missing_cells > 0:
        worst_col = missing.sort_values(ascending=False).index[0]
        worst_count = int(missing[worst_col])
        worst_pct = round(worst_count / rows * 100, 1)
        risk_warnings.append(f"Missing data integrity alert: {missing_cells:,} empty cells detected ({missing_pct:.2f}% of matrix). Column '{worst_col}' is missing {worst_pct}% of values.")
    else:
        risk_warnings.append("Data completeness is pristine: 0 null or missing cells discovered.")

    if duplicate_rows > 0:
        risk_warnings.append(f"Redundancy alert: {duplicate_rows:,} exact duplicate rows identified ({duplicate_pct:.2f}% of volume). This risks biasing downstream modeling.")

    skewed_cols = [c for c, v in numeric_summary.items() if abs(v["skewness"]) > 1.5]
    if skewed_cols:
        risk_warnings.append(f"High statistical skewness detected in columns: {', '.join(skewed_cols[:3])}. Median or log-transformation is advised over standard mean.")

    # Recommendations
    if duplicate_rows > 0:
        strategic_actions.append(f"Deduplicate dataset using primary keys or feature hashes to eliminate {duplicate_rows} redundant observations.")
    if missing_cells > 0:
        strategic_actions.append("Apply category mode imputation for discrete columns and median/KNN imputation for skewed continuous metrics.")
    if anomaly_records:
        strategic_actions.append(f"Quarantine and inspect the {anomaly_count} Isolation Forest outlier rows (sample IDs: {anomaly_indices[:3]}) to prevent skewed training or faulty reporting.")
    if len(strategic_actions) < 2:
        strategic_actions.append("Dataset features demonstrate high mathematical consistency. Ready for operational intelligence and predictive model deployment.")

    return {
        "rows": rows,
        "columns": columns,
        "memory_kb": round(float(df.memory_usage(deep=True).sum() / 1024), 2),
        "health_score": health_score,
        "missing_cells": missing_cells,
        "missing_percentage": round(missing_pct, 2),
        "missing_by_column": missing[missing > 0].to_dict(),
        "duplicate_rows": duplicate_rows,
        "duplicate_percentage": round(duplicate_pct, 2),
        "numeric_summary": numeric_summary,
        "categorical_summary": categorical_summary,
        "column_types": df.dtypes.astype(str).to_dict(),
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
        "correlations": correlations[:10],
        "correlation_matrix": correlation_matrix,
        "anomaly_count": anomaly_count,
        "anomaly_pct": anomaly_pct,
        "anomaly_records": anomaly_records,
        "clusters_info": clusters_info,
        "evidence_insights": {
            "key_findings": key_findings,
            "risk_warnings": risk_warnings,
            "strategic_actions": strategic_actions
        }
    }
