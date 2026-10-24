import os
from google import genai


def generate_insights(analysis_report):
    """Generate evidence-based data insights using Google Gemini."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Gemini API key is missing.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are OpenLens AI, a careful data analyst.
    Analyze these dataset statistics in simple language.
    Do not invent values or claim causation.
    If evidence is insufficient, say so.

    Dataset analysis:
    {analysis_report}

    Return:
    1. Three important observations
    2. Potential data quality issues
    3. Two actionable recommendations
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text