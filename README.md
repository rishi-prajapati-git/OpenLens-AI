# 🔍 OpenLens AI
**Your Data. Your Evidence.**

OpenLens AI is an open-source, AI-powered data analysis tool that transforms CSV files into clear insights. It detects data quality issues, visualizes patterns, and uses Google's Gemma model to explain findings.

## ✨ Features
- 📂 Upload and preview CSV datasets
- 🧹 Detect missing values and duplicate rows
- 📊 Explore statistics, outliers, and interactive charts
- 🤖 Generate AI-powered insights using Gemma
- 📥 Export analysis reports as JSON

## 🛠️ Tech Stack
Python • Pandas • NumPy • Streamlit • Plotly • Ollama • Gemma

## 🚀 Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Install Ollama: https://ollama.com/download/windows
3. Download the model: `ollama pull gemma3:1b`
4. Launch: `python -m streamlit run app.py`

## 🧠 AI Contribution
Python computes dataset statistics; Gemma interprets those statistics to generate explanations and recommendations. AI-generated results should be verified against the data.

## 📂 Project Structure
- `app.py` — Streamlit dashboard
- `analyzer.py` — Data quality and statistical analysis
- `llm_client.py` — Gemma integration
- `data/` — Sample CSV dataset
- `requirements.txt` — Python dependencies

## 📜 License
MIT License. See `LICENSE` for details.
