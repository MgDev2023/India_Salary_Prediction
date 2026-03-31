import streamlit as st
import pickle
import numpy as np
import os
import subprocess
import sys

MODEL_PATH   = "model/salary_model.pkl"
ENCODER_PATH = "model/encoders.pkl"

st.set_page_config(
    page_title="India Salary Predictor",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .salary-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
    }
    .salary-amount  { font-size: 3rem; font-weight: 800; color: #00d4aa; letter-spacing: -1px; }
    .salary-monthly { font-size: 1.2rem; color: #a0aec0; margin-top: 0.3rem; }
    .salary-range   { font-size: 0.95rem; color: #63b3ed; margin-top: 0.5rem; }
    .salary-label   { font-size: 1rem; color: #e2e8f0; margin-bottom: 0.5rem; opacity: 0.8; }
    .section-header {
        font-size: 1.1rem; font-weight: 700; color: #2d3748;
        padding: 0.4rem 0; border-bottom: 2px solid #e2e8f0; margin-bottom: 1rem;
    }
    div[data-testid="metric-container"] {
        background: #f7fafc; border: 1px solid #e2e8f0;
        border-radius: 10px; padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    needs_train = not os.path.exists(MODEL_PATH)
    if not needs_train:
        try:
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
            with open(ENCODER_PATH, "rb") as f:
                encoders = pickle.load(f)
            return model, encoders
        except Exception:
            needs_train = True
    if needs_train:
        with st.spinner("Setting up model — please wait (~1 min)..."):
            subprocess.run([sys.executable, "train_model.py"], check=True)
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(ENCODER_PATH, "rb") as f:
        encoders = pickle.load(f)
    return model, encoders


def make_prediction(model, encoders, job_title, education, location,
                    industry, company_type, years_exp, age, skill_values):
    all_skills      = encoders["all_skills"]
    role_skills     = encoders["role_skills"]
    skills_for_role = role_skills[job_title]
    job_enc = encoders["job"].transform([job_title])[0]
    edu_enc = encoders["edu"].transform([education])[0]
    loc_enc = encoders["loc"].transform([location])[0]
    ind_enc = encoders["ind"].transform([industry])[0]
    com_enc = encoders["com"].transform([company_type])[0]
    skill_vector  = [skill_values.get(s, 0) for s in all_skills]
    avg_skill_pct = sum(skill_values.values()) / len(skills_for_role)
    exp_x_skill   = years_exp * avg_skill_pct
    X = np.array([[job_enc, edu_enc, loc_enc, years_exp, age,
                   ind_enc, com_enc, avg_skill_pct, exp_x_skill] + skill_vector])
    return model.predict(X)[0]


# ── Load ──────────────────────────────────────────────────────────────────────
model, encoders = load_model()
le_job                 = encoders["job"]
le_edu                 = encoders["edu"]
le_loc                 = encoders["loc"]
le_ind                 = encoders["ind"]
le_com                 = encoders["com"]
role_skills            = encoders["role_skills"]
all_skills             = encoders["all_skills"]
skill_max_bonus        = encoders["skill_max_bonus"]
industry_company_bonus = encoders["industry_company_bonus"]

# ── Page ──────────────────────────────────────────────────────────────────────
st.markdown("## 💼 India Salary Predictor")
st.markdown("##### Predict your expected CTC — 2025-26 India Market Data")
st.markdown("---")

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="section-header">👤 Your Profile</div>', unsafe_allow_html=True)
    job_title = st.selectbox("Job Role", sorted(le_job.classes_))
    skills_for_role = role_skills[job_title]

    c1, c2 = st.columns(2)
    with c1:
        education = st.selectbox("Education", sorted(le_edu.classes_))
        location  = st.selectbox("State",     sorted(le_loc.classes_))
    with c2:
        years_exp = st.slider("Experience (yrs)", 0, 25, 0)
        age       = st.slider("Age", 21, 60, 22)

    st.markdown("")
    st.markdown('<div class="section-header">🏢 Company & Industry</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        industry = st.selectbox("Industry", sorted(le_ind.classes_))
    with c4:
        company_type = st.selectbox("Company Type", sorted(le_com.classes_))
    combo_bonus = industry_company_bonus[industry][company_type]
    st.caption(f"💰 **{company_type}** in **{industry}** → +₹{combo_bonus:,} salary premium")

    st.markdown("")
    st.markdown(f'<div class="section-header">🧠 Skill Knowledge — {job_title}</div>',
                unsafe_allow_html=True)
    st.caption("0 = no knowledge · 100 = expert")

    skill_values = {}
    sc1, sc2 = st.columns(2)
    for idx, skill in enumerate(skills_for_role):
        with (sc1 if idx % 2 == 0 else sc2):
            pct = st.slider(skill, 0, 100, 0, step=5,
                            help=f"Max salary boost at 100%: ₹{skill_max_bonus[skill]:,}")
            skill_values[skill] = pct

    st.markdown("")
    predict_btn = st.button("🔍 Predict My Salary", use_container_width=True, type="primary")

with right:
    st.markdown('<div class="section-header">📊 Prediction Result</div>', unsafe_allow_html=True)

    if not predict_btn:
        st.info("👈 Fill in your profile on the left and click **Predict My Salary**.")
        st.markdown("**After predicting, explore more in the sidebar:**")
        st.markdown("- 🧠 **Skill Analysis** — breakdown & what to improve")
        st.markdown("- 📈 **Growth & Insights** — salary projection & feature weightage")
    else:
        total_knowledge = sum(skill_values.values())
        avg_knowledge   = total_knowledge / len(skills_for_role)

        if total_knowledge == 0:
            st.error(f"❌ You cannot get a job as **{job_title}** with 0% knowledge in all skills.")
            st.markdown("**Skills you need to start learning:**")
            for skill in skills_for_role:
                st.markdown(f"- **{skill}** — up to ₹{skill_max_bonus[skill]:,} salary impact")
            st.info("💡 Gain at least 20–30% in 2–3 core skills to become hireable.")
            st.stop()

        if avg_knowledge < 20:
            st.warning(
                f"⚠️ Average skill level is only **{avg_knowledge:.0f}%**. "
                "Most employers expect 30–40% in core skills."
            )

        prediction = make_prediction(model, encoders, job_title, education, location,
                                     industry, company_type, years_exp, age, skill_values)
        low     = prediction * 0.90
        high    = prediction * 1.10
        monthly = prediction / 12

        # Save to session state for other pages
        st.session_state.prediction    = prediction
        st.session_state.skill_values  = skill_values
        st.session_state.skills_for_role = skills_for_role
        st.session_state.job_title     = job_title
        st.session_state.education     = education
        st.session_state.location      = location
        st.session_state.industry      = industry
        st.session_state.company_type  = company_type
        st.session_state.years_exp     = years_exp
        st.session_state.age           = age
        st.session_state.avg_knowledge = avg_knowledge

        st.markdown(f"""
        <div class="salary-card">
            <div class="salary-label">{job_title} · {location} · {company_type}</div>
            <div class="salary-amount">₹{prediction:,.0f}</div>
            <div class="salary-monthly">≈ ₹{monthly:,.0f} / month</div>
            <div class="salary-range">Typical range: ₹{low:,.0f} – ₹{high:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Annual CTC",  f"₹{prediction/100000:.1f}L")
        m2.metric("Monthly",     f"₹{monthly/1000:.0f}K")
        m3.metric("Avg Skill",   f"{avg_knowledge:.0f}%",
                  delta="Good" if avg_knowledge >= 60 else ("Fair" if avg_knowledge >= 35 else "Low"))

        st.success("✅ Prediction complete! Navigate to **Skill Analysis** or **Growth & Insights** in the sidebar for more details.")

st.markdown("---")
st.caption("Built with Streamlit · GradientBoosting Regression · Sklearn · 2025-26 India Market Data")
