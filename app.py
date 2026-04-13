"""
myAdvisr — AI-Powered Academic Advisor
Clarkson University | Innovation-Based AI Solution
Built with Streamlit + Anthropic Claude API
"""

import streamlit as st
from anthropic import Anthropic
import math

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="myAdvisr | Clarkson University",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Clarkson brand colors & global CSS ──────────────────────────────────────
st.markdown("""
<style>
/* ── Clarkson palette ── */
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

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* ── Top brand bar ── */
.brand-bar {
    height: 5px;
    background: linear-gradient(90deg, #004e42 60%, #ffcd00 100%);
    margin: -1rem -1rem 1.5rem -1rem;
}

/* ── Page header ── */
.page-header {
    background: var(--green);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.page-header h1 { margin: 0; font-size: 1.6rem; color: white; }
.page-header p  { margin: 0; color: rgba(255,255,255,0.75); font-size: 0.9rem; }
.logo-badge {
    background: var(--gold);
    color: var(--green);
    font-weight: 800;
    font-size: 1rem;
    padding: 8px 14px;
    border-radius: 10px;
    white-space: nowrap;
    letter-spacing: -0.3px;
}

/* ── Metric cards ── */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card {
    background: var(--card-bg);
    border: 1.5px solid #e0ece9;
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    flex: 1; min-width: 140px;
}
.metric-card.accent { border-color: var(--gold); border-width: 2px; }
.metric-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); font-weight: 600; margin-bottom: 4px; }
.metric-value { font-size: 2rem; font-weight: 700; color: var(--green); line-height: 1; margin-bottom: 2px; }
.metric-value.gold { color: var(--gold-dim); }
.metric-sub   { font-size: 0.75rem; color: var(--muted); }

/* ── Alert cards ── */
.alert-card {
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.7rem;
    display: flex;
    gap: 0.8rem;
    align-items: flex-start;
    border-left: 4px solid;
}
.alert-card.warn { background:#fffbea; border-color: var(--gold);  }
.alert-card.info { background:#eef7f0; border-color: var(--olive); }
.alert-card.crit { background:#fdf0eb; border-color: var(--coral); }
.alert-dot { width:10px; height:10px; border-radius:50%; margin-top:4px; flex-shrink:0; }
.dot-warn { background: var(--gold-dim); }
.dot-info { background: var(--olive);   }
.dot-crit { background: var(--coral);   }
.alert-text { font-size: 0.85rem; color: var(--text); line-height: 1.5; }
.alert-text b { color: var(--green); }

/* ── Progress bar ── */
.prog-wrap { background: #e0ece9; border-radius: 6px; height: 10px; margin: 6px 0 4px; overflow: hidden; }
.prog-bar  { height: 100%; border-radius: 6px; background: linear-gradient(90deg, var(--green), var(--olive)); transition: width 0.8s; }

/* ── Section heading ── */
.section-head {
    font-size: 1.15rem; font-weight: 700; color: var(--green);
    border-bottom: 2px solid var(--gold);
    padding-bottom: 6px; margin: 1.4rem 0 1rem;
}

/* ── Course table ── */
.sem-block { background: var(--card-bg); border: 1px solid #e0ece9; border-radius: 10px; margin-bottom: 1rem; overflow: hidden; }
.sem-header {
    background: var(--green); color: white;
    padding: 0.6rem 1rem;
    display: flex; justify-content: space-between; align-items: center;
    font-size: 0.85rem; font-weight: 600;
}
.course-row {
    display: flex; align-items: center; gap: 1rem;
    padding: 0.55rem 1rem;
    border-bottom: 1px solid #f5f5f5;
    font-size: 0.82rem;
}
.course-row:last-child { border-bottom: none; }
.course-code  { color: var(--muted); width: 72px; flex-shrink: 0; font-family: monospace; }
.course-name  { flex: 1; color: var(--text); }
.course-cr    { color: var(--muted); width: 36px; text-align: right; flex-shrink: 0; }
.badge        { padding: 2px 10px; border-radius: 100px; font-size: 0.7rem; font-weight: 600; }
.badge-done   { background: #eef7e6; color: #3a6e00; }
.badge-plan   { background: #fffbea; color: #8a6c00; }
.badge-rec    { background: #fdf0eb; color: #8a2a00; }

/* ── Career cards ── */
.career-card { background: var(--card-bg); border: 1px solid #e0ece9; border-radius: 10px; padding: 1.1rem 1.3rem; margin-bottom: 1rem; }
.career-title { font-size: 1rem; font-weight: 700; color: var(--green); margin-bottom: 6px; }
.match-wrap { background: #e0ece9; border-radius: 3px; height: 5px; display: inline-block; width: 90px; vertical-align: middle; margin-right: 6px; }
.match-fill { height: 100%; border-radius: 3px; background: var(--gold-dim); }
.skill-tag { display: inline-block; padding: 3px 10px; border: 1px solid #d0e8e4; border-radius: 100px; font-size: 0.72rem; color: var(--muted); margin: 3px 3px 3px 0; }
.skill-gap { border-color: #f5c4b0; color: var(--coral); }

/* ── Resource cards ── */
.resource-card { background: var(--card-bg); border: 1px solid #e0ece9; border-radius: 10px; padding: 1rem 1.3rem; margin-bottom: 0.8rem; display: flex; gap: 1rem; align-items: flex-start; }
.resource-tag { padding: 3px 10px; border-radius: 100px; font-size: 0.7rem; font-weight: 600; white-space: nowrap; }
.tag-tutoring    { background: #eef7e6; color: #3a6e00; }
.tag-career      { background: #fffbea; color: #8a6c00; }
.tag-registration{ background: #eef7e6; color: #3a6e00; }
.tag-wellbeing   { background: #fdf0eb; color: #8a2a00; }
.tag-financial   { background: #fffbea; color: #8a6c00; }
.tag-writing     { background: #eef7e6; color: #3a6e00; }

/* ── Chat bubbles ── */
.chat-ai {
    background: var(--light-bg);
    border: 1px solid #d0e8e4;
    border-radius: 4px 14px 14px 14px;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.88rem;
    color: var(--text);
    line-height: 1.55;
    max-width: 90%;
}
.chat-user {
    background: var(--green);
    color: white;
    border-radius: 14px 4px 14px 14px;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0 0.4rem auto;
    font-size: 0.88rem;
    line-height: 1.55;
    max-width: 85%;
    text-align: right;
}
.chat-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.05em; margin-bottom: 2px; }
.label-ai   { color: var(--muted); }
.label-user { color: var(--muted); text-align: right; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--green-dark) !important;
}
section[data-testid="stSidebar"] * { color: #c8e6e2 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: var(--gold) !important; }

/* ── Streamlit overrides ── */
div[data-testid="stVerticalBlock"] { gap: 0.5rem; }
.stButton > button {
    background: var(--gold) !important;
    color: var(--green) !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 100px !important;
    padding: 0.4rem 1.4rem !important;
}
.stButton > button:hover { background: var(--gold-dim) !important; }
div[data-testid="stChatInput"] textarea { border-color: #d0e8e4 !important; }
div[data-testid="stChatInput"] textarea:focus { border-color: var(--gold) !important; }
</style>
""", unsafe_allow_html=True)


# ── Constants ────────────────────────────────────────────────────────────────
TOTAL_CREDITS = 120
MAJORS = [
    "Computer Science", "Data Science", "Business Administration",
    "Psychology", "Biology", "Economics", "Mechanical Engineering",
    "Civil Engineering", "Environmental Engineering",
    "Mathematics", "Physics", "Communications", "Nursing",
]
YEARS = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
CAREER_OPTIONS = [
    "Software engineering", "Data & AI", "Product management",
    "Research & academia", "Entrepreneurship",
    "Finance & consulting", "Healthcare", "Government & policy",
]

CAREER_DATA = {
    "Software engineering": {
        "match": 92,
        "skills": ["Python", "Algorithms", "System design", "Git"],
        "gaps":   ["DevOps", "Cloud (AWS)"],
    },
    "Data & AI": {
        "match": 87,
        "skills": ["Python", "Statistics", "Machine Learning"],
        "gaps":   ["Deep Learning", "SQL (advanced)"],
    },
    "Product management": {
        "match": 74,
        "skills": ["Communication", "Project management"],
        "gaps":   ["UX research", "Agile certs"],
    },
    "Research & academia": {
        "match": 81,
        "skills": ["Research methods", "Writing", "Analysis"],
        "gaps":   ["Publications", "Graduate coursework"],
    },
    "Finance & consulting": {
        "match": 68,
        "skills": ["Quantitative analysis", "Excel"],
        "gaps":   ["Financial modeling", "CFA prep"],
    },
    "Healthcare": {
        "match": 77,
        "skills": ["Biology", "Patient communication"],
        "gaps":   ["Clinical hours", "Licensure prep"],
    },
    "Entrepreneurship": {
        "match": 79,
        "skills": ["Problem solving", "Networking"],
        "gaps":   ["Business finance", "Legal fundamentals"],
    },
    "Government & policy": {
        "match": 71,
        "skills": ["Analysis", "Writing", "Research"],
        "gaps":   ["Policy frameworks", "Public law"],
    },
}

RESOURCES = [
    {"name": "Academic Tutoring Center",   "desc": "Free one-on-one and group tutoring for math, writing, and STEM courses. Walk-ins Mon–Fri 9am–7pm.", "tag": "Tutoring",     "tag_class": "tag-tutoring"},
    {"name": "Career Services Office",     "desc": "Resume reviews, mock interviews, internship board, and career counseling for all majors.",            "tag": "Career",       "tag_class": "tag-career"},
    {"name": "Registrar's Office",         "desc": "Course registration help, transcript requests, graduation audits, and deadline reminders.",            "tag": "Registration", "tag_class": "tag-registration"},
    {"name": "Counseling & Mental Health", "desc": "Free confidential sessions for stress, anxiety, and academic burnout. Same-day crisis appointments.",  "tag": "Wellbeing",    "tag_class": "tag-wellbeing"},
    {"name": "Financial Aid Office",       "desc": "Scholarship search, emergency aid applications, and FAFSA guidance.",                                  "tag": "Financial",    "tag_class": "tag-financial"},
    {"name": "Writing Center",             "desc": "Drop-in and scheduled appointments for essays, research papers, and technical reports.",                "tag": "Writing",      "tag_class": "tag-writing"},
]


# ── Session state initialisation ─────────────────────────────────────────────
def init_state():
    defaults = {
        "onboarded":  False,
        "name":       "",
        "major":      MAJORS[0],
        "year":       YEARS[2],
        "credits":    60,
        "careers":    [],
        "challenges": "",
        "messages":   [],   # chat history: list of {"role": ..., "content": ...}
        "active_tab": "Overview",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── Helper: Clarkson brand bar ───────────────────────────────────────────────
def brand_bar():
    st.markdown('<div class="brand-bar"></div>', unsafe_allow_html=True)


# ── Helper: degree stats ─────────────────────────────────────────────────────
def degree_stats():
    credits   = st.session_state.credits
    remaining = max(0, TOTAL_CREDITS - credits)
    pct       = min(100, round((credits / TOTAL_CREDITS) * 100))
    sems_left = math.ceil(remaining / 15)
    grad_year = 2025 + math.ceil(sems_left / 2)
    return credits, remaining, pct, sems_left, grad_year


# ════════════════════════════════════════════════════════════════════════════
#  ONBOARDING SCREEN
# ════════════════════════════════════════════════════════════════════════════
def show_onboarding():
    brand_bar()
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1rem;">
        <div style="background:#ffcd00; color:#004e42; font-weight:800; font-size:1.1rem;
                    display:inline-block; padding:10px 20px; border-radius:12px; letter-spacing:-0.3px;">
            myAdvisr
        </div>
        <h1 style="color:#004e42; margin: 1rem 0 0.4rem; font-size:2.2rem;">
            Your AI academic advisor is here
        </h1>
        <p style="color:#555; font-size:1rem; max-width:480px; margin:0 auto 2rem;">
            Plan your degree, pick the right courses, and align your academic
            goals with your career — powered by AI, built for Clarkson students.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("onboarding_form"):
            st.markdown("#### Tell us about yourself")

            name = st.text_input("First name", placeholder="e.g. Graham")
            major = st.selectbox("Your major", MAJORS)
            year = st.selectbox("Academic year", YEARS, index=2)
            credits = st.number_input(
                "Credits completed", min_value=0, max_value=200, value=60, step=1
            )

            st.markdown("**Career interests** *(select all that apply)*")
            careers_selected = []
            cols = st.columns(2)
            for i, opt in enumerate(CAREER_OPTIONS):
                with cols[i % 2]:
                    if st.checkbox(opt, key=f"career_{i}"):
                        careers_selected.append(opt)

            challenges = st.text_area(
                "Any challenges or goals? *(optional)*",
                placeholder="e.g. Struggling with math, want to graduate early, unsure which electives to take...",
                height=80,
            )

            submitted = st.form_submit_button(
                "Launch myAdvisr →", use_container_width=True
            )

        if submitted:
            st.session_state.name       = name.strip() or "Student"
            st.session_state.major      = major
            st.session_state.year       = year
            st.session_state.credits    = int(credits)
            st.session_state.careers    = careers_selected or ["Software engineering", "Data & AI"]
            st.session_state.challenges = challenges
            st.session_state.onboarded  = True

            # Seed welcome message
            welcome = (
                f"Hi {st.session_state.name}! I'm myAdvisr, your personal AI academic "
                f"advisor for Clarkson University. I can see you're studying "
                f"{st.session_state.major} with {st.session_state.credits} credits "
                f"completed"
            )
            if st.session_state.careers:
                welcome += f", and you're interested in {' and '.join(st.session_state.careers[:2])}"
            welcome += (
                ".\n\nI've analysed your profile and built your dashboard. "
                "Ask me anything — courses, career paths, graduation planning, "
                "or campus resources. I'm here whenever you need me!"
            )
            st.session_state.messages = [{"role": "assistant", "content": welcome}]
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
def show_sidebar():
    with st.sidebar:
        st.markdown(
            '<p style="font-size:1.5rem;font-weight:800;color:#ffcd00!important;'
            'letter-spacing:-0.3px;margin-bottom:0;">myAdvisr</p>'
            '<p style="font-size:0.72rem;color:#9ecec8!important;margin-top:0;'
            'letter-spacing:0.05em;">CLARKSON UNIVERSITY</p>',
            unsafe_allow_html=True,
        )
        st.divider()

        credits, remaining, pct, sems_left, grad_year = degree_stats()

        st.markdown(
            f'<p style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;'
            f'font-weight:600;">Degree Progress</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="prog-wrap"><div class="prog-bar" style="width:{pct}%"></div></div>'
            f'<p style="font-size:0.75rem;color:#9ecec8!important;">'
            f'{credits} of {TOTAL_CREDITS} credits · {pct}%</p>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"**Student:** {st.session_state.name}  \n"
            f"**Major:** {st.session_state.major}  \n"
            f"**Year:** {st.session_state.year}  \n"
            f"**Grad target:** {grad_year}  \n"
            f"**Semesters left:** {sems_left}",
        )
        st.divider()

        st.markdown('<p style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;">Navigation</p>', unsafe_allow_html=True)
        tabs = ["Overview", "Course Plan", "Career Paths", "Campus Resources", "AI Advisor"]
        for tab in tabs:
            is_active = st.session_state.active_tab == tab
            if st.button(
                ("▶ " if is_active else "   ") + tab,
                key=f"nav_{tab}",
                use_container_width=True,
            ):
                st.session_state.active_tab = tab
                st.rerun()

        st.divider()
        if st.button("← Start over", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════
#  TAB: OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
def tab_overview():
    credits, remaining, pct, sems_left, grad_year = degree_stats()
    top_career = st.session_state.careers[0] if st.session_state.careers else "Software engineering"
    match_pct  = CAREER_DATA.get(top_career, {}).get("match", 80)

    st.markdown(
        f"""
        <div class="metric-row">
          <div class="metric-card accent">
            <div class="metric-label">Credits completed</div>
            <div class="metric-value">{credits}</div>
            <div class="metric-sub">of {TOTAL_CREDITS} required</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Semesters left</div>
            <div class="metric-value">{sems_left}</div>
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
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress bar
    st.markdown(
        f"""
        <div class="section-head">Degree progress</div>
        <div class="prog-wrap" style="height:14px;border-radius:8px;">
          <div class="prog-bar" style="width:{pct}%;height:14px;border-radius:8px;"></div>
        </div>
        <p style="font-size:0.8rem;color:#555;margin-top:4px;">{pct}% complete — {remaining} credits remaining</p>
        """,
        unsafe_allow_html=True,
    )

    # Advisor alerts
    st.markdown('<div class="section-head">Advisor alerts</div>', unsafe_allow_html=True)

    alerts = []
    if credits < 30:
        alerts.append(("info", f"<b>Great start, {st.session_state.name}!</b> You're building your foundation. Let's lock in a strong plan for {st.session_state.major}."))
    if st.session_state.major in ("Computer Science", "Data Science", "Mathematics"):
        alerts.append(("warn", "<b>Math prerequisite alert:</b> Linear Algebra and Discrete Math are required before upper-division courses. Confirm these are in your plan."))
    if "Data & AI" in st.session_state.careers:
        alerts.append(("info", "<b>Career tip:</b> For Data & AI roles, add STAT 301 (Statistics) and CS 445 (Machine Learning) to your upcoming semesters."))
    alerts.append(("crit", "<b>Registration opens in 14 days.</b> myAdvisr has pre-selected 4 courses based on your degree requirements and career goals."))
    if st.session_state.challenges:
        snippet = st.session_state.challenges[:80] + ("..." if len(st.session_state.challenges) > 80 else "")
        alerts.append(("info", f"<b>Your note:</b> \"{snippet}\" — your advisor is factoring this into all recommendations."))

    dot_class = {"warn": "dot-warn", "info": "dot-info", "crit": "dot-crit"}
    for kind, text in alerts:
        st.markdown(
            f"""<div class="alert-card {kind}">
                  <div class="alert-dot {dot_class[kind]}"></div>
                  <div class="alert-text">{text}</div>
                </div>""",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
#  TAB: COURSE PLAN
# ════════════════════════════════════════════════════════════════════════════
def tab_courses():
    is_tech = st.session_state.major in ("Computer Science", "Data Science", "Mathematics")
    core1   = "Algorithms & Data Structures" if is_tech else f"{st.session_state.major} Core I"
    core2   = "Software Engineering"          if is_tech else f"{st.session_state.major} Methods"
    adv1    = "Machine Learning"              if is_tech else f"{st.session_state.major} Advanced I"

    semesters = [
        {
            "name": "Current semester (Spring 2025)", "credits": 15,
            "courses": [
                {"code": "CS 301",   "name": core1,                 "cr": 3, "status": "plan"},
                {"code": "CS 320",   "name": core2,                 "cr": 3, "status": "plan"},
                {"code": "MATH 310", "name": "Linear Algebra",      "cr": 3, "status": "plan"},
                {"code": "ENGL 201", "name": "Technical Writing",   "cr": 3, "status": "plan"},
                {"code": "CS 395",   "name": "AI & Society",        "cr": 3, "status": "rec"},
            ],
        },
        {
            "name": "Next semester (Fall 2025)", "credits": 15,
            "courses": [
                {"code": "CS 401",   "name": adv1,                  "cr": 3, "status": "plan"},
                {"code": "STAT 301", "name": "Applied Statistics",  "cr": 3, "status": "plan"},
                {"code": "CS 410",   "name": "Database Systems",    "cr": 3, "status": "plan"},
                {"code": "CS 420",   "name": "Capstone Prep",       "cr": 3, "status": "plan"},
            ],
        },
        {
            "name": "Completed", "credits": st.session_state.credits,
            "courses": [
                {"code": "CS 101",   "name": "Intro to Programming","cr": 3, "status": "done"},
                {"code": "CS 201",   "name": "Data Structures",     "cr": 3, "status": "done"},
                {"code": "MATH 201", "name": "Calculus I",          "cr": 3, "status": "done"},
                {"code": "ENGL 101", "name": "Composition",         "cr": 3, "status": "done"},
            ],
        },
    ]

    badge = {"done": "badge-done", "plan": "badge-plan", "rec": "badge-rec"}
    label = {"done": "Completed",  "plan": "Planned",    "rec": "Recommended"}

    for sem in semesters:
        rows_html = "".join(
            f"""<div class="course-row">
                  <span class="course-code">{c['code']}</span>
                  <span class="course-name">{c['name']}</span>
                  <span class="course-cr">{c['cr']} cr</span>
                  <span class="badge {badge[c['status']]}">{label[c['status']]}</span>
                </div>"""
            for c in sem["courses"]
        )
        st.markdown(
            f"""<div class="sem-block">
                  <div class="sem-header">
                    <span>{sem['name']}</span>
                    <span>{sem['credits']} credits</span>
                  </div>
                  {rows_html}
                </div>""",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
#  TAB: CAREER PATHS
# ════════════════════════════════════════════════════════════════════════════
def tab_career():
    shown = (st.session_state.careers or ["Software engineering", "Data & AI"])[:3]
    st.markdown(
        f"<p style='color:#555;font-size:0.88rem;margin-bottom:1rem;'>"
        f"Based on your {st.session_state.major} major and interest in "
        f"{', '.join(shown)}, here are your strongest career paths.</p>",
        unsafe_allow_html=True,
    )

    for career in shown:
        d = CAREER_DATA.get(career, {"match": 75, "skills": ["Core skills"], "gaps": ["Specialized skills"]})
        skills_html = "".join(f'<span class="skill-tag">{s}</span>' for s in d["skills"])
        gaps_html   = "".join(f'<span class="skill-tag skill-gap">{g}</span>' for g in d["gaps"])
        st.markdown(
            f"""<div class="career-card">
                  <div class="career-title">{career}</div>
                  <div style="display:flex;align-items:center;gap:6px;margin-bottom:10px;font-size:0.82rem;color:#8a6c00;">
                    <div class="match-wrap"><div class="match-fill" style="width:{d['match']}%"></div></div>
                    {d['match']}% match with your profile
                  </div>
                  <div style="font-size:0.75rem;color:#555;margin-bottom:4px;">Strengths from your coursework:</div>
                  <div>{skills_html}</div>
                  <div style="font-size:0.75rem;color:#cf4520;margin:10px 0 4px;">Gaps to address:</div>
                  <div>{gaps_html}</div>
                </div>""",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
#  TAB: CAMPUS RESOURCES
# ════════════════════════════════════════════════════════════════════════════
def tab_resources():
    for r in RESOURCES:
        st.markdown(
            f"""<div class="resource-card">
                  <div style="flex:1">
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                      <span style="font-size:0.95rem;font-weight:700;color:#004e42;">{r['name']}</span>
                      <span class="resource-tag {r['tag_class']}">{r['tag']}</span>
                    </div>
                    <div style="font-size:0.82rem;color:#555;line-height:1.5;">{r['desc']}</div>
                  </div>
                </div>""",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
#  TAB: AI ADVISOR (CHAT)
# ════════════════════════════════════════════════════════════════════════════
def build_system_prompt():
    s = st.session_state
    return (
        f"You are myAdvisr, an expert AI academic advisor for Clarkson University students.\n\n"
        f"Student profile:\n"
        f"- Name: {s.name}\n"
        f"- Major: {s.major}\n"
        f"- Year: {s.year}\n"
        f"- Credits completed: {s.credits} of {TOTAL_CREDITS}\n"
        f"- Career interests: {', '.join(s.careers) if s.careers else 'Not specified'}\n"
        f"- Challenges/goals: {s.challenges if s.challenges else 'None specified'}\n\n"
        f"Be warm, concise, and specific. Give actionable advice tailored to Clarkson University. "
        f"Reference the student's major and career interests. "
        f"Keep responses under 150 words unless a detailed plan is requested. "
        f"Use plain text only — no markdown, no bullet symbols."
    )


def tab_chat():
    st.markdown(
        '<div style="font-size:0.8rem;color:#555;margin-bottom:1rem;">'
        'Powered by Claude · Context-aware · Always available</div>',
        unsafe_allow_html=True,
    )

    # Quick prompts
    st.markdown("**Quick questions:**")
    qcols = st.columns(4)
    quick_prompts = [
        ("Next semester courses", "What courses should I take next semester?"),
        ("Graduation check",      "Am I on track to graduate on time?"),
        ("Career options",        "What career options match my major and interests?"),
        ("GPA help",              "I need help improving my GPA"),
    ]
    for i, (label, prompt) in enumerate(quick_prompts):
        with qcols[i]:
            if st.button(label, key=f"qp_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.spinner("myAdvisr is thinking..."):
                    reply = get_claude_response(prompt)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

    st.divider()

    # Render chat history
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

    # Chat input
    user_input = st.chat_input("Ask your advisor anything...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("myAdvisr is thinking..."):
            reply = get_claude_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()


def get_claude_response(user_message: str) -> str:
    """Call the Anthropic Claude API and return the advisor reply."""
    try:
        client = Anthropic()   # reads ANTHROPIC_API_KEY from environment
        # Build messages list (exclude the message we just added — it goes in messages)
        history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[:-1]   # exclude latest user msg
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
            f"I'm having trouble connecting right now ({type(e).__name__}). "
            "Make sure your ANTHROPIC_API_KEY environment variable is set and try again."
        )


# ════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ════════════════════════════════════════════════════════════════════════════
def main():
    if not st.session_state.onboarded:
        show_onboarding()
        return

    show_sidebar()

    # ── Page header ──
    name    = st.session_state.name
    major   = st.session_state.major
    initials = name[:2].upper() if name else "ST"
    st.markdown(
        f"""<div class="page-header">
              <div class="logo-badge">myAdvisr</div>
              <div>
                <h1>Welcome back, {name}</h1>
                <p>{major} · {st.session_state.year} · Clarkson University</p>
              </div>
            </div>""",
        unsafe_allow_html=True,
    )

    # ── Render active tab ──
    tab = st.session_state.active_tab
    tab_titles = {
        "Overview":         "Overview",
        "Course Plan":      "Course Plan",
        "Career Paths":     "Career Paths",
        "Campus Resources": "Campus Resources",
        "AI Advisor":       "AI Advisor",
    }
    st.markdown(
        f'<div class="section-head">{tab_titles.get(tab, tab)}</div>',
        unsafe_allow_html=True,
    )

    if   tab == "Overview":         tab_overview()
    elif tab == "Course Plan":      tab_courses()
    elif tab == "Career Paths":     tab_career()
    elif tab == "Campus Resources": tab_resources()
    elif tab == "AI Advisor":       tab_chat()


if __name__ == "__main__":
    main()
