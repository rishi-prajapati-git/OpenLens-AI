"""
OpenLens AI - Enterprise Universal File Loader
Supports CSV, TSV, Excel (.xlsx, .xls), JSON, Parquet, PDF, DOCX, TXT/LOG, and Markdown.
"""

import io
import re
import json
import pandas as pd
from typing import Tuple, Dict, Any, Optional

def load_file_to_dataframe(uploaded_file, sheet_name: Optional[str] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Parses any supported file into a pandas DataFrame and returns metadata.
    Supported types: csv, tsv, xlsx, xls, json, parquet, pdf, docx, txt, log, md.
    """
    file_name = uploaded_file.name
    extension = file_name.split(".")[-1].lower()
    metadata = {
        "file_name": file_name,
        "extension": extension,
        "size_bytes": getattr(uploaded_file, "size", len(uploaded_file.getvalue()) if hasattr(uploaded_file, "getvalue") else 0),
        "sheets": [],
        "source_format": extension.upper(),
        "parsed_notes": ""
    }

    raw_bytes = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else uploaded_file.read()
    byte_stream = io.BytesIO(raw_bytes)

    df = pd.DataFrame()

    if extension in ["csv", "tsv"]:
        delimiters = [",", "\t", ";", "|"] if extension != "tsv" else ["\t", ","]
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
        success = False
        last_err = None

        for enc in encodings:
            for sep in delimiters:
                try:
                    byte_stream.seek(0)
                    df = pd.read_csv(byte_stream, sep=sep, encoding=enc, engine="python", on_bad_lines="skip")
                    if not df.empty and df.shape[1] > 1:
                        success = True
                        metadata["parsed_notes"] = f"Parsed using separator '{repr(sep)}' and encoding '{enc}'"
                        break
                except Exception as e:
                    last_err = e
            if success:
                break

        if not success:
            byte_stream.seek(0)
            df = pd.read_csv(byte_stream, engine="python", on_bad_lines="skip")

    elif extension in ["xlsx", "xls"]:
        excel_file = pd.ExcelFile(byte_stream)
        metadata["sheets"] = excel_file.sheet_names
        chosen_sheet = sheet_name if sheet_name in excel_file.sheet_names else excel_file.sheet_names[0]
        df = pd.read_excel(excel_file, sheet_name=chosen_sheet)
        metadata["parsed_notes"] = f"Loaded sheet '{chosen_sheet}' from {len(excel_file.sheet_names)} sheet(s)."

    elif extension == "json":
        try:
            byte_stream.seek(0)
            text_data = raw_bytes.decode("utf-8", errors="replace")
            parsed_json = json.loads(text_data)
            if isinstance(parsed_json, list):
                df = pd.json_normalize(parsed_json)
            elif isinstance(parsed_json, dict):
                # Check if it has a list inside
                list_keys = [k for k, v in parsed_json.items() if isinstance(v, list)]
                if list_keys:
                    df = pd.json_normalize(parsed_json[list_keys[0]])
                    metadata["parsed_notes"] = f"Normalized nested key '{list_keys[0]}'"
                else:
                    df = pd.DataFrame([parsed_json])
            else:
                df = pd.DataFrame([{"raw_content": str(parsed_json)}])
        except Exception:
            # Fallback to lines=True
            byte_stream.seek(0)
            df = pd.read_json(byte_stream, lines=True)

    elif extension == "parquet":
        df = pd.read_parquet(byte_stream)

    elif extension == "pdf":
        import pypdf
        byte_stream.seek(0)
        reader = pypdf.PdfReader(byte_stream)
        extracted_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_text.append(text)
        
        full_text = "\n".join(extracted_text)
        metadata["pdf_pages"] = len(reader.pages)
        metadata["parsed_notes"] = f"Extracted text from {len(reader.pages)} PDF pages."

        # Attempt to parse table or structured lines from PDF
        lines = [line.strip() for line in full_text.splitlines() if line.strip()]
        rows = []
        for line in lines:
            # split by 2+ spaces, comma, or pipe
            parts = [p.strip() for p in re.split(r'\s{2,}|\t|\|', line) if p.strip()]
            if len(parts) > 1:
                rows.append(parts)
            else:
                rows.append([line])
        
        if rows:
            max_cols = max(len(r) for r in rows)
            # normalize row lengths
            padded_rows = [r + [None] * (max_cols - len(r)) for r in rows]
            # If first row looks like header
            if len(padded_rows) > 1 and max_cols > 1:
                headers = [f"Col_{i+1}_{str(h)[:15]}" for i, h in enumerate(padded_rows[0])]
                df = pd.DataFrame(padded_rows[1:], columns=headers)
            else:
                df = pd.DataFrame(padded_rows, columns=[f"Column_{i+1}" for i in range(max_cols)])
        else:
            df = pd.DataFrame({"Text_Content": ["Empty PDF content"]})

    elif extension == "docx":
        import docx
        byte_stream.seek(0)
        doc = docx.Document(byte_stream)
        
        # Check if doc has tables
        if len(doc.tables) > 0:
            table = doc.tables[0]
            data = []
            for row in table.rows:
                data.append([cell.text.strip() for cell in row.cells])
            if len(data) > 1:
                df = pd.DataFrame(data[1:], columns=[f"Col_{i+1}_{h[:15]}" if h else f"Col_{i+1}" for i, h in enumerate(data[0])])
            elif len(data) == 1:
                df = pd.DataFrame(data)
            metadata["parsed_notes"] = f"Extracted table with {len(data)} rows from Word document."
        else:
            # Extract paragraphs
            paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            records = []
            for i, p in enumerate(paragraphs):
                records.append({"Paragraph_Index": i + 1, "Content": p, "Word_Count": len(p.split())})
            df = pd.DataFrame(records)
            metadata["parsed_notes"] = f"Extracted {len(paragraphs)} paragraphs from Word document."

    elif extension in ["txt", "log", "md"]:
        text_data = raw_bytes.decode("utf-8", errors="replace")
        lines = [line.rstrip() for line in text_data.splitlines() if line.strip()]
        
        # Common log regex parser (timestamp, level, message)
        log_pattern = re.compile(r'^(?:\[(?P<timestamp>[^\]]+)\]|\b(?P<ts_iso>\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?))\s*(?:\[?(?P<level>INFO|WARN|WARNING|ERROR|FATAL|DEBUG|CRITICAL)\]?)?\s*:?\s*(?P<message>.*)$', re.IGNORECASE)
        
        parsed_logs = []
        is_structured_log = False
        for line in lines[:100]:
            if log_pattern.match(line):
                is_structured_log = True
                break

        if is_structured_log:
            for idx, line in enumerate(lines):
                m = log_pattern.match(line)
                if m:
                    gd = m.groupdict()
                    ts = gd.get("timestamp") or gd.get("ts_iso") or ""
                    lvl = gd.get("level") or "INFO"
                    msg = gd.get("message") or ""
                    parsed_logs.append({"Log_ID": idx + 1, "Timestamp": ts, "Severity": lvl.upper(), "Message": msg})
                else:
                    parsed_logs.append({"Log_ID": idx + 1, "Timestamp": "", "Severity": "TEXT", "Message": line})
            df = pd.DataFrame(parsed_logs)
            metadata["parsed_notes"] = f"Telemetry/Log parser processed {len(lines)} log lines."
        else:
            # Try delimiter parsing (csv or tsv style)
            byte_stream.seek(0)
            try:
                df = pd.read_csv(byte_stream, sep=None, engine="python", on_bad_lines="skip")
            except Exception:
                df = pd.DataFrame({"Line_Number": range(1, len(lines) + 1), "Text_Record": lines})
            metadata["parsed_notes"] = f"Parsed text file with {len(df)} records."

    else:
        # Fallback generic reader
        byte_stream.seek(0)
        try:
            df = pd.read_csv(byte_stream, on_bad_lines="skip")
        except Exception as e:
            text_data = raw_bytes.decode("utf-8", errors="replace")
            lines = text_data.splitlines()
            df = pd.DataFrame({"Content": lines[:1000]})
            metadata["parsed_notes"] = f"Fallback text parse: {str(e)}"

    # Clean DataFrame: replace whitespace column names
    if not df.empty:
        df.columns = [str(col).strip() if str(col).strip() else f"Col_{i}" for i, col in enumerate(df.columns)]
        # Dedup duplicate column names if any
        seen = {}
        new_cols = []
        for col in df.columns:
            if col in seen:
                seen[col] += 1
                new_cols.append(f"{col}_{seen[col]}")
            else:
                seen[col] = 0
                new_cols.append(col)
        df.columns = new_cols

    return df, metadata
