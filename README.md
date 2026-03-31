# 💼 India Salary Predictor

A machine learning web application that predicts annual CTC (Cost to Company) for IT professionals in India based on job role, skills, experience, location, industry, and company type — calibrated to the **2025-26 India job market**.

🚀 **Live App:** [Click here to try it](https://indiasalaryprediction-xmbpz8ekgufvbyqdbhkdb3.streamlit.app/)

---

## 📌 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [How It Was Built — Step by Step](#how-it-was-built--step-by-step)
- [Project Structure](#project-structure)
- [Model Details](#model-details)
- [How to Run Locally](#how-to-run-locally)

---

## Overview

Most salary prediction projects use generic datasets (like Kaggle's DS salary dataset) with no India-specific context. This app was built from the ground up with:

- **15 Indian states** with realistic location premiums
- **15 specific industries** (Fintech, Cloud & SaaS, Gaming, EV, etc.)
- **Role-specific skills** — each job role has its own 6 relevant skills
- **Skill knowledge sliders** — salary scales with your actual knowledge level (0–100%)
- **Experience × Skill interaction** — a skilled senior earns far more than a rusty one
- **Industry × Company matrix** — 60 unique industry+company combinations with individual pay premiums
- All values calibrated against **Naukri, LinkedIn, AmbitionBox, Glassdoor India 2025-26 data**

---

## Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.11** | Core programming language |
| **Scikit-learn** | GradientBoostingRegressor model, LabelEncoders |
| **Pandas & NumPy** | Data generation and feature engineering |
| **Streamlit** | Web application UI and deployment |
| **Pickle** | Model serialization for deployment |
| **Git & GitHub** | Version control and source hosting |
| **Streamlit Community Cloud** | Free cloud deployment |

---

## Features

- 🎯 **Role-specific skill sliders** — only shows skills relevant to your selected job
- 📊 **Salary growth projection** — see your predicted salary at 0, 2, 5, 8, 12, 18 years
- 📚 **Skills to improve** — top 3 weak skills with exact ₹ salary gain if improved to 80%
- 💼 **Industry × Company premium** — live bonus shown for each combination
- ❌ **0% skill validation** — blocks prediction and guides users who have no skills
- ⚠️ **Low skill warning** — warns users below 20% average knowledge
- 🌙 **Dark salary card** — visual CTC display with annual + monthly breakdown
- ⚙️ **Feature importance** — shows what factors drive salary most for your profile

---

## How It Was Built — Step by Step

### Step 1 — Defined the Problem

The goal was to predict annual CTC for IT professionals in India. Key decisions made upfront:

- Use **synthetic data** calibrated to real market values (no privacy issues, full control over salary logic)
- Cover **8 job roles**, **15 Indian states**, **15 industries**, **4 company types**
- Make skills a **first-class feature** — not just one "skills" column but per-role knowledge percentages

---

### Step 2 — Designed the Salary Formula

Before writing any ML code, designed a realistic base formula:

```
salary = base_salary[role]
       + edu_bonus[education]
       + loc_bonus[state]
       + industry_company_bonus[industry][company_type]   ← matrix, not flat add
       + exp * 40,000                                     ← experience floor
       + exp * (avg_skill/100) * 120,000                  ← skill-weighted experience
       + Σ (skill_pct/100 * skill_max_bonus[skill])       ← per-skill contribution
       + noise(mean=0, std=10,000)
```

Key design decisions:
- **Industry × Company matrix** instead of two separate flat bonuses — because an MNC in IT Product (Google) pays very differently from an MNC in IT Services (Accenture)
- **Experience × Skill interaction** — so a 10yr/20%-skills engineer earns LESS than a 5yr/80%-skills engineer
- **Per-role skills** — ML Engineer has Python/ML/Docker/AWS skills; Frontend Developer has React/JavaScript/TypeScript

---

### Step 3 — Calibrated All Values to 2025-26 Market

Every salary value was calibrated against real India market data:

**Base salaries (fresher CTC):**
- TCS/Infosys offer ₹3.5–4.5L to freshers → set IT Services + Indian IT Giant as floor
- ML Engineers get ₹4.5–6L at product companies → set base accordingly

**Location bonuses:**
- Bangalore (Karnataka) highest — India's Silicon Valley
- Hyderabad (Telangana) bumped up — fastest growing IT city in 2024-25
- Remote work narrowing state gaps — differences kept moderate (₹8K–₹70K range)

**Industry × Company matrix (60 combinations):**
- IT Product + MNC (Google/Amazon/Microsoft India) = ₹3,50,000 premium
- IT Services + Indian IT Giant (TCS/Infosys/Wipro) = ₹15,000 premium (lowest)
- Fintech + Mid-size (PhonePe/CRED/Groww) = ₹2,00,000 premium
- Government & PSU + any = lowest across all

**Skill bonuses (at 100% knowledge):**
- System Design: ₹1,40,000 — senior engineer signal, huge impact
- Machine Learning: ₹1,80,000 — GenAI/LLM surge keeps this highest
- Git: ₹25,000 — expected everywhere, minimal premium

---

### Step 4 — Generated Training Data

```python
n = 50,000 samples
```

- Randomly assigned job title, education, location, industry, company type
- For each sample's role, generated random skill knowledge % (0–100) for the 6 relevant skills
- Computed salary using the formula above with small random noise

---

### Step 5 — Feature Engineering

Two interaction features added beyond raw inputs:

```python
avg_skill_pct = mean(skill_knowledge% for all role skills)
exp_x_skill   = years_experience × avg_skill_pct
```

These allow the model to learn that **experienced + skilled = exponential pay**, not just additive.

**Final feature set: 43 features**
- 7 base features (role, education, location, experience, age, industry, company)
- 2 interaction features (avg_skill_pct, exp_x_skill)
- 34 skill columns (one per skill across all roles, 0 for irrelevant skills)

---

### Step 6 — Model Selection

Tested **RandomForestRegressor** first → predictions were pulled toward dataset mean, giving errors of ₹1.5–2L for specific combinations.

Switched to **GradientBoostingRegressor** because it builds trees additively — perfectly suited for an additive salary formula.

```python
model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
```

Final R² score: **0.9995**

---

### Step 7 — Model Validation (15 Audit Checks)

Before deploying, ran 15 checks to verify realism:

| Test | Expected | Result |
|---|---|---|
| Fresher at TCS/Bihar | ₹3.2–5.5L | ✅ Pass |
| 3yr mid-level IT Services | ₹7–11L | ✅ Pass |
| 10yr senior IT Product MNC | ₹25–40L | ✅ Pass |
| Fresher 30% vs 100% skills gap | +₹2–5L | ✅ Pass |
| 10yr/20% < 5yr/80% skills | Rusty < Skilled | ✅ Pass |
| Industry pay order | IT Product > BFSI > IT Services > Govt | ✅ Pass |

---

### Step 8 — Built the Streamlit UI

UI designed with a **left inputs / right results** split layout:

- **Left panel:** Profile → Company → Skills (role-aware sliders)
- **Right panel:** Salary card → Skill breakdown → What to improve → Growth projection → Feature importance

Custom CSS added for:
- Dark gradient salary card
- Color-coded skill levels (🔴 Not learned / 🟡 Beginner / 🟠 Intermediate / 🟢 Expert)
- Bordered skill improvement cards with progress bars

---

### Step 9 — Deployed to Streamlit Community Cloud

1. Pushed all files to GitHub (including pre-trained `.pkl` model files)
2. Connected repo to **share.streamlit.io**
3. Set Python version to 3.11
4. App auto-retrains if pickle is incompatible with the cloud environment

---

## Project Structure

```
India_Salary_Prediction/
│
├── app.py               # Streamlit web application
├── train_model.py       # Model training script
├── requirements.txt     # Python dependencies
├── .gitignore
│
└── model/
    ├── salary_model.pkl # Trained GradientBoosting model
    └── encoders.pkl     # LabelEncoders + role metadata
```

---

## Model Details

| Property | Value |
|---|---|
| Algorithm | GradientBoostingRegressor |
| Training samples | 50,000 |
| Features | 43 |
| R² score | 0.9995 |
| Model size | 1.36 MB |
| Prediction speed | ~0.4ms |
| Roles covered | 8 |
| States covered | 15 |
| Industries covered | 15 |
| Company types | 4 |
| Skills covered | 34 |

---

## How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/MgDev2023/India_Salary_Prediction.git
cd India_Salary_Prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Retrain the model
python train_model.py

# 4. Run the app
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## Author

**Megan** — [GitHub](https://github.com/MgDev2023)

---

*Built with Streamlit · GradientBoosting Regression · Sklearn · 2025-26 India Market Data*
