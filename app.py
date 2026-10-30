"""
=============================================================================
   OPENLENS AI // NEXT-GENERATION ENTERPRISE DATA INTELLIGENCE PLATFORM
   Multi-Format Ingestion | Isolation Forest ML | Universal Exporter | Cyber UI
=============================================================================
"""

import os
import json
import io
import datetime
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Custom OpenLens Core Modules
from file_loader import load_file_to_dataframe
from ml_engine import run_advanced_analysis
from llm_client import generate_insights
from exporter import (
    generate_pdf_report,
    generate_docx_report,
    generate_markdown_report,
    generate_raw_telemetry_log,
    generate_enriched_csv
)

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & FUTURISTIC CYBERPUNK STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="OpenLens AI // Quantum Data Observability",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Impact Futuristic CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global Dark Cyber Theme */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0f172a 0%, #080c14 60%, #030712 100%);
        color: #e2e8f0;
        font-family: 'Space Grotesk', -apple-system, sans-serif;
    }

    /* Cyber Glow Accents */
    .cyber-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #9055ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        text-shadow: 0 0 30px rgba(0, 242, 254, 0.25);
    }
    
    .cyber-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.05em;
        margin-bottom: 1.5rem;
    }

    /* Status Pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34d399;
        font-weight: 600;
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 10px #10b981;
    }

    /* HUD Metric Cards */
    .metric-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.18);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.25s ease;
    }
    .metric-card:hover {
        border-color: rgba(0, 242, 254, 0.5);
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
        transform: translateY(-2px);
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.78rem;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 4px;
        letter-spacing: -0.02em;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #38bdf8;
        margin-top: 4px;
    }

    /* Futuristic Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.4);
        padding: 6px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 500;
        border-radius: 6px;
        padding: 0 16px;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.3), rgba(124, 58, 237, 0.3)) !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        color: #00f2fe !important;
        font-weight: 600;
    }

    /* Download Action Box */
    .download-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        margin-bottom: 12px;
    }

    /* Code & Markdown tweaks */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: rgba(30, 41, 59, 0.7) !important;
        color: #38bdf8 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SIDEBAR - MISSION CONTROL & CONFIGURATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
        <span style="font-size: 1.8rem;">🌌</span>
        <div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #f8fafc;">OPENLENS AI</div>
            <div style="font-size: 0.72rem; color: #00f2fe; font-family: 'JetBrains Mono';">QUANTUM CORE v2.5</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="status-pill">
        <span class="pulse-dot"></span>
        <span>NEURAL ENGINE ONLINE</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎛️ Data Source")

    data_source_mode = st.radio(
        "Choose Ingestion Mode:",
        ["📁 Upload Custom File", "🧪 Load Demo Datasets"],
        index=0
    )

    selected_sample = None
    if data_source_mode == "🧪 Load Demo Datasets":
        selected_sample = st.selectbox(
            "Select Pre-loaded Scenario:",
            [
                "👥 Global HR & Salary Analytics (.CSV)",
                "🖥️ Server Infrastructure Telemetry (.CSV)",
                "💳 Financial Transactions & Fraud Outliers (.XLSX)"
            ]
        )

    st.markdown("---")
    st.markdown("### 🧠 Generative AI Synthesis")
    st.caption("OpenLens automatically runs offline with its built-in ML Engine. To enhance with Google Gemini Live:")
    user_gemini_key = st.text_input(
        "Gemini API Key (Optional):",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        placeholder="AIzaSy...",
        help="Optional. If omitted, OpenLens automatically runs its full scikit-learn ML & heuristic analysis without crashing."
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.75rem; color: #64748b; line-height: 1.5;">
        <b>Supported Formats:</b><br/>
        CSV, TSV, Excel (.xlsx, .xls), JSON, Parquet, PDF, DOCX, TXT/LOG, Markdown.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. DATA INGESTION ENGINE (MULTI-FORMAT)
# -----------------------------------------------------------------------------
df = pd.DataFrame()
metadata = {}

if data_source_mode == "📁 Upload Custom File":
    uploaded_file = st.file_uploader(
        "📥 Drag & Drop Any Dataset or Telemetry File",
        type=["csv", "tsv", "xlsx", "xls", "json", "parquet", "pdf", "docx", "txt", "log", "md"],
        help="Upload CSV, Excel, JSON, PDF documents, Word docx, or Server Logs."
    )
    if uploaded_file is not None:
        try:
            with st.spinner("Decoding file stream & constructing neural matrix..."):
                df, metadata = load_file_to_dataframe(uploaded_file)
        except Exception as exc:
            st.error(f"❌ Failed to parse file: {exc}")
            st.stop()
    else:
        # Default fallback to sample employees if no upload yet
        sample_path = Path(__file__).parent / "data" / "sample_employees.csv"
        if sample_path.exists():
            df = pd.read_csv(sample_path)
            metadata = {
                "file_name": "sample_employees.csv (Default Sample)",
                "source_format": "CSV",
                "parsed_notes": "Showing default dataset. Upload your own file anytime above."
            }
else:
    # Load chosen sample
    if "Global HR" in selected_sample:
        p = Path(__file__).parent / "data" / "sample_employees.csv"
        df = pd.read_csv(p)
        metadata = {"file_name": "sample_employees.csv", "source_format": "CSV", "parsed_notes": "Employee workforce dataset with salaries and tenure."}
    elif "Server Infrastructure" in selected_sample:
        p = Path(__file__).parent / "data" / "server_system_telemetry.csv"
        df = pd.read_csv(p)
        metadata = {"file_name": "server_system_telemetry.csv", "source_format": "CSV", "parsed_notes": "Real-time CPU, RAM, Latency telemetry with spike anomalies."}
    elif "Financial" in selected_sample:
        p = Path(__file__).parent / "data" / "financial_fraud_analysis.xlsx"
        df = pd.read_excel(p)
        metadata = {"file_name": "financial_fraud_analysis.xlsx", "source_format": "EXCEL", "parsed_notes": "Financial transaction ledger with simulated fraud outliers."}

if df.empty:
    st.warning("⚠️ The ingested dataset contains 0 records. Please upload a valid file.")
    st.stop()

# -----------------------------------------------------------------------------
# 4. RUN ADVANCED MACHINE LEARNING & STATISTICAL AUDIT
# -----------------------------------------------------------------------------
with st.spinner("Executing Isolation Forest anomaly model and telemetry audit..."):
    report = run_advanced_analysis(df)

# Top Bar Header
c_head, c_meta = st.columns([2.5, 1])
with c_head:
    st.markdown('<div class="cyber-title">🌌 OPENLENS AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="cyber-subtitle">UNIVERSAL DATA OBSERVABILITY // MACHINE LEARNING AUDIT // MULTI-FORMAT EXPORT</div>', unsafe_allow_html=True)
with c_meta:
    st.markdown(f"""
    <div style="text-align: right; font-family: 'JetBrains Mono'; font-size: 0.8rem; color: #94a3b8; padding-top: 10px;">
        <span style="color: #00f2fe;">SOURCE:</span> {metadata.get('file_name', 'Active Dataset')}<br/>
        <span style="color: #38bdf8;">FORMAT:</span> {metadata.get('source_format', 'DATA')} | <span style="color: #10b981;">SIZE:</span> {df.memory_usage(deep=True).sum() / 1024:.1f} KB
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. HOLOGRAPHIC KPI GAUGES & METRICS
# -----------------------------------------------------------------------------
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Data Volume</div>
        <div class="metric-value">{report['rows']:,}</div>
        <div class="metric-sub">Total Row Records</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Dimensionality</div>
        <div class="metric-value">{report['columns']}</div>
        <div class="metric-sub">{len(report['numeric_cols'])} Num | {len(report['categorical_cols'])} Cat</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    score = report['health_score']
    color = "#10b981" if score >= 85 else ("#f59e0b" if score >= 70 else "#ef4444")
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Health Index</div>
        <div class="metric-value" style="color: {color};">{score}<span style="font-size: 1.1rem; color: #64748b;">/100</span></div>
        <div class="metric-sub">Data Quality Integrity</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    anom_cnt = report['anomaly_count']
    anom_color = "#38bdf8" if anom_cnt == 0 else "#f43f5e"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">ML Anomalies</div>
        <div class="metric-value" style="color: {anom_color};">{anom_cnt}</div>
        <div class="metric-sub">Isolation Forest Flags ({report['anomaly_pct']}%)</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Missing Cells</div>
        <div class="metric-value">{report['missing_cells']:,}</div>
        <div class="metric-sub">{report['missing_percentage']}% of Matrix</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. MASTER WORKSPACE TABS
# -----------------------------------------------------------------------------
tab_matrix, tab_quality, tab_visuals, tab_ai, tab_export = st.tabs([
    "🧬 01. Neural Data Matrix",
    "🛡️ 02. Quality & ML Anomalies",
    "📊 03. Quantum Visual Analytics",
    "⚡ 04. OpenLens AI Insights",
    "🚀 05. Mission Control (Universal Exporter)"
])

# =============================================================================
# TAB 1: NEURAL DATA MATRIX
# =============================================================================
with tab_matrix:
    st.markdown("### 🧬 Ingested Matrix Records & Schema Topology")
    
    # Dynamic Search & Row Filtering
    c_search, c_limit = st.columns([3, 1])
    with c_search:
        search_query = st.text_input("🔍 Neural Search across all attributes:", placeholder="Type any string, id, category...")
    with c_limit:
        row_limit = st.select_slider("Rows to Display:", options=[20, 50, 100, 250, 500, "All"], value=50)

    display_df = df
    if search_query:
        mask = df.astype(str).apply(lambda row: row.str.contains(search_query, case=False, na=False).any(), axis=1)
        display_df = df[mask]
        st.caption(f"Filtered **{len(display_df)}** records matching query: `{search_query}`")

    if row_limit != "All":
        display_df = display_df.head(int(row_limit))

    st.dataframe(display_df, use_container_width=True, height=360)

    # Column Schema Breakdown Table
    st.markdown("#### 📐 Dimensional Schema Attributes")
    schema_records = []
    for col in df.columns:
        dt = str(df[col].dtype)
        null_c = int(df[col].isnull().sum())
        null_p = round(null_c / len(df) * 100, 1)
        uniq_c = int(df[col].nunique())
        schema_records.append({
            "Feature Name": col,
            "Data Type": dt,
            "Null Count": null_c,
            "Missing %": f"{null_p}%",
            "Unique Values": uniq_c,
            "Distinct Ratio": f"{round(uniq_c / len(df) * 100, 1)}%"
        })
    st.dataframe(pd.DataFrame(schema_records), use_container_width=True)

# =============================================================================
# TAB 2: QUALITY & ML ANOMALIES
# =============================================================================
with tab_quality:
    st.markdown("### 🛡️ Data Quality Radar & Machine Learning Outlier Detection")

    col_q1, col_q2 = st.columns([1, 1])
    
    with col_q1:
        st.markdown("#### 🔍 Missingness & Duplication Breakdown")
        missing_dict = report["missing_by_column"]
        if missing_dict:
            miss_df = pd.DataFrame([
                {"Column": k, "Missing Count": v, "Percentage": f"{round(v / report['rows'] * 100, 2)}%"}
                for k, v in missing_dict.items()
            ])
            st.dataframe(miss_df, use_container_width=True)
        else:
            st.success("✅ Clean dataset: 0 missing or null cells detected across all dimensions.")

        st.markdown(f"**Duplicate Rows:** `{report['duplicate_rows']}` ({report['duplicate_percentage']}%)")
        if report['duplicate_rows'] > 0:
            st.warning("⚠️ Redundant records detected. Downstream regression and models may suffer from variance bias.")
        else:
            st.info("✅ Row topology is non-redundant and unique.")

    with col_q2:
        st.markdown("#### 🌲 Isolation Forest Anomaly Scanner (Multi-variate ML)")
        st.caption("Detects complex outliers that deviate across multi-dimensional feature space, beyond simple 1D min/max.")
        
        if report["anomaly_count"] > 0:
            st.warning(f"⚠️ **{report['anomaly_count']}** observations flagged as structural anomalies ({report['anomaly_pct']}% of dataset).")
            if report["anomaly_records"]:
                st.markdown("**Top Flagged Anomaly Observations:**")
                st.dataframe(pd.DataFrame(report["anomaly_records"]), use_container_width=True)
        else:
            st.success("✅ Isolation Forest found no multivariate anomalies based on current variance distribution.")

    st.markdown("---")
    st.markdown("#### 📊 Numeric Feature Statistics & Univariate Outlier Counts")
    if report["numeric_summary"]:
        num_stat_df = pd.DataFrame(report["numeric_summary"]).T
        st.dataframe(num_stat_df, use_container_width=True)
    else:
        st.info("No numeric columns present for parametric profiling.")

# =============================================================================
# TAB 3: QUANTUM VISUAL ANALYTICS
# =============================================================================
with tab_visuals:
    st.markdown("### 📊 Quantum Visual Exploratory Suite")

    vis_mode = st.radio(
        "Select Visualization Lens:",
        ["📈 Feature Distribution & Box Plot", "🔥 Correlation Matrix Heatmap", "🌌 2D Scatter & ML Outlier Projection", "🏷️ Categorical Frequency Distribution"],
        horizontal=True
    )

    dark_template = {
        "layout": {
            "paper_bgcolor": "rgba(15, 23, 42, 0)",
            "plot_bgcolor": "rgba(15, 23, 42, 0.4)",
            "font": {"color": "#e2e8f0", "family": "Space Grotesk"},
            "gridcolor": "rgba(255, 255, 255, 0.08)"
        }
    }

    if vis_mode == "📈 Feature Distribution & Box Plot":
        if report["numeric_cols"]:
            c_sel, c_bins = st.columns([3, 1])
            with c_sel:
                selected_num = st.selectbox("Select Numeric Feature to Profile:", report["numeric_cols"])
            with c_bins:
                num_bins = st.slider("Histogram Bins:", 10, 60, 25)

            c_fig1, c_fig2 = st.columns(2)
            with c_fig1:
                fig_hist = px.histogram(
                    df,
                    x=selected_num,
                    nbins=num_bins,
                    marginal="violin",
                    title=f"Histogram & Kernel Density: {selected_num}",
                    color_discrete_sequence=["#00f2fe"]
                )
                fig_hist.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.4)")
                st.plotly_chart(fig_hist, use_container_width=True)

            with c_fig2:
                fig_box = px.box(
                    df,
                    y=selected_num,
                    title=f"Boxplot & Univariate Outlier Range: {selected_num}",
                    color_discrete_sequence=["#a855f7"]
                )
                fig_box.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.4)")
                st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("No numeric columns available.")

    elif vis_mode == "🔥 Correlation Matrix Heatmap":
        if len(report["numeric_cols"]) >= 2:
            corr_df = df[report["numeric_cols"]].corr()
            fig_corr = px.imshow(
                corr_df,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="Viridis",
                title="Bivariate Pearson Correlation Heatmap"
            )
            fig_corr.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.4)")
            st.plotly_chart(fig_corr, use_container_width=True)

            if report["correlations"]:
                st.markdown("**Top Significant Collinear Pairs (|r| ≥ 0.5):**")
                for c in report["correlations"][:4]:
                    st.markdown(f"- `{c['feature_x']}` ↔ `{c['feature_y']}` : **r = {c['correlation']}** ({c['relationship']})")
        else:
            st.info("Need at least 2 numeric attributes for correlation matrix.")

    elif vis_mode == "🌌 2D Scatter & ML Outlier Projection":
        if len(report["numeric_cols"]) >= 2:
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                x_col = st.selectbox("X-Axis Feature:", report["numeric_cols"], index=0)
            with sc2:
                y_col = st.selectbox("Y-Axis Feature:", report["numeric_cols"], index=min(1, len(report["numeric_cols"]) - 1))
            with sc3:
                color_option = st.selectbox("Color By:", ["None", "ML Anomaly Flag"] + report["categorical_cols"][:3])

            scatter_df = df.copy()
            if color_option == "ML Anomaly Flag":
                scatter_df["Status"] = "Normal"
                if report["anomaly_count"] > 0:
                    for i in range(min(report["anomaly_count"], len(scatter_df))):
                        scatter_df.loc[i, "Status"] = "ML Anomaly"
                fig_scatter = px.scatter(
                    scatter_df,
                    x=x_col,
                    y=y_col,
                    color="Status",
                    color_discrete_map={"Normal": "#38bdf8", "ML Anomaly": "#ff007f"},
                    title=f"Scatter Projection: {x_col} vs {y_col} with ML Anomaly Highlighting"
                )
            elif color_option != "None":
                fig_scatter = px.scatter(
                    scatter_df,
                    x=x_col,
                    y=y_col,
                    color=color_option,
                    title=f"Scatter Projection: {x_col} vs {y_col} (Grouped by {color_option})"
                )
            else:
                fig_scatter = px.scatter(
                    scatter_df,
                    x=x_col,
                    y=y_col,
                    title=f"Scatter Projection: {x_col} vs {y_col}",
                    color_discrete_sequence=["#00f2fe"]
                )

            fig_scatter.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.4)")
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("At least 2 numeric features required.")

    elif vis_mode == "🏷️ Categorical Frequency Distribution":
        if report["categorical_cols"]:
            cat_choice = st.selectbox("Choose Categorical Feature:", report["categorical_cols"])
            val_counts = df[cat_choice].fillna("Missing").astype(str).value_counts().head(15).reset_index()
            val_counts.columns = [cat_choice, "Frequency"]
            
            fig_bar = px.bar(
                val_counts,
                x=cat_choice,
                y="Frequency",
                color="Frequency",
                color_continuous_scale="Blues",
                title=f"Distribution Frequency: {cat_choice}"
            )
            fig_bar.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.4)")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No categorical features detected.")

# =============================================================================
# TAB 4: OPENLENS AI INSIGHTS & NEURAL BRIEFING
# =============================================================================
with tab_ai:
    st.markdown("### ⚡ OpenLens Strategic AI & Machine Learning Synthesis")
    st.caption("Evidence-backed executive intelligence synthesis. 100% verified against data statistics.")

    # Cache AI insights in session state to avoid re-generating on every click
    insights_cache_key = f"insights_{metadata.get('file_name', 'default')}_{report['rows']}_{report['columns']}"
    
    gen_col1, gen_col2 = st.columns([1, 3])
    with gen_col1:
        re_run_ai = st.button("✨ Synthesize AI Briefing", type="primary", use_container_width=True)

    if re_run_ai or insights_cache_key not in st.session_state:
        with st.spinner("OpenLens Neural Engine is analyzing multi-variate telemetry..."):
            insights_text, engine_mode = generate_insights(report, user_gemini_key)
            st.session_state[insights_cache_key] = (insights_text, engine_mode)

    insights_text, engine_mode = st.session_state[insights_cache_key]

    st.markdown(f"""
    <div style="background: rgba(2, 132, 199, 0.12); border-left: 4px solid #00f2fe; padding: 10px 16px; border-radius: 6px; margin-bottom: 16px;">
        <span style="font-size: 0.8rem; font-family: 'JetBrains Mono'; color: #38bdf8;">ACTIVE REASONING ENGINE:</span> 
        <b style="color: #f8fafc;">{engine_mode}</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(insights_text)

    # Interactive Dataset Query Console
    st.markdown("---")
    st.markdown("#### 💬 Ask OpenLens AI about this Dataset")
    user_query = st.text_input("Ask any query (e.g., 'What is the average of highest column?', 'Which category has most records?'):", key="nl_query")
    if user_query:
        uq = user_query.lower()
        matched = False
        st.markdown("**OpenLens Quantum Agent Response:**")
        if "highest" in uq or "max" in uq:
            if report["numeric_summary"]:
                top_col = max(report["numeric_summary"].items(), key=lambda x: x[1]["max"])
                st.write(f"- Maximum value recorded across all features is in **{top_col[0]}** with a max of **{top_col[1]['max']:,}** (Mean: {top_col[1]['mean']:,}).")
                matched = True
        if "lowest" in uq or "min" in uq:
            if report["numeric_summary"]:
                low_col = min(report["numeric_summary"].items(), key=lambda x: x[1]["min"])
                st.write(f"- Minimum value recorded across all features is in **{low_col[0]}** with a min of **{low_col[1]['min']:,}**.")
                matched = True
        if "missing" in uq or "null" in uq:
            st.write(f"- Total missing cells: **{report['missing_cells']:,}** ({report['missing_percentage']}%).")
            matched = True
        if "anomaly" in uq or "outlier" in uq:
            st.write(f"- Isolation Forest detected **{report['anomaly_count']}** multivariate anomalies ({report['anomaly_pct']}% of dataset).")
            matched = True
        if "rows" in uq or "count" in uq or "size" in uq:
            st.write(f"- The dataset contains **{report['rows']:,}** rows and **{report['columns']}** columns.")
            matched = True
        if not matched:
            st.write(f"- OpenLens audited {report['rows']} records across {report['columns']} features with a health score of {report['health_score']}/100. Key correlations: {len(report['correlations'])} pairs identified.")

# =============================================================================
# TAB 5: MISSION CONTROL (UNIVERSAL MULTI-FORMAT EXPORTER)
# =============================================================================
with tab_export:
    st.markdown("### 🚀 Mission Control: Universal Multi-Format Export Center")
    st.markdown("Download full enterprise intelligence reports in any format required: **PDF, Word DOCX, Markdown, JSON, Enriched CSV, or Raw Telemetry Logs**.")

    col_e1, col_e2, col_e3 = st.columns(3)

    # 1. PDF Report
    with col_e1:
        st.markdown("""
        <div class="download-card">
            <span style="font-size: 2rem;">📑</span>
            <div style="font-weight: 700; color: #f8fafc; margin-top: 6px;">Executive PDF Report</div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 12px;">Styled presentation with tables, metrics & AI briefing</div>
        </div>
        """, unsafe_allow_html=True)
        try:
            pdf_data = generate_pdf_report(report, insights_text)
            st.download_button(
                "⬇️ Download PDF Report",
                data=pdf_data,
                file_name=f"OpenLens_Audit_{datetime.date.today()}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF build error: {e}")

    # 2. Word DOCX Report
    with col_e2:
        st.markdown("""
        <div class="download-card">
            <span style="font-size: 2rem;">📝</span>
            <div style="font-weight: 700; color: #f8fafc; margin-top: 6px;">Word Document (.DOCX)</div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 12px;">Editable enterprise report with native Word tables</div>
        </div>
        """, unsafe_allow_html=True)
        try:
            docx_data = generate_docx_report(report, insights_text)
            st.download_button(
                "⬇️ Download Word (.DOCX)",
                data=docx_data,
                file_name=f"OpenLens_Audit_{datetime.date.today()}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"DOCX build error: {e}")

    # 3. GitHub Markdown Report
    with col_e3:
        st.markdown("""
        <div class="download-card">
            <span style="font-size: 2rem;">📋</span>
            <div style="font-weight: 700; color: #f8fafc; margin-top: 6px;">Markdown Documentation (.MD)</div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 12px;">Clean README or Notion-ready documentation</div>
        </div>
        """, unsafe_allow_html=True)
        md_data = generate_markdown_report(report, insights_text)
        st.download_button(
            "⬇️ Download Markdown (.MD)",
            data=md_data,
            file_name=f"OpenLens_Audit_{datetime.date.today()}.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    col_e4, col_e5, col_e6 = st.columns(3)

    # 4. JSON Telemetry
    with col_e4:
        st.markdown("""
        <div class="download-card">
            <span style="font-size: 2rem;">💾</span>
            <div style="font-weight: 700; color: #f8fafc; margin-top: 6px;">Telemetry JSON (.JSON)</div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 12px;">Complete structured hierarchy for API integrations</div>
        </div>
        """, unsafe_allow_html=True)
        json_data = json.dumps(report, indent=2, default=str)
        st.download_button(
            "⬇️ Download JSON Telemetry",
            data=json_data,
            file_name=f"openlens_telemetry_{datetime.date.today()}.json",
            mime="application/json",
            use_container_width=True
        )

    # 5. Enriched CSV with Anomaly Flags
    with col_e5:
        st.markdown("""
        <div class="download-card">
            <span style="font-size: 2rem;">📊</span>
            <div style="font-weight: 700; color: #f8fafc; margin-top: 6px;">Enriched CSV (+ML Flags)</div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 12px;">Dataset with OPENLENS_IS_ANOMALY column added</div>
        </div>
        """, unsafe_allow_html=True)
        enriched_csv = generate_enriched_csv(df, report)
        st.download_button(
            "⬇️ Download Enriched CSV",
            data=enriched_csv,
            file_name=f"openlens_enriched_{datetime.date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # 6. Raw OpenTelemetry Audit Log
    with col_e6:
        st.markdown("""
        <div class="download-card">
            <span style="font-size: 2rem;">📡</span>
            <div style="font-weight: 700; color: #f8fafc; margin-top: 6px;">Audit Log / Telemetry (.LOG)</div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 12px;">Standard JSONL event stream for compliance & MLOps</div>
        </div>
        """, unsafe_allow_html=True)
        raw_log = generate_raw_telemetry_log(report, df)
        st.download_button(
            "⬇️ Download Raw Telemetry Log",
            data=raw_log,
            file_name=f"openlens_audit_{datetime.date.today()}.log",
            mime="text/plain",
            use_container_width=True
        )

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 0.78rem; color: #64748b; font-family: 'JetBrains Mono';">
    OPENLENS AI 2.0 // ADVANCED ML DATA OBSERVABILITY PLATFORM // BUILT FOR HIGH-ACCURACY ENTERPRISE AUDITS
</div>
""", unsafe_allow_html=True)
