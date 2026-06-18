import streamlit as st
from google import genai


API_KEY = "API_KEY"

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
# CALORIE CALCULATOR
# -----------------------------

st.header("🔥 Daily Calorie Calculator")

age = st.number_input(
    "Age",
    min_value=10,
    max_value=100,
    value=21
)

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

activity = st.selectbox(
    "Activity Level",
    [
        "Sedentary",
        "Lightly Active",
        "Moderately Active",
        "Very Active"
    ]
)

if st.button("Calculate Calories"):

    height_cm = height * 100

    if gender == "Male":
        bmr = (
            10 * weight +
            6.25 * height_cm -
            5 * age + 5
        )
    else:
        bmr = (
            10 * weight +
            6.25 * height_cm -
            5 * age - 161
        )

    factors = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }

    calories = bmr * factors[activity]

    st.success(
        f"Estimated Daily Calories: {int(calories)} kcal"
    )



# -----------------------------
# WELLNESS REPORT
# -----------------------------

st.header("📊 Wellness Dashboard")

sleep_hours = st.slider("Sleep Hours", 0, 12, 7)
water_intake = st.slider("Water Intake (Liters)", 0, 5, 2)
exercise_minutes = st.slider("Exercise Minutes", 0, 180, 30)
stress_level = st.slider("Stress Level", 1, 10, 5)

score = 100

if sleep_hours < 7:
    score -= 20

if water_intake < 2:
    score -= 15

if exercise_minutes < 30:
    score -= 15

if stress_level > 7:
    score -= 20

col1, col2, col3, col4 = st.columns(4)

col1.metric("😴 Sleep", f"{sleep_hours} hrs")
col2.metric("💧 Water", f"{water_intake} L")
col3.metric("🏃 Exercise", f"{exercise_minutes} min")
col4.metric("📈 Score", f"{score}/100")

st.divider()

st.header("📋 AI Wellness Report")

if st.button("Generate Wellness Report"):

    report_prompt = f"""
    Analyze this wellness profile.

    Sleep Hours: {sleep_hours}
    Water Intake: {water_intake} liters
    Exercise Minutes: {exercise_minutes}
    Stress Level: {stress_level}/10

    Current Wellness Score: {score}/100

    Give:
    - Wellness Score Analysis
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

st.header("📅 7-Day Wellness Plan")

if st.button("📅 Generate Personalized Plan"):

    plan_prompt = f"""
    Create a personalized 7-day wellness plan.

    Sleep Hours: {sleep_hours}
    Water Intake: {water_intake}
    Exercise Minutes: {exercise_minutes}
    Stress Level: {stress_level}

    Include:
    - Daily exercise
    - Sleep goals
    - Hydration goals
    - Stress management tips

    Format day by day.
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=plan_prompt
        )

        st.write(response.text)

    except Exception as e:
        st.error(f"Error: {e}")

# -----------------------------
# AI CHAT WITH MEMORY
# -----------------------------

st.subheader("📅 Personalized 7-Day Wellness Plan")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = ""

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

        Previous Conversation:
        {st.session_state.conversation_context}

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

        st.session_state.conversation_context += f"""

User: {user_input}

Assistant: {answer}
"""

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