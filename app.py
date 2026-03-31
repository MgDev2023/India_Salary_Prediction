import streamlit as st
import pickle
import numpy as np
import os
import subprocess
import sys

MODEL_PATH   = "model/salary_model.pkl"
ENCODER_PATH = "model/encoders.pkl"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Salary Predictor",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { padding-top: 1rem; }
    .salary-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
    }
    .salary-amount {
        font-size: 3rem;
        font-weight: 800;
        color: #00d4aa;
        letter-spacing: -1px;
    }
    .salary-monthly {
        font-size: 1.2rem;
        color: #a0aec0;
        margin-top: 0.3rem;
    }
    .salary-range {
        font-size: 0.95rem;
        color: #63b3ed;
        margin-top: 0.5rem;
    }
    .salary-label {
        font-size: 1rem;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2d3748;
        padding: 0.4rem 0;
        border-bottom: 2px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    .skill-tag-green {
        display: inline-block;
        background: #c6f6d5;
        color: #276749;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 2px;
    }
    .skill-tag-yellow {
        display: inline-block;
        background: #fefcbf;
        color: #744210;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 2px;
    }
    .skill-tag-red {
        display: inline-block;
        background: #fed7d7;
        color: #742a2a;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 2px;
    }
    .growth-card {
        background: #f7fafc;
        border-left: 4px solid #4299e1;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.4rem 0;
    }
    .stProgress > div > div > div { border-radius: 10px; }
    div[data-testid="metric-container"] {
        background: #f7fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def load_model():
    if not os.path.exists(MODEL_PATH):
        with st.spinner("Training model for the first time — please wait..."):
            subprocess.run([sys.executable, "train_model.py"], check=True)
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(ENCODER_PATH, "rb") as f:
        encoders = pickle.load(f)
    return model, encoders


def make_prediction(model, encoders, job_title, education, location, industry,
                    company_type, years_exp, age, skill_values):
    all_skills  = encoders["all_skills"]
    role_skills = encoders["role_skills"]
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


# ── Load model ────────────────────────────────────────────────────────────────
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

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 💼 India Salary Predictor")
st.markdown("##### Predict your expected CTC based on role, skills, experience & market — 2025-26 data")
st.markdown("---")

# ── Layout: Left inputs | Right results ───────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

with left:
    # ── Section 1: Role & Profile ─────────────────────────────────────────────
    st.markdown('<div class="section-header">👤 Your Profile</div>', unsafe_allow_html=True)

    job_title    = st.selectbox("Job Role", sorted(le_job.classes_))
    skills_for_role = role_skills[job_title]

    c1, c2 = st.columns(2)
    with c1:
        education = st.selectbox("Education", sorted(le_edu.classes_))
        location  = st.selectbox("State", sorted(le_loc.classes_))
    with c2:
        years_exp = st.slider("Experience (yrs)", 0, 25, 0)
        age       = st.slider("Age", 21, 60, 22)

    st.markdown("")

    # ── Section 2: Company ────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🏢 Company & Industry</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        industry = st.selectbox("Industry", sorted(le_ind.classes_))
    with c4:
        company_type = st.selectbox("Company Type", sorted(le_com.classes_))

    combo_bonus = industry_company_bonus[industry][company_type]
    st.caption(f"💰 **{company_type}** in **{industry}** → +₹{combo_bonus:,} salary premium")

    st.markdown("")

    # ── Section 3: Skills ─────────────────────────────────────────────────────
    st.markdown(f'<div class="section-header">🧠 Skill Knowledge — {job_title}</div>',
                unsafe_allow_html=True)
    st.caption("Drag each slider to your honest knowledge level. 0 = no knowledge · 100 = expert")

    skill_values = {}
    sc1, sc2 = st.columns(2)
    for idx, skill in enumerate(skills_for_role):
        col = sc1 if idx % 2 == 0 else sc2
        with col:
            pct = st.slider(
                skill, 0, 100, 0, step=5,
                help=f"Max salary boost at 100%: ₹{skill_max_bonus[skill]:,}"
            )
            skill_values[skill] = pct

    st.markdown("")
    predict_btn = st.button("🔍 Predict My Salary", use_container_width=True, type="primary")


# ── Right panel: Results ──────────────────────────────────────────────────────
with right:
    st.markdown('<div class="section-header">📊 Prediction Results</div>', unsafe_allow_html=True)

    if not predict_btn:
        st.info("👈 Fill in your profile and click **Predict My Salary** to see results.")

    else:
        total_knowledge = sum(skill_values.values())
        avg_knowledge   = total_knowledge / len(skills_for_role)

        # ── Block: zero skills ────────────────────────────────────────────────
        if total_knowledge == 0:
            st.error(f"❌ You cannot get a job as **{job_title}** with 0% knowledge in all skills.")
            st.markdown("**Skills you need to start learning:**")
            for skill in skills_for_role:
                st.markdown(f"- **{skill}** — up to ₹{skill_max_bonus[skill]:,} salary impact")
            st.info("💡 Gain at least 20–30% in 2–3 core skills to become hireable.")
            st.stop()

        # ── Warn: very low skills ─────────────────────────────────────────────
        if avg_knowledge < 20:
            st.warning(
                f"⚠️ Average skill level is only **{avg_knowledge:.0f}%**. "
                "Most employers expect 30–40% in core skills. Getting hired will be hard."
            )

        # ── Predict ───────────────────────────────────────────────────────────
        prediction = make_prediction(model, encoders, job_title, education, location,
                                     industry, company_type, years_exp, 25, skill_values)
        low  = prediction * 0.90
        high = prediction * 1.10
        monthly = prediction / 12

        # ── Salary card ───────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="salary-card">
            <div class="salary-label">{job_title} · {location} · {company_type}</div>
            <div class="salary-amount">₹{prediction:,.0f}</div>
            <div class="salary-monthly">≈ ₹{monthly:,.0f} / month</div>
            <div class="salary-range">Typical range: ₹{low:,.0f} – ₹{high:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Quick metrics ─────────────────────────────────────────────────────
        m1, m2, m3 = st.columns(3)
        m1.metric("Annual CTC", f"₹{prediction/100000:.1f}L")
        m2.metric("Monthly", f"₹{monthly/1000:.0f}K")
        m3.metric("Avg Skill", f"{avg_knowledge:.0f}%",
                  delta="Good" if avg_knowledge >= 60 else ("Fair" if avg_knowledge >= 35 else "Low"))

        # ── Skill breakdown ───────────────────────────────────────────────────
        st.markdown("")
        st.markdown('<div class="section-header">🧠 Your Skill Breakdown</div>', unsafe_allow_html=True)

        for skill in skills_for_role:
            pct    = skill_values[skill]
            impact = (pct / 100) * skill_max_bonus[skill]
            if pct == 0:
                level, color = "Not learned", "🔴"
            elif pct < 30:
                level, color = "Beginner", "🟡"
            elif pct < 70:
                level, color = "Intermediate", "🟠"
            else:
                level, color = "Expert", "🟢"
            bar_val = max(pct, 1)
            st.progress(bar_val, text=f"{color} **{skill}** — {pct}% ({level})  |  +₹{impact:,.0f} salary impact")

        # ── What to learn next ────────────────────────────────────────────────
        weak_skills = [(s, skill_max_bonus[s]) for s in skills_for_role if skill_values[s] < 50]
        if weak_skills:
            weak_skills.sort(key=lambda x: -x[1])
            st.markdown("")
            st.markdown('<div class="section-header">📚 Skills to Improve for Higher Pay</div>',
                        unsafe_allow_html=True)
            for skill, bonus in weak_skills[:3]:
                current_pct    = skill_values[skill]
                current_impact = (current_pct / 100) * bonus
                gain_at_80     = (0.8 * bonus) - current_impact
                gain_at_100    = bonus - current_impact
                with st.container(border=True):
                    sc_a, sc_b = st.columns([2, 1])
                    with sc_a:
                        st.markdown(f"**{skill}**")
                        st.caption(f"Current level: {current_pct}%  →  Target: 80%")
                        st.progress(max(current_pct, 1), text=f"{current_pct}% now")
                    with sc_b:
                        st.metric(
                            label="Salary gain at 80%",
                            value=f"+₹{gain_at_80:,.0f}",
                            help=f"Reaching 100% adds ₹{gain_at_100:,.0f}"
                        )

        # ── Salary growth projection ──────────────────────────────────────────
        st.markdown("")
        st.markdown('<div class="section-header">📈 Your Salary Growth Projection</div>',
                    unsafe_allow_html=True)
        st.caption("Assumes same skills & company type, growing experience over time")

        growth_data = {}
        for yr in [0, 2, 5, 8, 12, 18]:
            if yr >= years_exp:
                p = make_prediction(model, encoders, job_title, education, location,
                                    industry, company_type, yr, 21 + yr, skill_values)
                growth_data[yr] = p

        gcols = st.columns(len(growth_data))
        for i, (yr, sal) in enumerate(growth_data.items()):
            label = "Now" if yr == years_exp else f"{yr} yrs"
            delta = f"+₹{(sal - prediction)/100000:.1f}L" if yr > years_exp else None
            gcols[i].metric(label, f"₹{sal/100000:.1f}L", delta=delta)

        # ── Feature importance (user-friendly) ───────────────────────────────
        st.markdown("")
        st.markdown('<div class="section-header">⚙️ What Drives Your Salary</div>',
                    unsafe_allow_html=True)
        feat_importance  = model.feature_importances_
        base_feat_names  = ["Job Role", "Education", "Location", "Experience",
                            "Age", "Industry", "Company Type", "Avg Skill", "Exp × Skill"]
        skill_feat_names = [f"{s}" for s in all_skills]
        all_feat_names   = base_feat_names + skill_feat_names
        importance_pct   = feat_importance / feat_importance.sum() * 100

        top_pairs = sorted(zip(all_feat_names, importance_pct), key=lambda x: -x[1])[:8]
        for feat, imp in top_pairs:
            st.progress(int(imp), text=f"**{feat}**: {imp:.1f}%")


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with Streamlit · GradientBoosting Regression · Sklearn · 2025-26 India Market Data")
