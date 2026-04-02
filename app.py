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

st.markdown("""
<style>
    /* ── Hide Skill Analysis & Growth Insights from sidebar ── */
    [data-testid="stSidebarNav"] li:nth-child(2),
    [data-testid="stSidebarNav"] li:nth-child(3) {
        display: none !important;
    }

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
le_job                 = encoders["job"]
le_edu                 = encoders["edu"]
le_loc                 = encoders["loc"]
le_ind                 = encoders["ind"]
le_com                 = encoders["com"]
role_skills            = encoders["role_skills"]
all_skills             = encoders["all_skills"]
skill_max_bonus        = encoders["skill_max_bonus"]
industry_company_bonus = encoders["industry_company_bonus"]

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("## 💼 India Salary Predictor")
st.markdown("##### Predict your expected CTC — 2025-26 India Market Data")
st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_pred, tab_skill, tab_growth = st.tabs(
    ["💼 Salary Predictor", "🧠 Skill Analysis", "📈 Growth & Insights"]
)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — SALARY PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
with tab_pred:
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
            st.markdown("**After predicting, explore more using the tabs above:**")
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

            st.session_state.prediction      = prediction
            st.session_state.skill_values    = skill_values
            st.session_state.skills_for_role = skills_for_role
            st.session_state.job_title       = job_title
            st.session_state.education       = education
            st.session_state.location        = location
            st.session_state.industry        = industry
            st.session_state.company_type    = company_type
            st.session_state.years_exp       = years_exp
            st.session_state.age             = age
            st.session_state.avg_knowledge   = avg_knowledge

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

            st.success("✅ Prediction complete! Click **Skill Analysis** or **Growth & Insights** tabs above.")

    st.markdown("---")
    st.caption("Built with Streamlit · GradientBoosting Regression · Sklearn · 2025-26 India Market Data")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SKILL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab_skill:
    st.markdown("## 🧠 Skill Analysis")
    st.markdown("##### Breakdown of your skills and what to improve for higher pay")
    st.markdown("---")

    if "prediction" not in st.session_state:
        st.info("👈 Go to the **Salary Predictor** tab, fill in your profile and predict your salary first.")
    else:
        prediction      = st.session_state.prediction
        skill_values    = st.session_state.skill_values
        skills_for_role = st.session_state.skills_for_role
        job_title       = st.session_state.job_title
        avg_knowledge   = st.session_state.avg_knowledge

        st.markdown(f"**Role:** {job_title} &nbsp;|&nbsp; **Predicted CTC:** ₹{prediction:,.0f} &nbsp;|&nbsp; **Avg Skill:** {avg_knowledge:.0f}%")
        st.markdown("---")

        left, right = st.columns([1, 1], gap="large")

        with left:
            st.markdown('<div class="section-header">📊 Your Skill Knowledge Breakdown</div>',
                        unsafe_allow_html=True)

            for skill in skills_for_role:
                pct    = skill_values[skill]
                impact = (pct / 100) * skill_max_bonus[skill]

                if pct == 0:
                    level, color = "Not Learned", "🔴"
                elif pct < 30:
                    level, color = "Beginner", "🟡"
                elif pct < 70:
                    level, color = "Intermediate", "🟠"
                else:
                    level, color = "Expert", "🟢"

                st.progress(
                    max(pct, 1),
                    text=f"{color} **{skill}** — {pct}% ({level})  |  +₹{impact:,.0f} salary impact"
                )

            st.markdown("")
            st.markdown('<div class="section-header">📋 Skill Level Summary</div>', unsafe_allow_html=True)
            not_learned  = [s for s in skills_for_role if skill_values[s] == 0]
            beginner     = [s for s in skills_for_role if 0 < skill_values[s] < 30]
            intermediate = [s for s in skills_for_role if 30 <= skill_values[s] < 70]
            expert       = [s for s in skills_for_role if skill_values[s] >= 70]

            s1, s2, s3, s4 = st.columns(4)
            s1.metric("🔴 Not Learned",  len(not_learned))
            s2.metric("🟡 Beginner",     len(beginner))
            s3.metric("🟠 Intermediate", len(intermediate))
            s4.metric("🟢 Expert",       len(expert))

            if not_learned:
                st.markdown("")
                st.error(f"You have **{len(not_learned)} skill(s) not learned** — {', '.join(not_learned)}")

        with right:
            st.markdown('<div class="section-header">📚 Skills to Improve for Higher Pay</div>',
                        unsafe_allow_html=True)
            st.caption("Ranked by maximum salary impact — focus on the top ones first")

            weak_skills = [(s, skill_max_bonus[s]) for s in skills_for_role if skill_values[s] < 80]
            weak_skills.sort(key=lambda x: -x[1])

            if not weak_skills:
                st.success("🎉 You are at 80%+ on all skills — you are at expert level!")
            else:
                for skill, bonus in weak_skills:
                    current_pct    = skill_values[skill]
                    current_impact = (current_pct / 100) * bonus
                    gain_at_80     = (0.8 * bonus) - current_impact
                    gain_at_100    = bonus - current_impact

                    with st.container(border=True):
                        ca, cb = st.columns([2, 1])
                        with ca:
                            st.markdown(f"**{skill}**")
                            st.caption(f"Current: {current_pct}%  →  Target: 80%")
                            st.progress(max(current_pct, 1), text=f"{current_pct}% now")
                        with cb:
                            st.metric(
                                label="Gain at 80%",
                                value=f"+₹{gain_at_80:,.0f}",
                                help=f"Reaching 100% adds ₹{gain_at_100:,.0f} total"
                            )

            st.markdown("")
            st.markdown('<div class="section-header">💡 Total Salary Unlock Potential</div>',
                        unsafe_allow_html=True)

            current_total_impact = sum((skill_values[s] / 100) * skill_max_bonus[s] for s in skills_for_role)
            max_total_impact     = sum(skill_max_bonus[s] for s in skills_for_role)
            potential_gain       = max_total_impact - current_total_impact
            at_80_gain           = sum(
                max((0.8 * skill_max_bonus[s]) - (skill_values[s] / 100) * skill_max_bonus[s], 0)
                for s in skills_for_role
            )

            p1, p2, p3 = st.columns(3)
            p1.metric("Current Skill Impact",   f"₹{current_total_impact:,.0f}")
            p2.metric("Gain if all reach 80%",  f"+₹{at_80_gain:,.0f}")
            p3.metric("Gain if all reach 100%", f"+₹{potential_gain:,.0f}")

    st.markdown("---")
    st.caption("Built with Streamlit · GradientBoosting Regression · Sklearn · 2025-26 India Market Data")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — GROWTH & INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tab_growth:
    st.markdown("## 📈 Growth & Insights")
    st.markdown("##### Your salary trajectory and what drives your pay")
    st.markdown("---")

    if "prediction" not in st.session_state:
        st.info("👈 Go to the **Salary Predictor** tab, fill in your profile and predict your salary first.")
    else:
        prediction    = st.session_state.prediction
        skill_values  = st.session_state.skill_values
        job_title     = st.session_state.job_title
        education     = st.session_state.education
        location      = st.session_state.location
        industry      = st.session_state.industry
        company_type  = st.session_state.company_type
        years_exp     = st.session_state.years_exp
        age           = st.session_state.age
        avg_knowledge = st.session_state.avg_knowledge

        st.markdown(f"**Role:** {job_title} &nbsp;|&nbsp; **Predicted CTC:** ₹{prediction:,.0f} &nbsp;|&nbsp; **Experience:** {years_exp} yrs")
        st.markdown("---")

        left, right = st.columns([1, 1], gap="large")

        with left:
            st.markdown('<div class="section-header">📈 Salary Growth Projection</div>',
                        unsafe_allow_html=True)
            st.caption("Assumes same skills, role, and company — only experience increases")

            milestones  = [0, 2, 5, 8, 12, 18, 25]
            growth_data = {}
            for yr in milestones:
                if yr >= years_exp:
                    p = make_prediction(model, encoders, job_title, education, location,
                                        industry, company_type, yr, 21 + yr, skill_values)
                    growth_data[yr] = p

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
