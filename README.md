# 🌌 OpenLens AI 2.0
> **Universal Quantum Data Observability & Machine Learning Intelligence Platform**

OpenLens AI 2.0 is an enterprise-grade data intelligence and audit platform. It transforms raw, heterogeneous data into actionable evidence-based insights, detects multi-dimensional anomalies with scikit-learn's Isolation Forest, and generates professional executive reports across 6 different formats.

---

## ✨ Key Superpowers

- 📁 **Universal Multi-Format Ingestion**: Ingests **CSV, TSV, Excel (.xlsx, .xls), JSON, Parquet, PDF, Word DOCX, and Server Log/TXT files**.
- 🌲 **Advanced Machine Learning Engine**:
  - **Isolation Forest Multi-Variate Anomaly Detection**: Uncovers hidden multidimensional outlier records.
  - **Pearson/Spearman Collinearity Scanner**: Identifies high feature dependencies and correlations.
  - **K-Means Cluster Archetyping**: Groups records into distinct behavioural archetypes.
  - **Parametric & Non-Parametric Stats**: Skewness, Kurtosis, IQR bounds, and health score calculations.
- ⚡ **Hybrid AI Architecture**:
  - **Google Gemini Generative Intelligence**: Synthesizes high-level strategic executive briefings when API keys are available.
  - **Autonomous Heuristic Engine (Offline Guarantee)**: 100% mathematical accuracy without hallucination. Never crashes if keys or networks are offline.
- 🚀 **Universal Mission Control Exporter**:
  - 📑 **Executive PDF Audit Report** (with ReportLab tables & visual styling)
  - 📝 **Microsoft Word Document (.docx)** (editable tables & briefings)
  - 📋 **GitHub Flavored Markdown (.md)**
  - 💾 **Machine-Readable Telemetry (.json)**
  - 📊 **Enriched CSV Dataset** (with `OPENLENS_IS_ANOMALY` classification column)
  - 📡 **Raw OpenTelemetry Audit Log (.log)** (JSONL compliance event stream)
- 🌌 **Futuristic Cyberpunk UI**:
  - Dark glassmorphism HUD interface with holographic KPI cards, neon cyan/violet accents, and interactive dark Plotly charts.

---

## 🚀 Quickstart & How to Run

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Launch Streamlit Application**:
```bash
streamlit run app.py
```

3. **Open in Browser**:
Visit `http://localhost:8501` to access OpenLens AI.

---

## 📂 Project Architecture

```
MLH/
├── app.py                # Main Futuristic Streamlit HUD Dashboard
├── file_loader.py        # Universal multi-format ingestion module
├── ml_engine.py          # Isolation Forest, clustering & statistical audit core
├── llm_client.py         # Hybrid Gemini AI & deterministic offline synthesis
├── exporter.py           # Multi-format report generators (PDF, DOCX, MD, JSON, CSV, Log)
├── requirements.txt      # Production dependencies
└── data/
    ├── sample_employees.csv           # HR Workforce dataset
    ├── server_system_telemetry.csv    # Real-time infrastructure logs
    └── financial_fraud_analysis.xlsx  # Banking transactions with fraud outliers
```
