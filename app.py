
import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path
from analyzer import analyze_dataframe

st.set_page_config(
    page_title="OpenLens AI",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 OpenLens AI")
st.caption("Your Data. Your Evidence. | AI-powered data analysis")

uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read CSV: {exc}")
        st.stop()
else:
    sample_path = Path(__file__).parent / "data" / "sample_employees.csv"
    data = pd.read_csv(sample_path)
    st.info("Showing sample employee data. Upload your own CSV to analyze it.")

if data.empty:
    st.warning("The dataset is empty.")
    st.stop()

report = analyze_dataframe(data)

st.subheader("📊 Dataset Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", report["rows"])
c2.metric("Columns", report["columns"])
c3.metric("Missing Cells", report["missing_cells"])
c4.metric("Data Health Score", f'{report["health_score"]}/100')

tab1, tab2, tab3, tab4 = st.tabs([
    "Dataset Preview",
    "Data Quality",
    "Visual Analytics",
    "AI Insights"
])

with tab1:
    st.subheader("First 20 rows")
    st.dataframe(data.head(20), use_container_width=True)

    st.subheader("Column Information")
    info = pd.DataFrame({
        "Column": data.columns,
        "Data Type": data.dtypes.astype(str).values,
        "Missing Values": data.isnull().sum().values,
        "Unique Values": data.nunique().values
    })
    st.dataframe(info, use_container_width=True)

with tab2:
    st.subheader("Missing Values")
    missing = data.isnull().sum()
    missing = missing[missing > 0]

    if len(missing):
        missing_df = missing.rename("Missing Count").reset_index()
        missing_df.columns = ["Column", "Missing Count"]
        st.dataframe(missing_df, use_container_width=True)
    else:
        st.success("No missing values found.")

    duplicates = int(data.duplicated().sum())
    st.metric("Duplicate Rows", duplicates)

    st.subheader("Numeric Statistics")
    if report["numeric_summary"]:
        st.dataframe(
            pd.DataFrame(report["numeric_summary"]).T,
            use_container_width=True
        )
    else:
        st.info("No numeric columns found.")

with tab3:
    numeric_columns = data.select_dtypes(include="number").columns.tolist()
    categorical_columns = data.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    if numeric_columns:
        selected_num = st.selectbox(
            "Choose a numeric column",
            numeric_columns
        )
        fig = px.histogram(
            data,
            x=selected_num,
            title=f"Distribution of {selected_num}"
        )
        st.plotly_chart(fig, use_container_width=True)

    if categorical_columns:
        selected_cat = st.selectbox(
            "Choose a categorical column",
            categorical_columns
        )
        counts = data[selected_cat].fillna("Missing").astype(str).value_counts()
        fig = px.bar(
            x=counts.index,
            y=counts.values,
            labels={"x": selected_cat, "y": "Count"},
            title=f"Distribution of {selected_cat}"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    from llm_client import generate_insights

    st.subheader("🤖 Gemma AI Data Analyst")
    st.write("Generate explanations from the dataset's calculated statistics.")

    st.markdown("**Deterministic findings**")
    st.write(f"- Dataset contains {report['rows']} rows and {report['columns']} columns.")
    st.write(f"- {report['missing_cells']} missing cells were found.")
    st.write(f"- {report['duplicate_rows']} duplicate rows were found.")

    if st.button("✨ Generate AI Insights"):
        with st.spinner("Gemma is analyzing the evidence..."):
            try:
                insights = generate_insights(report)
                st.markdown("### AI-generated insights")
                st.write(insights)
                st.success("Generated using the configured local model.")
            except Exception as exc:
                st.error(
                    "Could not connect to Gemma. Make sure Ollama is installed, "
                    "running, and the configured model is downloaded."
                )
                st.caption(str(exc))

report_json = json.dumps(report, indent=2, default=str)
st.download_button(
    "⬇️ Download Analysis Report (JSON)",
    data=report_json,
    file_name="openlens_analysis.json",
    mime="application/json"
)

st.caption("OpenLens AI | Open-source project")
