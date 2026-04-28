"""
myAdvisr — AI-Powered Academic Advisor
Clarkson University | Innovation-Based AI Solution
Built with Streamlit + Anthropic Claude API
Data sourced from clarkson.edu, April 2026
"""

import streamlit as st
from anthropic import Anthropic
import math

st.set_page_config(
    page_title="myAdvisr | Clarkson University",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root{--green:#004e42;--green-dark:#003530;--green-mid:#005c4e;--gold:#ffcd00;
      --gold-dim:#c9a000;--olive:#7a9a01;--coral:#cf4520;--blue:#418fde;
      --navy:#002d72;--text:#1a1a1a;--muted:#555;--light-bg:#f0f7f5;--card-bg:#fff;}
html,body,[class*="css"]{font-family:'Segoe UI',Arial,sans-serif;}
.brand-bar{height:5px;background:linear-gradient(90deg,#004e42 60%,#ffcd00 100%);margin:-1rem -1rem 1.5rem -1rem;}
.page-header{background:var(--green);color:#fff;padding:1.5rem 2rem;border-radius:12px;margin-bottom:1.5rem;display:flex;align-items:center;gap:1rem;}
.page-header h1{margin:0;font-size:1.6rem;color:#fff;}
.page-header p{margin:0;color:rgba(255,255,255,0.75);font-size:0.9rem;}
.logo-badge{background:var(--gold);color:var(--green);font-weight:800;font-size:1rem;padding:8px 14px;border-radius:10px;white-space:nowrap;}
.metric-row{display:flex;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap;}
.metric-card{background:var(--card-bg);border:1.5px solid #e0ece9;border-radius:12px;padding:1.1rem 1.4rem;flex:1;min-width:140px;}
.metric-card.accent{border-color:var(--gold);border-width:2px;}
.metric-label{font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);font-weight:600;margin-bottom:4px;}
.metric-value{font-size:2rem;font-weight:700;color:var(--green);line-height:1;margin-bottom:2px;}
.metric-value.gold{color:var(--gold-dim);}
.metric-sub{font-size:0.75rem;color:var(--muted);}
.alert-card{border-radius:10px;padding:0.9rem 1.1rem;margin-bottom:0.7rem;display:flex;gap:0.8rem;align-items:flex-start;border-left:4px solid;}
.alert-card.warn{background:#fffbea;border-color:var(--gold);}
.alert-card.info{background:#eef7f0;border-color:var(--olive);}
.alert-card.crit{background:#fdf0eb;border-color:var(--coral);}
.alert-dot{width:10px;height:10px;border-radius:50%;margin-top:4px;flex-shrink:0;}
.dot-warn{background:var(--gold-dim);}.dot-info{background:var(--olive);}.dot-crit{background:var(--coral);}
.alert-text{font-size:0.85rem;color:var(--text);line-height:1.5;}
.alert-text b{color:var(--green);}
.prog-wrap{background:#e0ece9;border-radius:6px;height:10px;margin:6px 0 4px;overflow:hidden;}
.prog-bar{height:100%;border-radius:6px;background:linear-gradient(90deg,var(--green),var(--olive));}
.section-head{font-size:1.15rem;font-weight:700;color:var(--green);border-bottom:2px solid var(--gold);padding-bottom:6px;margin:1.4rem 0 1rem;}
.sem-block{background:var(--card-bg);border:1px solid #e0ece9;border-radius:10px;margin-bottom:1rem;overflow:hidden;}
.sem-header{background:var(--green);color:#fff;padding:0.6rem 1rem;display:flex;justify-content:space-between;align-items:center;font-size:0.85rem;font-weight:600;}
.course-row{display:flex;align-items:center;gap:1rem;padding:0.55rem 1rem;border-bottom:1px solid #f5f5f5;font-size:0.82rem;}
.course-row:last-child{border-bottom:none;}
.course-code{color:var(--muted);width:90px;flex-shrink:0;font-family:monospace;}
.course-name{flex:1;color:var(--text);}
.course-cr{color:var(--muted);width:36px;text-align:right;flex-shrink:0;}
.badge{padding:2px 10px;border-radius:100px;font-size:0.7rem;font-weight:600;}
.badge-done{background:#eef7e6;color:#3a6e00;}
.badge-plan{background:#fffbea;color:#8a6c00;}
.badge-rec{background:#fdf0eb;color:#8a2a00;}
.career-card{background:var(--card-bg);border:1px solid #e0ece9;border-radius:10px;padding:1.1rem 1.3rem;margin-bottom:1rem;}
.career-title{font-size:1rem;font-weight:700;color:var(--green);margin-bottom:6px;}
.match-wrap{background:#e0ece9;border-radius:3px;height:5px;display:inline-block;width:90px;vertical-align:middle;margin-right:6px;}
.match-fill{height:100%;border-radius:3px;background:var(--gold-dim);}
.skill-tag{display:inline-block;padding:3px 10px;border:1px solid #d0e8e4;border-radius:100px;font-size:0.72rem;color:var(--muted);margin:3px 3px 3px 0;}
.skill-gap{border-color:#f5c4b0;color:var(--coral);}
.resource-card{background:var(--card-bg);border:1px solid #e0ece9;border-radius:10px;padding:1rem 1.3rem;margin-bottom:0.8rem;}
.resource-tag{padding:3px 10px;border-radius:100px;font-size:0.7rem;font-weight:600;white-space:nowrap;}
.tag-tutoring{background:#eef7e6;color:#3a6e00;}.tag-career{background:#fffbea;color:#8a6c00;}
.tag-health{background:#fdf0eb;color:#8a2a00;}.tag-financial{background:#fffbea;color:#8a6c00;}
.tag-writing{background:#eef7e6;color:#3a6e00;}.tag-registration{background:#e8eef8;color:#1a3a6e;}
.tag-accessibility{background:#f0eef8;color:#3a2a6e;}.tag-international{background:#eef7f8;color:#1a5a6e;}
.chat-ai{background:var(--light-bg);border:1px solid #d0e8e4;border-radius:4px 14px 14px 14px;padding:0.7rem 1rem;margin:0.4rem 0;font-size:0.88rem;color:var(--text);line-height:1.55;max-width:90%;}
.chat-user{background:var(--green);color:#fff;border-radius:14px 4px 14px 14px;padding:0.7rem 1rem;margin:0.4rem 0 0.4rem auto;font-size:0.88rem;line-height:1.55;max-width:85%;text-align:right;}
.chat-label{font-size:0.7rem;font-weight:600;letter-spacing:0.05em;margin-bottom:2px;}
.label-ai{color:var(--muted);}.label-user{color:var(--muted);text-align:right;}
section[data-testid="stSidebar"]{background:var(--green-dark) !important;}
section[data-testid="stSidebar"] *{color:#c8e6e2 !important;}
section[data-testid="stSidebar"] h1,section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{color:var(--gold) !important;}
div[data-testid="stVerticalBlock"]{gap:0.5rem;}
.stButton>button{background:var(--gold) !important;color:var(--green) !important;border:none !important;
  font-weight:700 !important;border-radius:100px !important;padding:0.4rem 1.4rem !important;}
.stButton>button:hover{background:var(--gold-dim) !important;}
.prog-info{font-size:0.78rem;color:#555;padding:6px 10px;background:#f0f7f5;border-radius:6px;margin-bottom:12px;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  PROGRAM DATA  —  sourced directly from clarkson.edu, April 2026
#  credits_required = official total credits per program page
#  credits_per_sem  = typical credits per semester (for semesters-left calc)
# ═══════════════════════════════════════════════════════════════════════════════

# ── UNDERGRADUATE PROGRAMS ──────────────────────────────────────────────────
UG_PROGRAMS = {
    "Coulter School of Engineering & Applied Sciences": {
        "Aeronautical Engineering":     {"cr": 120, "cps": 16},
        "Chemical Engineering":         {"cr": 120, "cps": 16},
        "Civil Engineering":            {"cr": 120, "cps": 16},
        "Computer Engineering":         {"cr": 120, "cps": 16},
        "Computer Science":             {"cr": 120, "cps": 16},
        "Data Science":                 {"cr": 120, "cps": 16},
        "Electrical Engineering":       {"cr": 120, "cps": 16},
        "Environmental Engineering":    {"cr": 120, "cps": 16},
        "Mechanical Engineering":       {"cr": 120, "cps": 16},
        "Software Engineering":         {"cr": 120, "cps": 16},
        "Engineering & Management":     {"cr": 120, "cps": 16},
        "Engineering Studies (undecided)": {"cr": 120, "cps": 16},
    },
    "Reh School of Business": {
        "Business Administration":                    {"cr": 120, "cps": 15},
        "Business Analytics (STEM)":                  {"cr": 120, "cps": 15},
        "Business Intelligence & Data Analytics":     {"cr": 120, "cps": 15},
        "Financial Information & Analysis":           {"cr": 120, "cps": 15},
        "Global Supply Chain Management":             {"cr": 120, "cps": 15},
        "Innovation & Entrepreneurship":              {"cr": 120, "cps": 15},
        "Business Studies (undecided)":               {"cr": 120, "cps": 15},
    },
    "Lewis School of Health & Life Sciences": {
        "Applied Mathematics & Statistics": {"cr": 120, "cps": 15},
        "Biology":                          {"cr": 120, "cps": 15},
        "Biomolecular Science":             {"cr": 120, "cps": 15},
        "Chemistry":                        {"cr": 120, "cps": 15},
        "Environmental Health Science":     {"cr": 120, "cps": 15},
        "Healthcare":                       {"cr": 120, "cps": 15},
        "Mathematics":                      {"cr": 120, "cps": 15},
        "Mathematical Economics":           {"cr": 120, "cps": 15},
        "Physics":                          {"cr": 120, "cps": 15},
        "Psychology":                       {"cr": 120, "cps": 15},
    },
    "Institute for a Sustainable Environment": {
        "Digital Arts & Sciences":             {"cr": 120, "cps": 15},
        "Environmental Science & Policy":      {"cr": 120, "cps": 15},
        "Interdisciplinary Liberal Studies":   {"cr": 120, "cps": 15},
        "Interdisciplinary Social Sciences":   {"cr": 120, "cps": 15},
    },
}

# ── GRADUATE PROGRAMS ───────────────────────────────────────────────────────
# cps = typical credits per semester full-time
# dur = typical semesters to complete (for display)
GRAD_PROGRAMS = {
    "Engineering & Applied Sciences — MS Programs": {
        "Chemical Engineering (MS)":                        {"cr": 30, "cps": 9,  "dur": 4},
        "Chemistry (MS)":                                   {"cr": 30, "cps": 9,  "dur": 4},
        "Civil & Environmental Engineering (MS)":           {"cr": 30, "cps": 9,  "dur": 4},
        "Computer Science (MS)":                            {"cr": 30, "cps": 15, "dur": 2},
        "Electrical & Computer Engineering (MS)":           {"cr": 30, "cps": 9,  "dur": 4},
        "Electrical & Computer Engineering — Power (MS)":   {"cr": 30, "cps": 9,  "dur": 4},
        "Environmental Science & Engineering (MS)":         {"cr": 30, "cps": 9,  "dur": 4},
        "Mathematics (MS)":                                 {"cr": 30, "cps": 9,  "dur": 4},
        "Mechanical Engineering (MS)":                      {"cr": 30, "cps": 9,  "dur": 4},
        "Physics (MS)":                                     {"cr": 30, "cps": 9,  "dur": 4},
    },
    "Engineering & Applied Sciences — PhD Programs": {
        "Chemical Engineering (PhD)":                       {"cr": 90, "cps": 9,  "dur": 10},
        "Chemistry (PhD)":                                  {"cr": 90, "cps": 9,  "dur": 10},
        "Civil & Environmental Engineering (PhD)":          {"cr": 90, "cps": 9,  "dur": 10},
        "Computer Science (PhD)":                           {"cr": 90, "cps": 9,  "dur": 8},
        "Electrical & Computer Engineering (PhD)":          {"cr": 90, "cps": 9,  "dur": 10},
        "Environmental Science & Engineering (PhD)":        {"cr": 90, "cps": 9,  "dur": 10},
        "Materials Science & Engineering (PhD)":            {"cr": 90, "cps": 9,  "dur": 10},
        "Mathematics (PhD)":                                {"cr": 90, "cps": 9,  "dur": 10},
        "Mechanical Engineering (PhD)":                     {"cr": 90, "cps": 9,  "dur": 10},
        "Physics (PhD)":                                    {"cr": 90, "cps": 9,  "dur": 10},
    },
    "Interdisciplinary Graduate Programs": {
        "Applied Data Science (MS) — STEM":                 {"cr": 36, "cps": 12, "dur": 3},
        "Bioscience & Biotechnology (MS) — STEM":           {"cr": 30, "cps": 9,  "dur": 4},
        "Bioscience & Biotechnology (PhD)":                 {"cr": 90, "cps": 9,  "dur": 10},
        "Construction Engineering Management (MS)":         {"cr": 30, "cps": 9,  "dur": 4},
        "Engineering Management (MS)":                      {"cr": 30, "cps": 9,  "dur": 4},
        "Engineering Science (MS)":                         {"cr": 30, "cps": 9,  "dur": 4},
        "Engineering Science (PhD)":                        {"cr": 90, "cps": 9,  "dur": 10},
    },
    "Reh School of Business — Graduate": {
        "MBA — Residential (35 cr, 9 months–2 years)":      {"cr": 35, "cps": 18, "dur": 2},
        "MBA — Online (36 cr, ~1.5 years)":                 {"cr": 36, "cps": 9,  "dur": 4},
        "MBA — Business Analytics (STEM, 35 cr)":           {"cr": 35, "cps": 18, "dur": 2},
        "MBA — Global Supply Chain Management (35 cr)":     {"cr": 35, "cps": 18, "dur": 2},
        "MBA — Healthcare Management (42 cr)":              {"cr": 42, "cps": 12, "dur": 4},
        "MS — Applied Data Science / MBA Dual (56 cr)":     {"cr": 56, "cps": 12, "dur": 5},
        "MS — Clinical Leadership in Healthcare Mgmt":      {"cr": 30, "cps": 9,  "dur": 4},
        "MS — Healthcare Data Analytics":                   {"cr": 30, "cps": 9,  "dur": 4},
        "Advanced Business Certificate (12 cr)":            {"cr": 12, "cps": 9,  "dur": 2},
    },
    "Lewis School of Health & Life Sciences — Graduate": {
        "Occupational Therapy (MS, 92 cr, 6 semesters)":   {"cr": 92, "cps": 16, "dur": 6},
        "Physical Therapy (DPT, 105 cr, 8 semesters)":     {"cr": 105,"cps": 13, "dur": 8},
        "Physician Assistant Studies (MS, 28 months)":      {"cr": 115,"cps": 17, "dur": 7},
    },
    "Certificates & Advanced Credentials": {
        "Business of Energy (Advanced Certificate)":        {"cr": 12, "cps": 6,  "dur": 2},
        "Construction Engineering Management (Certificate)":{"cr": 12, "cps": 6,  "dur": 2},
        "Digital Transformation (Advanced Certificate)":    {"cr": 12, "cps": 6,  "dur": 2},
        "Power Systems Engineering (Advanced Certificate)": {"cr": 12, "cps": 6,  "dur": 2},
    },
}

YEARS = [
    "Freshman (1st year)", "Sophomore (2nd year)",
    "Junior (3rd year)", "Senior (4th year)",
    "Graduate Student — Year 1", "Graduate Student — Year 2",
    "Graduate Student — Year 3+",
]

CAREER_OPTIONS = [
    "Software Engineering", "Data Science & AI",
    "Mechanical / Aerospace Engineering", "Civil & Environmental Engineering",
    "Chemical / Biomolecular Engineering", "Electrical Engineering",
    "Product Management", "Supply Chain & Logistics",
    "Finance & Consulting", "Research & Academia",
    "Entrepreneurship", "Healthcare & Biomedical",
    "Physical / Occupational Therapy", "Physician Assistant",
    "Government & Policy", "Other (describe below)",
]

# ── COURSE PLANS (representative; based on Clarkson catalog) ────────────────
# Full undergraduate plans
UG_COURSE_PLANS = {
    "Computer Science": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"CS 141","name":"Intro to Computer Science I","cr":4},
         {"code":"MA 131","name":"Calculus I","cr":3},
         {"code":"CM 131","name":"General Chemistry I","cr":3}],
        [{"code":"CS 142","name":"Intro to Computer Science II","cr":3},
         {"code":"MA 132","name":"Calculus II","cr":3},
         {"code":"CS 242","name":"Advanced Programming","cr":3},
         {"code":"CM 132","name":"General Chemistry II","cr":3},
         {"code":"MA 211","name":"Foundations of Math","cr":3}],
        [{"code":"CS 344","name":"Algorithms & Data Structures","cr":3},
         {"code":"CS 348","name":"Computer Organization","cr":3},
         {"code":"MA 232","name":"Calculus III","cr":3},
         {"code":"STAT 282","name":"Probability & Statistics","cr":3},
         {"code":"CS 346","name":"Computer Programming Languages","cr":3}],
        [{"code":"CS 444","name":"Operating Systems","cr":3},
         {"code":"CS 451","name":"Computer Networks","cr":3},
         {"code":"CS 447","name":"Machine Learning","cr":3},
         {"code":"CS 443","name":"Database Systems","cr":3},
         {"code":"CS 499","name":"Professional Experience","cr":3}],
    ],
    "Mechanical Engineering": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"MA 131","name":"Calculus I","cr":3},
         {"code":"CM 131","name":"General Chemistry I","cr":3},
         {"code":"ES 110","name":"Engineering Graphics","cr":3},
         {"code":"PH 131","name":"Physics I: Mechanics","cr":3}],
        [{"code":"MA 132","name":"Calculus II","cr":3},
         {"code":"PH 132","name":"Physics II: E&M","cr":3},
         {"code":"ES 220","name":"Statics","cr":3},
         {"code":"ME 170","name":"Engineering Graphics & CAD","cr":3},
         {"code":"CM 132","name":"General Chemistry II","cr":3}],
        [{"code":"MA 231","name":"Differential Equations","cr":3},
         {"code":"ME 221","name":"Dynamics","cr":3},
         {"code":"ME 323","name":"Thermodynamics I","cr":3},
         {"code":"ME 332","name":"Mechanics of Materials","cr":3},
         {"code":"ES 250","name":"Electrical Science","cr":3}],
        [{"code":"ME 422","name":"Heat Transfer","cr":3},
         {"code":"ME 424","name":"Fluid Mechanics","cr":3},
         {"code":"ME 456","name":"Senior Design I","cr":3},
         {"code":"ME 457","name":"Senior Design II","cr":3},
         {"code":"ME Elective","name":"Professional Elective","cr":3}],
    ],
    "Chemical Engineering": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"MA 131","name":"Calculus I","cr":3},
         {"code":"CM 131","name":"General Chemistry I","cr":4},
         {"code":"PH 131","name":"Physics I: Mechanics","cr":3}],
        [{"code":"MA 132","name":"Calculus II","cr":3},
         {"code":"CM 132","name":"General Chemistry II","cr":4},
         {"code":"CHE 211","name":"Material & Energy Balances","cr":3},
         {"code":"ES 220","name":"Statics","cr":3},
         {"code":"BY 141","name":"General Biology I","cr":4}],
        [{"code":"MA 231","name":"Differential Equations","cr":3},
         {"code":"CM 231","name":"Organic Chemistry I","cr":3},
         {"code":"CHE 312","name":"ChE Thermodynamics I","cr":3},
         {"code":"CHE 321","name":"Fluid Mechanics","cr":3},
         {"code":"CHE 331","name":"Heat & Mass Transfer","cr":3}],
        [{"code":"CHE 411","name":"Chemical Reaction Engineering","cr":3},
         {"code":"CHE 421","name":"Process Control","cr":3},
         {"code":"CHE 451","name":"Senior Design I","cr":3},
         {"code":"CHE 452","name":"Senior Design II","cr":3},
         {"code":"CHE Elective","name":"Professional Elective","cr":3}],
    ],
    "Civil Engineering": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"MA 131","name":"Calculus I","cr":3},
         {"code":"CM 131","name":"General Chemistry I","cr":4},
         {"code":"PH 131","name":"Physics I: Mechanics","cr":3}],
        [{"code":"MA 132","name":"Calculus II","cr":3},
         {"code":"ES 220","name":"Statics","cr":3},
         {"code":"CE 201","name":"Civil Engineering Materials","cr":3},
         {"code":"PH 132","name":"Physics II: E&M","cr":3},
         {"code":"CM 132","name":"General Chemistry II","cr":4}],
        [{"code":"MA 231","name":"Differential Equations","cr":3},
         {"code":"CE 221","name":"Dynamics","cr":3},
         {"code":"CE 322","name":"Structural Analysis","cr":3},
         {"code":"CE 331","name":"Fluid Mechanics","cr":3},
         {"code":"CE 341","name":"Geotechnical Engineering","cr":3}],
        [{"code":"CE 421","name":"Structural Design","cr":3},
         {"code":"CE 431","name":"Environmental Engineering","cr":3},
         {"code":"CE 451","name":"Senior Design I","cr":3},
         {"code":"CE 452","name":"Senior Design II","cr":3},
         {"code":"CE Elective","name":"Professional Elective","cr":3}],
    ],
    "Electrical Engineering": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"MA 131","name":"Calculus I","cr":3},
         {"code":"PH 131","name":"Physics I: Mechanics","cr":3},
         {"code":"CM 131","name":"General Chemistry I","cr":4}],
        [{"code":"MA 132","name":"Calculus II","cr":3},
         {"code":"PH 132","name":"Physics II: E&M","cr":3},
         {"code":"EE 221","name":"Linear Circuits","cr":3},
         {"code":"EE 264","name":"Intro to Digital Design","cr":3},
         {"code":"ES 220","name":"Statics","cr":3}],
        [{"code":"MA 231","name":"Differential Equations","cr":3},
         {"code":"EE 321","name":"Systems & Signal Processing","cr":3},
         {"code":"EE 331","name":"Energy Conversion","cr":3},
         {"code":"EE 333","name":"Power System Engineering","cr":3},
         {"code":"EE 341","name":"Microelectronic Circuits","cr":3}],
        [{"code":"EE 381","name":"Electromagnetic Fields & Waves","cr":3},
         {"code":"EE 451","name":"Senior Design I","cr":3},
         {"code":"EE 452","name":"Senior Design II","cr":3},
         {"code":"EE Elective","name":"EE Professional Elective","cr":3},
         {"code":"EE Elective 2","name":"EE Technical Elective","cr":3}],
    ],
    "Aeronautical Engineering": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"MA 131","name":"Calculus I","cr":3},
         {"code":"PH 131","name":"Physics I: Mechanics","cr":3},
         {"code":"CM 131","name":"General Chemistry I","cr":4}],
        [{"code":"MA 132","name":"Calculus II","cr":3},
         {"code":"PH 132","name":"Physics II: E&M","cr":3},
         {"code":"ES 220","name":"Statics","cr":3},
         {"code":"ME 170","name":"Engineering Graphics & CAD","cr":3},
         {"code":"AE 160","name":"Intro to Aerospace Engineering","cr":3}],
        [{"code":"MA 231","name":"Differential Equations","cr":3},
         {"code":"ME 221","name":"Dynamics","cr":3},
         {"code":"ME 323","name":"Thermodynamics I","cr":3},
         {"code":"AE 324","name":"Aerodynamics","cr":3},
         {"code":"AE 333","name":"Aerospace Structures","cr":3}],
        [{"code":"AE 421","name":"Flight Dynamics & Control","cr":3},
         {"code":"AE 432","name":"Propulsion Systems","cr":3},
         {"code":"AE 451","name":"Senior Design I","cr":3},
         {"code":"AE 452","name":"Senior Design II","cr":3},
         {"code":"AE Elective","name":"Aerospace Elective","cr":3}],
    ],
    "Data Science": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"CS 141","name":"Intro to Computer Science I","cr":4},
         {"code":"MA 131","name":"Calculus I","cr":3},
         {"code":"STAT 282","name":"Probability & Statistics","cr":3}],
        [{"code":"CS 142","name":"Intro to Computer Science II","cr":3},
         {"code":"MA 132","name":"Calculus II","cr":3},
         {"code":"CS 344","name":"Algorithms & Data Structures","cr":3},
         {"code":"STAT 383","name":"Applied Statistics","cr":3},
         {"code":"MA 211","name":"Foundations of Math","cr":3}],
        [{"code":"CS 447","name":"Machine Learning","cr":3},
         {"code":"CS 443","name":"Database Systems","cr":3},
         {"code":"CS 453","name":"Data Visualization","cr":3},
         {"code":"MA 335","name":"Linear Algebra","cr":3},
         {"code":"DS Elective","name":"Data Science Elective","cr":3}],
        [{"code":"CS 547","name":"Deep Learning","cr":3},
         {"code":"CS 543","name":"Big Data Analytics","cr":3},
         {"code":"CS 499","name":"Professional Experience","cr":3},
         {"code":"DS Capstone","name":"Data Science Capstone","cr":6}],
    ],
    "Business Administration": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"SB 113","name":"Entrepreneurship & Business Innovation","cr":3},
         {"code":"AC 201","name":"Financial Accounting","cr":3},
         {"code":"MA 131","name":"Calculus I","cr":3}],
        [{"code":"EC 200","name":"Principles of Economics","cr":3},
         {"code":"AC 202","name":"Managerial Accounting","cr":3},
         {"code":"MG 201","name":"Management Principles","cr":3},
         {"code":"MK 201","name":"Marketing Principles","cr":3},
         {"code":"IS 201","name":"Business Info Systems","cr":3}],
        [{"code":"FI 301","name":"Financial Management","cr":3},
         {"code":"MG 301","name":"Organizational Behavior","cr":3},
         {"code":"MK 301","name":"Marketing Management","cr":3},
         {"code":"BA 301","name":"Business Analytics","cr":3},
         {"code":"BA Elective","name":"Business Elective","cr":3}],
        [{"code":"MG 401","name":"Strategic Management","cr":3},
         {"code":"Intl Exp","name":"International Experience (required)","cr":3},
         {"code":"BA 499","name":"Professional Experience","cr":3},
         {"code":"BA Elective 2","name":"Senior Elective","cr":3},
         {"code":"BA Elective 3","name":"Senior Elective","cr":3}],
    ],
    "Global Supply Chain Management": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"SB 113","name":"Entrepreneurship & Business Innovation","cr":3},
         {"code":"SCM 201","name":"Intro to Supply Chain Mgmt","cr":3},
         {"code":"EC 200","name":"Principles of Economics","cr":3}],
        [{"code":"AC 201","name":"Financial Accounting","cr":3},
         {"code":"STAT 282","name":"Statistics for Business","cr":3},
         {"code":"MG 201","name":"Management Principles","cr":3},
         {"code":"IS 201","name":"Business Info Systems","cr":3},
         {"code":"Intl Exp","name":"International Experience","cr":3}],
        [{"code":"SCM 301","name":"Operations Management","cr":3},
         {"code":"SCM 311","name":"Logistics & Transportation","cr":3},
         {"code":"SCM 321","name":"Global Sourcing","cr":3},
         {"code":"FI 301","name":"Financial Management","cr":3},
         {"code":"SCM Elective","name":"SCM Elective","cr":3}],
        [{"code":"SCM 401","name":"Supply Chain Strategy","cr":3},
         {"code":"SCM 421","name":"Sustainable Supply Chains","cr":3},
         {"code":"MG 401","name":"Strategic Management","cr":3},
         {"code":"SCM 499","name":"Professional Experience","cr":3},
         {"code":"SCM Elective 2","name":"SCM Senior Elective","cr":3}],
    ],
    "Financial Information & Analysis": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"SB 113","name":"Entrepreneurship & Business Innovation","cr":3},
         {"code":"AC 201","name":"Financial Accounting","cr":3},
         {"code":"MA 131","name":"Calculus I","cr":3}],
        [{"code":"EC 200","name":"Principles of Economics","cr":3},
         {"code":"AC 202","name":"Managerial Accounting","cr":3},
         {"code":"FI 201","name":"Introduction to Finance","cr":3},
         {"code":"STAT 282","name":"Statistics for Business","cr":3},
         {"code":"IS 201","name":"Business Info Systems","cr":3}],
        [{"code":"FI 301","name":"Financial Management","cr":3},
         {"code":"FI 311","name":"Investments","cr":3},
         {"code":"AC 301","name":"Intermediate Accounting I","cr":3},
         {"code":"EC 301","name":"Intermediate Microeconomics","cr":3},
         {"code":"FI Elective","name":"Finance Elective","cr":3}],
        [{"code":"FI 401","name":"Corporate Finance","cr":3},
         {"code":"FI 411","name":"Financial Modeling","cr":3},
         {"code":"MG 401","name":"Strategic Management","cr":3},
         {"code":"FI 499","name":"Professional Experience","cr":3},
         {"code":"Intl Exp","name":"International Experience (required)","cr":3}],
    ],
    "Innovation & Entrepreneurship": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"SB 113","name":"Entrepreneurship & Business Innovation","cr":3},
         {"code":"IE 201","name":"Principles of Innovation","cr":3},
         {"code":"MA 131","name":"Calculus I","cr":3}],
        [{"code":"MG 201","name":"Management Principles","cr":3},
         {"code":"MK 201","name":"Marketing Principles","cr":3},
         {"code":"AC 201","name":"Financial Accounting","cr":3},
         {"code":"IE 211","name":"Design Thinking","cr":3},
         {"code":"Intl Exp","name":"International Experience","cr":3}],
        [{"code":"IE 301","name":"Venture Creation","cr":3},
         {"code":"FI 301","name":"Financial Management","cr":3},
         {"code":"MK 301","name":"Marketing Management","cr":3},
         {"code":"IE 311","name":"Social Entrepreneurship","cr":3},
         {"code":"IE Elective","name":"IE Elective","cr":3}],
        [{"code":"IE 401","name":"New Venture Launch","cr":3},
         {"code":"MG 401","name":"Strategic Management","cr":3},
         {"code":"IE 411","name":"Entrepreneurial Finance","cr":3},
         {"code":"IE 499","name":"Professional Experience","cr":3},
         {"code":"IE Elective 2","name":"Senior Elective","cr":3}],
    ],
    "Business Analytics (STEM)": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"SB 113","name":"Entrepreneurship & Business Innovation","cr":3},
         {"code":"MA 131","name":"Calculus I","cr":3},
         {"code":"STAT 282","name":"Probability & Statistics","cr":3}],
        [{"code":"AC 201","name":"Financial Accounting","cr":3},
         {"code":"EC 200","name":"Principles of Economics","cr":3},
         {"code":"CS 141","name":"Intro to Computer Science I","cr":4},
         {"code":"BA 201","name":"Intro to Business Analytics","cr":3}],
        [{"code":"BA 301","name":"Data Visualization & Reporting","cr":3},
         {"code":"BA 311","name":"Predictive Analytics","cr":3},
         {"code":"IS 301","name":"Business Info Systems","cr":3},
         {"code":"FI 301","name":"Financial Management","cr":3},
         {"code":"MK 301","name":"Marketing Management","cr":3}],
        [{"code":"BA 401","name":"Advanced Analytics & AI","cr":3},
         {"code":"MG 401","name":"Strategic Management","cr":3},
         {"code":"BA 499","name":"Professional Experience","cr":3},
         {"code":"Intl Exp","name":"International Experience (required)","cr":3},
         {"code":"BA Elective","name":"Analytics Elective","cr":3}],
    ],
    "Biology": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"BY 141","name":"General Biology I","cr":4},
         {"code":"CM 131","name":"General Chemistry I","cr":4},
         {"code":"MA 131","name":"Calculus I","cr":3}],
        [{"code":"BY 142","name":"General Biology II","cr":4},
         {"code":"CM 132","name":"General Chemistry II","cr":4},
         {"code":"BY 241","name":"Genetics","cr":3},
         {"code":"MA 132","name":"Calculus II","cr":3}],
        [{"code":"BY 344","name":"Cell Biology","cr":3},
         {"code":"CM 231","name":"Organic Chemistry I","cr":3},
         {"code":"STAT 282","name":"Statistics for Scientists","cr":3},
         {"code":"BY 361","name":"Ecology","cr":3},
         {"code":"BY Elective","name":"Biology Elective","cr":3}],
        [{"code":"BY 441","name":"Senior Seminar","cr":2},
         {"code":"BY 499","name":"Professional Experience","cr":3},
         {"code":"BY Elective 2","name":"Upper-div Biology Elective","cr":3},
         {"code":"Science Elective","name":"Science Elective","cr":3}],
    ],
    "Environmental Engineering": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"MA 131","name":"Calculus I","cr":3},
         {"code":"CM 131","name":"General Chemistry I","cr":4},
         {"code":"PH 131","name":"Physics I: Mechanics","cr":3}],
        [{"code":"MA 132","name":"Calculus II","cr":3},
         {"code":"CM 132","name":"General Chemistry II","cr":4},
         {"code":"ES 220","name":"Statics","cr":3},
         {"code":"BY 141","name":"General Biology I","cr":4}],
        [{"code":"MA 231","name":"Differential Equations","cr":3},
         {"code":"CE 331","name":"Fluid Mechanics","cr":3},
         {"code":"EnvE 341","name":"Environmental Chemistry","cr":3},
         {"code":"EnvE 361","name":"Air Quality Engineering","cr":3},
         {"code":"EnvE 371","name":"Water Resources Engineering","cr":3}],
        [{"code":"EnvE 421","name":"Hazardous Waste Management","cr":3},
         {"code":"EnvE 431","name":"Environmental Impact Assessment","cr":3},
         {"code":"EnvE 451","name":"Senior Design I","cr":3},
         {"code":"EnvE 452","name":"Senior Design II","cr":3},
         {"code":"EnvE Elective","name":"Environmental Elective","cr":3}],
    ],
    "Psychology": [
        [{"code":"FY100","name":"First-Year Seminar","cr":1},
         {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
         {"code":"PSY 101","name":"Introduction to Psychology","cr":3},
         {"code":"MA 131","name":"Calculus I","cr":3},
         {"code":"BY 141","name":"General Biology I","cr":4}],
        [{"code":"PSY 201","name":"Research Methods in Psychology","cr":3},
         {"code":"PSY 211","name":"Statistics for Psychology","cr":3},
         {"code":"PSY 221","name":"Developmental Psychology","cr":3},
         {"code":"PSY 231","name":"Social Psychology","cr":3}],
        [{"code":"PSY 301","name":"Abnormal Psychology","cr":3},
         {"code":"PSY 311","name":"Cognitive Psychology","cr":3},
         {"code":"PSY 321","name":"Neuroscience","cr":3},
         {"code":"PSY Elective","name":"Psychology Elective","cr":3},
         {"code":"Free Elective","name":"Free Elective","cr":3}],
        [{"code":"PSY 401","name":"Advanced Research Methods","cr":3},
         {"code":"PSY 411","name":"Senior Seminar","cr":3},
         {"code":"PSY 499","name":"Professional Experience","cr":3},
         {"code":"PSY Elective 2","name":"Upper-div Psych Elective","cr":3}],
    ],
}

# Graduate course plans
GRAD_COURSE_PLANS = {
    "Computer Science (MS)": {
        "sem1": [{"code":"CS 541","name":"Computer Algorithms","cr":3},
                 {"code":"CS 547","name":"Machine Learning I","cr":3},
                 {"code":"CS 544","name":"Advanced OS","cr":3},
                 {"code":"CS 545","name":"Computer Networks","cr":3}],
        "sem2": [{"code":"CS 6xx","name":"600-level CS Elective","cr":3},
                 {"code":"CS 6xx","name":"600-level CS Elective","cr":3},
                 {"code":"CS 707","name":"Seminar in CS","cr":1},
                 {"code":"CS 699","name":"Thesis Research","cr":6}],
    },
    "Applied Data Science (MS) — STEM": {
        "sem1": [{"code":"DS 501","name":"Foundations of Data Science","cr":3},
                 {"code":"DS 511","name":"Machine Learning I","cr":3},
                 {"code":"STAT 510","name":"Statistical Learning","cr":3}],
        "sem2": [{"code":"DS 521","name":"Deep Learning","cr":3},
                 {"code":"DS 531","name":"Big Data Analytics","cr":3},
                 {"code":"DS Elective","name":"Graduate Elective","cr":3}],
        "sem3": [{"code":"DS 599","name":"Capstone Project (sponsored)","cr":6},
                 {"code":"DS Elective 2","name":"Graduate Elective","cr":3}],
    },
    "MBA — Residential (35 cr, 9 months–2 years)": {
        "sem1": [{"code":"MBA 501","name":"Managerial Economics","cr":2},
                 {"code":"MBA 511","name":"Financial & Managerial Accounting","cr":2},
                 {"code":"MBA 521","name":"Marketing Strategy","cr":2},
                 {"code":"MBA 531","name":"Operations & Supply Chain","cr":2},
                 {"code":"MBA 541","name":"Organizational Behavior","cr":2},
                 {"code":"MBA 551","name":"Business Analytics","cr":2},
                 {"code":"MBA 561","name":"Business Law & Ethics","cr":2}],
        "sem2": [{"code":"MBA 571","name":"Corporate Finance","cr":3},
                 {"code":"MBA 581","name":"Strategic Management","cr":2},
                 {"code":"MBA 591","name":"Strategic Planning","cr":2},
                 {"code":"MBA 596","name":"Global Business Strategies","cr":3},
                 {"code":"MBA Elective","name":"MBA Elective","cr":3}],
    },
    "MBA — Healthcare Management (42 cr)": {
        "sem1": [{"code":"HCA 501","name":"Healthcare Systems & Policy","cr":3},
                 {"code":"HCA 511","name":"Financial Mgmt in Healthcare","cr":3},
                 {"code":"MBA 501","name":"Managerial Economics","cr":3},
                 {"code":"MBA 521","name":"Marketing Strategy","cr":3}],
        "sem2": [{"code":"HCA 521","name":"Healthcare Quality & Safety","cr":3},
                 {"code":"HCA 531","name":"Healthcare Law & Ethics","cr":3},
                 {"code":"HCA 541","name":"Healthcare Data Analytics","cr":3},
                 {"code":"MBA 531","name":"Operations & Supply Chain","cr":3}],
        "sem3": [{"code":"HCA 551","name":"Strategic Planning in Healthcare","cr":3},
                 {"code":"HCA 561","name":"Leadership in Healthcare","cr":3},
                 {"code":"HCA 571","name":"Internship in Healthcare","cr":3},
                 {"code":"HCA Elective","name":"Healthcare Elective","cr":3}],
    },
    "Occupational Therapy (MS, 92 cr, 6 semesters)": {
        "sem1": [{"code":"OT 501","name":"Foundations of OT","cr":4},
                 {"code":"OT 511","name":"Occupational Science","cr":3},
                 {"code":"OT 521","name":"Human Development & Occupation","cr":3},
                 {"code":"OT 531","name":"Neuroscience for OT","cr":4}],
        "sem2": [{"code":"OT 541","name":"OT with Mental Health Populations","cr":4},
                 {"code":"OT 551","name":"OT with Pediatric Populations","cr":4},
                 {"code":"OT 561","name":"Level I Fieldwork — Mental Health","cr":2},
                 {"code":"OT 571","name":"Assistive Technology","cr":3}],
        "sem3": [{"code":"OT 599A","name":"Level II Fieldwork I (full-time)","cr":12}],
    },
    "Physical Therapy (DPT, 105 cr, 8 semesters)": {
        "sem1": [{"code":"PT 501","name":"Functional Anatomy","cr":5},
                 {"code":"PT 511","name":"Neuroscience for PT","cr":3},
                 {"code":"PT 521","name":"Patient Examination & Evaluation","cr":5}],
        "sem2": [{"code":"PT 531","name":"Therapeutic Exercise","cr":4},
                 {"code":"PT 541","name":"Cardiopulmonary PT","cr":3},
                 {"code":"PT 551","name":"ICE: Integrated Clinical Experience","cr":3}],
        "sem3": [{"code":"PT 561","name":"Neurological Rehabilitation","cr":5},
                 {"code":"PT 571","name":"Musculoskeletal PT I","cr":5},
                 {"code":"PT 581","name":"ICE: Pediatric & Geriatric","cr":3}],
    },
    "Physician Assistant Studies (MS, 28 months)": {
        "sem1": [{"code":"PA 501","name":"Anatomy & Physiology for PAs","cr":6},
                 {"code":"PA 511","name":"Clinical Medicine I","cr":6},
                 {"code":"PA 521","name":"Pharmacology I","cr":4}],
        "sem2": [{"code":"PA 531","name":"Clinical Medicine II","cr":6},
                 {"code":"PA 541","name":"Pharmacology II","cr":4},
                 {"code":"PA 551","name":"Medical History & Physical Exam","cr":4}],
        "sem3": [{"code":"PA 561","name":"Clinical Rotations I","cr":10},
                 {"code":"PA 571","name":"Clinical Rotations II","cr":10}],
    },
    "Chemical Engineering (MS)": {
        "sem1": [{"code":"CHE 511","name":"Transport Phenomena I","cr":3},
                 {"code":"CHE 521","name":"Chemical Engineering Thermodynamics","cr":3},
                 {"code":"CHE 531","name":"Reactor Design & Analysis","cr":3},
                 {"code":"CHE 599","name":"Thesis Research","cr":5}],
        "sem2": [{"code":"CHE 541","name":"Advanced Separations","cr":3},
                 {"code":"CHE Elective","name":"Graduate Technical Elective","cr":3},
                 {"code":"CHE 591","name":"Seminar","cr":1},
                 {"code":"CHE 599","name":"Thesis Research","cr":5}],
    },
    "Civil & Environmental Engineering (MS)": {
        "sem1": [{"code":"CE 511","name":"Advanced Structural Analysis","cr":3},
                 {"code":"CE 521","name":"Environmental Systems","cr":3},
                 {"code":"CE 531","name":"Graduate Core Elective","cr":3},
                 {"code":"CE 599","name":"Thesis Research","cr":3}],
        "sem2": [{"code":"CE Elective","name":"Specialty Area Elective","cr":3},
                 {"code":"CE Elective 2","name":"Specialty Area Elective","cr":3},
                 {"code":"CE 591","name":"Graduate Seminar","cr":1},
                 {"code":"CE 599","name":"Thesis Research","cr":4}],
    },
    "Mechanical Engineering (MS)": {
        "sem1": [{"code":"ME 511","name":"Advanced Fluid Mechanics","cr":3},
                 {"code":"ME 521","name":"Advanced Thermodynamics","cr":3},
                 {"code":"ME 531","name":"Finite Element Analysis","cr":3},
                 {"code":"ME 599","name":"Thesis Research","cr":3}],
        "sem2": [{"code":"ME 541","name":"Advanced Materials","cr":3},
                 {"code":"ME Elective","name":"Graduate Technical Elective","cr":3},
                 {"code":"ME 591","name":"Graduate Seminar","cr":1},
                 {"code":"ME 599","name":"Thesis Research","cr":4}],
    },
}

DEFAULT_UG_PLAN = [
    [{"code":"FY100","name":"First-Year Seminar","cr":1},
     {"code":"UNIV 190","name":"The Clarkson Seminar","cr":3},
     {"code":"Core 101","name":"Major Core I","cr":3},
     {"code":"MA 131","name":"Calculus I","cr":3},
     {"code":"Science 1","name":"Science Foundation","cr":3}],
    [{"code":"Core 201","name":"Major Core II","cr":3},
     {"code":"Core 211","name":"Major Core III","cr":3},
     {"code":"MA 132","name":"Calculus II","cr":3},
     {"code":"Science 2","name":"Science Elective","cr":3}],
    [{"code":"Core 301","name":"Major Advanced I","cr":3},
     {"code":"Core 311","name":"Major Advanced II","cr":3},
     {"code":"Elective 1","name":"Knowledge Area Elective","cr":3},
     {"code":"Elective 2","name":"Free Elective","cr":3}],
    [{"code":"Core 401","name":"Senior Design / Capstone I","cr":3},
     {"code":"Core 411","name":"Senior Design / Capstone II","cr":3},
     {"code":"Prof Exp","name":"Professional Experience","cr":3},
     {"code":"Elective 3","name":"Upper-div Elective","cr":3}],
]

DEFAULT_GRAD_PLAN = {
    "sem1": [{"code":"GRAD 501","name":"Graduate Core I","cr":3},
             {"code":"GRAD 511","name":"Graduate Core II","cr":3},
             {"code":"GRAD 521","name":"Research Methods","cr":3}],
    "sem2": [{"code":"GRAD 531","name":"Elective I","cr":3},
             {"code":"GRAD 541","name":"Elective II","cr":3},
             {"code":"GRAD 599","name":"Thesis / Capstone","cr":6}],
}

CAREER_DATA = {
    "Software Engineering":             {"match":91,"avg_salary":"$74,000","skills":["CS 141/142","CS 344 Data Structures","Software Design"],"gaps":["CS 444 OS","Cloud platforms","DevOps"],"employers":["Amazon","IBM","GE Digital","Lockheed Martin"]},
    "Data Science & AI":                {"match":87,"avg_salary":"$78,000","skills":["Python","STAT 383","CS 447 ML"],"gaps":["Deep Learning","CS 547 DL","Big Data frameworks"],"employers":["IBM","NYSERDA","GE Aviation","Webroot"]},
    "Mechanical / Aerospace Engineering":{"match":93,"avg_salary":"$74,814","skills":["ME 221 Statics","CAD/SolidWorks","Thermodynamics"],"gaps":["ME 423 Propulsion Systems","Materials elective"],"employers":["GE Aviation","NASA","Tesla","SpaceX","Lockheed Martin"]},
    "Civil & Environmental Engineering": {"match":88,"avg_salary":"$68,000","skills":["CE 322 Structural Analysis","AutoCAD","Fluid Mechanics"],"gaps":["CE 451 Senior Design","Environmental regulations"],"employers":["HDR","AECOM","NYS DOT","US Army Corps"]},
    "Chemical / Biomolecular Engineering":{"match":85,"avg_salary":"$71,000","skills":["CHE 211 Material & Energy Balances","Process simulation"],"gaps":["CHE 421 Reactor Design","Plant design capstone"],"employers":["Pfizer","BASF","Air Products","Kodak"]},
    "Electrical Engineering":           {"match":89,"avg_salary":"$75,000","skills":["EE 221 Linear Circuits","EE 321 Signals","Digital Design"],"gaps":["EE 381 Electromagnetic Fields","Power systems elective"],"employers":["GE","Raytheon","Lockheed","Amphenol Aerospace"]},
    "Product Management":               {"match":74,"avg_salary":"$75,000","skills":["Communication","Business fundamentals","Project management"],"gaps":["UX research","Agile/Scrum certification"],"employers":["Amazon","Disney","GE","IBM"]},
    "Supply Chain & Logistics":         {"match":82,"avg_salary":"$71,000","skills":["SCM 201/301","Operations mgmt","Data analysis"],"gaps":["SAP ERP","CSCP certification"],"employers":["Amazon","Walmart","Raytheon","Amphenol"]},
    "Finance & Consulting":             {"match":70,"avg_salary":"$71,000","skills":["AC 201 Accounting","FI 301 Financial Mgmt","Excel"],"gaps":["CFA prep","FI 401 Investments","Financial modeling"],"employers":["Deloitte","PwC","Goldman Sachs","JP Morgan"]},
    "Research & Academia":              {"match":78,"avg_salary":"$55,000","skills":["Research methods","STAT coursework","Technical writing"],"gaps":["GRE prep","Conference publications","Lab experience"],"employers":["Clarkson CAMP","NSF","NIH","National Labs"]},
    "Entrepreneurship":                 {"match":80,"avg_salary":"$60,000","skills":["SB 113 Entrepreneurship","Networking","Problem-solving"],"gaps":["Ignite Presidential Fellowship","Cube Accelerator","Legal/IP basics"],"employers":["Cube Accelerator startups","Self-founded ventures"]},
    "Healthcare & Biomedical":          {"match":76,"avg_salary":"$62,000","skills":["Biology coursework","Chemistry","Research lab skills"],"gaps":["Clinical hours","MCAT prep","Healthcare policy"],"employers":["Albany Medical Center","Pfizer","Boston Scientific"]},
    "Physical / Occupational Therapy":  {"match":85,"avg_salary":"$70,000","skills":["BY 141 Biology","CM 131 Chemistry","Anatomy coursework"],"gaps":["DPT/OT prerequisite hours","Clinical observation (40+ hrs)"],"employers":["Hospitals","Private practice","Rehabilitation centers"]},
    "Physician Assistant":              {"match":83,"avg_salary":"$115,000","skills":["Biology","Chemistry","Medical terminology"],"gaps":["PA program prerequisites","Direct patient care hours (2000+)"],"employers":["Hospitals","Medical practices","Urgent care clinics"]},
    "Government & Policy":              {"match":68,"avg_salary":"$55,000","skills":["Environmental Science & Policy","Research","Writing"],"gaps":["Government internship","Public law fundamentals"],"employers":["NYSERDA","EPA","NYS DEC","US Army Corps"]},
}

CAMPUS_RESOURCES = [
    {"name":"Student Success Center (SSC)","desc":"Hub of academic support. Free tutoring (sign up via myCU), academic skills coaching, time/task management, study strategies, test prep. Also home to HEOP and CUPO programs.","contact":"315-268-2209 | ssc@clarkson.edu | ERC 1400","hours":"Mon–Fri 8am–4:30pm","tag":"Tutoring","tag_class":"tag-tutoring"},
    {"name":"Writing Center","desc":"Free 25-min one-on-one sessions with peer tutors. Reviews all writing: essays, lab reports, business plans, technical documents. Bring your assignment instructions.","contact":"315-268-4439 | wcenter@clarkson.edu | Snell Hall 139","hours":"Mon–Fri, by appointment","tag":"Writing","tag_class":"tag-writing"},
    {"name":"Kevin & Annie Parker Career Center","desc":"Resume/cover letter reviews, mock interviews, co-op & internship search via Handshake (750k+ companies). Career Fairs twice a year (fall & spring) with 200+ employers. ALL students must complete a Professional Experience before graduation.","contact":"315-268-6477 | career@clarkson.edu | ERC 2nd Floor","hours":"Mon–Fri 8am–4:30pm","tag":"Career","tag_class":"tag-career"},
    {"name":"Student Health & Counseling (SHAC)","desc":"On-campus clinic and counseling. Illness/injury care, immunizations, individual & group counseling, 24/7 crisis support. Also partnered with Mantra Health for FREE online therapy, wellness coaching, and emotional support for all enrolled students.","contact":"315-268-6633 | shac@clarkson.edu | ERC Suite 1300","hours":"Mon–Fri 8am–4:30pm | 24/7 crisis: Campus Safety 315-268-6666","tag":"Health & Counseling","tag_class":"tag-health"},
    {"name":"Student Achievement Services (SAS)","desc":"One-stop: Registrar, advising, Bursar, Financial Aid. FAFSA guidance, loans, payment plans, transcripts, course scheduling, graduation audits, academic calendar.","contact":"315-268-6451 | sas@clarkson.edu | TAC 207","hours":"Mon–Fri 8am–4:30pm","tag":"Financial Aid & Registration","tag_class":"tag-registration"},
    {"name":"Accessibility Services","desc":"Accommodations for learning differences, mental health conditions, physical disabilities. Assistive technology, extended test time, note-taking support, and other academic adjustments.","contact":"315-268-2006 | accessibility@clarkson.edu","hours":"Mon–Fri 8am–4:30pm","tag":"Accessibility","tag_class":"tag-accessibility"},
    {"name":"International Center","desc":"Visa & OPT processes, STEM OPT eligibility, campus adjustment. Study abroad partnerships with 55 universities in 28 countries. International experience is REQUIRED for all Reh School undergrads.","contact":"315-268-3943 | Potsdam Campus","hours":"Mon–Fri 8am–4:30pm","tag":"International","tag_class":"tag-international"},
    {"name":"Reach Out Hotline","desc":"24/7 crisis hotline for mental health, basic needs, alcohol/drug concerns. Mobile crisis team available to meet individuals at risk anywhere in the region.","contact":"315-265-2422 | reachouthotline.org","hours":"24/7, 365 days","tag":"Health & Counseling","tag_class":"tag-health"},
    {"name":"988 Suicide & Crisis Lifeline","desc":"Free, confidential support for anyone in crisis or emotional distress. Previously the National Suicide Prevention Hotline. Call, text, or chat available.","contact":"Call or text 988 | 988lifeline.org","hours":"24/7","tag":"Health & Counseling","tag_class":"tag-health"},
]

# ── Session state ───────────────────────────────────────────────────────────
def init_state():
    d = {"onboarded":False,"name":"","level":"Undergraduate","school":"","major":"",
         "year":YEARS[0],"credits":0,"careers":[],"career_other":"","challenges":"",
         "messages":[],"active_tab":"Overview"}
    for k,v in d.items():
        if k not in st.session_state: st.session_state[k]=v

init_state()

def get_prog_info():
    lv = st.session_state.level
    mj = st.session_state.major
    if lv=="Graduate":
        for school,progs in GRAD_PROGRAMS.items():
            if mj in progs: return progs[mj]
        return {"cr":30,"cps":9,"dur":4}
    else:
        for school,progs in UG_PROGRAMS.items():
            if mj in progs: return progs[mj]
        return {"cr":120,"cps":15}

def degree_stats():
    info = get_prog_info()
    total = info["cr"]; cps = info["cps"]
    creds = st.session_state.credits
    remaining = max(0, total-creds)
    pct = min(100, round((creds/total)*100))
    sems_left = math.ceil(remaining/cps) if remaining>0 else 0
    grad_year = 2025 + math.ceil(sems_left/2)
    return creds, remaining, pct, sems_left, grad_year, total, cps

def all_careers():
    c = list(st.session_state.careers)
    if st.session_state.career_other: c.append(st.session_state.career_other)
    return c

# ── Onboarding ──────────────────────────────────────────────────────────────
def show_onboarding():
    st.markdown('<div class="brand-bar"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0.5rem;">
      <img src="https://www.clarkson.edu/themes/custom/clarkson_theme/dist/img/logo.png"
           alt="Clarkson University" style="height:64px;margin-bottom:12px;" />
    </div>
    <div style="text-align:center;padding:0 0 1.2rem;">
      <div style="background:#ffcd00;color:#004e42;font-weight:800;font-size:1.3rem;
                  display:inline-block;padding:10px 26px;border-radius:12px;">myAdvisr</div>
      <h1 style="color:#004e42;margin:1rem 0 0.3rem;font-size:2rem;">Your AI academic advisor is here</h1>
      <p style="color:#555;font-size:1rem;max-width:520px;margin:0 auto 1.5rem;">
        Powered by AI, built for Clarkson Golden Knights. Plan your degree, find the right
        courses, and align your goals with your career.
      </p>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("#### Tell us about yourself")

        # All widgets outside st.form so school->major cascade reruns instantly
        name  = st.text_input("First name", placeholder="e.g. Graham", key="ob_name")
        level = st.radio("Degree level", ["Undergraduate", "Graduate"],
                         horizontal=True, key="ob_level")

        if level == "Undergraduate":
            school = st.selectbox("School / College",
                                  list(UG_PROGRAMS.keys()), key="ob_school")
            major  = st.selectbox("Your major",
                                  list(UG_PROGRAMS[school].keys()),
                                  key=f"ob_major_{school}")
        else:
            school = st.selectbox("Graduate program area",
                                  list(GRAD_PROGRAMS.keys()), key="ob_school")
            major  = st.selectbox("Your program",
                                  list(GRAD_PROGRAMS[school].keys()),
                                  key=f"ob_major_{school}")

        year = st.selectbox("Academic year / standing", YEARS, key="ob_year")

        cr_lbl = ("Credits completed so far" if level == "Undergraduate"
                  else "Graduate credits completed so far")
        credits = st.number_input(cr_lbl, min_value=0, max_value=250,
                                  value=0, step=1, key="ob_credits")

        st.markdown("**Career interests** *(select all that apply)*")
        chosen = []
        cols2  = st.columns(2)
        for i, opt in enumerate(CAREER_OPTIONS):
            with cols2[i % 2]:
                if st.checkbox(opt, key=f"ob_c_{i}"):
                    chosen.append(opt)

        career_other = ""
        if "Other (describe below)" in chosen:
            career_other = st.text_input(
                "Describe your career interest",
                placeholder="e.g. Sports analytics, climate tech, film production...",
                key="ob_career_other")

        challenges = st.text_area(
            "Any challenges or goals? *(optional)*",
            placeholder="e.g. Struggling with calculus, want a co-op, unsure which electives...",
            height=80, key="ob_challenges")

        if st.button("Launch myAdvisr →", use_container_width=True, key="ob_submit"):
            final        = [c for c in chosen if c != "Other (describe below)"]
            saved_credits = int(st.session_state.get("ob_credits", 0))
            st.session_state.update({
                "name":         name.strip() or "Student",
                "level":        level,
                "school":       school,
                "major":        major,
                "year":         year,
                "credits":      saved_credits,
                "careers":      final or ["Software Engineering"],
                "career_other": career_other.strip(),
                "challenges":   challenges,
                "onboarded":    True,
            })
            info  = get_prog_info()
            total = info["cr"]
            welcome = (
                f"Hi {st.session_state.name}! I'm myAdvisr, your AI academic advisor "
                f"for Clarkson University. You're in the {major} program ({total} credits required) "
                f"with {saved_credits} credits completed.\n\n"
                f"I've built your personalized dashboard using real Clarkson program data. "
                f"Ask me anything \u2014 courses, co-ops, career planning, or campus resources. Go Knights!"
            )
            st.session_state.messages = [{"role": "assistant", "content": welcome}]
            st.rerun()

# ── Sidebar ─────────────────────────────────────────────────────────────────
def show_sidebar():
    with st.sidebar:
        st.markdown('<p style="font-size:1.4rem;font-weight:800;color:#ffcd00!important;margin-bottom:0;">myAdvisr</p>'
                    '<p style="font-size:0.7rem;color:#9ecec8!important;margin-top:0;">CLARKSON UNIVERSITY · GO KNIGHTS</p>',
                    unsafe_allow_html=True)
        st.divider()
        creds,rem,pct,sems,gyr,total,cps = degree_stats()
        st.markdown(f'<p style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;">Degree Progress</p>',unsafe_allow_html=True)
        st.markdown(f'<div class="prog-wrap"><div class="prog-bar" style="width:{pct}%"></div></div>'
                    f'<p style="font-size:0.75rem;color:#9ecec8!important;">{creds} of {total} credits · {pct}% complete</p>',
                    unsafe_allow_html=True)
        st.markdown(f"**Student:** {st.session_state.name}  \n"
                    f"**Program:** {st.session_state.major}  \n"
                    f"**Year:** {st.session_state.year}  \n"
                    f"**Semesters left:** ~{sems}  \n"
                    f"**Grad target:** {gyr}")
        st.divider()
        st.markdown('<p style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;">Navigation</p>',unsafe_allow_html=True)
        for tab in ["Overview","Course Plan","Career Paths","Campus Resources","AI Advisor"]:
            prefix = "▶ " if st.session_state.active_tab==tab else "   "
            if st.button(prefix+tab, key=f"nav_{tab}", use_container_width=True):
                st.session_state.active_tab=tab; st.rerun()
        st.divider()
        if st.button("← Start over", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

# ── Overview ─────────────────────────────────────────────────────────────────
def tab_overview():
    creds,rem,pct,sems,gyr,total,cps = degree_stats()
    info = get_prog_info()
    ac = all_careers()
    top = ac[0] if ac else "Software Engineering"
    match_pct = CAREER_DATA.get(top,{}).get("match",80)
    is_grad = st.session_state.level=="Graduate"
    dur_note = f"~{info.get('dur',sems)} semesters typical" if is_grad else f"at ~{cps} cr/semester"

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card accent">
        <div class="metric-label">Credits completed</div>
        <div class="metric-value">{creds}</div>
        <div class="metric-sub">of {total} required</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Semesters left</div>
        <div class="metric-value">~{sems}</div>
        <div class="metric-sub">{dur_note}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Grad target</div>
        <div class="metric-value">{gyr}</div>
        <div class="metric-sub">on current pace</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Top career match</div>
        <div class="metric-value gold">{match_pct}%</div>
        <div class="metric-sub">{top}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="prog-wrap" style="height:14px;border-radius:8px;">'
                f'<div class="prog-bar" style="width:{pct}%;height:14px;border-radius:8px;"></div></div>'
                f'<p style="font-size:0.8rem;color:#555;margin-top:4px;">{pct}% complete — {rem} credits remaining</p>',
                unsafe_allow_html=True)

    st.markdown('<div class="section-head">Advisor alerts</div>', unsafe_allow_html=True)
    alerts=[]
    if creds==0:
        if is_grad: alerts.append(("info",f"<b>Welcome to Clarkson Graduate School, {st.session_state.name}!</b> Connect with your faculty advisor early. Graduate Admissions: 518-631-9831 | graduate@clarkson.edu"))
        else: alerts.append(("info",f"<b>Welcome to Clarkson, {st.session_state.name}!</b> Start with FY100 (First-Year Seminar) and UNIV 190 (The Clarkson Seminar). Visit Student Achievement Services (TAC 207) to confirm your plan."))
    elif creds<30 and not is_grad:
        alerts.append(("info","<b>Building momentum!</b> Focus on your math/science sequence and major core. Over 30% of Clarkson students use the Student Success Center — sign up for tutoring via myCU."))

    if not is_grad:
        alerts.append(("warn","<b>Professional Experience required:</b> ALL Clarkson undergrads must complete at least one co-op or internship before graduation. Visit the Parker Career Center (ERC 2nd floor, 315-268-6477) and create your Handshake profile today."))

    if "Data Science & AI" in ac or "Software Engineering" in ac:
        alerts.append(("info","<b>Career tip:</b> CS 344 (Algorithms), CS 447 (ML), and CS 443 (Databases) are top skills for tech roles. Career Fairs each fall & spring bring Amazon, IBM, GE, and 200+ companies."))

    if is_grad and "MBA" in st.session_state.major:
        alerts.append(("info","<b>Reh School MBA:</b> 97-100% placement rate. Class of 2023 avg starting salary $76,300. International experience trip is included in the Residential MBA. Explore dual-degree option with Applied Data Science."))

    alerts.append(("crit","<b>Registration:</b> Plan next semester with Student Achievement Services (TAC 207, 315-268-6451). Grad students contact your faculty advisor or graduate@clarkson.edu."))

    if st.session_state.challenges:
        snippet=st.session_state.challenges[:100]+("..." if len(st.session_state.challenges)>100 else "")
        alerts.append(("info",f"<b>Your goal:</b> \"{snippet}\" — factoring this into all recommendations."))

    dc={"warn":"dot-warn","info":"dot-info","crit":"dot-crit"}
    for kind,text in alerts:
        st.markdown(f'<div class="alert-card {kind}"><div class="alert-dot {dc[kind]}"></div><div class="alert-text">{text}</div></div>',unsafe_allow_html=True)

# ── Course Plan ───────────────────────────────────────────────────────────────
def tab_courses():
    lv = st.session_state.level
    mj = st.session_state.major
    info = get_prog_info()
    total = info["cr"]

    if lv=="Graduate":
        plan = GRAD_COURSE_PLANS.get(mj, DEFAULT_GRAD_PLAN)
        st.markdown(f'<p class="prog-info"><b>{mj}</b> — <b>{total} credits</b> required. '
                    f'Typical completion: <b>{info.get("dur","varies")} semesters</b> full-time. '
                    f'Courses based on Clarkson graduate catalog.</p>', unsafe_allow_html=True)
        sem_labels={"sem1":"Semester 1 — Core Courses","sem2":"Semester 2","sem3":"Semester 3 / Clinical Rotations"}
        for key,label in sem_labels.items():
            if key not in plan: continue
            courses = plan[key]
            total_cr = sum(c["cr"] for c in courses)
            rows="".join(f'<div class="course-row"><span class="course-code">{c["code"]}</span>'
                        f'<span class="course-name">{c["name"]}</span>'
                        f'<span class="course-cr">{c["cr"]} cr</span>'
                        f'<span class="badge badge-plan">Planned</span></div>' for c in courses)
            st.markdown(f'<div class="sem-block"><div class="sem-header"><span>{label}</span>'
                        f'<span>{total_cr} credits</span></div>{rows}</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.78rem;color:#888;">Confirm your plan with your faculty advisor or '
                    'Graduate Admissions: 518-631-9831 | graduate@clarkson.edu</p>', unsafe_allow_html=True)
    else:
        plan = UG_COURSE_PLANS.get(mj, DEFAULT_UG_PLAN)
        cr_completed = st.session_state.credits
        st.markdown(f'<p class="prog-info"><b>{mj}</b> — <b>{total} credits</b> required over 8 semesters. '
                    f'All engineering programs include the Clarkson Common Experience (UNIV 190, FY100). '
                    f'All Reh School programs include SB 113 and an international experience requirement.</p>',
                    unsafe_allow_html=True)
        sem_names=["Year 1, Semester 1 (Fall)","Year 1, Semester 2 (Spring)",
                   "Year 2–3, Core Courses","Year 3–4, Advanced Courses"]
        badge_map=["badge-done" if i*16<cr_completed else "badge-plan" for i in range(len(plan))]
        label_map=["Completed" if i*16<cr_completed else "Planned" for i in range(len(plan))]
        for i,(sem,courses) in enumerate(zip(sem_names,plan)):
            total_cr=sum(c["cr"] for c in courses)
            rows="".join(f'<div class="course-row"><span class="course-code">{c["code"]}</span>'
                        f'<span class="course-name">{c["name"]}</span>'
                        f'<span class="course-cr">{c["cr"]} cr</span>'
                        f'<span class="badge {badge_map[i]}">{label_map[i]}</span></div>' for c in courses)
            st.markdown(f'<div class="sem-block"><div class="sem-header"><span>{sem}</span>'
                        f'<span>{total_cr} credits</span></div>{rows}</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.78rem;color:#888;">Based on Clarkson 2023-24 undergraduate catalog. '
                    'Confirm your exact plan with Student Achievement Services: TAC 207, 315-268-6451.</p>',
                    unsafe_allow_html=True)

# ── Career Paths ──────────────────────────────────────────────────────────────
def tab_career():
    ac=all_careers(); shown=ac[:3]
    st.markdown(f'<p style="color:#555;font-size:0.88rem;margin-bottom:1rem;">'
                f'Based on your {st.session_state.major} program. '
                f'Clarkson Class of 2023: 99% placement rate, avg $71,000+ starting salary.</p>',
                unsafe_allow_html=True)
    for career in shown:
        d=CAREER_DATA.get(career,{"match":75,"avg_salary":"$65,000","skills":["Core coursework"],"gaps":["Internship experience"],"employers":["Various"]})
        sh="".join(f'<span class="skill-tag">{s}</span>' for s in d["skills"])
        gh="".join(f'<span class="skill-tag skill-gap">{g}</span>' for g in d["gaps"])
        eh="".join(f'<span class="skill-tag">{e}</span>' for e in d["employers"])
        st.markdown(f"""<div class="career-card">
          <div class="career-title">{career}</div>
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;font-size:0.82rem;color:#8a6c00;">
            <div class="match-wrap"><div class="match-fill" style="width:{d['match']}%"></div></div>
            {d['match']}% match &nbsp;·&nbsp; Avg salary: <b>{d['avg_salary']}</b>
          </div>
          <div style="font-size:0.75rem;color:#555;margin-bottom:4px;">Relevant Clarkson coursework & skills:</div>
          <div style="margin-bottom:8px;">{sh}</div>
          <div style="font-size:0.75rem;color:#cf4520;margin-bottom:4px;">Gaps / courses to complete:</div>
          <div style="margin-bottom:8px;">{gh}</div>
          <div style="font-size:0.75rem;color:#555;margin-bottom:4px;">Companies that recruit at Clarkson:</div>
          <div>{eh}</div>
        </div>""", unsafe_allow_html=True)

# ── Campus Resources ──────────────────────────────────────────────────────────
def tab_resources():
    st.markdown('<p style="color:#555;font-size:0.88rem;margin-bottom:1rem;">'
                'Real Clarkson University resources with actual contacts and locations. '
                'Over 50% of Clarkson students use health & counseling services every year.</p>',
                unsafe_allow_html=True)
    for r in CAMPUS_RESOURCES:
        st.markdown(f"""<div class="resource-card">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <span style="font-size:0.95rem;font-weight:700;color:#004e42;">{r['name']}</span>
            <span class="resource-tag {r['tag_class']}">{r['tag']}</span>
          </div>
          <div style="font-size:0.82rem;color:#333;line-height:1.5;margin-bottom:6px;">{r['desc']}</div>
          <div style="font-size:0.75rem;color:#555;"><b>Contact:</b> {r['contact']} &nbsp;·&nbsp; <b>Hours:</b> {r['hours']}</div>
        </div>""", unsafe_allow_html=True)

# ── AI Advisor ────────────────────────────────────────────────────────────────
def build_system_prompt():
    s=st.session_state; info=get_prog_info(); ac=all_careers()
    is_grad=s.level=="Graduate"
    return (
        f"You are myAdvisr, an expert AI academic advisor for Clarkson University (Potsdam, NY).\n\n"
        f"Student profile:\n"
        f"- Name: {s.name}\n"
        f"- Program: {s.major} ({info['cr']} credits required, {info.get('dur','varies')} semesters typical)\n"
        f"- Level: {s.level}\n"
        f"- Year/standing: {s.year}\n"
        f"- Credits completed: {s.credits} of {info['cr']}\n"
        f"- Career interests: {', '.join(ac) if ac else 'Not specified'}\n"
        f"- Challenges/goals: {s.challenges if s.challenges else 'None'}\n\n"
        f"Key Clarkson facts to reference:\n"
        f"- Parker Career Center: ERC 2nd floor, 315-268-6477, career@clarkson.edu, Handshake\n"
        f"- Student Success Center (tutoring): ERC 1400, 315-268-2209, ssc@clarkson.edu\n"
        f"- SHAC (health/counseling): ERC Suite 1300, 315-268-6633; Mantra Health free for all students\n"
        f"- Student Achievement Services (registrar/advising/financial aid): TAC 207, 315-268-6451\n"
        f"- Graduate Admissions: 518-631-9831, graduate@clarkson.edu\n"
        f"- Writing Center: Snell Hall 139, 315-268-4439\n"
        f"- ALL undergrads must complete a Professional Experience (co-op/internship) before graduation\n"
        f"- ALL Reh School undergrads must complete an international experience\n"
        f"- SB 113 (Entrepreneurship & Business Innovation) required for all Reh School undergrads\n"
        f"- UNIV 190 (The Clarkson Seminar) and FY100 (First-Year Seminar) required for all first-year students\n"
        f"- Career Fairs: twice yearly (fall & spring), 200+ employers, open to all students\n"
        f"- Class of 2023: 99% placement rate, avg $71,000+ starting salary undergrads, $76,300 MBA\n"
        f"- 4+1 programs: any BS → MBA; BS Biology/Biomolecular → MS Bioscience & Biotechnology\n"
        f"- DPT: 105 credits, 8 semesters (2.67 years). OT MS: 92 credits, 6 semesters. PA MS: 28 months\n"
        f"- MBA Residential: 35 credits, 9 months minimum. MBA Online: 36 credits, ~1.5 years\n"
        f"- Applied Data Science MS: 36 credits, 3 semesters full-time (STEM-designated)\n"
        f"- Most engineering MS programs: 30 credits. PhD programs: 90 credits from BS.\n\n"
        f"Be warm, specific, and actionable. Reference real Clarkson courses, offices, phone numbers. "
        f"Keep responses under 160 words unless detail is requested. Plain text only, no markdown."
    )

def tab_chat():
    if RAG_AVAILABLE:
        try:
            stats = get_index_stats()
            rag_badge = (
                f'<span style="background:#eef7e6;color:#3a6e00;padding:2px 8px;'
                f'border-radius:100px;font-size:0.72rem;font-weight:600;">'
                f'RAG ACTIVE · {stats["total_documents"]} docs indexed</span>'
            ) if stats["status"] == "ready" else ""
        except Exception:
            rag_badge = ""
    else:
        rag_badge = (
            '<span style="background:#fffbea;color:#8a6c00;padding:2px 8px;'
            'border-radius:100px;font-size:0.72rem;font-weight:600;">'
            'Install sentence-transformers & chromadb to enable RAG</span>'
        )
    st.markdown(
        f'<div style="font-size:0.8rem;color:#555;margin-bottom:1rem;">'
        f'Powered by Claude · {rag_badge} · Grounded in real Clarkson data</div>',
        unsafe_allow_html=True)
    st.markdown("**Quick questions:**")
    is_grad=st.session_state.level=="Graduate"
    qcols=st.columns(4)
    quick=[
        ("Next courses",     "What courses should I take next semester for my program?"),
        ("Co-op / Career" if not is_grad else "Graduate career","How do I find a co-op or internship at Clarkson?" if not is_grad else "What career resources does Clarkson offer for graduate students?"),
        ("Graduation check", "Am I on track to graduate on time?"),
        ("Campus help",      "What resources are available if I am struggling academically?"),
    ]
    for i,(lbl,prompt) in enumerate(quick):
        with qcols[i]:
            if st.button(lbl,key=f"qp_{i}",use_container_width=True):
                st.session_state.messages.append({"role":"user","content":prompt})
                with st.spinner("myAdvisr is thinking..."):
                    reply=get_claude_response(prompt)
                st.session_state.messages.append({"role":"assistant","content":reply})
                st.rerun()
    st.divider()
    for msg in st.session_state.messages:
        if msg["role"]=="assistant":
            st.markdown(f'<div class="label-ai chat-label">myAdvisr</div>'
                        f'<div class="chat-ai">{msg["content"].replace(chr(10),"<br>")}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="label-user chat-label">{st.session_state.name}</div>'
                        f'<div class="chat-user">{msg["content"]}</div>',
                        unsafe_allow_html=True)
    user_input=st.chat_input("Ask your advisor anything about Clarkson...")
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        with st.spinner("myAdvisr is thinking..."):
            reply=get_claude_response(user_input)
        st.session_state.messages.append({"role":"assistant","content":reply})
        st.rerun()

def get_claude_response(user_message):
    try:
        client=Anthropic()
        history=[{"role":m["role"],"content":m["content"]}
                 for m in st.session_state.messages[:-1] if m["role"] in ("user","assistant")]
        response=client.messages.create(
            model="claude-sonnet-4-5", max_tokens=512,
            system=build_system_prompt(),
            messages=history+[{"role":"user","content":user_message}])
        return response.content[0].text
    except Exception as e:
        return (f"I am having trouble connecting right now ({type(e).__name__}). "
                "Make sure your ANTHROPIC_API_KEY is set and try again.")

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.onboarded:
        show_onboarding(); return
    show_sidebar()
    st.markdown('<div class="brand-bar"></div>', unsafe_allow_html=True)
    lv_badge="Graduate" if st.session_state.level=="Graduate" else "Undergraduate"
    st.markdown(f'<div class="page-header"><div class="logo-badge">myAdvisr</div>'
                f'<div><h1>Welcome back, {st.session_state.name}</h1>'
                f'<p>{st.session_state.major} · {lv_badge} · {st.session_state.year} · Clarkson University, Potsdam NY</p>'
                f'</div></div>', unsafe_allow_html=True)
    tab=st.session_state.active_tab
    st.markdown(f'<div class="section-head">{tab}</div>', unsafe_allow_html=True)
    if   tab=="Overview":         tab_overview()
    elif tab=="Course Plan":      tab_courses()
    elif tab=="Career Paths":     tab_career()
    elif tab=="Campus Resources": tab_resources()
    elif tab=="AI Advisor":       tab_chat()

if __name__=="__main__":
    main()
