import streamlit as st
import pandas as pd
from joblib import load

# =======================
# Page Config
# =======================
st.set_page_config(
    page_title="Liver Cancer Risk Assessment",
    # page_icon="🧬",
    layout="wide"
)

# =======================
# DARK UI + VISIBILITY FIX
# =======================
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top right, rgba(255,255,255,0.25), transparent 45%),
            linear-gradient(135deg, #000000, #081a33, #000000);
        background-attachment: fixed;
    }

    .card {
        background: rgba(8, 16, 32, 0.97);
        padding: 28px;
        border-radius: 18px;
        border: 1px solid rgba(120,180,255,0.35);
        box-shadow: 0 0 22px rgba(0,140,255,0.35);
        margin-bottom: 22px;
    }

    .main-title {
        font-size: 42px;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
    }

    .subtitle {
        text-align: center;
        color: #dbe9ff;
        font-size: 16px;
    }

    .section-title {
        color: #ffffff !important;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 14px;
    }

    label {
        color: #ffffff !important;
        font-weight: 600;
    }

    /* Predict Button — BLACK with WHITE border */
    .stButton>button {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-weight: 800;
        border-radius: 16px;
        padding: 16px 36px;
        font-size: 20px;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 25px rgba(255,255,255,0.35);
    }

    .stButton>button:hover {
        background-color: #000000 !important;
        box-shadow: 0 0 35px rgba(255,255,255,0.7);
        transform: scale(1.04);
    }

    /* Result text visibility */
    .result-text {
        color: #ffffff;
        font-size: 18px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =======================
# Load Model
# =======================
model = load("liver_cancer_model.joblib")

# =======================
# Header
# =======================
st.markdown(
    """
    <div class="card">
        <div class="main-title">Liver Cancer Risk Assessment</div>
        # <div class="subtitle">AI-powered clinical decision support system</div>
    </div>
    """,
    unsafe_allow_html=True
)

# =======================
# Input Layout
# =======================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Patient Information</div>', unsafe_allow_html=True)

    age = st.number_input("Age", 1, 100, 30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    bmi = st.number_input("Body Mass Index (BMI)", 10.0, 50.0, 22.0)
    physical_activity = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
    smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
    alcohol = st.selectbox("Alcohol Consumption", ["Never", "Occasional", "Regular"])

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Medical Information</div>', unsafe_allow_html=True)

    afp = st.number_input("Alpha Fetoprotein (AFP)", 0.0, 2000.0, 10.0)
    hepatitis_b = st.selectbox("Hepatitis B", [0, 1])
    hepatitis_c = st.selectbox("Hepatitis C", [0, 1])
    cirrhosis = st.selectbox("Cirrhosis History", [0, 1])
    diabetes = st.selectbox("Diabetes", [0, 1])
    family_history = st.selectbox("Family History of Cancer", [0, 1])

    st.markdown('</div>', unsafe_allow_html=True)

# =======================
# CENTER Predict Button (NO EXTRA BOX)
# =======================
st.markdown("<br>", unsafe_allow_html=True)
predict_col = st.columns([3, 2, 3])[1]
with predict_col:
    predict = st.button("Predict Risk", use_container_width=True)

# =======================
# Prepare Input
# =======================
user_input = {
    "age": age,
    "bmi": bmi,
    "alpha_fetoprotein_level": afp,
    "physical_activity_level": physical_activity,
    "gender": gender,
    "alcohol_consumption": alcohol,
    "smoking_status": smoking,
    "hepatitis_b": hepatitis_b,
    "hepatitis_c": hepatitis_c,
    "cirrhosis_history": cirrhosis,
    "diabetes": diabetes,
    "family_history_cancer": family_history
}

input_data = pd.DataFrame(
    {col: [user_input.get(col, 0)] for col in model.feature_names_in_}
)

# =======================
# RESULT — FULLY VISIBLE
# =======================
if predict:
    prob = model.predict_proba(input_data)[0][1]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Prediction Result</div>', unsafe_allow_html=True)

    st.markdown(f"<div class='result-text'>Risk Probability: <b>{prob:.2f}</b></div>", unsafe_allow_html=True)

    if prob >= 0.4:
        st.error("⚠️ High Risk of Liver Cancer")

        st.markdown("### 🛡️ Safety Measures")
        st.markdown("""
        - Stop alcohol immediately  
        - Quit smoking and tobacco  
        - Regular liver screening  
        - Consult a hepatologist  
        """)

        st.markdown("### 💡 Lifestyle Tips")
        st.markdown("""
        - Follow liver-friendly diet  
        - Exercise daily  
        - Maintain healthy BMI  
        - Manage diabetes properly  
        """)

    else:
        st.success("✅ Low Risk of Liver Cancer")

        st.markdown("### 💡 Preventive Tips")
        st.markdown("""
        - Maintain healthy lifestyle  
        - Avoid excessive alcohol  
        - Periodic health checkups  
        """)

    st.markdown('</div>', unsafe_allow_html=True)

# =======================
# Disclaimer
# =======================
st.warning("⚠️ This application is for educational purposes only and not a medical diagnosis.")
