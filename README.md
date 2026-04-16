# India Salary Predictor

A web app that predicts your expected annual salary (CTC) if you work in the IT industry in India.

**Live App:** [Click here to try it](https://indiasalaryprediction-xmbpz8ekgufvbyqdbhkdb3.streamlit.app/)

---

## What does it do?

You fill in your profile — job role, location, experience, skills, company type — and it predicts your expected salary in Indian rupees.

It also shows:
- How your salary could grow over time
- Which skills are holding your salary back
- How much you could earn if you improved specific skills

---

## How it works

I created a dataset of 50,000 IT professional profiles with salaries calibrated to real India market data (Naukri, LinkedIn, AmbitionBox 2025-26). Then I trained a machine learning model on it.

The salary depends on:
- Your job role (ML Engineer, Frontend Developer, etc.)
- Your state/city (Bangalore pays more than most places)
- Industry and company type (product company vs IT services)
- Your years of experience
- How well you know each skill (you rate yourself 0–100%)

---

## Tech used

- Python
- Scikit-learn (GradientBoosting model)
- Pandas
- Streamlit (web app)

---

## How to run it locally

```bash
git clone https://github.com/MgDev2023/India_Salary_Prediction.git
cd India_Salary_Prediction
pip install -r requirements.txt
streamlit run app.py
```

---

## Model details

| Property | Value |
|---|---|
| Algorithm | Gradient Boosting Regressor |
| Training samples | 50,000 |
| R² score | 0.9995 |
| Job roles covered | 8 |
| States covered | 15 |
| Industries covered | 15 |

---

## Project structure

```
India_Salary_Prediction/
├── app.py            ← Streamlit web app
├── train_model.py    ← Model training script
├── requirements.txt
└── model/
    ├── salary_model.pkl
    └── encoders.pkl
```

---

## Made by

Megan — fresher portfolio project to practice machine learning and data analysis with real-world context.
