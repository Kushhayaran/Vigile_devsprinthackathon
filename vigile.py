import streamlit as st
from google import genai
import time
import os
import json
from dotenv import load_dotenv

# -------------------- ENV SETUP --------------------
load_dotenv()
API_KEY = os.getenv("Gemini_api_key")

MODELS = [
    "gemini-2.5-flash-lite-preview-09-2025",
    "gemini-2.0-flash"
]

client = genai.Client(api_key=API_KEY)

# -------------------- STREAMLIT CONFIG --------------------
st.set_page_config(page_title="VIGILE: The Chat Moderator", layout="wide")

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("⚙️ Moderation Settings")
    strictness = st.slider(
        "Blocking Threshold (Hard Gate)",
        1, 10, 7
    )
    warn_threshold = st.slider(
        "Warning Threshold",
        1, 10, 4
    )

    st.divider()
    st.header("📊 Admin Logs")

    if "logs" not in st.session_state:
        st.session_state.logs = []

    for log in reversed(st.session_state.logs[-10:]):
        st.write(f"[{log['status']}] Score {log['score']} → {log['msg'][:20]}")

# -------------------- AI MODERATION FUNCTION --------------------
def process_safe_message(user_text):

    # 🚨 Emergency bypass for greetings (DEMO SAFE)
    if user_text.lower().strip() in ["hi", "hello", "hey", "good morning", "good evening"]:
        return 0, user_text

    prompt = f"""
You are a real-time chat moderation engine.

Analyze the message below and respond ONLY in valid JSON.

Message:
"{user_text}"

Return JSON ONLY in this format:
{{
  "score": <integer between 0 and 10>,
  "reply": "<polite alternative or same message if safe>"
}}

Rules:
- Friendly greetings must score 0 or 1
- Polite neutral messages score <= 2
- Toxic, abusive, hateful content score >= 7
- Do not include explanations or extra text
"""

    for model_id in MODELS:
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt
            )

            raw = response.text.strip()
            data = json.loads(raw)

            score = int(data.get("score", 0))
            reply = data.get("reply", user_text)

            # 🛡️ Clamp score safely
            score = max(0, min(score, 10))

            return score, reply

        except Exception as e:
            if "429" in str(e):
                continue  # Try next model
            st.error(f"Model error ({model_id}): {e}")

    return 0, "System busy. Please try again."

# -------------------- UI --------------------
st.title("🛡️ VIGILE")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------- CHAT INPUT --------------------
if user_input := st.chat_input("Type your message..."):

    with st.spinner("Moderating message..."):
        score, ai_reply = process_safe_message(user_input)

    # ----------- DECISION LOGIC -----------
    if score >= strictness:
        status = "BLOCK"
        st.error(f"🚫 Message Blocked (Score: {score})")
        st.info(f"Suggested polite version:\n\n*{ai_reply}*")

    elif score >= warn_threshold:
        status = "WARNING"
        st.warning(f"⚠️ Warning (Score: {score}) – Message allowed")

        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            st.markdown(ai_reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_reply}
        )

    else:
        status = "SAFE"

        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            st.markdown(ai_reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_reply}
        )

    # ----------- LOGGING -----------
    st.session_state.logs.append({
        "score": score,
        "status": status,
        "msg": user_input
    })
