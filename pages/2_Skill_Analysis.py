import streamlit as st
import pickle
import os
import subprocess
import sys

MODEL_PATH   = "model/salary_model.pkl"
ENCODER_PATH = "model/encoders.pkl"

st.set_page_config(
    page_title="Skill Analysis",
    page_icon="🧠",
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
def load_encoders():
    needs_train = not os.path.exists(ENCODER_PATH)
    if not needs_train:
        try:
            with open(ENCODER_PATH, "rb") as f:
                return pickle.load(f)
        except Exception:
            needs_train = True
    if needs_train:
        with st.spinner("Setting up model — please wait (~1 min)..."):
            subprocess.run([sys.executable, "train_model.py"], check=True)
    with open(ENCODER_PATH, "rb") as f:
        return pickle.load(f)


encoders        = load_encoders()
skill_max_bonus = encoders["skill_max_bonus"]

st.markdown("## 🧠 Skill Analysis")
st.markdown("##### Breakdown of your skills and what to improve for higher pay")
st.markdown("---")

# ── Guard: no prediction yet ──────────────────────────────────────────────────
if "prediction" not in st.session_state:
    st.warning("⚠️ No prediction found. Please go to **💼 Home** and predict your salary first.")
    st.stop()

prediction      = st.session_state.prediction
skill_values    = st.session_state.skill_values
skills_for_role = st.session_state.skills_for_role
job_title       = st.session_state.job_title
avg_knowledge   = st.session_state.avg_knowledge

st.markdown(f"**Role:** {job_title} &nbsp;|&nbsp; **Predicted CTC:** ₹{prediction:,.0f} &nbsp;|&nbsp; **Avg Skill:** {avg_knowledge:.0f}%")
st.markdown("---")

left, right = st.columns([1, 1], gap="large")

# ── Left: Skill knowledge breakdown ──────────────────────────────────────────
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

    # Skill level summary
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

# ── Right: What to improve ────────────────────────────────────────────────────
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
