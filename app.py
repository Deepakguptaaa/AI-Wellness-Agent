import streamlit as st
from google import genai

# Gemini API Key
API_KEY = "AQ.Ab8RN6KaYZlKTzce5uogjhZTiZJl1zFy1utWYkTfCqIZ2FpTtw"

client = genai.Client(api_key=API_KEY)

# Page Settings
st.set_page_config(
    page_title="AI Wellness Agent",
    page_icon="🩺",
    layout="wide"
)

# Title
st.title("🩺 AI Wellness Agent")

# Health Tips
st.info("""
💧 Drink enough water
😴 Sleep 7-8 hours daily
🏃 Exercise regularly
🥗 Eat balanced meals
""")

# Sidebar
st.sidebar.title("Health Categories")

category = st.sidebar.selectbox(
    "Select Category",
    [
        "General",
        "Sleep",
        "Fitness",
        "Nutrition",
        "Stress"
    ]
)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
prompt = st.chat_input("Ask your health question...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
You are an AI Wellness Agent.

Category: {category}

Provide practical and easy-to-understand wellness advice.

Focus on:
- Sleep
- Fitness
- Nutrition
- Stress Management

Question:
{prompt}
"""
    )

    answer = response.text

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.write(answer)