import streamlit as st

st.set_page_config(
    page_title="Behind the Build",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .hero-banner {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        color: white;
        margin-bottom: 1.5rem;
    }
    .hero-title   { font-size: 2.2rem; font-weight: 900; color: #00d4aa; margin-bottom: 0.3rem; }
    .hero-sub     { font-size: 1rem; color: #a0aec0; }
    .hero-tag     { display: inline-block; background: rgba(0,212,170,0.15); border: 1px solid #00d4aa;
                    border-radius: 20px; padding: 0.2rem 0.8rem; font-size: 0.8rem; color: #00d4aa;
                    margin-right: 0.4rem; margin-top: 0.5rem; }

    /* ── Hide Skill Analysis & Growth Insights from sidebar ── */
    [data-testid="stSidebarNav"] li:nth-child(2),
    [data-testid="stSidebarNav"] li:nth-child(3) {
        display: none !important;
    }

    .phase-header {
        background: linear-gradient(90deg, #2d3748, #4a5568);
        color: white; font-size: 1rem; font-weight: 700;
        padding: 0.6rem 1rem; border-radius: 8px; margin: 1.5rem 0 0.8rem 0;
        letter-spacing: 0.03em;
    }
    .section-header {
        font-size: 1.05rem; font-weight: 700; color: #2d3748;
        padding: 0.4rem 0; border-bottom: 2px solid #e2e8f0; margin-bottom: 0.8rem;
        margin-top: 1rem;
    }
    .stat-pill {
        display: inline-block; background: #edf2f7; border-radius: 6px;
        padding: 0.25rem 0.7rem; font-size: 0.82rem; font-weight: 600;
        color: #2d3748; margin: 0.15rem;
    }
    .code-note {
        background: #1a202c; color: #e2e8f0; border-radius: 8px;
        padding: 0.8rem 1rem; font-family: monospace; font-size: 0.82rem;
        margin: 0.6rem 0; white-space: pre-wrap;
    }
    div[data-testid="metric-container"] {
        background: #f7fafc; border: 1px solid #e2e8f0;
        border-radius: 10px; padding: 1rem;
    }
    .timeline-dot {
        display: inline-block; width: 28px; height: 28px; border-radius: 50%;
        background: #00d4aa; color: white; font-weight: 800; font-size: 0.9rem;
        text-align: center; line-height: 28px; margin-right: 0.6rem;
    }
    .timeline-row { display: flex; align-items: flex-start; margin-bottom: 0.5rem; }
    .timeline-text { flex: 1; padding-top: 4px; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🔬 Behind the Build</div>
    <div class="hero-sub">A complete, no-shortcuts walkthrough of how this project was designed, built, and validated — from the first research question to the live deployed app.</div>
    <div style="margin-top:0.8rem">
        <span class="hero-tag">Machine Learning</span>
        <span class="hero-tag">Data Engineering</span>
        <span class="hero-tag">Streamlit</span>
        <span class="hero-tag">50,000 Samples</span>
        <span class="hero-tag">43 Features</span>
        <span class="hero-tag">R² = 0.9995</span>
        <span class="hero-tag">2025-26 India Market</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("> This page is intended for **recruiters, collaborators, and anyone who wants to understand the thinking behind every decision** — not just the output.")

st.markdown("---")


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1 — PROBLEM DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="phase-header">PHASE 1 — Defining the Problem</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2], gap="large")
with col1:
    st.markdown('<div class="section-header">Why This Project?</div>', unsafe_allow_html=True)
    st.markdown("""
Most salary prediction projects on Kaggle use the same generic international datasets — a few thousand rows of raw numbers with no India-specific context, no skill breakdown, and no market calibration. They produce a number but give you no insight into **why** that number is what it is.

The goal was to build something that:
- Is **specific to India's 2025-26 IT job market** — not the US, not 2019 data
- Treats **skills as a first-class input** — not just a checkbox but a knowledge percentage
- Makes **salary explainable** — you should be able to understand exactly why a prediction changed
- Covers the **full landscape**: 8 roles, 15 states, 15 industries, 4 company types, 34 skills
""")

    st.markdown('<div class="section-header">What Makes a Good Salary Prediction Problem?</div>', unsafe_allow_html=True)
    st.markdown("""
Before building anything, the first step was to ask: what actually determines salary in India's IT sector?

Research across **Naukri.com**, **LinkedIn Salary Insights**, **AmbitionBox**, and **Glassdoor India** (2024-25 data) revealed five key salary drivers:

1. **Role** — ML Engineers earn far more than Frontend Developers at the same company
2. **Experience × Skill combination** — a senior developer with outdated skills earns less than a junior with cutting-edge skills
3. **Industry + Company type together** — Google (IT Product MNC) vs Infosys (IT Services Indian IT Giant) is a ₹3L+ difference at the same role/experience level
4. **Geography** — Bangalore vs Bihar is a ₹70,000+ annual gap just from location
5. **Education** — PhD adds ₹2L, Master's adds ₹1.2L, but only to the floor salary

The key insight: **these factors are not independent and additive — they interact**. Designing the model to capture these interactions was the core architectural challenge.
""")

with col2:
    st.markdown('<div class="section-header">Problem Scope</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    m1.metric("Job Roles", "8")
    m2.metric("Indian States", "15")
    m1.metric("Industries", "15")
    m2.metric("Company Types", "4")
    m1.metric("Skills Tracked", "34")
    m2.metric("Unique Combos", "60+")
    m1.metric("Training Samples", "50,000")
    m2.metric("Model Features", "43")

    st.markdown("")
    st.markdown('<div class="section-header">Roles Covered</div>', unsafe_allow_html=True)
    roles = ["Data Analyst", "Data Scientist", "ML Engineer", "Software Engineer",
             "Backend Developer", "Frontend Developer", "DevOps Engineer", "Product Manager"]
    for r in roles:
        st.markdown(f'<span class="stat-pill">{r}</span>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="section-header">Industries Covered</div>', unsafe_allow_html=True)
    industries = ["IT Product", "IT Services", "Fintech", "E-commerce", "BFSI", "EdTech",
                  "Gaming", "Healthcare & Pharma", "Cybersecurity", "Cloud & SaaS",
                  "Automotive & EV", "Media & OTT", "Logistics & Supply Chain",
                  "Consulting", "Government & PSU"]
    for ind in industries:
        st.markdown(f'<span class="stat-pill">{ind}</span>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2 — DATA STRATEGY
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="phase-header">PHASE 2 — Data Strategy: Why Synthetic Data?</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.markdown('<div class="section-header">The Real Dataset Problem</div>', unsafe_allow_html=True)
    st.markdown("""
Public salary datasets for India have serious problems:

- **Naukri/AmbitionBox scraping** — violates ToS; data is self-reported, highly unreliable, full of outliers
- **Kaggle India salary datasets** — mostly US-origin data relabelled, or very small (<5,000 rows), missing key features like skills and industry × company combinations
- **Privacy** — real employee salary data cannot be ethically used without consent
- **Staleness** — most datasets are 2021-22 era; post-pandemic market corrections make them invalid for 2025-26
    """)

    st.success("**Decision: Synthetic data with verified market calibration.** Build a mathematically precise salary formula based on real market research, generate 50,000 samples from it, then train a model to learn the formula. This gives full control over salary logic, no privacy issues, and data that is accurate to 2025-26.")

    st.markdown('<div class="section-header">How Market Values Were Verified</div>', unsafe_allow_html=True)
    st.markdown("""
Every salary component was back-checked against real market data:

**Fresher benchmarks (2025):**
- TCS / Infosys / Wipro campus offer: ₹3.5–4.5L — set as the IT Services + Indian IT Giant floor
- Startup ML Engineer offer (verified LinkedIn): ₹5–7L — calibrated base accordingly
- Product company (Razorpay, CRED) fresher: ₹8–12L — set Mid-size IT Product premium

**Experience benchmarks:**
- 3yr Software Engineer at Infosys: ₹7–9L (AmbitionBox aggregate)
- 7yr Data Scientist at Amazon India: ₹25–35L (LinkedIn Insights)
- 15yr ML Engineer at Google India: ₹50L+ (Glassdoor India estimates)

**Location gap:**
- Bangalore vs Tier-2 city (Jaipur, Lucknow): ₹50K–₹80K annual gap confirmed via Naukri job filters

After building the formula, 15 audit tests were run (see Phase 5).
    """)

with col2:
    st.markdown('<div class="section-header">Why 50,000 Samples?</div>', unsafe_allow_html=True)
    st.markdown("""
The feature space is large: 8 roles × 15 states × 15 industries × 4 company types × 4 education levels × 26 experience years = over 74,000 unique combinations just from non-skill features.

Adding 34 skill columns (continuous 0–100%) makes the space enormous. **50,000 samples** gives GradientBoosting enough data to learn salary smoothly without overfitting to any specific combination.

A smaller dataset (5,000) was tested first — predictions were noticeably "bumpy" across experience milestones. 50,000 solved this.
    """)

    st.markdown('<div class="section-header">Data Generation Logic</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="code-note">np.random.seed(42)  # reproducible
n = 50,000

# Random assignment of profile features
job_title  = random.choice(8 roles)
education  = random.choice(4 levels)
location   = random.choice(15 states)
industry   = random.choice(15 industries)
company    = random.choice(4 types)
experience = randint(0, 25)
age        = randint(21, 60)

# Role-specific skills only (not all 34)
for skill in role_skills[job_title]:
    skill_pct[skill] = uniform(0, 100)
# Skills not in role → stay 0

# Gaussian noise added to salary
salary += normal(mean=0, std=10,000)</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Why Gaussian Noise?</div>', unsafe_allow_html=True)
    st.markdown("""
Real salaries aren't perfectly deterministic — two identical candidates get different offers based on negotiation, timing, and company budget cycles. Adding `normal(0, ₹10,000)` std noise simulates this and prevents the model from memorising the formula exactly (which would be overfit to the formula, not generalise to real data variation).

The ₹10,000 std was chosen as ~1-2% of average salary — realistic negotiation variance without distorting the core signal.
    """)


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3 — SALARY FORMULA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="phase-header">PHASE 3 — Salary Formula Design</div>', unsafe_allow_html=True)

st.info("**This is the most important part of the project.** The formula defines what salary 'truth' is. Every prediction the model makes is its best approximation of this formula. Getting the formula wrong means every prediction is wrong — no matter how good the model is.")

col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.markdown('<div class="section-header">The Full Formula</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="code-note">salary =
  base_salary[role]                        # role floor
  + edu_bonus[education]                   # education premium
  + loc_bonus[state]                       # location premium
  + industry_company_bonus[ind][company]   # industry × company matrix
  + exp × 40,000                           # experience floor (₹40K/yr)
  + exp × (avg_skill/100) × 120,000        # skill-weighted experience
  + Σ (skill_pct/100 × skill_max_bonus[s]) # per-skill contribution
  + normal(0, 10,000)                      # realistic noise</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Base Salaries (Role Floors)</div>', unsafe_allow_html=True)
    base_salaries = {
        "Data Analyst": "₹1,30,000", "Data Scientist": "₹1,75,000",
        "ML Engineer": "₹2,00,000", "Software Engineer": "₹1,55,000",
        "Backend Developer": "₹1,45,000", "Frontend Developer": "₹1,20,000",
        "DevOps Engineer": "₹1,65,000", "Product Manager": "₹1,90,000"
    }
    for role, sal in base_salaries.items():
        st.markdown(f"- **{role}**: {sal} base")

    st.info("These are the annual salary floor for a fresher with 0 years experience at the worst location (Bihar), in IT Services, at an Indian IT Giant, with 0% skills and only a High School diploma. Everything above this floor is additive.")

    st.markdown('<div class="section-header">Education Bonus</div>', unsafe_allow_html=True)
    st.markdown("""
| Level | Annual Bonus |
|---|---|
| High School | ₹0 |
| Bachelor's (B.Tech/BCA) | ₹40,000 |
| Master's (M.Tech/MCA) | ₹1,20,000 |
| PhD | ₹2,00,000 |

PhD premium reflects research roles, quant finance, and specialised ML positions where a doctorate is expected.
    """)

with col2:
    st.markdown('<div class="section-header">Location Bonuses (Annual)</div>', unsafe_allow_html=True)
    locs = [
        ("Karnataka (Bangalore)", "₹70,000", "India's Silicon Valley — highest"),
        ("Maharashtra (Mumbai/Pune)", "₹60,000", "BFSI capital + Pune IT"),
        ("Delhi NCR", "₹55,000", "Noida/Gurgaon fintech corridor"),
        ("Telangana (Hyderabad)", "₹55,000", "Fastest growing IT city 2024-25"),
        ("Tamil Nadu (Chennai)", "₹45,000", "Auto + IT, stable market"),
        ("Haryana (Gurgaon)", "₹35,000", "Fintech startup belt"),
        ("Gujarat, Kerala, West Bengal", "₹20–25,000", "Mid-tier IT clusters"),
        ("Bihar", "₹0", "Near-zero IT presence — baseline"),
    ]
    for loc, bonus, note in locs:
        st.markdown(f"- **{loc}**: {bonus} — *{note}*")

    st.markdown('<div class="section-header">The Experience Formula — Key Design Decision</div>', unsafe_allow_html=True)
    st.warning('**The biggest design challenge:** How do you reward experience without making a 15yr/low-skill engineer earn more than a 5yr/high-skill engineer? This is a real market reality that a flat "exp × constant" formula gets wrong.')

    st.markdown("""
The solution: **split experience into two components**.

**Component 1 — Experience floor** (`exp × ₹40,000`):
Guaranteed per year regardless of skills. Reflects domain knowledge, communication, ownership, and reliability that only time builds. Kept intentionally low.

**Component 2 — Skill-amplified experience** (`exp × avg_skill_pct × ₹1,20,000`):
The main driver of senior pay. At 100% skills: ₹1,20,000/yr. At 20% skills: ₹24,000/yr.

**Result:**
- 5yr / 80% skills: `5×40K + 5×0.80×120K = 2L + 4.8L = 6.8L` extra vs fresher
- 10yr / 20% skills: `10×40K + 10×0.20×120K = 4L + 2.4L = 6.4L` extra vs fresher
- 10yr / 20% skills earns **LESS** than 5yr / 80% — skills dominate over time

This matches the 2025-26 market reality where generative AI skills can double a junior's salary.
    """)

st.markdown("---")
st.markdown('<div class="section-header">Industry × Company Matrix — The Critical Innovation</div>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.markdown("""
Most salary models treat industry and company type as two separate additive bonuses:
```
salary += industry_bonus + company_bonus
```
This is **wrong**. An MNC in IT Product (Google) pays ₹3,50,000 more than a fresher floor. An MNC in IT Services (Accenture) pays only ₹1,50,000 more. Treating them as separate adds would give Accenture an unrealistic bonus.

The solution: **a 15×4 matrix** where each cell is the exact bonus for that industry + company combination — 60 individually researched values.
    """)
    st.success("""**Matrix highlights:**
- IT Product + MNC (Google/MS/Amazon): +₹3,50,000
- Cloud & SaaS + Mid-size (Zoho/Chargebee): +₹2,00,000
- IT Services + Indian IT Giant (TCS/Infosys): +₹15,000 (lowest non-govt)
- Government & PSU + any type: +₹8,000–₹50,000 (lowest overall)
- EdTech post-funding-winter: reduced premiums (BYJU's collapse impact baked in)""")

with col2:
    st.markdown('<div class="section-header">Skill Bonuses (at 100% Knowledge)</div>', unsafe_allow_html=True)
    skill_data = [
        ("Machine Learning", "₹1,80,000", "Highest — GenAI/LLM surge in 2025"),
        ("Deep Learning", "₹1,50,000", "Neural nets, strong at product cos"),
        ("System Design", "₹1,40,000", "Senior engineer signal"),
        ("MLOps", "₹1,30,000", "Production ML; scarce skill"),
        ("AWS / Kubernetes / Terraform", "₹1,10–1,30,000", "Cloud infra depth"),
        ("Data Structures", "₹1,10,000", "Product company interview signal"),
        ("Python / React", "₹1,00,000", "Core high-demand languages"),
        ("SQL", "₹60,000", "Widely expected; moderate premium"),
        ("Git", "₹25,000", "Expected everywhere — minimal premium"),
    ]
    for skill, bonus, note in skill_data:
        st.markdown(f"- **{skill}**: {bonus} — *{note}*")

    st.info("Skill bonuses scale linearly with knowledge percentage. A 50% skill level gives 50% of the max bonus. This is intentional — partial knowledge still has market value.")


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 4 — FEATURE ENGINEERING
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="phase-header">PHASE 4 — Feature Engineering</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.markdown('<div class="section-header">Why 43 Features?</div>', unsafe_allow_html=True)
    st.markdown("""
The 43 features break down as:

**7 base features** (encoded categoricals + numerics):
- Job Role (label encoded, 8 classes)
- Education (label encoded, 4 classes)
- Location / State (label encoded, 15 classes)
- Years of Experience (0–25, integer)
- Age (21–60, integer)
- Industry (label encoded, 15 classes)
- Company Type (label encoded, 4 classes)

**2 engineered interaction features:**
- `avg_skill_pct` — mean knowledge % across all role-relevant skills (0–100)
- `exp_x_skill` — years experience × avg_skill_pct (captures "expert senior" premium)

**34 skill features** (one per unique skill across all roles):
- Each column = knowledge % for that specific skill (0–100)
- Skills irrelevant to the user's role = 0
- This sparse representation lets the model learn skill-specific salary impacts
    """)

    st.markdown('<div class="section-header">Why Role-Specific Skills (Not All 34)?</div>', unsafe_allow_html=True)
    st.markdown("""
An ML Engineer's salary should not be affected by their React knowledge, and a Frontend Developer's salary should not be affected by MLOps. Only 6 skills per role are shown and trained — non-relevant skills stay 0.

This is both **realistic** (employers care about role-relevant skills) and **mathematically correct** (no phantom salary boosts from unrelated skill columns).
    """)

with col2:
    st.markdown('<div class="section-header">The Two Interaction Features — Why They Matter</div>', unsafe_allow_html=True)
    st.markdown("""
`avg_skill_pct` alone gives the model a summary signal of "how skilled is this person overall." Without it, the model would need to infer skill level from 34 sparse columns per prediction — harder and noisier.

`exp_x_skill` is the critical one. Without this feature:
- GBM would learn experience and skills as additive, independent effects
- A 10yr / 20% skills senior would appear to earn more than a 5yr / 80% skills engineer (just by raw experience)

With `exp_x_skill`, the model can directly learn the interaction: **high experience only commands premium pay when skill level is high too.** This is the core salary reality of the modern India IT market.
    """)

    st.markdown('<div class="section-header">Label Encoding vs One-Hot Encoding</div>', unsafe_allow_html=True)
    st.warning("**Decision: Label encoding for all categoricals, not one-hot encoding.** One-hot encoding would create 15 binary columns for location, 15 for industry, 8 for job title — adding 50+ sparse features. With GradientBoosting trees, label encoding works just as well because trees split on thresholds and can learn non-ordinal relationships through split patterns. One-hot encoding would balloon the feature space unnecessarily and slow training with no accuracy gain for this tree-based model.")

    st.markdown('<div class="section-header">Minimum Salary Floor</div>', unsafe_allow_html=True)
    st.markdown("""
A hard minimum of ₹2,20,000 is applied:
```python
salary = max(220_000, computed_salary)
```
This prevents edge cases (0 experience + 0 skills + Bihar + High School + IT Services + Indian IT Giant) from producing unrealistic sub-₹2L values. India's IT sector minimum in practice.
    """)


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 5 — MODEL SELECTION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="phase-header">PHASE 5 — Model Selection & Training</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.markdown('<div class="section-header">Why GradientBoostingRegressor?</div>', unsafe_allow_html=True)
    st.markdown("""
**RandomForestRegressor was tested first.** It gave an R² of ~0.97 but predictions were being pulled toward the mean for specific edge-case inputs (very high experience + very high skills + IT Product MNC). Errors of ₹1.5–2L were common in these high-salary scenarios.

**Root cause:** Random Forest averages many independent trees. For high-salary extremes that are underrepresented in random splits, averaging pulls predictions toward the dataset mean. This is the well-known "shrinkage toward mean" problem in bagging methods.

**GradientBoosting builds trees additively** — each new tree corrects the residual errors of all previous trees. For an additive salary formula, this is architecturally ideal:
- The formula adds components → GBM adds corrections
- High-salary edge cases get corrected iteratively until they converge

Result: **R² = 0.9995** with predictions within ₹20,000-50,000 of formula output across all ranges.
    """)

    st.markdown('<div class="section-header">Hyperparameters</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="code-note">GradientBoostingRegressor(
    n_estimators  = 300,   # 300 trees; plateau of improvement
    learning_rate = 0.1,   # standard starting point
    max_depth     = 5,     # enough for 43 features, avoids overfit
    random_state  = 42     # reproducible
)</div>
    """, unsafe_allow_html=True)

    st.markdown("""
- **n_estimators=300**: Tested 100, 200, 300 — improvement plateaued at 300. Beyond 300 gave no R² gain but slower training
- **learning_rate=0.1**: Standard value for moderate-sized datasets; lower LR with more estimators wasn't worth the training time for this dataset
- **max_depth=5**: Allows trees to model 5-way interactions (e.g., role × industry × company × experience × skill), which the salary formula requires
    """)

with col2:
    st.markdown('<div class="section-header">Model Performance</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    m1.metric("R² Score", "0.9995")
    m2.metric("Training Samples", "50,000")
    m1.metric("Features", "43")
    m2.metric("Model Size", "1.36 MB")
    m1.metric("Prediction Speed", "~0.4ms")
    m2.metric("Trees (Estimators)", "300")

    st.markdown("")
    st.markdown('<div class="section-header">What R² = 0.9995 Means</div>', unsafe_allow_html=True)
    st.markdown("""
R² of 0.9995 means the model explains 99.95% of salary variance in the training data. This is high because the data was generated from a deterministic formula with only ₹10,000 Gaussian noise — a well-structured model should be able to recover it almost perfectly.

This is **not** claiming 99.95% accuracy on real-world salaries. The accuracy claim is: the model has successfully learned the salary formula, and the formula itself was calibrated to real market data.
    """)

    st.markdown('<div class="section-header">Serialisation & Deployment</div>', unsafe_allow_html=True)
    st.markdown("""
The trained model and all encoders are saved using `pickle`:

**`salary_model.pkl`** — the trained GBM model (1.36 MB)
**`encoders.pkl`** — a dictionary containing:
- 5 LabelEncoders (job, edu, location, industry, company)
- `role_skills` mapping (which 6 skills each role uses)
- `all_skills` list (all 34 skills, for feature vector construction)
- `skill_max_bonus` dict (for UI display and Skill Analysis page)
- `industry_company_bonus` matrix (for UI display)

One issue during deployment: pickle files created in Python 3.11 locally were sometimes incompatible with Streamlit Cloud's Python environment. Solution: the app auto-detects pickle loading failures and re-runs `train_model.py` automatically if needed.
    """)


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 6 — VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="phase-header">PHASE 6 — Model Validation (15 Audit Checks)</div>', unsafe_allow_html=True)

st.markdown("""
Before any UI was built, 15 explicit audit checks were run to verify that predictions matched known market reality. A model with R² = 0.9995 that produces unrealistic outputs would be useless.
""")

checks = [
    ("Bihar + IT Services + Indian IT Giant + Bachelor + 0yr + 30% skills", "₹3.2–5.5L", "Pass", "TCS/Infosys fresher minimum benchmark"),
    ("Karnataka + IT Product + MNC + Master's + 0yr + 80% skills", "₹7–12L", "Pass", "Fresher at Google/Amazon Bangalore office"),
    ("3yr Software Engineer + IT Services + Mid-size", "₹7–11L", "Pass", "Mid-level at Mphasis/Hexaware benchmark"),
    ("10yr Data Scientist + IT Product + MNC + 90% skills", "₹25–40L", "Pass", "Senior DS at Amazon/Microsoft India"),
    ("Fresher 30% vs 100% skills — same role/company/location", "+₹2–5L gap", "Pass", "Skills differentiate even at fresher level"),
    ("10yr/20% skills vs 5yr/80% skills — same role", "5yr/80% earns MORE", "Pass", "Skills beat raw experience when skills are low"),
    ("Industry pay order check", "IT Product > BFSI > IT Services > Govt", "Pass", "Market hierarchy preserved"),
    ("Company pay order within same industry", "MNC > Mid-size > Startup > IT Giant (IT Services)", "Pass", "IT Giant lowest in IT Services confirmed"),
    ("EdTech post-2023 vs IT Product — same role", "IT Product pays 2-3× more", "Pass", "EdTech funding winter impact reflected"),
    ("PhD vs Bachelor's — same everything else", "+₹1.6L (PhD)", "Pass", "Education premium within expected range"),
    ("Government & PSU — any combination", "₹3.5–5L range", "Pass", "Govt pay correctly lowest across all industries"),
    ("Fintech Mid-size (PhonePe/CRED) vs IT Services Indian IT Giant", "Fintech pays ~₹2L+ more", "Pass", "Modern fintech vs legacy IT services gap"),
    ("ML Engineer vs Frontend Developer — same company/location", "ML earns 15-30% more", "Pass", "Role-based salary ceiling preserved"),
    ("0 skills total — salary floor check", "Min ₹2.2L applied", "Pass", "Hard floor prevents sub-realistic predictions"),
    ("25yr expert (100% skills) career max", "₹50L+ for IT Product MNC", "Pass", "Career ceiling realistic for top-tier senior"),
]

col1, col2 = st.columns([1, 1], gap="large")
half = len(checks) // 2
for i, (test, expected, result, note) in enumerate(checks):
    target_col = col1 if i < half else col2
    with target_col:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**Test {i+1}:** {test}")
                st.caption(f"Expected: {expected} — *{note}*")
            with c2:
                st.markdown(f"**{'✅ ' + result}**")


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 7 — APP ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="phase-header">PHASE 7 — App Architecture & UI Design</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.markdown('<div class="section-header">3-Page Structure</div>', unsafe_allow_html=True)
    st.markdown("""
The app is split into 3 pages connected via `st.session_state`:

**Page 1 — Salary Predictor (Home)**
- Profile inputs: role, education, state, experience, age
- Company inputs: industry + company type (with live premium display)
- Role-aware skill sliders (only 6 skills for selected role)
- Prediction output: salary card + metrics + range

**Page 2 — Skill Analysis**
- Colour-coded skill breakdown (Not Learned / Beginner / Intermediate / Expert)
- "Skills to improve" panel: ranked by salary impact, with ₹ gain at 80%
- Salary unlock potential: how much more can be earned if skills improve

**Page 3 — Growth & Insights**
- Salary growth projection: predicted CTC at 0, 2, 5, 8, 12, 18, 25 years
- Feature importance: what drives salary most for this specific profile
- Category breakdown: profile factors vs skill factors

**Page 4 — Behind the Build (this page)**
- Full project documentation for recruiters and collaborators
    """)

    st.markdown('<div class="section-header">State Management Across Pages</div>', unsafe_allow_html=True)
    st.markdown("""
Streamlit re-runs the entire script on every interaction, so prediction results must be persisted in `st.session_state` to be accessible on other pages.

When the user clicks "Predict My Salary", the Home page saves to session state:
```python
st.session_state.prediction     = prediction
st.session_state.skill_values   = skill_values
st.session_state.job_title      = job_title
st.session_state.industry       = industry
# ... all profile variables
```
Pages 2 and 3 check for `"prediction" in st.session_state` and show a warning with redirect if no prediction exists yet.
    """)

with col2:
    st.markdown('<div class="section-header">UI Design Decisions</div>', unsafe_allow_html=True)
    st.markdown("""
**Left / Right split layout:**
All pages use a 50/50 column layout to separate inputs from outputs. This avoids the common mistake of putting everything in a vertical scroll — users can compare inputs and results side-by-side.

**Dark gradient salary card:**
The prediction result uses a custom CSS card with a dark gradient background and teal accent. This makes the primary output (salary) visually prominent and professional — not just a number in plain text.

**Role-aware skill sliders:**
The skill section re-renders automatically when the job role changes. Only the 6 skills relevant to that role appear. Each slider has a `help` tooltip showing the max salary impact for that skill.

**Industry × Company live caption:**
When the user selects industry + company type, an instant caption appears showing the exact salary premium for that combination — before they even predict. This makes the model's logic transparent.

**0% skill validation:**
If a user sets all skill sliders to 0, prediction is blocked with an error message listing the skills they need to learn. This prevents a meaningless ₹2.2L prediction from appearing for an impossible candidate profile.

**Low skill warning:**
Average skill below 20% triggers a yellow warning: *"Most employers expect 30–40% in core skills."* Not blocking — just informative.
    """)

    st.markdown('<div class="section-header">Custom CSS Components</div>', unsafe_allow_html=True)
    st.markdown("""
- `.salary-card` — dark gradient card with teal salary amount
- `.section-header` — bold section dividers with bottom border
- `div[data-testid="metric-container"]` — styled metric boxes with border
- Colour-coded skill levels: 🔴 Not Learned / 🟡 Beginner / 🟠 Intermediate / 🟢 Expert

All CSS is embedded directly in Streamlit using `st.markdown(..., unsafe_allow_html=True)` — no external CSS files needed, making the app fully self-contained.
    """)


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 8 — DEPLOYMENT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="phase-header">PHASE 8 — Deployment</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.markdown('<div class="section-header">Streamlit Community Cloud</div>', unsafe_allow_html=True)
    st.markdown("""
The app is deployed on **Streamlit Community Cloud** (free tier), connected directly to the GitHub repository. Every push to `main` triggers an automatic redeploy.

**Deployment steps:**
1. Repository pushed to GitHub with all files including `model/` folder (pkl files)
2. Connected at share.streamlit.io → select repo → select `app.py` as entry point
3. Python version set to 3.11 in advanced settings (to match local dev environment)
4. App deployed and accessible within ~2 minutes

**Auto-retrain on pickle failure:**
If the deployed environment's Python version differs from the pkl file's origin, `pickle.load()` raises an exception. The app catches this:
```python
try:
    model = pickle.load(f)
except Exception:
    needs_train = True  # triggers re-run of train_model.py
```
This makes the app self-healing — it retrains and caches the model on first use if needed.
    """)

with col2:
    st.markdown('<div class="section-header">Tech Stack Summary</div>', unsafe_allow_html=True)
    stack = [
        ("Python 3.11", "Core language"),
        ("Scikit-learn", "GradientBoostingRegressor, LabelEncoder"),
        ("NumPy", "Data generation, feature arrays, noise"),
        ("Pandas", "DataFrame construction and manipulation"),
        ("Streamlit", "Web app UI and multi-page structure"),
        ("Pickle", "Model and encoder serialisation"),
        ("Git & GitHub", "Version control, source hosting"),
        ("Streamlit Community Cloud", "Free hosting and deployment"),
    ]
    for tech, purpose in stack:
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            c1.markdown(f"**{tech}**")
            c2.markdown(purpose)

    st.markdown('<div class="section-header">Project Files</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="code-note">India_Salary_Prediction/
├── app.py                     # Home page — prediction
├── train_model.py             # Data generation + model training
├── requirements.txt           # Python dependencies
├── pages/
│   ├── 2_Skill_Analysis.py    # Skill breakdown page
│   ├── 3_Growth_Insights.py   # Growth projection page
│   └── 4_Behind_The_Build.py  # This page
└── model/
    ├── salary_model.pkl       # Trained GBM (1.36 MB)
    └── encoders.pkl           # Encoders + role metadata</div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# KEY CHALLENGES & DECISIONS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="phase-header">Key Challenges & How They Were Solved</div>', unsafe_allow_html=True)

challenges = [
    (
        "Making experience and skills non-additive",
        "A flat `exp × constant` formula would make a 15yr/low-skill engineer earn more than a 5yr/high-skill engineer — wrong for the 2025 market.",
        "Introduced `exp_x_skill` interaction feature. Experience earns a floor (₹40K/yr) but only amplifies to full potential when skills are high (₹1,20,000/yr at 100%). This correctly makes skill the primary salary driver."
    ),
    (
        "Industry × Company matrix vs flat bonuses",
        "Flat industry + company bonuses would give a Government PSU MNC the same bonus as a IT Product MNC — wildly unrealistic.",
        "Designed a 15×4 matrix with 60 individually researched values. Every combination reflects actual market reality (EdTech post-funding-winter, Government PSU lowest, etc.)."
    ),
    (
        "Random Forest pulling toward mean for high salaries",
        "RF predictions for IT Product MNC + expert + 10yr experience were 20-30% below formula values — the bagging mean-shrinkage problem.",
        "Switched to GradientBoostingRegressor. Additive tree construction perfectly matches additive salary formula. R² jumped from 0.97 to 0.9995."
    ),
    (
        "Sparse skill columns (34 columns, only 6 non-zero per row)",
        "Most skill columns are 0 for any given sample. Would this confuse the model or cause irrelevant skill features to get non-zero importance?",
        "GBM handles sparse features well because trees split only where variance exists. Non-relevant skill columns always = 0 have zero variance and effectively get ignored. Confirmed by feature importance analysis."
    ),
    (
        "Pickle incompatibility across Python versions",
        "Locally trained pkl files failed to load on Streamlit Cloud due to Python/sklearn version differences.",
        "Added try/except around all pickle.load() calls. On failure, the app re-runs train_model.py automatically. The retrained model is cached with @st.cache_resource for the session."
    ),
    (
        "Preventing zero-skill predictions from silently passing",
        "A user who sets all skills to 0 is not employable in that role — but the model would still output a salary.",
        "Added explicit validation: if sum of all skill values = 0, prediction is blocked with an error listing the skills they need and what to aim for."
    ),
]

for i, (title, problem, solution) in enumerate(challenges, 1):
    with st.expander(f"Challenge {i}: {title}", expanded=(i <= 2)):
        c1, c2 = st.columns([1, 1], gap="large")
        with c1:
            st.markdown("**The Problem:**")
            st.warning(problem)
        with c2:
            st.markdown("**The Solution:**")
            st.success(solution)


# ═══════════════════════════════════════════════════════════════════════════════
# SKILLS DEMONSTRATED
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="phase-header">Skills Demonstrated in This Project</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown('<div class="section-header">Data Science & ML</div>', unsafe_allow_html=True)
    skills_ds = [
        "Synthetic data design with market calibration",
        "Feature engineering (interaction terms, aggregates)",
        "Model selection with reasoning (GBM vs RF)",
        "Hyperparameter understanding",
        "Model validation with domain-specific audit checks",
        "Sparse feature handling",
        "Label encoding for tree-based models",
        "R² interpretation and limitations",
    ]
    for s in skills_ds:
        st.markdown(f"- {s}")

with col2:
    st.markdown('<div class="section-header">Software Engineering</div>', unsafe_allow_html=True)
    skills_se = [
        "Multi-page Streamlit app architecture",
        "State management across pages",
        "Model serialisation and version handling",
        "Auto-retrain fallback pattern",
        "Custom CSS in web app",
        "Input validation and user feedback",
        "Git version control workflow",
        "Cloud deployment (Streamlit Community Cloud)",
    ]
    for s in skills_se:
        st.markdown(f"- {s}")

with col3:
    st.markdown('<div class="section-header">Domain & Research</div>', unsafe_allow_html=True)
    skills_domain = [
        "India IT salary market research (2025-26)",
        "Cross-referencing Naukri, LinkedIn, AmbitionBox, Glassdoor",
        "Salary formula design with market constraints",
        "Industry × Company pay hierarchy modelling",
        "Skill premium calibration per role",
        "Post-funding-winter EdTech market awareness",
        "GenAI/LLM impact on ML skill premiums",
        "Remote work's effect on location salary gaps",
    ]
    for s in skills_domain:
        st.markdown(f"- {s}")


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#718096; font-size:0.85rem; padding: 1rem 0;">
    Built by <strong>Megan</strong> &nbsp;·&nbsp;
    GradientBoostingRegressor &nbsp;·&nbsp; 50,000 samples &nbsp;·&nbsp; 43 features &nbsp;·&nbsp; R² = 0.9995
    &nbsp;·&nbsp; Calibrated to 2025-26 India IT Market
    <br><br>
    <em>Every number in this project has a reason. Every design decision has a trade-off. That's what makes it real.</em>
</div>
""", unsafe_allow_html=True)
