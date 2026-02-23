import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Retail AI Research Dashboard", layout="wide")

# =====================================================
# SESSION STATE INIT
# =====================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_conversation" not in st.session_state:
    st.session_state.selected_conversation = None

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("💬 Conversations")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    st.session_state.chat_history = []
    st.session_state.selected_conversation = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📚 Previous Research")

try:
    response = requests.get("http://127.0.0.1:8000/search-history")
    history = response.json()
except:
    history = []

if history:
    df = pd.DataFrame(history)

    for i, row in df.iterrows():
        if st.sidebar.button(
            f"{row['query'][:35]}...",
            key=f"history_{i}",
            use_container_width=True
        ):
            report_response = requests.get(
                f"http://127.0.0.1:8000/report/{row['_id']}"
            )

            if report_response.status_code == 200:
                conversation_data = report_response.json()

                st.session_state.chat_history = conversation_data.get(
                    "chat_history", []
                )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": conversation_data.get("report"),
                    "timestamp": row["timestamp"]
                })

                st.session_state.selected_conversation = row["_id"]
                st.rerun()

# =====================================================
# HERO
# =====================================================
st.markdown("""
<div style='background: linear-gradient(90deg,#141e30,#243b55);
padding:30px;border-radius:15px;color:white;text-align:center;'>
<h1>🚀 Autonomous Retail Researcher Agent</h1>
<p>Conversational AI for Retail Market Intelligence</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# KPI SECTION
# =====================================================
def fetch_kpis():
    if not history:
        return 0, 0, 0

    df = pd.DataFrame(history)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    now = datetime.now()
    last_7 = now - timedelta(days=7)
    prev_7 = now - timedelta(days=14)

    recent = df[df["timestamp"] >= last_7]
    previous = df[(df["timestamp"] >= prev_7) & (df["timestamp"] < last_7)]

    growth = (
        100 if len(previous) == 0
        else round(((len(recent) - len(previous)) / len(previous)) * 100, 2)
    )

    return len(df), df["query"].nunique(), growth


total_reports, unique_queries, growth_percent = fetch_kpis()

st.subheader("📊 Platform Intelligence Metrics")

c1, c2, c3 = st.columns(3)
c1.metric("📄 Total Reports", total_reports, delta=f"{growth_percent}%")
c2.metric("🔎 Unique Queries", unique_queries)
c3.metric("⚡ AI Engine", "Gemini 2.5")

st.markdown("---")

# =====================================================
# SMART REPORT FORMATTER
# =====================================================
def format_report(report_text):

    if not report_text:
        return "No report generated."

    # Pre-clean
    report_text = report_text.replace("Key Insights:", "Key Insights")
    report_text = report_text.replace("New Strategic Suggestions", "Strategic Recommendations")

    lines = report_text.split("\n")

    sections = {
        "Executive Summary": [],
        "Market Overview": [],
        "Key Insights": [],
        "Market Trends": [],
        "Opportunities": [],
        "Risks & Challenges": [],
        "Strategic Recommendations": [],
        "Conclusion": []
    }

    current_section = None

    for line in lines:
        clean = line.strip().lower()

        # Detect section headings strictly
        if clean.startswith("executive"):
            current_section = "Executive Summary"
            continue

        elif clean.startswith("market overview"):
            current_section = "Market Overview"
            continue

        elif clean.startswith("key insights"):
            current_section = "Key Insights"
            continue

        elif clean.startswith("market trends"):
            current_section = "Market Trends"
            continue

        elif clean.startswith("opportunities"):
            current_section = "Opportunities"
            continue

        elif clean.startswith("risks"):
            current_section = "Risks & Challenges"
            continue

        elif clean.startswith("strategic"):
            current_section = "Strategic Recommendations"
            continue

        elif clean.startswith("conclusion"):
            current_section = "Conclusion"
            continue

        # Add content
        if current_section:
            if line.strip().startswith("-") or line.strip().startswith("•"):
                sections[current_section].append(f"- {line.strip()[1:]}")
            elif line.strip() != "":
                sections[current_section].append(line.strip())

    # Build final ordered report
    formatted = ""

    for section_name in sections:
        content = sections[section_name]
        if content:
            formatted += f"\n\n## {section_name}\n\n"
            for item in content:
                formatted += f"{item}\n\n"

    return formatted

# =====================================================
# CHAT DISPLAY
# =====================================================
st.subheader("💬 Retail Intelligence Conversation")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):

        if msg["role"] == "assistant":
            formatted_text = format_report(msg["content"])
            st.markdown(formatted_text)
        else:
            st.markdown(msg["content"])

        st.caption(msg.get("timestamp", ""))

# =====================================================
# CHAT INPUT
# =====================================================
user_query = st.chat_input("Ask about retail market trends, growth, risks…")

if user_query:

    user_time = datetime.now().strftime("%H:%M:%S")

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_query,
        "timestamp": user_time
    })

    with st.chat_message("user"):
        st.markdown(user_query)
        st.caption(user_time)

    payload = {
        "query": user_query,
        "chat_history": [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.chat_history
        ]
    }

    with st.chat_message("assistant"):

        try:
            response = requests.post(
                "http://127.0.0.1:8000/research", json=payload
            )

            if response.status_code != 200:
                st.error("Backend error.")
                full_response = "Error generating research."
            else:
                data = response.json()

                if "report" in data:
                    full_response = data["report"]
                    formatted_text = format_report(full_response)
                    st.markdown(formatted_text)
                else:
                    full_response = "Error generating research."
                    st.error(full_response)

        except:
            full_response = "Backend connection failed."
            st.error(full_response)

        assistant_time = datetime.now().strftime("%H:%M:%S")
        st.caption(assistant_time)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": full_response,
        "timestamp": assistant_time
    })
