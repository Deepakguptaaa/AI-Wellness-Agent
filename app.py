import streamlit as st
from google import genai


API_KEY = "YOUR_API_KEY_HERE"

client = genai.Client(api_key=API_KEY)

st.set_page_config(
    page_title="AI Wellness Agent Pro",
    page_icon="🩺",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------

st.title("🩺 AI Wellness Agent Pro")
st.caption("AI-powered wellness assistant")

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("Health Categories")

category = st.sidebar.selectbox(
    "Choose Category",
    ["General", "Sleep", "Fitness", "Nutrition", "Stress"]
)

st.sidebar.markdown("---")
st.sidebar.write("### Daily Health Goals")
st.sidebar.write("💧 Drink 2-3L Water")
st.sidebar.write("😴 Sleep 7-8 Hours")
st.sidebar.write("🏃 Exercise 30 Minutes")

# -----------------------------
# BMI CALCULATOR
# -----------------------------

st.header("⚖️ BMI Calculator")

weight = st.number_input(
    "Weight (kg)",
    min_value=1.0,
    value=70.0
)

height = st.number_input(
    "Height (meters)",
    min_value=0.5,
    value=1.70
)

if st.button("Calculate BMI"):

    bmi = weight / (height ** 2)

    st.success(f"Your BMI is {bmi:.2f}")

    if bmi < 18.5:
        st.warning("Category: Underweight")
    elif bmi < 25:
        st.success("Category: Normal Weight")
    elif bmi < 30:
        st.warning("Category: Overweight")
    else:
        st.error("Category: Obese")

st.divider()

# -----------------------------
# WELLNESS REPORT
# -----------------------------

st.header("📊 Wellness Report Generator")

sleep_hours = st.slider("Sleep Hours", 0, 12, 7)
water_intake = st.slider("Water Intake (Liters)", 0, 5, 2)
exercise_minutes = st.slider("Exercise Minutes", 0, 180, 30)
stress_level = st.slider("Stress Level", 1, 10, 5)

if st.button("Generate Wellness Report"):

    report_prompt = f"""
    Analyze this wellness profile.

    Sleep Hours: {sleep_hours}
    Water Intake: {water_intake} liters
    Exercise Minutes: {exercise_minutes}
    Stress Level: {stress_level}/10

    Give:
    - Wellness Score out of 100
    - Strengths
    - Weaknesses
    - Recommendations
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=report_prompt
        )

        st.success("Report Generated")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

# -----------------------------
# AI CHAT
# -----------------------------

st.header("💬 AI Wellness Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input(
    "Ask a wellness question..."
)

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

    try:

        prompt = f"""
        You are a professional wellness coach.

        Category: {category}

        Give practical advice related to:
        - Sleep
        - Fitness
        - Nutrition
        - Stress Management

        User Question:
        {user_input}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = response.text

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.write(answer)

    except Exception as e:
        st.error(f"Error: {e}")