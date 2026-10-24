
import ollama

def generate_insights(analysis_report, model="gemma3:1b"):
    """Generate evidence-based explanations using a local Gemma model."""

    prompt = f"""
    You are OpenLens AI, a careful data analyst.

    Analyze the following computed dataset statistics.
    Explain the findings in simple language.
    Do not invent values or claim causation.
    If evidence is insufficient, clearly say so.

    Dataset analysis:
    {analysis_report}

    Return:
    1. Three important observations
    2. Potential data quality issues
    3. Two actionable recommendations
    """

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
