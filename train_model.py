import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os

np.random.seed(42)
n = 50000

job_titles = ["Data Analyst", "Data Scientist", "ML Engineer", "Software Engineer",
              "Backend Developer", "Frontend Developer", "DevOps Engineer", "Product Manager"]
education_levels = ["Bachelor's", "Master's", "PhD", "High School"]
locations = [
    "Andhra Pradesh", "Bihar", "Delhi", "Gujarat", "Haryana",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Punjab",
    "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh", "West Bengal"
]
industries = [
    "IT Product",          # FAANG, Razorpay, Zerodha, Freshworks
    "IT Services",         # TCS, Infosys, Wipro, HCL
    "Fintech",             # PhonePe, Paytm, CRED, Groww, BharatPe
    "E-commerce",          # Amazon, Flipkart, Meesho, Nykaa
    "BFSI",                # Goldman, JP Morgan, HDFC, ICICI (non-fintech)
    "EdTech",              # BYJU's, Unacademy, upGrad, Coursera India
    "Gaming",              # Nazara, MPL, Dream11, Mobile Premier League
    "Healthcare & Pharma", # Practo, 1mg, Dr Reddy's, Sun Pharma tech
    "Cybersecurity",       # Quick Heal, Tata Elxsi security, startups
    "Cloud & SaaS",        # Zoho, Chargebee, Postman, Hasura
    "Automotive & EV",     # Ola Electric, Tata Motors tech, Ather
    "Media & OTT",         # Netflix India tech, Hotstar, Zee tech
    "Logistics & Supply Chain", # Delhivery, Shiprocket, Porter
    "Consulting",          # Deloitte, McKinsey, BCG, Big 4 tech arms
    "Government & PSU",    # ISRO, DRDO, NIC, BSNL, BHEL tech
]
company_types = ["MNC", "Indian IT Giant", "Mid-size", "Startup"]

# ── Skills per role (2025-26 job market relevance) ────────────────────────────
role_skills = {
    "Data Analyst":       ["SQL", "Python", "Excel", "Power BI", "Tableau", "Statistics"],
    "Data Scientist":     ["Python", "Machine Learning", "Deep Learning", "SQL", "Statistics", "R"],
    "ML Engineer":        ["Python", "Machine Learning", "Deep Learning", "MLOps", "Docker", "AWS"],
    "Software Engineer":  ["Python", "Java", "Data Structures", "System Design", "Git", "SQL"],
    "Backend Developer":  ["Java", "Node.js", "REST API", "SQL", "Docker", "Redis"],
    "Frontend Developer": ["JavaScript", "React", "TypeScript", "HTML/CSS", "Vue.js", "Redux"],
    "DevOps Engineer":    ["Docker", "Kubernetes", "AWS", "Terraform", "CI/CD", "Linux"],
    "Product Manager":    ["Product Strategy", "Agile", "Data Analysis", "SQL", "Roadmapping", "Stakeholder Management"],
}

all_skills = sorted(set(s for skills in role_skills.values() for s in skills))

# ── Skill max bonus at 100% knowledge (INR) — corrected for 2025-26 market ───
# IT hiring has slowed post-2023 layoffs; salary bands compressed across roles.
# These are the ADDITIONAL amount a fully skilled person earns vs 0% on that skill.
skill_max_bonus = {
    # Data / Analytics skills
    "SQL":                    60000,   # Core data skill; widely expected
    "Python":                100000,   # Most demanded language; strong premium
    "Excel":                  30000,   # Baseline office skill
    "Power BI":               70000,   # BI demand high; dashboards everywhere
    "Tableau":                70000,   # Competitive with Power BI
    "Statistics":             90000,   # Core DS/DA; strong differentiator
    # ML / AI — GenAI surge keeps these highest in 2025-26
    "Machine Learning":      180000,   # Highest demand; LLM/GenAI wave
    "Deep Learning":         150000,   # Neural nets; strong in product companies
    "R":                      50000,   # Niche but valued in research/pharma
    "MLOps":                 130000,   # Critical for production ML; scarce skill
    # Engineering skills
    "Docker":                 90000,   # Standard now but depth still valued
    "AWS":                   130000,   # Cloud #1; certifications drive pay
    "Java":                   90000,   # Enterprise backbone; Spring Boot demand
    "Data Structures":       110000,   # Product company interview signal
    "System Design":         140000,   # Senior engineer signal; huge pay impact
    "Git":                    25000,   # Expected everywhere; very low premium
    "Node.js":                80000,   # Full-stack backend; microservices
    "REST API":               65000,   # Core backend skill
    "Redis":                  60000,   # Caching expertise; valued in scale-ups
    # Frontend skills
    "JavaScript":             70000,   # Core web; strong when deep
    "React":                 100000,   # Dominant framework; high demand 2025
    "TypeScript":             90000,   # Rising fast; strong hiring signal
    "HTML/CSS":               35000,   # Entry-level; baseline only
    "Vue.js":                 65000,   # Niche but growing
    "Redux":                  50000,   # State management; valued in large apps
    # DevOps / Infra skills
    "Kubernetes":            130000,   # High demand; container orchestration scarce
    "Terraform":             110000,   # IaC critical for cloud-native teams
    "CI/CD":                  90000,   # DevOps pipeline; strong in 2025
    "Linux":                  65000,   # Foundational for infra; depth valued
    # PM skills
    "Product Strategy":      110000,   # Core PM differentiator
    "Agile":                  50000,   # Expected but depth still valued
    "Data Analysis":          80000,   # Data-driven PM in high demand
    "Roadmapping":            70000,   # PM execution skill
    "Stakeholder Management": 60000,   # Leadership signal for senior PMs
}

# ── Base salaries: calibrated to 2025-26 verified market table ────────────────
# Back-calculated so Bihar/IT-Services/Mid-size/Bachelor/0yr/30%-skills
# matches the verified salary table exactly.
# Base = what TCS/Infosys actually pay freshers in 2025 (verified campus offers)
# Bihar + IT Services + Indian IT Giant + Bachelor + 0yr + 30% skills = 3.5-4.5L
# Recalibrated for larger skill_max_bonus values above.
base_salary = {
    "Data Analyst":       130000,  # Calibrated: Bihar/IITGiant floor ~3.5L
    "Data Scientist":     175000,  # Calibrated: Bihar/IITGiant floor ~3.8L
    "ML Engineer":        200000,  # Calibrated: Bihar/IITGiant floor ~4.0L
    "Software Engineer":  155000,  # Calibrated: Bihar/IITGiant floor ~3.6L
    "Backend Developer":  145000,  # Calibrated: Bihar/IITGiant floor ~3.5L
    "Frontend Developer": 120000,  # Calibrated: Bihar/IITGiant floor ~3.4L
    "DevOps Engineer":    165000,  # Calibrated: Bihar/IITGiant floor ~3.7L
    "Product Manager":    190000,  # Calibrated: Bihar/IITGiant floor ~3.9L
}

edu_bonus = {
    "High School":  0,       # Rarely hired in IT directly
    "Bachelor's":   40000,   # Standard B.Tech/BCA
    "Master's":    120000,   # M.Tech/MCA adds clear premium
    "PhD":         200000,   # Research/quant roles only
}

loc_bonus = {
    # 2025-26: remote work narrowing gaps slightly but metros still premium
    "Karnataka":      70000,  # Bangalore — still India's #1 IT hub
    "Maharashtra":    60000,  # Mumbai BFSI + Pune IT
    "Delhi":          55000,  # NCR: Noida/Gurgaon corridors
    "Telangana":      55000,  # Hyderabad — strong growth, near Bangalore now
    "Tamil Nadu":     45000,  # Chennai — auto+IT, stable
    "Haryana":        35000,  # Gurgaon fintech/startup
    "Gujarat":        25000,  # Ahmedabad IT parks growing slowly
    "Kerala":         20000,  # Kochi Infopark; mid-tier
    "West Bengal":    20000,  # Kolkata; limited IT base
    "Andhra Pradesh": 15000,  # Vizag SEZ; early stage
    "Punjab":         12000,  # Mohali; small cluster
    "Uttar Pradesh":  10000,  # Noida overlaps Delhi; Lucknow small
    "Rajasthan":       8000,  # Jaipur emerging slowly
    "Madhya Pradesh":  4000,  # Indore/Bhopal minimal
    "Bihar":               0, # Near zero IT presence
}

# ── Industry × Company matrix bonus (INR) — 2025-26 realistic combinations ───
# Each cell = realistic pay premium for that exact combo above bare base.
# Replaces flat industry+company bonuses which were unrealistic when combined.
#
# Key market realities baked in:
#   - Indian IT Giant in IT Services (TCS/Infosys/Wipro) = lowest pay always
#   - MNC in IT Product (Google/MS/Amazon/Razorpay) = highest pay always
#   - Startup in IT Services = rare & pays poorly (outsourcing startup)
#   - Startup in IT Product  = ESOP story; moderate cash but upside
#   - BFSI MNC (Goldman, JP Morgan tech) > BFSI Indian IT Giant (Infosys BFSI)
#   - Consulting Big4 MNC > Consulting Mid-size
#   - Healthcare pays lowest across all company types

# ── Industry × Company matrix (INR) — 2025-26 India market ───────────────────
# Columns: MNC | Indian IT Giant | Mid-size | Startup
industry_company_bonus = {

    # ── Highest paying ────────────────────────────────────────────────────────
    "IT Product": {
        "MNC":             350000,  # Google/MS/Amazon/Adobe India — peak CTC
        "Indian IT Giant":  80000,  # Rare product arm inside TCS/Infosys
        "Mid-size":        180000,  # Razorpay/Zerodha/Freshworks/BrowserStack
        "Startup":         150000,  # Series B+ product startup; ESOP upside
    },
    "Cloud & SaaS": {
        "MNC":             320000,  # AWS/Azure/GCP India engineering teams
        "Indian IT Giant":  70000,  # TCS/Infosys cloud practice arm
        "Mid-size":        200000,  # Zoho/Chargebee/Postman/Hasura — great pay
        "Startup":         160000,  # SaaS startup; recurring rev model = stable
    },
    "Fintech": {
        "MNC":             270000,  # Visa/Mastercard/Stripe India tech
        "Indian IT Giant":  55000,  # IT Giant fintech vertical
        "Mid-size":        200000,  # PhonePe/Paytm/CRED/Groww/BharatPe
        "Startup":         160000,  # Early fintech; ESOP heavy, decent cash
    },

    # ── Strong paying ─────────────────────────────────────────────────────────
    "BFSI": {
        "MNC":             230000,  # Goldman Sachs/JP Morgan/Citi India tech
        "Indian IT Giant":  50000,  # Infosys BFSI / Wipro BFSI practice
        "Mid-size":        130000,  # HDFC tech/ICICI tech/Kotak tech teams
        "Startup":          90000,  # Neo-bank or insurance startup
    },
    "Cybersecurity": {
        "MNC":             260000,  # Palo Alto/CrowdStrike/IBM Security India
        "Indian IT Giant":  60000,  # TCS Cyber/Infosys CyberNext
        "Mid-size":        170000,  # Quick Heal/Tata Elxsi security/Sectona
        "Startup":         140000,  # Cybersec startup; niche & high demand
    },
    "E-commerce": {
        "MNC":             240000,  # Amazon/Walmart/Flipkart (MNC-owned)
        "Indian IT Giant":  55000,  # IT Giant ecomm vertical
        "Mid-size":        140000,  # Meesho/Nykaa/Snapdeal/Mamaearth tech
        "Startup":         100000,  # D2C / quick-commerce startup
    },

    # ── Mid paying ────────────────────────────────────────────────────────────
    "Consulting": {
        "MNC":             180000,  # Deloitte/McKinsey/BCG/Accenture Strategy
        "Indian IT Giant":  40000,  # TCS/Infosys consulting arm — low pay
        "Mid-size":        110000,  # LTIMindtree/Mphasis/Hexaware
        "Startup":          70000,  # Boutique niche consulting firm
    },
    "Automotive & EV": {
        "MNC":             200000,  # Bosch/Continental/Tesla India tech
        "Indian IT Giant":  50000,  # TCS/Infosys automotive vertical
        "Mid-size":        140000,  # Ola Electric/Ather/Tata Motors tech
        "Startup":         110000,  # EV startup; growing sector
    },
    "Gaming": {
        "MNC":             210000,  # EA/Ubisoft/Activision India studios
        "Indian IT Giant":  30000,  # Rare — IT giants rarely in gaming
        "Mid-size":        150000,  # Nazara/Dream11/MPL/Games24x7
        "Startup":         120000,  # Mobile gaming startup; moderate pay
    },
    "Media & OTT": {
        "MNC":             190000,  # Netflix/Disney Hotstar/Warner India tech
        "Indian IT Giant":  35000,  # IT Giant media vertical
        "Mid-size":        120000,  # Zee tech/Jio Studios/Sony LIV tech
        "Startup":          90000,  # Content-tech startup
    },
    "IT Services": {
        "MNC":             150000,  # Accenture/Capgemini/IBM/Cognizant India
        "Indian IT Giant":  15000,  # TCS/Infosys/Wipro/HCL — fixed low bands
        "Mid-size":         70000,  # Mphasis/Hexaware/Birlasoft/Mastech
        "Startup":          30000,  # Small outsourcing shop; limited growth
    },

    # ── Lower paying ──────────────────────────────────────────────────────────
    "EdTech": {
        "MNC":             140000,  # Coursera/Udemy India tech teams
        "Indian IT Giant":  30000,  # IT Giant edtech vertical (rare)
        "Mid-size":         90000,  # upGrad/Unacademy — post-funding-winter cut
        "Startup":          60000,  # EdTech startup; BYJU's collapse hurt sector
    },
    "Logistics & Supply Chain": {
        "MNC":             160000,  # DHL/FedEx/Maersk India tech
        "Indian IT Giant":  40000,  # TCS/Infosys logistics vertical
        "Mid-size":        100000,  # Delhivery/Shiprocket/Porter/Rivigo
        "Startup":          70000,  # Last-mile delivery startup
    },
    "Healthcare & Pharma": {
        "MNC":             130000,  # Philips/Siemens/Abbott India tech
        "Indian IT Giant":  25000,  # IT Giant pharma vertical
        "Mid-size":         75000,  # Practo/1mg/Tata 1mg/Dr Reddy's tech
        "Startup":          50000,  # HealthTech early stage; lowest cash
    },

    # ── Lowest paying ─────────────────────────────────────────────────────────
    "Government & PSU": {
        "MNC":              50000,  # Rare; foreign govt orgs in India
        "Indian IT Giant":   8000,  # TCS/Infosys govt projects — absolute lowest
        "Mid-size":         12000,  # NIC vendors/CDAC — below IT Services Indian IT Giant
        "Startup":           8000,  # GovTech startup; job security > pay
    },
}

# ── Generate dataset ──────────────────────────────────────────────────────────
data = {
    "job_title":       np.random.choice(job_titles, n),
    "education":       np.random.choice(education_levels, n),
    "location":        np.random.choice(locations, n),
    "years_experience": np.random.randint(0, 26, n),
    "age":             np.random.randint(21, 60, n),
    "industry":        np.random.choice(industries, n),
    "company_type":    np.random.choice(company_types, n),
}

# Initialise all skill columns to 0
for skill in all_skills:
    data[f"skill_{skill}"] = np.zeros(n, dtype=float)

# Fill knowledge levels only for skills relevant to each row's role
for i in range(n):
    for skill in role_skills[data["job_title"][i]]:
        data[f"skill_{skill}"][i] = np.random.uniform(0, 100)

# ── Compute interaction features ──────────────────────────────────────────────
# avg_skill_pct : mean knowledge % across role's skills (0–100)
# exp_x_skill   : experience × avg skill — captures "senior + skilled" premium
avg_skill_pct = np.zeros(n)
for i in range(n):
    skills_i = role_skills[data["job_title"][i]]
    avg_skill_pct[i] = np.mean([data[f"skill_{s}"][i] for s in skills_i])

data["avg_skill_pct"] = avg_skill_pct
data["exp_x_skill"]   = data["years_experience"] * avg_skill_pct  # max = 25*100 = 2500

# ── Compute salaries ──────────────────────────────────────────────────────────
# Weightage logic:
#   - Base experience value:  exp * 35,000  (floor even with low skills)
#   - Skill-weighted exp:     exp * avg_skill_pct/100 * 40,000
#     → 0 yrs + 100% skills  = skill bonus only (good fresher)
#     → 10 yrs + 100% skills = 35k*10 + 40k*10 = 750k extra (expert senior)
#     → 10 yrs + 20% skills  = 35k*10 + 8k*10  = 430k extra (rusty senior)
#   - Skill knowledge bonus:  per-skill (knowledge/100 * max_bonus)
salaries = []
for i in range(n):
    exp   = data["years_experience"][i]
    avgs  = avg_skill_pct[i] / 100          # 0.0 – 1.0

    # Experience weightage — 2025-26 India IT market
    #
    # exp_base: guaranteed per year regardless of skills.
    #   Reflects domain knowledge, ownership, communication, reliability
    #   that only time in the industry builds — ₹80K/yr.
    #   7yr  = ₹5.6L extra | 15yr = ₹12L extra | 25yr = ₹20L extra
    #
    # exp_skill_bonus: ADDITIONAL reward when experience is backed by strong skills.
    #   High exp + low skills  → only base (rusty senior, slow growth)
    #   High exp + high skills → base + full amplifier (expert senior, top pay)
    #   ₹50K/yr at 100% skills.
    #   7yr at 85% = ₹3.0L | 7yr at 30% = ₹1.1L
    #
    # Combined: 7yr senior (85% skills) earns ₹8.6L MORE than fresher
    #           25yr expert (100% skills) earns ₹32.5L MORE than fresher
    # exp_base: guaranteed per year for domain knowledge, ownership, reliability
    # Kept intentionally LOW so that skills remain the key differentiator.
    # 10yr/20%-skills should NOT overtake 5yr/80%-skills.
    # ₹40K/yr floor  →  10yr = +₹4L guaranteed above fresher base
    exp_base        = exp * 40000
    # exp_skill_bonus: the MAIN driver of senior pay — scales hard with skill level
    # ₹120K/yr at 100% skills
    # 5yr/80%  = 5 * 0.80 * 120K = +₹4.8L   →  total exp contribution ₹6.8L
    # 10yr/20% = 10 * 0.20 * 120K = +₹2.4L  →  total exp contribution ₹6.4L  (LESS than 5yr/80%)
    # 10yr/90% = 10 * 0.90 * 120K = +₹10.8L →  total exp contribution ₹14.8L (expert senior)
    exp_skill_bonus = exp * avgs * 120000

    sal = (
        base_salary[data["job_title"][i]]
        + edu_bonus[data["education"][i]]
        + loc_bonus[data["location"][i]]
        + industry_company_bonus[data["industry"][i]][data["company_type"][i]]
        + exp_base
        + exp_skill_bonus
    )
    # Per-skill knowledge contribution
    for skill in role_skills[data["job_title"][i]]:
        sal += (data[f"skill_{skill}"][i] / 100) * skill_max_bonus[skill]

    sal += np.random.normal(0, 10000)
    salaries.append(max(220000, sal))

data["salary"] = salaries
df = pd.DataFrame(data)

# ── Encode categoricals ───────────────────────────────────────────────────────
le_job = LabelEncoder()
le_edu = LabelEncoder()
le_loc = LabelEncoder()
le_ind = LabelEncoder()
le_com = LabelEncoder()

df["job_enc"] = le_job.fit_transform(df["job_title"])
df["edu_enc"] = le_edu.fit_transform(df["education"])
df["loc_enc"] = le_loc.fit_transform(df["location"])
df["ind_enc"] = le_ind.fit_transform(df["industry"])
df["com_enc"] = le_com.fit_transform(df["company_type"])

skill_cols   = [f"skill_{s}" for s in all_skills]
feature_cols = ["job_enc", "edu_enc", "loc_enc", "years_experience", "age",
                "ind_enc", "com_enc", "avg_skill_pct", "exp_x_skill"] + skill_cols

X = df[feature_cols]
y = df["salary"]

model = GradientBoostingRegressor(n_estimators=300, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X, y)

os.makedirs("model", exist_ok=True)
with open("model/salary_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("model/encoders.pkl", "wb") as f:
    pickle.dump({
        "job": le_job, "edu": le_edu, "loc": le_loc, "ind": le_ind, "com": le_com,
        "role_skills":            role_skills,
        "all_skills":             all_skills,
        "skill_max_bonus":        skill_max_bonus,
        "industry_company_bonus": industry_company_bonus,
    }, f)

print("Model trained and saved to model/")
print(f"Features: {len(feature_cols)}")
print(f"R² score: {model.score(X, y):.4f}")
