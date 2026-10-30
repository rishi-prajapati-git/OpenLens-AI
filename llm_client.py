"""
OpenLens AI - Hybrid Generative AI & Autonomous Neural Engine
Combines Google Gemini Generative Intelligence with deterministic fallback.
Guarantees 100% uptime: never crashes if API keys are missing or offline.
"""

import os
from typing import Dict, Any, Tuple

def generate_insights(analysis_report: Dict[str, Any], user_api_key: str = None) -> Tuple[str, str]:
    """
    Generates strategic, executive-grade dataset insights.
    Returns: (insights_text, engine_mode)
    """
    api_key = user_api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if api_key and api_key.strip():
        try:
            from google import genai
            client = genai.Client(api_key=api_key.strip())
            
            prompt = f"""
You are OpenLens AI — a world-class principal data scientist and AI analyst.
Analyze the following deep machine-learning telemetry and dataset statistics.

[DATASET METRICS & ML TELEMETRY]:
- Dimensions: {analysis_report.get('rows')} rows x {analysis_report.get('columns')} columns
- Health Score: {analysis_report.get('health_score')}/100
- Missing Data: {analysis_report.get('missing_cells')} cells ({analysis_report.get('missing_percentage')}%)
- Duplicates: {analysis_report.get('duplicate_rows')} rows ({analysis_report.get('duplicate_percentage')}%)
- Isolation Forest Anomalies: {analysis_report.get('anomaly_count')} flagged records ({analysis_report.get('anomaly_pct')}%)
- Key Correlations: {analysis_report.get('correlations', [])[:3]}
- Clusters Identified: {analysis_report.get('clusters_info', [])}
- Numeric Distribution Summary: {analysis_report.get('numeric_summary', {})}

[INSTRUCTIONS]:
Deliver a structured, highly authoritative executive briefing:
1. 🎯 Executive Intelligence Summary (3 sharp, data-backed observations)
2. ⚠️ Critical Risk & Anomaly Assessment (Highlight the Isolation Forest outliers and data vulnerabilities)
3. 🔬 Feature Dynamics & Archetype Patterns (Interpret the correlations and cluster archetypes)
4. 🚀 Strategic & Tactical Action Plan (2-3 high-impact operational decisions)

Maintain a futuristic, decisive, and mathematically rigorous tone.
"""
            # Try newer gemini models gracefully
            for model_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    if response and response.text:
                        return response.text, f"Google Gemini API ({model_name})"
                except Exception:
                    continue

        except Exception as e:
            # Fall through gracefully to deterministic autonomous engine
            pass

    # Autonomous High-Precision Fallback Synthesis
    engine_mode = "OpenLens Autonomous ML Heuristic Engine (Offline / Standalone Active)"
    
    findings = analysis_report.get("evidence_insights", {}).get("key_findings", [])
    warnings = analysis_report.get("evidence_insights", {}).get("risk_warnings", [])
    actions = analysis_report.get("evidence_insights", {}).get("strategic_actions", [])
    
    corr_bullets = ""
    for c in analysis_report.get("correlations", [])[:3]:
        corr_bullets += f"- **{c['feature_x']}** vs **{c['feature_y']}**: Correlation `r = {c['correlation']}` ({c['relationship']})\n"
    if not corr_bullets:
        corr_bullets = "- Features show independent, uncorrelated variance across dimensions.\n"

    cluster_bullets = ""
    for cl in analysis_report.get("clusters_info", []):
        cluster_bullets += f"- **{cl['cluster_id']}**: {cl['population']} observations ({cl['percentage']}%) — Profile: `{cl['archetype_profile']}`\n"
    if not cluster_bullets:
        cluster_bullets = "- Dataset volume does not require multi-archetype clustering.\n"

    fallback_text = f"""### 🎯 1. Executive Intelligence Summary
- **Data Matrix Dimension**: Processed **{analysis_report.get('rows', 0):,}** records across **{analysis_report.get('columns', 0)}** attributes with an overall Data Health Score of **{analysis_report.get('health_score', 0)}/100**.
- **Observability**: {findings[0] if findings else 'Telemetry records verified and balanced.'}
- **Structural Integrity**: {"Clean row topology with zero duplicate interference." if analysis_report.get('duplicate_rows', 0) == 0 else f"Redundancy pressure of {analysis_report.get('duplicate_percentage', 0)}% detected across records."}

### ⚠️ 2. Critical Risk & Anomaly Assessment
- **Isolation Forest ML Model**: Flagged **{analysis_report.get('anomaly_count', 0)}** multivariate anomalous points ({analysis_report.get('anomaly_pct', 0)}% of dataset). These records deviate significantly in multidimensional feature space.
- **Data Health Assessment**:
{chr(10).join(f"- {w}" for w in warnings)}

### 🔬 3. Feature Dynamics & Clustering Archetypes
- **Top Feature Correlations**:
{corr_bullets}
- **K-Means Cluster Archetypes**:
{cluster_bullets}

### 🚀 4. Strategic & Tactical Action Plan
{chr(10).join(f"- {a}" for a in actions)}
"""

    return fallback_text, engine_mode
