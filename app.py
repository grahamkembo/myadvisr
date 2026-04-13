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
</style>
""", unsafe_allow_html=True)

TOTAL_CREDITS = 120

CLARKSON_SCHOOLS = {
    "Coulter School of Engineering & Applied Sciences": [
        "Aeronautical Engineering", "Chemical Engineering", "Civil Engineering",
        "Computer Engineering", "Computer Science", "Data Science",
        "Electrical Engineering", "Environmental Engineering",
        "Mechanical Engineering", "Engineering & Management",
        "Engineering Studies (undecided)",
    ],
    "Reh School of Business": [
        "Business Administration", "Business Intelligence & Data Analytics",
        "Financial Information & Analysis", "Global Supply Chain Management",
        "Innovation & Entrepreneurship", "Business Studies (undecided)",
    ],
    "Lewis School of Health & Life Sciences": [
        "Biology", "Biomolecular Science", "Chemistry",
        "Environmental Health Science", "Physics",
        "Applied Mathematics & Statistics", "Mathematics",
        "Mathematical Economics", "Psychology",
    ],
    "Institute for a Sustainable Environment": [
        "Environmental Science & Policy", "Digital Arts & Sciences",
        "Interdisciplinary Liberal Studies", "Interdisciplinary Social Sciences",
    ],
}

ALL_MAJORS = sorted(set(m for mlist in CLARKSON_SCHOOLS.values() for m in mlist))
YEARS = ["Freshman (1st year)", "Sophomore (2nd year)", "Junior (3rd year)", "Senior (4th year)", "Graduate Student"]

CAREER_OPTIONS = [
    "Software Engineering", "Data Science & AI",
    "Mechanical / Aerospace Engineering", "Civil & Environmental Engineering",
    "Chemical Engineering", "Product Management",
    "Supply Chain & Logistics", "Finance & Consulting",
    "Research & Academia", "Entrepreneurship",
    "Healthcare & Biomedical", "Government & Policy",
]

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
            {"code": "BA 100",   "name": "Introduction to Business",          "cr": 3, "status": "plan"},
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
    "Global Supply Chain Management": {
        "credits_required": 120,
        "current": [
            {"code": "SCM 201",  "name": "Introduction to Supply Chain Mgmt", "cr": 3, "status": "plan"},
            {"code": "AC 201",   "name": "Financial Accounting",              "cr": 3, "status": "plan"},
            {"code": "EC 200",   "name": "Principles of Economics",           "cr": 3, "status": "plan"},
            {"code": "UNIV 190", "name": "The Clarkson Seminar",              "cr": 3, "status": "plan"},
            {"code": "IS 301",   "name": "Business Information Systems",      "cr": 3, "status": "rec"},
        ],
        "next": [
            {"code": "SCM 301",  "name": "Operations Management",             "cr": 3, "status": "plan"},
            {"code": "SCM 311",  "name": "Logistics & Transportation",        "cr": 3, "status": "plan"},
            {"code": "MG 301",   "name": "Organizational Behavior",           "cr": 3, "status": "plan"},
            {"code": "STAT 282", "name": "Statistics for Engineers",          "cr": 3, "status": "plan"},
        ],
        "completed": [
            {"code": "ENG 110",  "name": "Academic Writing & Communication",  "cr": 3, "status": "done"},
            {"code": "EC 200",   "name": "Principles of Economics",           "cr": 3, "status": "done"},
        ],
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
        {"code": "UNIV 190", "name": "The Clarkson Seminar",             "cr": 3, "status": "done"},
    ],
}

CAREER_DATA = {
    "Software Engineering": {
        "match": 91, "avg_salary": "$74,000",
        "skills": ["Python", "Algorithms", "CS 344 Data Structures", "Software Design"],
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
        "gaps":   ["CE 451 Senior Design Project", "Environmental regulations coursework"],
        "employers": ["HDR", "AECOM", "NYS DOT", "US Army Corps of Engineers"],
    },
    "Chemical Engineering": {
        "match": 85, "avg_salary": "$71,000",
        "skills": ["CHE 211 Material & Energy Balances", "Process simulation", "Chemistry"],
        "gaps":   ["CHE 421 Reactor Design", "Plant design capstone"],
        "employers": ["Pfizer", "BASF", "Air Products", "Kodak"],
    },
    "Product Management": {
        "match": 74, "avg_salary": "$75,000",
        "skills": ["Communication", "Business fundamentals", "Project management"],
        "gaps":   ["UX research methods", "Agile/Scrum certification", "Strategy coursework"],
        "employers": ["Amazon", "Disney", "GE", "IBM"],
    },
    "Supply Chain & Logistics": {
        "match": 82, "avg_salary": "$67,000",
        "skills": ["Global Supply Chain Mgmt coursework", "Data analysis", "Operations"],
        "gaps":   ["ERP systems (SAP)", "Certified Supply Chain Professional (CSCP)"],
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
        "gaps":   ["Graduate school prep (GRE)", "Conference publications", "Lab experience"],
        "employers": ["Clarkson CAMP", "NSF", "NIH", "National Laboratories"],
    },
    "Entrepreneurship": {
        "match": 80, "avg_salary": "$60,000",
        "skills": ["Innovation & Entrepreneurship courses", "Networking", "Problem-solving"],
        "gaps":   ["Ignite Presidential Fellowship", "Business plan competition", "Legal/IP basics"],
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
        "gaps":   ["Internship in government agency", "Public law fundamentals"],
        "employers": ["NYSERDA", "EPA", "NYS DEC", "US Army Corps"],
    },
}

CAMPUS_RESOURCES = [
    {
        "name": "Student Success Center (SSC)",
        "desc": "The hub of academic support at Clarkson. Free tutoring (sign up via myCU), academic skills coaching, time management, study strategies, and test prep. Also home to HEOP and CUPO programs for underrepresented students. Located in ERC 1400.",
        "contact": "315-268-2209 | ssc@clarkson.edu",
        "hours": "Mon–Fri, 8am–4:30pm",
        "tag": "Tutoring", "tag_class": "tag-tutoring",
    },
    {
        "name": "Writing Center",
        "desc": "Free 25-minute one-on-one sessions with peer writing tutors. Reviews all writing including essays, lab reports, business plans, and technical documents. Bring your assignment instructions. Online resources also available.",
        "contact": "315-268-4439 | wcenter@clarkson.edu | Snell Hall 139",
        "hours": "Mon–Fri, by appointment",
        "tag": "Writing", "tag_class": "tag-writing",
    },
    {
        "name": "Kevin & Annie Parker Career Center",
        "desc": "Comprehensive career support for all students. Resume/cover letter reviews, mock interviews, co-op and internship search via Handshake (750,000+ companies). Twice-yearly Career Fairs bring 200+ employers to campus. All majors must complete a Professional Experience before graduation. Located on 2nd floor of ERC.",
        "contact": "315-268-6477 | career@clarkson.edu",
        "hours": "Mon–Fri, 8am–4:30pm",
        "tag": "Career", "tag_class": "tag-career",
    },
    {
        "name": "Student Health & Counseling (SHAC)",
        "desc": "Integrated on-campus health clinic and counseling center. Offers illness/injury care, immunizations, individual and group counseling, and 24/7 mental health crisis support. Also partnered with Mantra Health for free online therapy, emotional wellness coaching, and on-demand support.",
        "contact": "315-268-6633 | shac@clarkson.edu | ERC Suite 1300 | 24/7 crisis: Campus Safety 315-268-6666",
        "hours": "Mon–Fri, 8am–4:30pm | 24/7 crisis support available",
        "tag": "Health & Counseling", "tag_class": "tag-health",
    },
    {
        "name": "Student Achievement Services (SAS)",
        "desc": "One-stop office housing the Registrar, academic advising, Bursar, and Office of Financial Aid. Handles FAFSA guidance, student loans, tuition payment plans, transcript requests, academic records, course scheduling, and graduation audits.",
        "contact": "315-268-6451 | sas@clarkson.edu | TAC 207",
        "hours": "Mon–Fri, 8am–4:30pm",
        "tag": "Financial Aid & Registration", "tag_class": "tag-registration",
    },
    {
        "name": "Office of Accessibility Services",
        "desc": "Provides academic accommodations for students with disabilities, including learning disabilities, mental health conditions, and physical disabilities. Coordinates assistive technology, extended test time, note-taking support, and other adjustments.",
        "contact": "315-268-2006",
        "hours": "Mon–Fri, 8am–4:30pm",
        "tag": "Accessibility", "tag_class": "tag-accessibility",
    },
    {
        "name": "International Center",
        "desc": "Supports international students with visa and OPT processes, STEM OPT eligibility, study abroad programs, and campus life adjustment. Clarkson has partnerships with 55 universities in 28 countries for international study opportunities.",
        "contact": "315-268-3943",
        "hours": "Mon–Fri, 8am–4:30pm",
        "tag": "International", "tag_class": "tag-international",
    },
    {
        "name": "Reach Out Hotline",
        "desc": "24/7 crisis and information hotline for basic needs, mental health support, and alcohol/drug concerns. A mobile crisis team of counselors is available to meet and assess individuals at risk anywhere in the region.",
        "contact": "24/7 Hotline: 315-265-2422 | reachouthotline.org",
        "hours": "24/7, 365 days a year",
        "tag": "Health & Counseling", "tag_class": "tag-health",
    },
    {
        "name": "Suicide & Crisis Lifeline",
        "desc": "Free, confidential emotional support for people in suicidal crisis or emotional distress. Available by call, text, or chat. Previously known as the National Suicide Prevention Hotline.",
        "contact": "Call or text 988 | 988lifeline.org",
        "hours": "24/7",
        "tag": "Health & Counseling", "tag_class": "tag-health",
    },
]

def init_state():
    defaults = {
        "onboarded": False, "name": "", "major": ALL_MAJORS[0],
        "year": YEARS[0], "credits": 0, "careers": [],
        "challenges": "", "messages": [], "active_tab": "Overview",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def degree_stats():
    plan = COURSE_PLANS.get(st.session_state.major, DEFAULT_COURSE_PLAN)
    total = plan["credits_required"]
    credits = st.session_state.credits
    remaining = max(0, total - credits)
    pct = min(100, round((credits / total) * 100))
    sems_left = math.ceil(remaining / 15)
    grad_year = 2025 + math.ceil(sems_left / 2)
    return credits, remaining, pct, sems_left, grad_year, total

def show_onboarding():
    st.markdown('<div class="brand-bar"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 1rem;">
      <div style="background:#ffcd00;color:#004e42;font-weight:800;font-size:1.2rem;display:inline-block;padding:10px 22px;border-radius:12px;">myAdvisr</div>
      <h1 style="color:#004e42;margin:1rem 0 0.4rem;font-size:2rem;">Your AI academic advisor is here</h1>
      <p style="color:#555;font-size:1rem;max-width:520px;margin:0 auto 1.5rem;">
        Powered by AI, built for Clarkson Golden Knights. Plan your degree, find the right courses,
        align your goals with your career.
      </p>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("onboarding_form"):
            st.markdown("#### Tell us about yourself")
            name   = st.text_input("First name", placeholder="e.g. Graham")
            school = st.selectbox("School / College", list(CLARKSON_SCHOOLS.keys()))
            major  = st.selectbox("Your major", CLARKSON_SCHOOLS[school])
            year   = st.selectbox("Academic year", YEARS)
            credits = st.number_input("Credits completed so far", min_value=0, max_value=200, value=0, step=1)
            st.markdown("**Career interests** *(select all that apply)*")
            careers_selected = []
            cols = st.columns(2)
            for i, opt in enumerate(CAREER_OPTIONS):
                with cols[i % 2]:
                    if st.checkbox(opt, key=f"c_{i}"):
                        careers_selected.append(opt)
            challenges = st.text_area("Any challenges or goals? *(optional)*",
                placeholder="e.g. Struggling with calculus, want to do a co-op, unsure which electives to pick...", height=80)
            submitted = st.form_submit_button("Launch myAdvisr →", use_container_width=True)

        if submitted:
            st.session_state.name       = name.strip() or "Student"
            st.session_state.major      = major
            st.session_state.year       = year
            st.session_state.credits    = int(credits)
            st.session_state.careers    = careers_selected or ["Software Engineering"]
            st.session_state.challenges = challenges
            st.session_state.onboarded  = True
            plan = COURSE_PLANS.get(major, DEFAULT_COURSE_PLAN)
            total = plan["credits_required"]
            welcome = (
                f"Hi {st.session_state.name}! I'm myAdvisr, your personal AI academic advisor "
                f"for Clarkson University. You're studying {major} ({total} credits required) "
                f"with {int(credits)} credits completed.\n\n"
                f"I've built your personalized dashboard using real Clarkson course plans and "
                f"campus resources. Ask me anything — which courses to take next, how to land "
                f"a co-op, career planning, or any campus resource. Go Knights!"
            )
            st.session_state.messages = [{"role": "assistant", "content": welcome}]
            st.rerun()

def show_sidebar():
    with st.sidebar:
        st.markdown(
            '<p style="font-size:1.4rem;font-weight:800;color:#ffcd00!important;margin-bottom:0;">myAdvisr</p>'
            '<p style="font-size:0.7rem;color:#9ecec8!important;margin-top:0;">CLARKSON UNIVERSITY · GO KNIGHTS</p>',
            unsafe_allow_html=True,
        )
        st.divider()
        credits, remaining, pct, sems_left, grad_year, total = degree_stats()
        st.markdown('<p style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;">Degree Progress</p>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="prog-wrap"><div class="prog-bar" style="width:{pct}%"></div></div>'
            f'<p style="font-size:0.75rem;color:#9ecec8!important;">{credits} of {total} credits · {pct}% complete</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"**Student:** {st.session_state.name}  \n"
            f"**Major:** {st.session_state.major}  \n"
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

def tab_overview():
    credits, remaining, pct, sems_left, grad_year, total = degree_stats()
    top_career = st.session_state.careers[0] if st.session_state.careers else "Software Engineering"
    match_pct  = CAREER_DATA.get(top_career, {}).get("match", 80)

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card accent">
        <div class="metric-label">Credits completed</div>
        <div class="metric-value">{credits}</div>
        <div class="metric-sub">of {total} required</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Semesters left</div>
        <div class="metric-value">~{sems_left}</div>
        <div class="metric-sub">at 15 cr/semester</div>
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
    if credits == 0:
        alerts.append(("info", f"<b>Welcome to Clarkson, {st.session_state.name}!</b> Start with UNIV 190 (The Clarkson Seminar) and your school core courses. Connect with Student Achievement Services (TAC 207) to confirm your course plan."))
    elif credits < 30:
        alerts.append(("info", f"<b>Building momentum, {st.session_state.name}!</b> Focus on your math/science sequence and core major courses. Over 30% of Clarkson students use the Student Success Center — don't wait to ask for help."))

    if st.session_state.major in ("Computer Science", "Data Science", "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Chemical Engineering", "Aeronautical Engineering", "Business Administration", "Global Supply Chain Management"):
        alerts.append(("warn", "<b>Professional Experience required:</b> All Clarkson students must complete at least one co-op or internship before graduation. Visit the Parker Career Center (ERC 2nd floor, 315-268-6477) and create your Handshake profile today."))

    if "Data Science & AI" in st.session_state.careers or "Software Engineering" in st.session_state.careers:
        alerts.append(("info", "<b>Career tip:</b> CS 344 (Data Structures) and CS 447 (Machine Learning) are key for tech roles. Clarkson's Career Fairs (fall & spring) bring Amazon, IBM, GE, and 200+ companies to campus."))

    alerts.append(("crit", "<b>Registration reminder:</b> Plan your next semester with your advisor at Student Achievement Services (TAC 207, 315-268-6451). They handle advising, registration, and financial aid under one roof."))

    if st.session_state.challenges:
        snippet = st.session_state.challenges[:100] + ("..." if len(st.session_state.challenges) > 100 else "")
        alerts.append(("info", f"<b>Your goal:</b> \"{snippet}\" — factoring this into all your recommendations."))

    dot_class = {"warn": "dot-warn", "info": "dot-info", "crit": "dot-crit"}
    for kind, text in alerts:
        st.markdown(
            f'<div class="alert-card {kind}"><div class="alert-dot {dot_class[kind]}"></div><div class="alert-text">{text}</div></div>',
            unsafe_allow_html=True,
        )

def tab_courses():
    plan = COURSE_PLANS.get(st.session_state.major, DEFAULT_COURSE_PLAN)
    total = plan["credits_required"]
    st.markdown(
        f'<p style="color:#555;font-size:0.88rem;margin-bottom:1rem;">'
        f'<b>{st.session_state.major}</b> requires <b>{total} credits</b> to graduate. '
        f'Courses are based on the Clarkson University 2023-24 undergraduate catalog.</p>',
        unsafe_allow_html=True,
    )
    semesters = [
        {"name": "Current semester (Spring 2025)", "courses": plan["current"], "credits": sum(c["cr"] for c in plan["current"])},
        {"name": "Recommended next semester (Fall 2025)", "courses": plan["next"], "credits": sum(c["cr"] for c in plan["next"])},
        {"name": "Completed", "courses": plan["completed"], "credits": st.session_state.credits},
    ]
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
        'Confirm your exact plan with your academic advisor at Student Achievement Services, TAC 207, 315-268-6451.</p>',
        unsafe_allow_html=True,
    )

def tab_career():
    shown = (st.session_state.careers or ["Software Engineering"])[:3]
    st.markdown(
        f'<p style="color:#555;font-size:0.88rem;margin-bottom:1rem;">'
        f'Based on your {st.session_state.major} major. '
        f"Clarkson Class of 2023: 99% placement rate, avg starting salary $71,000+.</p>",
        unsafe_allow_html=True,
    )
    for career in shown:
        d = CAREER_DATA.get(career, {"match": 75, "avg_salary": "$65,000", "skills": [], "gaps": [], "employers": []})
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
          <div style="font-size:0.75rem;color:#555;margin-bottom:4px;">Relevant Clarkson coursework & skills:</div>
          <div style="margin-bottom:8px;">{skills_html}</div>
          <div style="font-size:0.75rem;color:#cf4520;margin-bottom:4px;">Courses/skills still to complete:</div>
          <div style="margin-bottom:8px;">{gaps_html}</div>
          <div style="font-size:0.75rem;color:#555;margin-bottom:4px;">Companies that recruit at Clarkson:</div>
          <div>{employer_html}</div>
        </div>""", unsafe_allow_html=True)

def tab_resources():
    st.markdown(
        '<p style="color:#555;font-size:0.88rem;margin-bottom:1rem;">'
        'Real Clarkson University resources with actual contacts and locations. '
        'Over 50% of Clarkson students use health and counseling services every year.</p>',
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

def build_system_prompt():
    s = st.session_state
    plan = COURSE_PLANS.get(s.major, DEFAULT_COURSE_PLAN)
    return (
        f"You are myAdvisr, an expert AI academic advisor for Clarkson University (Potsdam, NY).\n\n"
        f"Student profile:\n"
        f"- Name: {s.name}\n"
        f"- Major: {s.major} ({plan['credits_required']} credits required)\n"
        f"- Year: {s.year}\n"
        f"- Credits completed: {s.credits} of {plan['credits_required']}\n"
        f"- Career interests: {', '.join(s.careers) if s.careers else 'Not specified'}\n"
        f"- Challenges/goals: {s.challenges if s.challenges else 'None specified'}\n\n"
        f"Real Clarkson context to use in responses:\n"
        f"- All students must complete a Professional Experience (co-op/internship) before graduation\n"
        f"- Parker Career Center: ERC 2nd floor, 315-268-6477, career@clarkson.edu, uses Handshake\n"
        f"- Student Success Center (tutoring): ERC 1400, 315-268-2209, ssc@clarkson.edu\n"
        f"- SHAC (health/counseling): ERC Suite 1300, 315-268-6633, shac@clarkson.edu\n"
        f"- Student Achievement Services (registrar/financial aid/advising): TAC 207, 315-268-6451\n"
        f"- Writing Center: Snell Hall 139, 315-268-4439, wcenter@clarkson.edu\n"
        f"- Career Fairs: twice yearly (fall and spring), 200+ employers attend\n"
        f"- Class of 2023: 99% placement rate, average starting salary $71,000+\n"
        f"- 4+1 programs available to earn a master's degree in 5 years\n"
        f"- The Clarkson Seminar (UNIV 190) is required for all first-year students\n"
        f"- Mantra Health partnership provides free online therapy for all enrolled students\n"
        f"- Ignite entrepreneurship program and Cube business accelerator available\n\n"
        f"Be warm, specific, and actionable. Reference real Clarkson courses, offices, phone numbers, and programs. "
        f"Keep responses under 160 words unless a detailed plan is requested. Plain text only, no markdown."
    )

def tab_chat():
    st.markdown('<div style="font-size:0.8rem;color:#555;margin-bottom:1rem;">Powered by Claude · Knows real Clarkson programs, courses, and resources</div>', unsafe_allow_html=True)
    st.markdown("**Quick questions:**")
    qcols = st.columns(4)
    quick = [
        ("Next semester courses", "What courses should I take next semester for my major?"),
        ("Find a co-op",          "How do I find a co-op or internship at Clarkson?"),
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

def main():
    if not st.session_state.onboarded:
        show_onboarding()
        return
    show_sidebar()
    st.markdown('<div class="brand-bar"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="page-header">'
        f'<div class="logo-badge">myAdvisr</div>'
        f'<div><h1>Welcome back, {st.session_state.name}</h1>'
        f'<p>{st.session_state.major} · {st.session_state.year} · Clarkson University, Potsdam NY</p></div>'
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
