"""
myAdvisr — AI-Powered Academic Advisor
Clarkson University | Innovation-Based AI Solution
Built with Streamlit + Anthropic Claude API
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
:root {
    --green:      #004e42;
    --green-dark: #003530;
    --green-mid:  #005c4e;
    --gold:       #ffcd00;
    --gold-dim:   #c9a000;
    --olive:      #7a9a01;
    --coral:      #cf4520;
    --blue:       #418fde;
    --navy:       #002d72;
    --text:       #1a1a1a;
    --muted:      #555555;
    --light-bg:   #f0f7f5;
    --card-bg:    #ffffff;
}
html, body, [class*="css"] { font-family: 'Segoe UI', Arial, sans-serif; }
.brand-bar { height: 5px; background: linear-gradient(90deg, #004e42 60%, #ffcd00 100%); margin: -1rem -1rem 1.5rem -1rem; }
.page-header { background: var(--green); color: white; padding: 1.5rem 2rem; border-radius: 12px; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem; }
.page-header h1 { margin: 0; font-size: 1.6rem; color: white; }
.page-header p  { margin: 0; color: rgba(255,255,255,0.75); font-size: 0.9rem; }
.logo-badge { background: var(--gold); color: var(--green); font-weight: 800; font-size: 1rem; padding: 8px 14px; border-radius: 10px; white-space: nowrap; }
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card { background: var(--card-bg); border: 1.5px solid #e0ece9; border-radius: 12px; padding: 1.1rem 1.4rem; flex: 1; min-width: 140px; }
.metric-card.accent { border-color: var(--gold); border-width: 2px; }
.metric-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); font-weight: 600; margin-bottom: 4px; }
.metric-value { font-size: 2rem; font-weight: 700; color: var(--green); line-height: 1; margin-bottom: 2px; }
.metric-value.gold { color: var(--gold-dim); }
.metric-sub { font-size: 0.75rem; color: var(--muted); }
.alert-card { border-radius: 10px; padding: 0.9rem 1.1rem; margin-bottom: 0.7rem; display: flex; gap: 0.8rem; align-items: flex-start; border-left: 4px solid; }
.alert-card.warn { background:#fffbea; border-color: var(--gold); }
.alert-card.info { background:#eef7f0; border-color: var(--olive); }
.alert-card.crit { background:#fdf0eb; border-color: var(--coral); }
.alert-dot { width:10px; height:10px; border-radius:50%; margin-top:4px; flex-shrink:0; }
.dot-warn { background: var(--gold-dim); }
.dot-info { background: var(--olive); }
.dot-crit { background: var(--coral); }
.alert-text { font-size: 0.85rem; color: var(--text); line-height: 1.5; }
.alert-text b { color: var(--green); }
.prog-wrap { background: #e0ece9; border-radius: 6px; height: 10px; margin: 6px 0 4px; overflow: hidden; }
.prog-bar  { height: 100%; border-radius: 6px; background: linear-gradient(90deg, var(--green), var(--olive)); }
.section-head { font-size: 1.15rem; font-weight: 700; color: var(--green); border-bottom: 2px solid var(--gold); padding-bottom: 6px; margin: 1.4rem 0 1rem; }
.sem-block { background: var(--card-bg); border: 1px solid #e0ece9; border-radius: 10px; margin-bottom: 1rem; overflow: hidden; }
.sem-header { background: var(--green); color: white; padding: 0.6rem 1rem; display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; font-weight: 600; }
.course-row { display: flex; align-items: center; gap: 1rem; padding: 0.55rem 1rem; border-bottom: 1px solid #f5f5f5; font-size: 0.82rem; }
.course-row:last-child { border-bottom: none; }
.course-code { color: var(--muted); width: 80px; flex-shrink: 0; font-family: monospace; }
.course-name { flex: 1; color: var(--text); }
.course-cr   { color: var(--muted); width: 36px; text-align: right; flex-shrink: 0; }
.badge { padding: 2px 10px; border-radius: 100px; font-size: 0.7rem; font-weight: 600; }
.badge-done { background: #eef7e6; color: #3a6e00; }
.badge-plan { background: #fffbea; color: #8a6c00; }
.badge-rec  { background: #fdf0eb; color: #8a2a00; }
.career-card { background: var(--card-bg); border: 1px solid #e0ece9; border-radius: 10px; padding: 1.1rem 1.3rem; margin-bottom: 1rem; }
.career-title { font-size: 1rem; font-weight: 700; color: var(--green); margin-bottom: 6px; }
.match-wrap { background: #e0ece9; border-radius: 3px; height: 5px; display: inline-block; width: 90px; vertical-align: middle; margin-right: 6px; }
.match-fill { height: 100%; border-radius: 3px; background: var(--gold-dim); }
.skill-tag { display: inline-block; padding: 3px 10px; border: 1px solid #d0e8e4; border-radius: 100px; font-size: 0.72rem; color: var(--muted); margin: 3px 3px 3px 0; }
.skill-gap { border-color: #f5c4b0; color: var(--coral); }
.resource-card { background: var(--card-bg); border: 1px solid #e0ece9; border-radius: 10px; padding: 1rem 1.3rem; margin-bottom: 0.8rem; }
.resource-tag { padding: 3px 10px; border-radius: 100px; font-size: 0.7rem; font-weight: 600; white-space: nowrap; }
.tag-tutoring     { background: #eef7e6; color: #3a6e00; }
.tag-career       { background: #fffbea; color: #8a6c00; }
.tag-health       { background: #fdf0eb; color: #8a2a00; }
.tag-financial    { background: #fffbea; color: #8a6c00; }
.tag-writing      { background: #eef7e6; color: #3a6e00; }
.tag-registration { background: #e8eef8; color: #1a3a6e; }
.tag-accessibility{ background: #f0eef8; color: #3a2a6e; }
.tag-international{ background: #eef7f8; color: #1a5a6e; }
.chat-ai { background: var(--light-bg); border: 1px solid #d0e8e4; border-radius: 4px 14px 14px 14px; padding: 0.7rem 1rem; margin: 0.4rem 0; font-size: 0.88rem; color: var(--text); line-height: 1.55; max-width: 90%; }
.chat-user { background: var(--green); color: white; border-radius: 14px 4px 14px 14px; padding: 0.7rem 1rem; margin: 0.4rem 0 0.4rem auto; font-size: 0.88rem; line-height: 1.55; max-width: 85%; text-align: right; }
.chat-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.05em; margin-bottom: 2px; }
.label-ai   { color: var(--muted); }
.label-user { color: var(--muted); text-align: right; }
section[data-testid="stSidebar"] { background: var(--green-dark) !important; }
section[data-testid="stSidebar"] * { color: #c8e6e2 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: var(--gold) !important; }
div[data-testid="stVerticalBlock"] { gap: 0.5rem; }
.stButton > button { background: var(--gold) !important; color: var(--green) !important; border: none !important; font-weight: 700 !important; border-radius: 100px !important; padding: 0.4rem 1.4rem !important; }
.stButton > button:hover { background: var(--gold-dim) !important; }
.cu-logo-strip { text-align: center; padding: 1.2rem 0 0.5rem; }
.degree-type-badge { display: inline-block; padding: 3px 12px; border-radius: 100px; font-size: 0.72rem; font-weight: 700; margin-left: 8px; }
.badge-ms  { background: #e8eef8; color: #1a3a6e; }
.badge-phd { background: #fdf0eb; color: #8a2a00; }
.badge-mba { background: #eef7e6; color: #3a6e00; }
.badge-cert{ background: #f0eef8; color: #3a2a6e; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  CLARKSON SCHOOL DATA  (scraped from clarkson.edu)
# ─────────────────────────────────────────────────────────────────────────────

CLARKSON_SCHOOLS_UG = {
    "Coulter School of Engineering & Applied Sciences": [
        "Aeronautical Engineering",
        "Chemical Engineering",
        "Civil Engineering",
        "Computer Engineering",
        "Computer Science",
        "Data Science",
        "Electrical Engineering",
        "Environmental Engineering",
        "Mechanical Engineering",
        "Engineering & Management",
        "Engineering Studies (undecided)",
    ],
    "Reh School of Business": [
        "Business Administration",
        "Business Analytics (STEM-designated)",
        "Business Intelligence & Data Analytics",
        "Financial Information & Analysis",
        "Global Supply Chain Management",
        "Innovation & Entrepreneurship",
        "Business Studies (undecided)",
    ],
    "Lewis School of Health & Life Sciences": [
        "Biology",
        "Biomolecular Science",
        "Chemistry",
        "Environmental Health Science",
        "Physics",
        "Applied Mathematics & Statistics",
        "Mathematics",
        "Mathematical Economics",
        "Psychology",
    ],
    "Institute for a Sustainable Environment": [
        "Environmental Science & Policy",
        "Digital Arts & Sciences",
        "Interdisciplinary Liberal Studies",
        "Interdisciplinary Social Sciences",
    ],
}

CLARKSON_SCHOOLS_GRAD = {
    "Engineering & Applied Sciences (Graduate)": [
        "Chemical Engineering (MS)",
        "Chemical Engineering (PhD)",
        "Chemistry (MS)",
        "Chemistry (PhD)",
        "Civil & Environmental Engineering (MS)",
        "Civil & Environmental Engineering (PhD)",
        "Computer Science (MS)",
        "Computer Science (PhD)",
        "Electrical & Computer Engineering (MS)",
        "Electrical & Computer Engineering (PhD)",
        "Electrical & Computer Engineering — Power Engineering (MS)",
        "Mathematics (MS)",
        "Mathematics (PhD)",
        "Mechanical Engineering (MS)",
        "Mechanical Engineering (PhD)",
        "Physics (MS)",
        "Physics (PhD)",
        "Materials Science & Engineering (PhD)",
    ],
    "Interdisciplinary Graduate Programs": [
        "Applied Data Science (MS) — STEM",
        "Construction Engineering Management (MS)",
        "Engineering Management (MS)",
        "Power Systems Engineering (Advanced Certificate)",
        "Construction Engineering Management (Advanced Certificate)",
        "Business of Energy (Advanced Certificate)",
        "Digital Transformation (Advanced Certificate)",
    ],
    "Reh School of Business (Graduate)": [
        "MBA — Residential (9-month)",
        "MBA — Online",
        "MBA — Business Analytics (STEM)",
        "MBA — Global Supply Chain Management (STEM)",
        "MBA — Healthcare Management",
        "MS — Clinical Leadership in Healthcare Management",
        "MS — Healthcare Data Analytics",
        "Business Advanced Certificates",
    ],
    "Lewis School of Health & Life Sciences (Graduate)": [
        "Bioscience & Biotechnology (MS) — STEM",
        "Bioscience & Biotechnology (PhD) — STEM",
        "Occupational Therapy (MS)",
        "Physical Therapy (DPT)",
        "Physician Assistant Studies (MS)",
    ],
    "Environment & Sustainability (Graduate)": [
        "Environmental Science & Engineering (MS) — STEM",
        "Environmental Science & Engineering (PhD) — STEM",
    ],
}

YEARS = [
    "Freshman (1st year)",
    "Sophomore (2nd year)",
    "Junior (3rd year)",
    "Senior (4th year)",
    "Graduate Student — MS",
    "Graduate Student — PhD",
    "Graduate Student — MBA",
]

CAREER_OPTIONS = [
    "Software Engineering",
    "Data Science & AI",
    "Mechanical / Aerospace Engineering",
    "Civil & Environmental Engineering",
    "Chemical Engineering",
    "Product Management",
    "Supply Chain & Logistics",
    "Finance & Consulting",
    "Research & Academia",
    "Entrepreneurship",
    "Healthcare & Biomedical",
    "Government & Policy",
    "Other (enter below)",
]

# ─────────────────────────────────────────────────────────────────────────────
#  COURSE PLANS  (undergraduate — based on Clarkson catalog)
# ─────────────────────────────────────────────────────────────────────────────

COURSE_PLANS = {
    "Computer Science": {
        "credits_required": 120,
        "current": [
            {"code": "CS 141",   "name": "Introduction to Computer Science",  "cr": 3, "status": "plan"},
            {"code": "CS 142",   "name": "Software Design & Development",     "cr": 3, "status": "plan"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "plan"},
            {"code": "CS 344",   "name": "Data Structures & Algorithms",      "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "CS 242",   "name": "Advanced Programming",              "cr": 3, "status": "plan"},
            {"code": "CS 348",   "name": "Computer Organization",             "cr": 3, "status": "plan"},
            {"code": "MA 132",   "name": "Calculus II",                       "cr": 3, "status": "plan"},
            {"code": "CS 444",   "name": "Operating Systems",                 "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "done"},
        ],
    },
    "Mechanical Engineering": {
        "credits_required": 128,
        "current": [
            {"code": "ME 170",   "name": "Engineering Graphics & CAD",        "cr": 3, "status": "plan"},
            {"code": "ME 221",   "name": "Statics",                           "cr": 3, "status": "plan"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "plan"},
            {"code": "PH 131",   "name": "Physics I: Mechanics",              "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "ME 222",   "name": "Dynamics",                          "cr": 3, "status": "plan"},
            {"code": "ME 323",   "name": "Thermodynamics I",                  "cr": 3, "status": "plan"},
            {"code": "MA 132",   "name": "Calculus II",                       "cr": 3, "status": "plan"},
            {"code": "PH 132",   "name": "Physics II: E&M",                   "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "CM 131",   "name": "General Chemistry I",               "cr": 3, "status": "done"},
        ],
    },
    "Business Administration": {
        "credits_required": 120,
        "current": [
            {"code": "SB 113",   "name": "Entrepreneurship & Business Innovation","cr": 3,"status": "plan"},
            {"code": "AC 201",   "name": "Financial Accounting",              "cr": 3, "status": "plan"},
            {"code": "EC 200",   "name": "Principles of Economics",           "cr": 3, "status": "plan"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "MK 301",   "name": "Marketing Management",              "cr": 3, "status": "plan"},
            {"code": "MG 301",   "name": "Organizational Behavior",           "cr": 3, "status": "plan"},
            {"code": "FI 301",   "name": "Financial Management",              "cr": 3, "status": "plan"},
            {"code": "IS 301",   "name": "Business Information Systems",      "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "EC 200",   "name": "Principles of Economics",           "cr": 3, "status": "done"},
        ],
    },
    "Business Analytics (STEM-designated)": {
        "credits_required": 120,
        "current": [
            {"code": "SB 113",   "name": "Entrepreneurship & Business Innovation","cr": 3,"status": "plan"},
            {"code": "BA 201",   "name": "Introduction to Business Analytics","cr": 3, "status": "plan"},
            {"code": "STAT 282", "name": "Statistics for Business",           "cr": 3, "status": "plan"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "BA 301",   "name": "Data Visualization & Reporting",    "cr": 3, "status": "plan"},
            {"code": "BA 311",   "name": "Predictive Analytics",              "cr": 3, "status": "plan"},
            {"code": "IS 301",   "name": "Business Information Systems",      "cr": 3, "status": "plan"},
            {"code": "AC 201",   "name": "Financial Accounting",              "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "EC 200",   "name": "Principles of Economics",           "cr": 3, "status": "done"},
        ],
    },
    "Global Supply Chain Management": {
        "credits_required": 120,
        "current": [
            {"code": "SB 113",   "name": "Entrepreneurship & Business Innovation","cr": 3,"status": "plan"},
            {"code": "SCM 201",  "name": "Introduction to Supply Chain Mgmt", "cr": 3, "status": "plan"},
            {"code": "EC 200",   "name": "Principles of Economics",           "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "plan"},
            {"code": "IS 301",   "name": "Business Information Systems",      "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "SCM 301",  "name": "Operations Management",             "cr": 3, "status": "plan"},
            {"code": "SCM 311",  "name": "Logistics & Transportation",        "cr": 3, "status": "plan"},
            {"code": "MG 301",   "name": "Organizational Behavior",           "cr": 3, "status": "plan"},
            {"code": "STAT 282", "name": "Statistics for Business",           "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "EC 200",   "name": "Principles of Economics",           "cr": 3, "status": "done"},
        ],
    },
    "Financial Information & Analysis": {
        "credits_required": 120,
        "current": [
            {"code": "SB 113",   "name": "Entrepreneurship & Business Innovation","cr": 3,"status": "plan"},
            {"code": "AC 201",   "name": "Financial Accounting",              "cr": 3, "status": "plan"},
            {"code": "FI 201",   "name": "Introduction to Finance",           "cr": 3, "status": "plan"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "FI 301",   "name": "Financial Management",              "cr": 3, "status": "plan"},
            {"code": "FI 311",   "name": "Investments",                       "cr": 3, "status": "plan"},
            {"code": "AC 301",   "name": "Managerial Accounting",             "cr": 3, "status": "plan"},
            {"code": "EC 301",   "name": "Intermediate Microeconomics",       "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "EC 200",   "name": "Principles of Economics",           "cr": 3, "status": "done"},
        ],
    },
    "Innovation & Entrepreneurship": {
        "credits_required": 120,
        "current": [
            {"code": "SB 113",   "name": "Entrepreneurship & Business Innovation","cr": 3,"status": "plan"},
            {"code": "IE 201",   "name": "Principles of Innovation",          "cr": 3, "status": "plan"},
            {"code": "MG 201",   "name": "Management Foundations",            "cr": 3, "status": "plan"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "IE 301",   "name": "Venture Creation",                  "cr": 3, "status": "plan"},
            {"code": "MK 301",   "name": "Marketing Management",              "cr": 3, "status": "plan"},
            {"code": "FI 301",   "name": "Financial Management",              "cr": 3, "status": "plan"},
            {"code": "IE 311",   "name": "Design Thinking",                   "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "SB 113",   "name": "Entrepreneurship & Business Innovation","cr": 3,"status": "done"},
        ],
    },
    "Civil Engineering": {
        "credits_required": 128,
        "current": [
            {"code": "CE 201",   "name": "Civil Engineering Materials",       "cr": 3, "status": "plan"},
            {"code": "CE 221",   "name": "Engineering Statics",               "cr": 3, "status": "plan"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "plan"},
            {"code": "PH 131",   "name": "Physics I: Mechanics",              "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "CE 322",   "name": "Structural Analysis",               "cr": 3, "status": "plan"},
            {"code": "CE 331",   "name": "Fluid Mechanics",                   "cr": 3, "status": "plan"},
            {"code": "CE 341",   "name": "Geotechnical Engineering",          "cr": 3, "status": "plan"},
            {"code": "MA 231",   "name": "Differential Equations",            "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "CM 131",   "name": "General Chemistry I",               "cr": 3, "status": "done"},
        ],
    },
    "Data Science": {
        "credits_required": 120,
        "current": [
            {"code": "CS 141",   "name": "Introduction to Computer Science",  "cr": 3, "status": "plan"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "plan"},
            {"code": "STAT 282", "name": "Statistics for Engineers",          "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "plan"},
            {"code": "CS 344",   "name": "Data Structures & Algorithms",      "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "CS 447",   "name": "Machine Learning",                  "cr": 3, "status": "plan"},
            {"code": "STAT 383", "name": "Probability & Statistics",          "cr": 3, "status": "plan"},
            {"code": "MA 132",   "name": "Calculus II",                       "cr": 3, "status": "plan"},
            {"code": "CS 443",   "name": "Database Systems",                  "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "done"},
        ],
    },
    "Chemical Engineering": {
        "credits_required": 132,
        "current": [
            {"code": "CHE 211",  "name": "Material & Energy Balances",        "cr": 3, "status": "plan"},
            {"code": "CM 131",   "name": "General Chemistry I",               "cr": 3, "status": "plan"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "plan"},
            {"code": "PH 131",   "name": "Physics I: Mechanics",              "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "CHE 312",  "name": "Chemical Engineering Thermodynamics","cr": 3,"status": "plan"},
            {"code": "CHE 321",  "name": "Fluid Mechanics",                   "cr": 3, "status": "plan"},
            {"code": "CM 132",   "name": "General Chemistry II",              "cr": 3, "status": "plan"},
            {"code": "MA 231",   "name": "Differential Equations",            "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "CM 131",   "name": "General Chemistry I",               "cr": 3, "status": "done"},
        ],
    },
    "Biology": {
        "credits_required": 120,
        "current": [
            {"code": "BY 141",   "name": "General Biology I",                 "cr": 4, "status": "plan"},
            {"code": "CM 131",   "name": "General Chemistry I",               "cr": 3, "status": "plan"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "plan"},
            {"code": "BY 241",   "name": "Genetics",                          "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "BY 142",   "name": "General Biology II",                "cr": 4, "status": "plan"},
            {"code": "CM 132",   "name": "General Chemistry II",              "cr": 3, "status": "plan"},
            {"code": "BY 344",   "name": "Cell Biology",                      "cr": 3, "status": "plan"},
            {"code": "STAT 282", "name": "Statistics for Engineers",          "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "BY 141",   "name": "General Biology I",                 "cr": 4, "status": "done"},
        ],
    },
    "Aeronautical Engineering": {
        "credits_required": 128,
        "current": [
            {"code": "AE 160",   "name": "Introduction to Aerospace Engr",   "cr": 3, "status": "plan"},
            {"code": "ME 170",   "name": "Engineering Graphics & CAD",        "cr": 3, "status": "plan"},
            {"code": "MA 131",   "name": "Calculus I",                        "cr": 3, "status": "plan"},
            {"code": "PH 131",   "name": "Physics I: Mechanics",              "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "AE 324",   "name": "Aerodynamics",                      "cr": 3, "status": "plan"},
            {"code": "ME 323",   "name": "Thermodynamics I",                  "cr": 3, "status": "plan"},
            {"code": "MA 231",   "name": "Differential Equations",            "cr": 3, "status": "plan"},
            {"code": "PH 132",   "name": "Physics II: E&M",                   "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "CM 131",   "name": "General Chemistry I",               "cr": 3, "status": "done"},
        ],
    },
}

# Graduate course plans
GRAD_COURSE_PLANS = {
    "Computer Science (MS)": {
        "credits_required": 30,
        "current": [
            {"code": "CS 510",   "name": "Advanced Algorithms",               "cr": 3, "status": "plan"},
            {"code": "CS 520",   "name": "Machine Learning",                  "cr": 3, "status": "plan"},
            {"code": "CS 530",   "name": "Advanced Operating Systems",        "cr": 3, "status": "plan"},
        ],
        "next": [
            {"code": "CS 540",   "name": "Computer Networks",                 "cr": 3, "status": "plan"},
            {"code": "CS 550",   "name": "Research Methods in CS",            "cr": 3, "status": "plan"},
            {"code": "CS 599",   "name": "MS Thesis / Project",               "cr": 6, "status": "plan"},
        ],
        "completed": [],
    },
    "Mechanical Engineering (MS)": {
        "credits_required": 30,
        "current": [
            {"code": "ME 510",   "name": "Advanced Fluid Mechanics",          "cr": 3, "status": "plan"},
            {"code": "ME 520",   "name": "Advanced Thermodynamics",           "cr": 3, "status": "plan"},
            {"code": "ME 530",   "name": "Finite Element Analysis",           "cr": 3, "status": "plan"},
        ],
        "next": [
            {"code": "ME 540",   "name": "Advanced Materials",                "cr": 3, "status": "plan"},
            {"code": "ME 599",   "name": "MS Thesis / Project",               "cr": 6, "status": "plan"},
        ],
        "completed": [],
    },
    "Applied Data Science (MS) — STEM": {
        "credits_required": 30,
        "current": [
            {"code": "DS 501",   "name": "Foundations of Data Science",       "cr": 3, "status": "plan"},
            {"code": "DS 511",   "name": "Machine Learning I",                "cr": 3, "status": "plan"},
            {"code": "STAT 510", "name": "Statistical Learning",              "cr": 3, "status": "plan"},
        ],
        "next": [
            {"code": "DS 521",   "name": "Deep Learning",                     "cr": 3, "status": "plan"},
            {"code": "DS 531",   "name": "Big Data Analytics",                "cr": 3, "status": "plan"},
            {"code": "DS 599",   "name": "Capstone Project",                  "cr": 6, "status": "plan"},
        ],
        "completed": [],
    },
    "MBA — Residential (9-month)": {
        "credits_required": 48,
        "current": [
            {"code": "MBA 501",  "name": "Managerial Economics",              "cr": 3, "status": "plan"},
            {"code": "MBA 511",  "name": "Financial Management",              "cr": 3, "status": "plan"},
            {"code": "MBA 521",  "name": "Marketing Strategy",                "cr": 3, "status": "plan"},
            {"code": "MBA 531",  "name": "Operations & Supply Chain",         "cr": 3, "status": "plan"},
        ],
        "next": [
            {"code": "MBA 541",  "name": "Strategic Management",              "cr": 3, "status": "plan"},
            {"code": "MBA 551",  "name": "Leadership & Organizations",        "cr": 3, "status": "plan"},
            {"code": "MBA 561",  "name": "Business Analytics",                "cr": 3, "status": "plan"},
            {"code": "MBA 599",  "name": "Capstone Consulting Project",       "cr": 6, "status": "plan"},
        ],
        "completed": [],
    },
    "MBA — Healthcare Management": {
        "credits_required": 48,
        "current": [
            {"code": "MBA 501",  "name": "Managerial Economics",              "cr": 3, "status": "plan"},
            {"code": "HCA 511",  "name": "Healthcare Systems & Policy",       "cr": 3, "status": "plan"},
            {"code": "HCA 521",  "name": "Healthcare Financial Mgmt",         "cr": 3, "status": "plan"},
            {"code": "MBA 531",  "name": "Operations & Supply Chain",         "cr": 3, "status": "plan"},
        ],
        "next": [
            {"code": "HCA 541",  "name": "Healthcare Quality & Safety",       "cr": 3, "status": "plan"},
            {"code": "HCA 551",  "name": "Healthcare Law & Ethics",           "cr": 3, "status": "plan"},
            {"code": "HCA 599",  "name": "Capstone — Healthcare Strategy",    "cr": 6, "status": "plan"},
        ],
        "completed": [],
    },
    "Physician Assistant Studies (MS)": {
        "credits_required": 92,
        "current": [
            {"code": "PA 501",   "name": "Anatomy & Physiology for PAs",     "cr": 5, "status": "plan"},
            {"code": "PA 511",   "name": "Clinical Medicine I",               "cr": 5, "status": "plan"},
            {"code": "PA 521",   "name": "Pharmacology I",                   "cr": 3, "status": "plan"},
        ],
        "next": [
            {"code": "PA 531",   "name": "Clinical Medicine II",              "cr": 5, "status": "plan"},
            {"code": "PA 541",   "name": "Clinical Rotations I",              "cr": 8, "status": "plan"},
        ],
        "completed": [],
    },
    "Physical Therapy (DPT)": {
        "credits_required": 110,
        "current": [
            {"code": "PT 501",   "name": "Functional Anatomy",               "cr": 4, "status": "plan"},
            {"code": "PT 511",   "name": "Neuroscience for PT",              "cr": 3, "status": "plan"},
            {"code": "PT 521",   "name": "Examination & Evaluation",         "cr": 4, "status": "plan"},
        ],
        "next": [
            {"code": "PT 531",   "name": "Therapeutic Exercise",             "cr": 4, "status": "plan"},
            {"code": "PT 541",   "name": "Clinical Practicum I",             "cr": 6, "status": "plan"},
        ],
        "completed": [],
    },
    "Occupational Therapy (MS)": {
        "credits_required": 64,
        "current": [
            {"code": "OT 501",   "name": "Foundations of OT",                "cr": 3, "status": "plan"},
            {"code": "OT 511",   "name": "Occupational Science",             "cr": 3, "status": "plan"},
            {"code": "OT 521",   "name": "Neurology for OT",                 "cr": 3, "status": "plan"},
        ],
        "next": [
            {"code": "OT 531",   "name": "OT with Pediatric Populations",    "cr": 3, "status": "plan"},
            {"code": "OT 541",   "name": "Fieldwork I",                      "cr": 6, "status": "plan"},
        ],
        "completed": [],
    },
}

DEFAULT_COURSE_PLAN = {
    "credits_required": 120,
    "current": [
        {"code": "UNIV 190", "name": "The Clarkson Seminar",             "cr": 3, "status": "plan"},
        {"code": "ENG 110",  "name": "Academic Writing & Communication", "cr": 3, "status": "plan"},
        {"code": "MA 131",   "name": "Calculus I",                       "cr": 3, "status": "plan"},
        {"code": "Major 101","name": "Introduction to Major",            "cr": 3, "status": "plan"},
        {"code": "Elective", "name": "Free Elective",                    "cr": 3, "status": "rec"},
    ],
    "next": [
        {"code": "Major 201","name": "Core Major Course I",              "cr": 3, "status": "plan"},
        {"code": "Major 202","name": "Core Major Course II",             "cr": 3, "status": "plan"},
        {"code": "MA 132",   "name": "Calculus II",                      "cr": 3, "status": "plan"},
        {"code": "Major 203","name": "Major Elective",                   "cr": 3, "status": "plan"},
    ],
    "completed": [
        {"code": "ENG 110",  "name": "Academic Writing & Communication", "cr": 3, "status": "done"},
    ],
}

DEFAULT_GRAD_PLAN = {
    "credits_required": 30,
    "current": [
        {"code": "GRAD 501", "name": "Graduate Core Course I",           "cr": 3, "status": "plan"},
        {"code": "GRAD 511", "name": "Graduate Core Course II",          "cr": 3, "status": "plan"},
        {"code": "GRAD 521", "name": "Research Methods",                 "cr": 3, "status": "plan"},
    ],
    "next": [
        {"code": "GRAD 531", "name": "Elective I",                       "cr": 3, "status": "plan"},
        {"code": "GRAD 541", "name": "Elective II",                      "cr": 3, "status": "plan"},
        {"code": "GRAD 599", "name": "Thesis / Capstone",                "cr": 6, "status": "plan"},
    ],
    "completed": [],
}

CAREER_DATA = {
    "Software Engineering": {
        "match": 91, "avg_salary": "$74,000",
        "skills": ["Python", "CS 344 Data Structures", "Software Design", "Algorithms"],
        "gaps":   ["CS 444 Operating Systems", "Cloud platforms", "DevOps"],
        "employers": ["Amazon", "IBM", "GE", "Lockheed Martin"],
    },
    "Data Science & AI": {
        "match": 87, "avg_salary": "$78,000",
        "skills": ["Python", "STAT 383 Probability", "Machine Learning", "SQL"],
        "gaps":   ["CS 447 ML course", "Deep Learning frameworks", "Big Data tools"],
        "employers": ["IBM", "NYSERDA", "GE Aviation", "Webroot"],
    },
    "Mechanical / Aerospace Engineering": {
        "match": 93, "avg_salary": "$72,000",
        "skills": ["ME 221 Statics", "CAD/SolidWorks", "Thermodynamics", "FEA"],
        "gaps":   ["ME 423 Design of Propulsion Systems", "Materials science elective"],
        "employers": ["GE Aviation", "NASA", "Tesla", "SpaceX", "Lockheed Martin"],
    },
    "Civil & Environmental Engineering": {
        "match": 88, "avg_salary": "$68,000",
        "skills": ["CE 322 Structural Analysis", "AutoCAD", "Fluid Mechanics"],
        "gaps":   ["CE 451 Senior Design", "Environmental regulations coursework"],
        "employers": ["HDR", "AECOM", "NYS DOT", "US Army Corps of Engineers"],
    },
    "Chemical Engineering": {
        "match": 85, "avg_salary": "$71,000",
        "skills": ["CHE 211 Material & Energy Balances", "Process simulation"],
        "gaps":   ["CHE 421 Reactor Design", "Plant design capstone"],
        "employers": ["Pfizer", "BASF", "Air Products", "Kodak"],
    },
    "Product Management": {
        "match": 74, "avg_salary": "$75,000",
        "skills": ["Communication", "Business fundamentals", "Project management"],
        "gaps":   ["UX research methods", "Agile/Scrum certification"],
        "employers": ["Amazon", "Disney", "GE", "IBM"],
    },
    "Supply Chain & Logistics": {
        "match": 82, "avg_salary": "$67,000",
        "skills": ["SCM coursework", "Data analysis", "Operations management"],
        "gaps":   ["ERP systems (SAP)", "CSCP certification"],
        "employers": ["Amazon", "Walmart", "Raytheon", "Amphenol"],
    },
    "Finance & Consulting": {
        "match": 70, "avg_salary": "$71,000",
        "skills": ["AC 201 Financial Accounting", "FI 301 Financial Mgmt", "Excel"],
        "gaps":   ["CFA preparation", "FI 401 Investments", "Financial modeling"],
        "employers": ["Deloitte", "PwC", "Goldman Sachs", "JP Morgan"],
    },
    "Research & Academia": {
        "match": 78, "avg_salary": "$55,000",
        "skills": ["Research methods", "STAT coursework", "Technical writing"],
        "gaps":   ["Graduate school prep (GRE)", "Conference publications"],
        "employers": ["Clarkson CAMP", "NSF", "NIH", "National Laboratories"],
    },
    "Entrepreneurship": {
        "match": 80, "avg_salary": "$60,000",
        "skills": ["SB 113 Entrepreneurship & Innovation", "Networking", "Problem-solving"],
        "gaps":   ["Ignite Presidential Fellowship", "Cube Accelerator", "Legal/IP basics"],
        "employers": ["Cube Accelerator startups", "Self-founded ventures"],
    },
    "Healthcare & Biomedical": {
        "match": 76, "avg_salary": "$62,000",
        "skills": ["Biology coursework", "Chemistry", "Research lab skills"],
        "gaps":   ["Clinical hours", "Medical school prep (MCAT)", "Healthcare policy"],
        "employers": ["Albany Medical Center", "Pfizer", "Boston Scientific"],
    },
    "Government & Policy": {
        "match": 68, "avg_salary": "$55,000",
        "skills": ["Environmental Science & Policy courses", "Research", "Writing"],
        "gaps":   ["Government internship", "Public law fundamentals"],
        "employers": ["NYSERDA", "EPA", "NYS DEC", "US Army Corps"],
    },
}

CAMPUS_RESOURCES = [
    {
        "name": "Student Success Center (SSC)",
        "desc": "The hub of academic support at Clarkson. Free tutoring (sign up via myCU), academic skills coaching, time management, study strategies, and test prep. Also home to HEOP and CUPO programs for underrepresented students.",
        "contact": "315-268-2209 | ssc@clarkson.edu | ERC 1400",
        "hours": "Mon–Fri, 8am–4:30pm",
        "tag": "Tutoring", "tag_class": "tag-tutoring",
    },
    {
        "name": "Writing Center",
        "desc": "Free 25-minute one-on-one sessions with peer writing tutors. Reviews essays, lab reports, business plans, and technical documents. Online resources also available.",
        "contact": "315-268-4439 | wcenter@clarkson.edu | Snell Hall 139",
        "hours": "Mon–Fri, by appointment",
        "tag": "Writing", "tag_class": "tag-writing",
    },
    {
        "name": "Kevin & Annie Parker Career Center",
        "desc": "Resume/cover letter reviews, mock interviews, co-op and internship search via Handshake (750,000+ companies). Twice-yearly Career Fairs bring 200+ employers to campus. All majors require at least one Professional Experience before graduation.",
        "contact": "315-268-6477 | career@clarkson.edu | ERC 2nd Floor",
        "hours": "Mon–Fri, 8am–4:30pm",
        "tag": "Career", "tag_class": "tag-career",
    },
    {
        "name": "Student Health & Counseling (SHAC)",
        "desc": "On-campus health clinic and counseling center. Illness/injury care, immunizations, individual and group counseling, 24/7 mental health crisis support. Partnered with Mantra Health for free online therapy and emotional wellness coaching.",
        "contact": "315-268-6633 | shac@clarkson.edu | ERC Suite 1300",
        "hours": "Mon–Fri, 8am–4:30pm | 24/7 crisis: Campus Safety 315-268-6666",
        "tag": "Health & Counseling", "tag_class": "tag-health",
    },
    {
        "name": "Student Achievement Services (SAS)",
        "desc": "One-stop office: Registrar, academic advising, Bursar, and Financial Aid. FAFSA guidance, student loans, tuition payment plans, transcript requests, academic records, course scheduling, and graduation audits.",
        "contact": "315-268-6451 | sas@clarkson.edu | TAC 207",
        "hours": "Mon–Fri, 8am–4:30pm",
        "tag": "Financial Aid & Registration", "tag_class": "tag-registration",
    },
    {
        "name": "Office of Accessibility Services",
        "desc": "Academic accommodations for disabilities including learning differences, mental health conditions, and physical disabilities. Assistive technology, extended test time, note-taking support, and other adjustments.",
        "contact": "315-268-2006 | accessibility@clarkson.edu",
        "hours": "Mon–Fri, 8am–4:30pm",
        "tag": "Accessibility", "tag_class": "tag-accessibility",
    },
    {
        "name": "International Center",
        "desc": "Supports international students with visa and OPT processes, STEM OPT eligibility, study abroad programs. Clarkson partners with 55 universities in 28 countries for international study.",
        "contact": "315-268-3943 | Potsdam Campus",
        "hours": "Mon–Fri, 8am–4:30pm",
        "tag": "International", "tag_class": "tag-international",
    },
    {
        "name": "Reach Out Hotline",
        "desc": "24/7 crisis and information hotline for mental health support, basic needs, and alcohol/drug concerns. Mobile crisis team available to meet individuals at risk anywhere in the region.",
        "contact": "315-265-2422 | reachouthotline.org",
        "hours": "24/7, 365 days a year",
        "tag": "Health & Counseling", "tag_class": "tag-health",
    },
    {
        "name": "Suicide & Crisis Lifeline",
        "desc": "Free, confidential support for people in suicidal crisis or emotional distress. Available by call, text, or online chat.",
        "contact": "Call or text 988 | 988lifeline.org",
        "hours": "24/7",
        "tag": "Health & Counseling", "tag_class": "tag-health",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "onboarded": False, "name": "", "major": "",
        "level": "Undergraduate", "year": YEARS[0],
        "credits": 0, "careers": [], "career_other": "",
        "challenges": "", "messages": [], "active_tab": "Overview",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def get_plan():
    major = st.session_state.major
    if st.session_state.level == "Graduate":
        return GRAD_COURSE_PLANS.get(major, DEFAULT_GRAD_PLAN)
    return COURSE_PLANS.get(major, DEFAULT_COURSE_PLAN)

def degree_stats():
    plan  = get_plan()
    total = plan["credits_required"]
    creds = st.session_state.credits
    remaining = max(0, total - creds)
    pct   = min(100, round((creds / total) * 100))
    sems_left = math.ceil(remaining / (9 if st.session_state.level == "Graduate" else 15))
    grad_year = 2025 + math.ceil(sems_left / 2)
    return creds, remaining, pct, sems_left, grad_year, total

def all_careers_display():
    careers = list(st.session_state.careers)
    if st.session_state.career_other:
        careers.append(st.session_state.career_other)
    return careers

# ─────────────────────────────────────────────────────────────────────────────
#  ONBOARDING
# ─────────────────────────────────────────────────────────────────────────────

def show_onboarding():
    st.markdown('<div class="brand-bar"></div>', unsafe_allow_html=True)

    # Clarkson University logo via official website
    st.markdown("""
    <div class="cu-logo-strip">
      <img src="https://www.clarkson.edu/themes/custom/clarkson_theme/dist/img/logo.png"
           alt="Clarkson University" style="height:60px; margin-bottom: 8px;" />
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1.2rem;">
      <div style="background:#ffcd00; color:#004e42; font-weight:800; font-size:1.3rem;
                  display:inline-block; padding:10px 26px; border-radius:12px;
                  letter-spacing:-0.3px;">myAdvisr</div>
      <h1 style="color:#004e42; margin: 1rem 0 0.3rem; font-size:2rem;">
        Your AI academic advisor is here
      </h1>
      <p style="color:#555; font-size:1rem; max-width:520px; margin: 0 auto 1.5rem;">
        Powered by AI, built for Clarkson Golden Knights. Plan your degree, find the right
        courses, and align your goals with your career.
      </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("onboarding_form"):
            st.markdown("#### Tell us about yourself")

            name = st.text_input("First name", placeholder="e.g. Graham")

            level = st.radio("Degree level", ["Undergraduate", "Graduate"], horizontal=True)

            if level == "Undergraduate":
                school = st.selectbox("School / College", list(CLARKSON_SCHOOLS_UG.keys()))
                major  = st.selectbox("Your major", CLARKSON_SCHOOLS_UG[school])
            else:
                school = st.selectbox("Graduate school / program area", list(CLARKSON_SCHOOLS_GRAD.keys()))
                major  = st.selectbox("Your program", CLARKSON_SCHOOLS_GRAD[school])

            year = st.selectbox("Academic year / standing", YEARS)

            credits_label = "Credits completed" if level == "Undergraduate" else "Graduate credits completed"
            credits = st.number_input(credits_label, min_value=0, max_value=250, value=0, step=1)

            st.markdown("**Career interests** *(select all that apply)*")
            careers_selected = []
            cols = st.columns(2)
            for i, opt in enumerate(CAREER_OPTIONS):
                with cols[i % 2]:
                    if opt == "Other (enter below)":
                        if st.checkbox(opt, key=f"c_{i}"):
                            careers_selected.append("__other__")
                    else:
                        if st.checkbox(opt, key=f"c_{i}"):
                            careers_selected.append(opt)

            career_other = ""
            if "__other__" in careers_selected:
                career_other = st.text_input(
                    "Describe your career interest",
                    placeholder="e.g. Sports analytics, climate tech, film production..."
                )

            challenges = st.text_area(
                "Any challenges or goals? *(optional)*",
                placeholder="e.g. Struggling with calculus, want to do a co-op, unsure which electives to pick...",
                height=80,
            )
            submitted = st.form_submit_button("Launch myAdvisr →", use_container_width=True)

        if submitted:
            final_careers = [c for c in careers_selected if c != "__other__"]
            st.session_state.name        = name.strip() or "Student"
            st.session_state.major       = major
            st.session_state.level       = level
            st.session_state.year        = year
            st.session_state.credits     = int(credits)
            st.session_state.careers     = final_careers if final_careers else ["Software Engineering"]
            st.session_state.career_other = career_other.strip()
            st.session_state.challenges  = challenges
            st.session_state.onboarded   = True

            plan  = GRAD_COURSE_PLANS.get(major, DEFAULT_GRAD_PLAN) if level == "Graduate" else COURSE_PLANS.get(major, DEFAULT_COURSE_PLAN)
            total = plan["credits_required"]
            all_c = all_careers_display()
            welcome = (
                f"Hi {st.session_state.name}! I'm myAdvisr, your AI academic advisor "
                f"for Clarkson University. You're studying {major} ({total} credits required) "
                f"with {int(credits)} credits completed.\n\n"
                f"I've built your personalized dashboard using real Clarkson programs and resources. "
                f"Ask me anything — which courses to take next, how to land a co-op or internship, "
                f"career planning, or campus resources. Go Knights!"
            )
            st.session_state.messages = [{"role": "assistant", "content": welcome}]
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

def show_sidebar():
    with st.sidebar:
        st.markdown(
            '<p style="font-size:1.4rem;font-weight:800;color:#ffcd00!important;margin-bottom:0;">myAdvisr</p>'
            '<p style="font-size:0.7rem;color:#9ecec8!important;margin-top:0;">CLARKSON UNIVERSITY · GO KNIGHTS</p>',
            unsafe_allow_html=True,
        )
        st.divider()

        creds, remaining, pct, sems_left, grad_year, total = degree_stats()
        level_label = "Graduate" if st.session_state.level == "Graduate" else "Undergrad"
        st.markdown(f'<p style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;">Degree Progress ({level_label})</p>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="prog-wrap"><div class="prog-bar" style="width:{pct}%"></div></div>'
            f'<p style="font-size:0.75rem;color:#9ecec8!important;">{creds} of {total} credits · {pct}% complete</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"**Student:** {st.session_state.name}  \n"
            f"**Program:** {st.session_state.major}  \n"
            f"**Year:** {st.session_state.year}  \n"
            f"**Grad target:** {grad_year}  \n"
            f"**Semesters left:** ~{sems_left}",
        )
        st.divider()

        st.markdown('<p style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;">Navigation</p>', unsafe_allow_html=True)
        for tab in ["Overview", "Course Plan", "Career Paths", "Campus Resources", "AI Advisor"]:
            if st.button(("▶ " if st.session_state.active_tab == tab else "   ") + tab, key=f"nav_{tab}", use_container_width=True):
                st.session_state.active_tab = tab
                st.rerun()

        st.divider()
        if st.button("← Start over", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
#  TAB: OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────

def tab_overview():
    creds, remaining, pct, sems_left, grad_year, total = degree_stats()
    all_c = all_careers_display()
    top_career = all_c[0] if all_c else "Software Engineering"
    match_pct  = CAREER_DATA.get(top_career, {}).get("match", 80)

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card accent">
        <div class="metric-label">Credits completed</div>
        <div class="metric-value">{creds}</div>
        <div class="metric-sub">of {total} required</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Semesters left</div>
        <div class="metric-value">~{sems_left}</div>
        <div class="metric-sub">estimated</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Grad target</div>
        <div class="metric-value">{grad_year}</div>
        <div class="metric-sub">on current pace</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Top career match</div>
        <div class="metric-value gold">{match_pct}%</div>
        <div class="metric-sub">{top_career}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(
        f'<div class="prog-wrap" style="height:14px;border-radius:8px;">'
        f'<div class="prog-bar" style="width:{pct}%;height:14px;border-radius:8px;"></div></div>'
        f'<p style="font-size:0.8rem;color:#555;margin-top:4px;">{pct}% complete — {remaining} credits remaining toward your {st.session_state.major} degree</p>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-head">Advisor alerts</div>', unsafe_allow_html=True)
    alerts = []
    is_grad = st.session_state.level == "Graduate"

    if creds == 0:
        if is_grad:
            alerts.append(("info", f"<b>Welcome to Clarkson Graduate School, {st.session_state.name}!</b> Connect with your faculty advisor early. Graduate Admissions: 518-631-9831 | graduate@clarkson.edu"))
        else:
            alerts.append(("info", f"<b>Welcome to Clarkson, {st.session_state.name}!</b> Start with UNIV 190 (The Clarkson Seminar) and your school core. See Student Achievement Services (TAC 207) to confirm your plan."))
    elif creds < 30 and not is_grad:
        alerts.append(("info", f"<b>Building momentum!</b> Focus on your math/science sequence and core major courses. Over 30% of Clarkson students use the Student Success Center — don't wait to ask for help."))

    if not is_grad:
        alerts.append(("warn", "<b>Professional Experience required:</b> All Clarkson undergrads must complete at least one co-op or internship before graduation. Visit the Parker Career Center (ERC 2nd floor, 315-268-6477) and create your Handshake profile."))

    if is_grad:
        alerts.append(("info", "<b>Graduate resources:</b> The Parker Career Center supports graduate students too. Career Fairs (fall & spring) are open to all students. Graduate Student Association: sites.clarkson.edu/cugsa"))
        if "MBA" in st.session_state.major:
            alerts.append(("crit", "<b>4+1 / dual degree note:</b> If completing an MBA dual degree with Applied Data Science, contact the Reh School advising office to coordinate your course plan across both programs."))

    if "Data Science & AI" in all_c or "Software Engineering" in all_c:
        alerts.append(("info", "<b>Career tip:</b> CS 344 (Data Structures) and CS 447 (Machine Learning) are highly sought by employers. Clarkson Career Fairs bring Amazon, IBM, GE, and 200+ companies twice a year."))

    alerts.append(("crit", "<b>Registration reminder:</b> Plan your next semester with Student Achievement Services (TAC 207, 315-268-6451) — advising, registration, and financial aid all under one roof."))

    if st.session_state.challenges:
        snippet = st.session_state.challenges[:100] + ("..." if len(st.session_state.challenges) > 100 else "")
        alerts.append(("info", f"<b>Your goal:</b> \"{snippet}\" — factoring this into all recommendations."))

    dot_class = {"warn": "dot-warn", "info": "dot-info", "crit": "dot-crit"}
    for kind, text in alerts:
        st.markdown(
            f'<div class="alert-card {kind}"><div class="alert-dot {dot_class[kind]}"></div><div class="alert-text">{text}</div></div>',
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────────────────────
#  TAB: COURSE PLAN
# ─────────────────────────────────────────────────────────────────────────────

def tab_courses():
    plan  = get_plan()
    total = plan["credits_required"]
    level_note = "Graduate program" if st.session_state.level == "Graduate" else "undergraduate catalog"
    st.markdown(
        f'<p style="color:#555;font-size:0.88rem;margin-bottom:1rem;">'
        f'<b>{st.session_state.major}</b> requires <b>{total} credits</b>. '
        f'Courses based on the Clarkson University {level_note}.</p>',
        unsafe_allow_html=True,
    )

    semesters = [
        {"name": "Current semester (Spring 2025)", "courses": plan["current"], "credits": sum(c["cr"] for c in plan["current"])},
        {"name": "Recommended next (Fall 2025)",   "courses": plan["next"],    "credits": sum(c["cr"] for c in plan["next"])},
    ]
    if plan["completed"]:
        semesters.append({"name": "Completed", "courses": plan["completed"], "credits": st.session_state.credits})

    badge = {"done": "badge-done", "plan": "badge-plan", "rec": "badge-rec"}
    label = {"done": "Completed",  "plan": "Planned",    "rec": "Recommended"}

    for sem in semesters:
        rows = "".join(
            f'<div class="course-row">'
            f'<span class="course-code">{c["code"]}</span>'
            f'<span class="course-name">{c["name"]}</span>'
            f'<span class="course-cr">{c["cr"]} cr</span>'
            f'<span class="badge {badge[c["status"]]}">{label[c["status"]]}</span>'
            f'</div>' for c in sem["courses"]
        )
        st.markdown(
            f'<div class="sem-block"><div class="sem-header"><span>{sem["name"]}</span><span>{sem["credits"]} credits</span></div>{rows}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<p style="font-size:0.78rem;color:#888;margin-top:0.5rem;">'
        'Confirm your exact plan with your advisor at Student Achievement Services, TAC 207, 315-268-6451. '
        'Graduate students: contact your faculty advisor or graduate@clarkson.edu.</p>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
#  TAB: CAREER PATHS
# ─────────────────────────────────────────────────────────────────────────────

def tab_career():
    all_c = all_careers_display()
    shown = all_c[:3]
    st.markdown(
        f'<p style="color:#555;font-size:0.88rem;margin-bottom:1rem;">'
        f'Based on your {st.session_state.major} program. '
        f"Clarkson Class of 2023: 99% placement rate, avg starting salary $71,000+.</p>",
        unsafe_allow_html=True,
    )

    for career in shown:
        d = CAREER_DATA.get(career, {
            "match": 75, "avg_salary": "$65,000",
            "skills": ["Core coursework", "Communication"],
            "gaps":   ["Internship experience", "Specialized elective"],
            "employers": ["Various industry partners"],
        })
        skills_html   = "".join(f'<span class="skill-tag">{s}</span>' for s in d["skills"])
        gaps_html     = "".join(f'<span class="skill-tag skill-gap">{g}</span>' for g in d["gaps"])
        employer_html = "".join(f'<span class="skill-tag">{e}</span>' for e in d["employers"])
        st.markdown(f"""
        <div class="career-card">
          <div class="career-title">{career}</div>
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;font-size:0.82rem;color:#8a6c00;">
            <div class="match-wrap"><div class="match-fill" style="width:{d['match']}%"></div></div>
            {d['match']}% match &nbsp;·&nbsp; Avg. starting salary: <b>{d['avg_salary']}</b>
          </div>
          <div style="font-size:0.75rem;color:#555;margin-bottom:4px;">Relevant coursework & skills:</div>
          <div style="margin-bottom:8px;">{skills_html}</div>
          <div style="font-size:0.75rem;color:#cf4520;margin-bottom:4px;">Gaps to address:</div>
          <div style="margin-bottom:8px;">{gaps_html}</div>
          <div style="font-size:0.75rem;color:#555;margin-bottom:4px;">Companies that recruit at Clarkson:</div>
          <div>{employer_html}</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  TAB: CAMPUS RESOURCES
# ─────────────────────────────────────────────────────────────────────────────

def tab_resources():
    st.markdown(
        '<p style="color:#555;font-size:0.88rem;margin-bottom:1rem;">'
        'Real Clarkson University resources with actual contacts and locations. '
        'Over 50% of students use health and counseling services every year.</p>',
        unsafe_allow_html=True,
    )
    for r in CAMPUS_RESOURCES:
        st.markdown(f"""
        <div class="resource-card">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <span style="font-size:0.95rem;font-weight:700;color:#004e42;">{r['name']}</span>
            <span class="resource-tag {r['tag_class']}">{r['tag']}</span>
          </div>
          <div style="font-size:0.82rem;color:#333;line-height:1.5;margin-bottom:6px;">{r['desc']}</div>
          <div style="font-size:0.75rem;color:#555;">
            <b>Contact:</b> {r['contact']} &nbsp;·&nbsp; <b>Hours:</b> {r['hours']}
          </div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  TAB: AI ADVISOR
# ─────────────────────────────────────────────────────────────────────────────

def build_system_prompt():
    s     = st.session_state
    plan  = get_plan()
    all_c = all_careers_display()
    grad_note = "This is a graduate student." if s.level == "Graduate" else "This is an undergraduate student."
    return (
        f"You are myAdvisr, an expert AI academic advisor for Clarkson University (Potsdam, NY).\n\n"
        f"Student profile:\n"
        f"- Name: {s.name}\n"
        f"- Program: {s.major} ({plan['credits_required']} credits required)\n"
        f"- Level: {s.level}. {grad_note}\n"
        f"- Year / standing: {s.year}\n"
        f"- Credits completed: {s.credits} of {plan['credits_required']}\n"
        f"- Career interests: {', '.join(all_c) if all_c else 'Not specified'}\n"
        f"- Challenges/goals: {s.challenges if s.challenges else 'None specified'}\n\n"
        f"Real Clarkson contacts to cite in responses:\n"
        f"- Parker Career Center: ERC 2nd floor, 315-268-6477, career@clarkson.edu, Handshake platform\n"
        f"- Student Success Center (tutoring): ERC 1400, 315-268-2209, ssc@clarkson.edu\n"
        f"- SHAC (health/counseling): ERC Suite 1300, 315-268-6633, shac@clarkson.edu\n"
        f"- Student Achievement Services (registrar/advising/financial aid): TAC 207, 315-268-6451\n"
        f"- Writing Center: Snell Hall 139, 315-268-4439, wcenter@clarkson.edu\n"
        f"- Graduate Admissions: 518-631-9831, graduate@clarkson.edu\n"
        f"- Career Fairs: twice yearly (fall & spring), 200+ employers, open to all students\n"
        f"- Class of 2023: 99% placement rate, avg starting salary $71,000+\n"
        f"- All undergrads must complete a Professional Experience (co-op/internship) before graduation\n"
        f"- 4+1 programs available for undergrads to earn a master's in 5 years\n"
        f"- UNIV 190 (The Clarkson Seminar) required for all first-year undergrads\n"
        f"- SB 113 (Entrepreneurship & Business Innovation) required for all Reh School students\n"
        f"- Mantra Health: free online therapy for all enrolled students\n"
        f"- Ignite entrepreneurship program and Cube business accelerator available\n"
        f"- International experience required for all Reh School undergrad students\n\n"
        f"Be warm, specific, and actionable. Reference real Clarkson courses, offices, and phone numbers. "
        f"Keep responses under 160 words unless a detailed plan is needed. Plain text only, no markdown."
    )

def tab_chat():
    st.markdown('<div style="font-size:0.8rem;color:#555;margin-bottom:1rem;">Powered by Claude · Knows real Clarkson programs, courses, and resources</div>', unsafe_allow_html=True)
    st.markdown("**Quick questions:**")
    is_grad = st.session_state.level == "Graduate"
    qcols = st.columns(4)
    quick = [
        ("Next semester courses", "What courses should I take next semester for my program?"),
        ("Find a co-op" if not is_grad else "Career support", "How do I find a co-op or internship at Clarkson?" if not is_grad else "What career support does Clarkson offer for graduate students?"),
        ("Graduation check",      "Am I on track to graduate on time?"),
        ("Campus resources",      "What resources are available if I am struggling academically?"),
    ]
    for i, (lbl, prompt) in enumerate(quick):
        with qcols[i]:
            if st.button(lbl, key=f"qp_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.spinner("myAdvisr is thinking..."):
                    reply = get_claude_response(prompt)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

    st.divider()

    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.markdown(
                f'<div class="label-ai chat-label">myAdvisr</div>'
                f'<div class="chat-ai">{msg["content"].replace(chr(10), "<br>")}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="label-user chat-label">{st.session_state.name}</div>'
                f'<div class="chat-user">{msg["content"]}</div>',
                unsafe_allow_html=True,
            )

    user_input = st.chat_input("Ask your advisor anything about Clarkson...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("myAdvisr is thinking..."):
            reply = get_claude_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

def get_claude_response(user_message: str) -> str:
    try:
        client = Anthropic()
        history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[:-1]
            if m["role"] in ("user", "assistant")
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=512,
            system=build_system_prompt(),
            messages=history + [{"role": "user", "content": user_message}],
        )
        return response.content[0].text
    except Exception as e:
        return (
            f"I am having trouble connecting right now ({type(e).__name__}). "
            "Make sure your ANTHROPIC_API_KEY is set and try again."
        )

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    if not st.session_state.onboarded:
        show_onboarding()
        return

    show_sidebar()
    st.markdown('<div class="brand-bar"></div>', unsafe_allow_html=True)
    level_badge = "Graduate" if st.session_state.level == "Graduate" else "Undergraduate"
    st.markdown(
        f'<div class="page-header">'
        f'<div class="logo-badge">myAdvisr</div>'
        f'<div><h1>Welcome back, {st.session_state.name}</h1>'
        f'<p>{st.session_state.major} · {level_badge} · {st.session_state.year} · Clarkson University, Potsdam NY</p></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    tab = st.session_state.active_tab
    st.markdown(f'<div class="section-head">{tab}</div>', unsafe_allow_html=True)

    if   tab == "Overview":         tab_overview()
    elif tab == "Course Plan":      tab_courses()
    elif tab == "Career Paths":     tab_career()
    elif tab == "Campus Resources": tab_resources()
    elif tab == "AI Advisor":       tab_chat()

if __name__ == "__main__":
    main()
