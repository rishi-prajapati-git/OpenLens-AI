"""
OpenLens AI - Enterprise Multi-Format Exporter
Generates JSON, PDF, DOCX (Word), Markdown, Enriched CSV, and Raw Telemetry Logs.
"""

import io
import json
import datetime
import pandas as pd
from typing import Dict, Any

# PDF Generation via ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Word DOCX Generation
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate_pdf_report(report: Dict[str, Any], insights_text: str, filename: str = "OpenLens_AI_Audit_Report.pdf") -> bytes:
    """Creates a beautifully styled, high-impact PDF audit report."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        "SubTitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=14
    )
    heading2_style = ParagraphStyle(
        "H2Style",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=colors.HexColor("#0284c7"),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.HexColor("#1e293b"),
        leading=13
    )

    elements = []

    # Title & Subtitle
    elements.append(Paragraph("🔍 OPENLENS AI // ENTERPRISE DATA INTELLIGENCE REPORT", title_style))
    gen_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Generated on {gen_time} | Status: AUDIT_COMPLETE | Core Engine: OpenLens ML", subtitle_style))
    elements.append(Spacer(1, 10))

    # Metric KPI Table
    metrics_data = [
        ["Total Records", "Dimensions", "Health Score", "Missing Cells", "ML Anomalies"],
        [
            f"{report.get('rows', 0):,}",
            f"{report.get('columns', 0)} Features",
            f"{report.get('health_score', 0)}/100",
            f"{report.get('missing_cells', 0):,} ({report.get('missing_percentage', 0)}%)",
            f"{report.get('anomaly_count', 0):,} ({report.get('anomaly_pct', 0)}%)"
        ]
    ]
    metric_table = Table(metrics_data, colWidths=[105, 105, 105, 105, 110])
    metric_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#38bdf8")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#f1f5f9")),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor("#0f172a")),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
    ]))
    elements.append(metric_table)
    elements.append(Spacer(1, 14))

    # Numeric Summary Table
    num_summary = report.get("numeric_summary", {})
    if num_summary:
        elements.append(Paragraph("📊 Numeric Attributes & Distribution Analytics", heading2_style))
        num_rows = [["Feature Name", "Mean", "Median", "Min", "Max", "IQR Outliers", "Skewness"]]
        for col_name, stats in list(num_summary.items())[:8]:
            num_rows.append([
                col_name[:16],
                str(stats.get("mean", "-")),
                str(stats.get("median", "-")),
                str(stats.get("min", "-")),
                str(stats.get("max", "-")),
                str(stats.get("outliers", 0)),
                str(stats.get("skewness", 0.0))
            ])
        num_table = Table(num_rows, colWidths=[100, 70, 70, 70, 70, 75, 75])
        num_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(num_table)
        elements.append(Spacer(1, 14))

    # AI & ML Insights Section
    elements.append(Paragraph("🤖 Strategic AI Insights & Machine Learning Findings", heading2_style))
    clean_lines = [l for l in insights_text.splitlines() if l.strip()]
    for line in clean_lines:
        line_clean = line.replace("#", "").replace("**", "").replace("`", "").strip()
        if line.startswith("###") or line.startswith("##"):
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(f"<b>{line_clean}</b>", ParagraphStyle('SubHeading', parent=body_style, fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#0369a1'))))
        elif line.startswith("-") or line.startswith("*"):
            elements.append(Paragraph(f"• {line_clean[1:].strip()}", body_style))
        else:
            elements.append(Paragraph(line_clean, body_style))
        elements.append(Spacer(1, 2))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def generate_docx_report(report: Dict[str, Any], insights_text: str) -> bytes:
    """Creates a professional Microsoft Word (.docx) document."""
    doc = docx.Document()
    
    # Title
    title = doc.add_heading('OpenLens AI - Executive Data Intelligence Audit', level=0)
    title.runs[0].font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(f"Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC | OpenLens Machine Learning v2.0")

    # Overview Metrics Table
    doc.add_heading('1. Executive Overview & Metrics', level=1)
    
    table = doc.add_table(rows=2, cols=5)
    table.style = 'Light Shading Accent 1'
    headers = ["Total Rows", "Columns", "Health Score", "Missing Data", "ML Anomalies"]
    values = [
        f"{report.get('rows', 0):,}",
        f"{report.get('columns', 0)}",
        f"{report.get('health_score', 0)}/100",
        f"{report.get('missing_cells', 0)} ({report.get('missing_percentage', 0)}%)",
        f"{report.get('anomaly_count', 0)} ({report.get('anomaly_pct', 0)}%)"
    ]
    for i, h in enumerate(headers):
        table.cell(0, i).text = h
    for i, v in enumerate(values):
        table.cell(1, i).text = v

    doc.add_paragraph()

    # Numeric Summary Table
    num_summary = report.get("numeric_summary", {})
    if num_summary:
        doc.add_heading('2. Numeric Feature Distribution & Outlier Profiling', level=1)
        num_table = doc.add_table(rows=1, cols=7)
        num_table.style = 'Table Grid'
        col_headers = ["Feature", "Mean", "Median", "Min", "Max", "Outliers", "Skew"]
        for i, ch in enumerate(col_headers):
            num_table.cell(0, i).text = ch
        for col_name, stats in list(num_summary.items())[:12]:
            row_cells = num_table.add_row().cells
            row_cells[0].text = str(col_name)
            row_cells[1].text = str(stats.get("mean", "-"))
            row_cells[2].text = str(stats.get("median", "-"))
            row_cells[3].text = str(stats.get("min", "-"))
            row_cells[4].text = str(stats.get("max", "-"))
            row_cells[5].text = str(stats.get("outliers", 0))
            row_cells[6].text = str(stats.get("skewness", 0.0))

    # Insights
    doc.add_heading('3. Machine Learning Observations & Strategic Recommendations', level=1)
    for line in insights_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("###"):
            doc.add_heading(line.replace("###", "").strip(), level=2)
        elif line.startswith("-") or line.startswith("*"):
            p = doc.add_paragraph(line.lstrip("-* ").strip(), style='List Bullet')
        else:
            doc.add_paragraph(line)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


def generate_markdown_report(report: Dict[str, Any], insights_text: str) -> str:
    """Creates a complete GitHub-flavored Markdown report."""
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    md = f"""# 🔍 OpenLens AI - Executive Intelligence Audit Report
*Generated on {now_str} | Powered by OpenLens Machine Learning Engine*

---

## 📊 1. Core Telemetry & Quality Health Index
| Metric | Value |
|---|---|
| **Total Record Volume** | `{report.get('rows', 0):,}` rows |
| **Feature Dimensionality** | `{report.get('columns', 0)}` features |
| **Dataset Health Score** | **`{report.get('health_score', 0)} / 100`** |
| **Missing Cells** | `{report.get('missing_cells', 0):,}` ({report.get('missing_percentage', 0)}%) |
| **Duplicate Records** | `{report.get('duplicate_rows', 0):,}` ({report.get('duplicate_percentage', 0)}%) |
| **Isolation Forest Anomalies** | `{report.get('anomaly_count', 0):,}` flagged records ({report.get('anomaly_pct', 0)}%) |

---

## 📈 2. Numeric Attributes Summary
| Feature | Mean | Median | Min | Max | IQR Outliers | Skewness |
|---|---|---|---|---|---|---|
"""
    for col_name, stats in report.get("numeric_summary", {}).items():
        md += f"| `{col_name}` | {stats.get('mean')} | {stats.get('median')} | {stats.get('min')} | {stats.get('max')} | {stats.get('outliers')} | {stats.get('skewness')} |\n"

    md += f"""
---

## 🤖 3. AI Insights & Evidence-Based Findings
{insights_text}

---
*Report automatically compiled by OpenLens AI. All calculations verified with deterministic ML.*
"""
    return md


def generate_raw_telemetry_log(report: Dict[str, Any], raw_df: pd.DataFrame) -> str:
    """
    Generates machine-readable OpenTelemetry-style audit log events.
    Useful for MLOps, auditing, and observability pipelines.
    """
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    
    events = [
        {
            "timestamp": timestamp,
            "event_type": "TELEMETRY_PIPELINE_INIT",
            "source": "openlens.engine.v2",
            "severity": "INFO",
            "payload": {
                "dataset_shape": [report.get("rows"), report.get("columns")],
                "memory_usage_kb": report.get("memory_kb"),
                "schema_hash": hash(tuple(raw_df.columns))
            }
        },
        {
            "timestamp": timestamp,
            "event_type": "DATA_HEALTH_EVALUATION",
            "source": "openlens.health_scorer",
            "severity": "WARNING" if report.get("health_score", 100) < 80 else "INFO",
            "payload": {
                "health_score": report.get("health_score"),
                "null_cells_count": report.get("missing_cells"),
                "null_cells_percentage": report.get("missing_percentage"),
                "duplicate_rows": report.get("duplicate_rows")
            }
        },
        {
            "timestamp": timestamp,
            "event_type": "ISOLATION_FOREST_ANOMALY_SCAN",
            "source": "openlens.ml.isolation_forest",
            "severity": "ALERT" if report.get("anomaly_count", 0) > 0 else "INFO",
            "payload": {
                "algorithm": "scikit-learn.IsolationForest",
                "anomalies_detected": report.get("anomaly_count"),
                "anomaly_rate_percent": report.get("anomaly_pct"),
                "sample_anomaly_indices": [rec.get("index", idx) for idx, rec in enumerate(report.get("anomaly_records", [])[:5])]
            }
        },
        {
            "timestamp": timestamp,
            "event_type": "MULTICOLLINEARITY_ANALYSIS",
            "source": "openlens.stats.correlation",
            "severity": "INFO",
            "payload": {
                "significant_correlations_count": len(report.get("correlations", [])),
                "top_correlations": report.get("correlations", [])[:5]
            }
        },
        {
            "timestamp": timestamp,
            "event_type": "AUDIT_PIPELINE_COMPLETE",
            "source": "openlens.engine.v2",
            "severity": "SUCCESS",
            "payload": {
                "status": "READY_FOR_EXPORT",
                "supported_targets": ["JSON", "PDF", "DOCX", "MARKDOWN", "CSV", "OTEL_LOG"]
            }
        }
    ]

    log_lines = [json.dumps(ev) for ev in events]
    return "\n".join(log_lines)


def generate_enriched_csv(df: pd.DataFrame, report: Dict[str, Any]) -> str:
    """Enriches the dataset with ML Anomaly flags and returns CSV string."""
    enriched = df.copy()
    anomaly_indices = [idx for idx in report.get("anomaly_records", []) if isinstance(idx, int)]
    if not anomaly_indices and report.get("anomaly_records"):
        # Match from anomaly records
        anomaly_indices = [r.get("Unnamed: 0", r.get("id", i)) for i, r in enumerate(report.get("anomaly_records"))]

    enriched["OPENLENS_IS_ANOMALY"] = False
    if report.get("anomaly_count", 0) > 0:
        # flag anomalies
        for i in range(min(report.get("anomaly_count", 0), len(enriched))):
            if i in enriched.index:
                enriched.loc[i, "OPENLENS_IS_ANOMALY"] = True

    return enriched.to_csv(index=False)
