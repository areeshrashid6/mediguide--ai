import streamlit as st

st.set_page_config(
    page_title="MediGuide AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Shared styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: linear-gradient(180deg, #f7f8fc 0%, #f3f5fb 100%);
}
.block-container {
    max-width: 1100px;
    padding-top: 34px;
    padding-bottom: 60px;
}
.hero {
    background: linear-gradient(135deg, #6757f5 0%, #4d9df8 100%);
    color: white;
    border-radius: 24px;
    padding: 34px 38px;
    box-shadow: 0 18px 45px rgba(91, 92, 220, .20);
    margin-bottom: 28px;
}
.hero .small { opacity: .85; font-size: 14px; margin-bottom: 5px; }
.hero h1 { margin: 0; font-size: 34px; font-weight: 800; letter-spacing: -.7px; }
.hero p { margin: 9px 0 0; opacity: .9; font-size: 15px; }
.badge {
    display:inline-block; padding:7px 12px; border-radius:999px;
    background:rgba(255,255,255,.16); font-size:12px; font-weight:600;
    margin-bottom:14px;
}
.card {
    background:#fff; border:1px solid #e9eaf2; border-radius:20px;
    padding:26px; box-shadow:0 8px 25px rgba(35,38,60,.045);
    margin-bottom:18px;
}
.step {
    display:flex; align-items:center; gap:12px; margin-bottom:22px;
}
.stepnum {
    width:36px; height:36px; border-radius:50%; display:flex;
    align-items:center; justify-content:center; color:white; font-weight:800;
    background:linear-gradient(135deg,#6757f5,#4d9df8);
}
.steptitle { font-size:19px; font-weight:800; color:#24263a; }
.stepsub { color:#8b8ea3; font-size:13px; margin-top:2px; }
.info {
    background:#f3f0ff; border:1px solid #ddd6ff; color:#514b70;
    border-radius:14px; padding:13px 15px; font-size:13px; margin:15px 0 20px;
}
.security {
    text-align:center; color:#8b8ea3; font-size:12px; margin-top:14px;
}
div.stButton > button, div.stFormSubmitButton > button {
    border:0; border-radius:12px; min-height:46px; font-weight:700;
    background:linear-gradient(135deg,#6757f5,#4d9df8); color:white;
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {
    color:white; opacity:.92;
}
.back-btn button {
    background:white !important; color:#4f5062 !important;
    border:1px solid #e3e4ed !important;
}
.result {
    background:white; border:1px solid #e9eaf2; border-radius:20px;
    padding:26px; line-height:1.7; box-shadow:0 8px 25px rgba(35,38,60,.05);
}
</style>
""", unsafe_allow_html=True)

def header():
    st.markdown("""
    <div class="hero">
      <div class="badge">🔒 Secure · Private · AI-Powered</div>
      <div class="small">Welcome to</div>
      <h1>MediGuide AI ✨</h1>
      <p>Get clear, educational health guidance from your symptoms in a simple two-step process.</p>
    </div>
    """, unsafe_allow_html=True)

header()

# Session state
if "page" not in st.session_state:
    st.session_state.page = 1
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "settings" not in st.session_state:
    st.session_state.settings = {
        "model": "gpt-4o-mini",
        "temperature": 0.3,
        "language": "English",
    }

# ---------- STEP 1: API KEY ----------
if st.session_state.page == 1:
    st.markdown("""
    <div class="card">
      <div class="step">
        <div class="stepnum">1</div>
        <div>
          <div class="steptitle">Connect your AI</div>
          <div class="stepsub">Enter your OpenAI API key to continue</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.15, .85], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🔑 OpenAI API Key")
        st.caption("Your key is used for this session only.")
        api_key = st.text_input(
            "API key",
            value=st.session_state.api_key,
            type="password",
            placeholder="sk-...",
            label_visibility="collapsed",
        )

        st.markdown("""
        <div class="info">
        🛡️ <b>Your privacy matters.</b><br>
        The key is kept in the current Streamlit session and is not written to a file or database by this app.
        </div>
        """, unsafe_allow_html=True)

        if st.button("Continue to health information  →", use_container_width=True):
            if not api_key.strip():
                st.error("Please enter your OpenAI API key.")
            elif not api_key.startswith("sk-"):
                st.warning("This doesn't look like a standard OpenAI API key. You can still continue if it is valid.")
                st.session_state.api_key = api_key.strip()
                st.session_state.page = 2
                st.rerun()
            else:
                st.session_state.api_key = api_key.strip()
                st.session_state.page = 2
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ✨ How it works")
        st.markdown("""
        **01 — Connect**  
        Add your OpenAI API key.

        **02 — Tell us**  
        Enter basic information and symptoms.

        **03 — Get guidance**  
        MediGuide creates educational guidance using the AI model.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="security">🔐 Session-only • No local key storage</div>', unsafe_allow_html=True)

# ---------- STEP 2: HEALTH INFORMATION ----------
elif st.session_state.page == 2:
    st.markdown("""
    <div class="card">
      <div class="step">
        <div class="stepnum">2</div>
        <div>
          <div class="steptitle">Tell us how you're feeling</div>
          <div class="stepsub">Provide some basic information and symptoms</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("health_form"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 👤 Basic information")
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age", min_value=0, max_value=120, value=29, step=1)
        with c2:
            gender = st.selectbox("Gender", ["Select gender", "Male", "Female", "Other", "Prefer not to say"])
        with c3:
            duration = st.selectbox(
                "Duration of symptoms",
                ["Select duration", "Less than a day", "1-3 days", "4-7 days", "1-2 weeks", "More than 2 weeks"]
            )

        st.markdown("---")
        st.markdown("#### ❤️ Health details")
        severity = st.slider("Severity (1 = mild, 10 = worst)", 1, 10, 5)

        c4, c5 = st.columns(2)
        with c4:
            conditions = st.text_area(
                "Existing medical conditions",
                placeholder="e.g. Asthma, diabetes, or None",
                height=100
            )
        with c5:
            medications = st.text_area(
                "Current medications",
                placeholder="e.g. Metformin, or None",
                height=100
            )

        st.markdown("---")
        st.markdown("#### 🩹 Symptoms")
        common_symptoms = st.multiselect(
            "Select symptoms",
            [
                "Fever", "Cough", "Headache", "Sore throat", "Fatigue",
                "Nausea", "Shortness of breath", "Muscle aches", "Chills",
                "Loss of appetite", "Dizziness", "Rash"
            ],
            placeholder="Choose from common symptoms"
        )
        other_symptoms = st.text_input(
            "Other symptoms (optional)",
            placeholder="Describe any other symptoms"
        )
        additional_notes = st.text_area(
            "Additional notes (optional)",
            placeholder="Anything else you'd like to mention?",
            height=90
        )

        st.markdown("---")
        st.markdown("#### ⚙️ AI preferences")
        s1, s2, s3 = st.columns(3)
        with s1:
            model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], index=0)
        with s2:
            temperature = st.slider("Creativity", 0.0, 1.0, .3, .1)
        with s3:
            language = st.selectbox("Answer language", ["English", "Urdu", "Spanish", "French", "German", "Arabic"])

        st.markdown("""
        <div class="info">
        ⚠️ <b>Important:</b> MediGuide AI provides educational information only.
        It does not diagnose conditions or replace a qualified healthcare professional.
        </div>
        """, unsafe_allow_html=True)

        submitted = st.form_submit_button("✨ Get Health Guidance", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    b1, b2 = st.columns([1, 1])
    with b1:
        if st.button("← Back to API key", use_container_width=True):
            st.session_state.page = 1
            st.rerun()

    if submitted:
        if gender == "Select gender" or duration == "Select duration":
            st.warning("Please select your gender and symptom duration.")
        elif not common_symptoms and not other_symptoms.strip():
            st.warning("Please provide at least one symptom.")
        else:
            from openai import OpenAI

            prompt = f"""
You are MediGuide AI, an educational health-information assistant.

User information:
Age: {age}
Gender: {gender}
Symptom duration: {duration}
Severity: {severity}/10
Existing medical conditions: {conditions or 'None'}
Current medications: {medications or 'None'}
Symptoms: {', '.join(common_symptoms) if common_symptoms else 'None selected'}
Other symptoms: {other_symptoms or 'None'}
Additional notes: {additional_notes or 'None'}

Provide general educational health guidance in {language}.
Do not claim to diagnose the user. Explain possible general considerations,
safe next steps, warning signs that warrant urgent medical attention, and
when contacting a healthcare professional would be appropriate.
Keep the answer clear and easy to understand.
"""

            try:
                client = OpenAI(api_key=st.session_state.api_key)
                with st.spinner("Analyzing your information..."):
                    response = client.chat.completions.create(
                        model=model,
                        temperature=temperature,
                        messages=[
                            {
                                "role": "system",
                                "content": "You provide cautious, educational health information and never present it as a medical diagnosis."
                            },
                            {"role": "user", "content": prompt},
                        ],
                    )
                guidance = response.choices[0].message.content
                st.session_state.guidance = guidance
                st.session_state.submitted_details = {
                    "Age": age,
                    "Gender": gender,
                    "Duration": duration,
                    "Severity": f"{severity}/10",
                    "Symptoms": ", ".join(common_symptoms) or "None",
                    "Other symptoms": other_symptoms or "None",
                }
                st.success("Your AI-generated guidance is ready.")

            except Exception as e:
                st.error(f"Unable to contact OpenAI: {e}")

    if "guidance" in st.session_state:
        st.markdown("### 🩺 Your health guidance")
        st.markdown(f'<div class="result">{st.session_state.guidance}</div>', unsafe_allow_html=True)
        with st.expander("View submitted details"):
            st.json(st.session_state.get("submitted_details", {}))
