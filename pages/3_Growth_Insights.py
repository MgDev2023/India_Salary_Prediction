import streamlit as st
import pickle
import numpy as np
import os
import subprocess
import sys

MODEL_PATH   = "model/salary_model.pkl"
ENCODER_PATH = "model/encoders.pkl"

st.set_page_config(
    page_title="Growth & Insights",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
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


model, encoders = load_model()

st.markdown("## 📈 Growth & Insights")
st.markdown("##### Your salary trajectory and what drives your pay")
st.markdown("---")

# ── Guard ─────────────────────────────────────────────────────────────────────
if "prediction" not in st.session_state:
    st.warning("⚠️ No prediction found. Please go to **💼 Home** and predict your salary first.")
    st.stop()

prediction   = st.session_state.prediction
skill_values = st.session_state.skill_values
job_title    = st.session_state.job_title
education    = st.session_state.education
location     = st.session_state.location
industry     = st.session_state.industry
company_type = st.session_state.company_type
years_exp    = st.session_state.years_exp
age          = st.session_state.age
avg_knowledge = st.session_state.avg_knowledge

st.markdown(f"**Role:** {job_title} &nbsp;|&nbsp; **Predicted CTC:** ₹{prediction:,.0f} &nbsp;|&nbsp; **Experience:** {years_exp} yrs")
st.markdown("---")

left, right = st.columns([1, 1], gap="large")

# ── Left: Salary growth projection ───────────────────────────────────────────
with left:
    st.markdown('<div class="section-header">📈 Salary Growth Projection</div>',
                unsafe_allow_html=True)
    st.caption("Assumes same skills, role, and company — only experience increases")

    milestones = [0, 2, 5, 8, 12, 18, 25]
    growth_data = {}
    for yr in milestones:
        if yr >= years_exp:
            p = make_prediction(model, encoders, job_title, education, location,
                                industry, company_type, yr, 21 + yr, skill_values)
            growth_data[yr] = p

    # Metrics row
    cols = st.columns(len(growth_data))
    for i, (yr, sal) in enumerate(growth_data.items()):
        label = "Now" if yr == years_exp else f"{yr} yrs"
        delta = f"+₹{(sal - prediction)/100000:.1f}L" if yr > years_exp else None
        cols[i].metric(label, f"₹{sal/100000:.1f}L", delta=delta)

    st.markdown("")

    # Table view
    st.markdown('<div class="section-header">📋 Detailed Growth Table</div>',
                unsafe_allow_html=True)

    for yr, sal in growth_data.items():
        gain    = sal - prediction
        monthly = sal / 12
        label   = "← You are here" if yr == years_exp else ""
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            c1.metric(f"{yr} Years Exp {label}", f"₹{sal/100000:.1f}L")
            c2.metric("Monthly",                 f"₹{monthly/1000:.0f}K")
            c3.metric("Growth from now",
                      f"+₹{gain/100000:.1f}L" if gain > 0 else "—",
                      delta=f"+{(gain/prediction*100):.0f}%" if gain > 0 else None)

    st.markdown("")
    st.info(
        f"💡 At your current skill level ({avg_knowledge:.0f}%), "
        f"your salary will grow from **₹{prediction/100000:.1f}L → "
        f"₹{list(growth_data.values())[-1]/100000:.1f}L** over your career."
    )

# ── Right: Feature importance (weightage) ────────────────────────────────────
with right:
    st.markdown('<div class="section-header">⚙️ What Drives Your Salary (Feature Weightage)</div>',
                unsafe_allow_html=True)
    st.caption("How much each factor contributes to salary predictions overall")

    feat_importance  = model.feature_importances_
    base_feat_names  = [
        "Job Role", "Education", "Location", "Experience",
        "Age", "Industry", "Company Type", "Avg Skill Level", "Experience × Skill"
    ]
    skill_feat_names = list(encoders["all_skills"])
    all_feat_names   = base_feat_names + skill_feat_names
    importance_pct   = feat_importance / feat_importance.sum() * 100

    top_pairs = sorted(zip(all_feat_names, importance_pct), key=lambda x: -x[1])[:12]

    for feat, imp in top_pairs:
        st.progress(int(imp), text=f"**{feat}**: {imp:.1f}%")

    st.markdown("")
    st.markdown('<div class="section-header">🏆 Top 3 Salary Drivers for You</div>',
                unsafe_allow_html=True)

    top3 = top_pairs[:3]
    for rank, (feat, imp) in enumerate(top3, 1):
        medal = ["🥇", "🥈", "🥉"][rank - 1]
        with st.container(border=True):
            st.markdown(f"{medal} **{feat}** — {imp:.1f}% importance")
            if feat == "Experience × Skill":
                st.caption("Your years of experience combined with your skill level — the most powerful salary driver")
            elif feat == "Experience":
                st.caption("Raw years in the industry — grows steadily over time")
            elif feat == "Avg Skill Level":
                st.caption("Your overall knowledge across all required skills")
            elif feat == "Job Role":
                st.caption("The role you're in sets your salary ceiling")
            elif feat == "Company Type":
                st.caption("MNC vs Startup vs IT Giant makes a large difference")
            elif feat == "Industry":
                st.caption("Which industry you work in strongly affects pay")
            else:
                st.caption(f"This factor contributes {imp:.1f}% to salary determination")

    st.markdown("")
    st.markdown('<div class="section-header">📊 Category Breakdown</div>',
                unsafe_allow_html=True)

    base_imp  = sum(imp for feat, imp in zip(all_feat_names, importance_pct)
                    if feat in base_feat_names)
    skill_imp = sum(imp for feat, imp in zip(all_feat_names, importance_pct)
                    if feat not in base_feat_names)

    bc1, bc2 = st.columns(2)
    bc1.metric("Profile & Company Factors", f"{base_imp:.1f}%",
               help="Job role, experience, education, location, industry, company type")
    bc2.metric("Skill Knowledge Factors",   f"{skill_imp:.1f}%",
               help="Your knowledge level across all role-specific skills")

st.markdown("---")
st.caption("Built with Streamlit · GradientBoosting Regression · Sklearn · 2025-26 India Market Data")
