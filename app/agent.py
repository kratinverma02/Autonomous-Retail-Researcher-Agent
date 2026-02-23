import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "models/gemini-2.5-flash"


def generate_report(
    query,
    web_data,
    conversation_context="",
    memory_context="",
    history_context=""
):

    # ------------------------------
    # Build Web Research Context
    # ------------------------------
    if web_data and len(web_data) > 0:
        web_context = "\n\n".join(
            [
                f"Title: {item.get('title','')}\n"
                f"Content: {item.get('content','')}\n"
                f"URL: {item.get('url','')}"
                for item in web_data
            ]
        )
    else:
        web_context = "No recent web data found. Use industry expertise."

    # ------------------------------
    # Construct Final Prompt
    # ------------------------------
    prompt = f"""
You are a Senior Retail Market Intelligence Expert.

Your goal is to provide structured, executive-level, easy-to-read retail research.

RULES:
- Be concise and business-friendly
- Avoid repeating past answers
- Extend previous insights intelligently
- Do NOT invent fake statistics
- Keep insights practical and strategic

--------------------------------------------------
Previous Conversation Context:
{conversation_context}

--------------------------------------------------
Relevant Past Research Memory:
{memory_context}

--------------------------------------------------
Additional History Context:
{history_context}

--------------------------------------------------
Current User Query:
{query}

--------------------------------------------------
Latest Web Intelligence Data:
{web_context}

==================================================

Generate the report STRICTLY in the following format:

Executive Summary:
(3–5 short business-focused sentences)

Key Market Trends:
- Trend Name: Short explanation
- Trend Name: Short explanation

Key Insights:
- Insight 1
- Insight 2
- Insight 3

Opportunities:
- Opportunity 1
- Opportunity 2

Risks & Challenges:
- Risk 1
- Risk 2

Strategic Recommendations:
- Actionable recommendation
- Actionable recommendation

New Strategic Suggestions Based on Past Research:
(Only if relevant. Avoid repetition.)
"""

    # ------------------------------
    # Call Gemini Model
    # ------------------------------
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception:
        return """
Executive Summary:
Unable to generate report at this time.

Key Market Trends:
- Data unavailable

Key Insights:
- Model execution failed

Opportunities:
- Retry request

Risks & Challenges:
- Temporary AI processing issue

Strategic Recommendations:
- Check API configuration

New Strategic Suggestions Based on Past Research:
None
"""
