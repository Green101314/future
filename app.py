import streamlit as st
import json
import anthropic

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FuturePath – Student AI Consultant",
    page_icon="🎓",
    layout="wide"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.hero {
    background: linear-gradient(135deg, #0a0e1a 0%, #1a2235 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    border: 1px solid rgba(99,160,255,0.2);
}
.hero h1 {
    font-family: 'Sora', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #e8f0fe 30%, #4f9eff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.4rem;
}
.hero p { color: #8fa3c0; font-size: 1rem; }
.hero-badge {
    display: inline-block;
    background: rgba(79,158,255,0.12);
    border: 1px solid rgba(79,158,255,0.3);
    color: #4f9eff;
    font-size: 0.7rem;
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 1rem;
}

.section-card {
    background: #111827;
    border: 1px solid rgba(99,160,255,0.15);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
}
.section-title {
    font-family: 'Sora', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #e8f0fe;
    margin-bottom: 1rem;
}

.college-card {
    background: #1a2235;
    border: 1px solid rgba(99,160,255,0.15);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
    transition: border 0.2s;
}
.college-card:hover { border-color: rgba(99,160,255,0.35); }
.college-rank {
    display: inline-block;
    background: rgba(79,158,255,0.12);
    color: #4f9eff;
    font-family: 'Sora', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 6px;
    margin-right: 8px;
}
.college-name { font-size: 0.95rem; font-weight: 500; color: #e8f0fe; }
.college-meta { font-size: 0.8rem; color: #8fa3c0; margin-top: 3px; }
.college-why { font-size: 0.8rem; color: #4f9eff; margin-top: 3px; }

.tag {
    display: inline-block;
    font-size: 0.65rem;
    font-family: 'Sora', sans-serif;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 10px;
    background: rgba(79,158,255,0.1);
    color: #4f9eff;
    border: 1px solid rgba(79,158,255,0.2);
    margin: 3px 2px 0 0;
}
.tag-gold { background: rgba(245,200,66,0.1); color: #f5c842; border-color: rgba(245,200,66,0.2); }
.tag-green { background: rgba(52,211,153,0.1); color: #34d399; border-color: rgba(52,211,153,0.2); }
.tag-purple { background: rgba(123,111,255,0.1); color: #7b6fff; border-color: rgba(123,111,255,0.2); }

.result-hero {
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
}
.tier-badge {
    display: inline-block;
    font-size: 0.75rem;
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 6px;
}
.roadmap-step {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    margin-bottom: 10px;
}
.step-num {
    min-width: 26px; height: 26px;
    background: rgba(79,158,255,0.15);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; font-weight: 700; color: #4f9eff;
    font-family: 'Sora', sans-serif;
    flex-shrink: 0;
    padding-top: 1px;
}
.ai-advice-box {
    background: rgba(79,158,255,0.05);
    border: 1px solid rgba(79,158,255,0.2);
    border-radius: 12px;
    padding: 1.2rem;
    font-size: 0.9rem;
    color: #8fa3c0;
    line-height: 1.75;
}
.ai-label {
    font-size: 0.7rem;
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #4f9eff;
    margin-bottom: 8px;
}
.cutoff-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 10px;
    margin-bottom: 6px;
}
.dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

.stButton > button {
    background: #4f9eff !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }

div[data-testid="metric-container"] {
    background: #1a2235;
    border: 1px solid rgba(99,160,255,0.15);
    border-radius: 12px;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-Powered • Free • India-Focused</div>
    <h1>🎓 FuturePath Consultant</h1>
    <p>Your personal college guidance counselor — powered by AI, built for Indian students.</p>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋 Profile & Interests", "🔢 Marks ↔ CGPA Converter", "🎯 Results"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — PROFILE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-card"><div class="section-title">👤 Your Academic Profile</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Full Name", placeholder="e.g. Arjun Sharma")
        grade = st.selectbox("Current Status", [
            "After 12th / Class 12", "After UG (Bachelors)",
            "After PG (Masters)", "After Diploma"
        ])
        score_type = st.selectbox("Score Type", [
            "Percentage (%)", "CGPA (out of 10)", "CGPA (out of 4)"
        ])
    with c2:
        state = st.selectbox("Home State / Region", [
            "Delhi / NCR", "Maharashtra", "Tamil Nadu", "Karnataka",
            "Andhra Pradesh / Telangana", "Uttar Pradesh", "West Bengal",
            "Gujarat", "Rajasthan", "Kerala", "Punjab / Haryana", "Other / All India"
        ])
        budget = st.selectbox("Annual Budget", [
            "Low — Government / Scholarship",
            "Medium — Up to ₹3–5 LPA",
            "High — ₹5–15 LPA",
            "Premium — No limit"
        ])
        category = st.selectbox("Category", ["General", "OBC", "SC", "ST", "EWS"])

    if score_type == "Percentage (%)":
        score = st.slider("Your Percentage (%)", 0.0, 100.0, 75.0, 0.5)
        score_display = f"{score}%"
        pct_equiv = score
    elif score_type == "CGPA (out of 10)":
        score = st.slider("Your CGPA (out of 10)", 0.0, 10.0, 7.5, 0.1)
        score_display = f"{score} / 10"
        pct_equiv = score * 9.5
    else:
        score = st.slider("Your GPA (out of 4)", 0.0, 4.0, 3.0, 0.1)
        score_display = f"{score} / 4"
        pct_equiv = (score / 4) * 100

    st.markdown(f"**≈ {pct_equiv:.1f}% equivalent** &nbsp;|&nbsp; Score entered: **{score_display}**", unsafe_allow_html=True)
    location_pref = st.selectbox("Preferred College Location", [
        "No preference", "North India", "South India",
        "West India", "East India", "My home state only"
    ])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">✨ Your Interests & Goals</div>', unsafe_allow_html=True)
    interests = st.text_area(
        "Describe what you love, want to study, or your goals",
        placeholder=(
            "e.g. I love solving math problems and enjoy building apps. "
            "I want to get into AI/ML or data science. I've built small Python projects "
            "and my dream is to work at a top tech company.\n\n"
            "OR: I'm passionate about biology and want to become a doctor, "
            "specialising in neurology..."
        ),
        height=130
    )
    exams = st.text_input(
        "Entrance Exams Appearing / Appeared",
        placeholder="e.g. JEE Mains, NEET, CAT, CUET, CLAT, GATE (leave blank if none)"
    )
    extras = st.text_area(
        "Extra Achievements or Notes (optional)",
        placeholder="e.g. State-level chess champion, coding internship, NCC cadet, NGO volunteer...",
        height=80
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("✦ Evaluate My Profile with AI"):
        if not interests.strip():
            st.error("Please describe your interests so the AI can evaluate your profile!")
        else:
            st.session_state["profile"] = {
                "name": name or "Student",
                "grade": grade,
                "score": score,
                "score_type": score_type,
                "score_display": score_display,
                "pct_equiv": pct_equiv,
                "state": state,
                "budget": budget,
                "category": category,
                "location_pref": location_pref,
                "interests": interests,
                "exams": exams,
                "extras": extras,
            }
            st.session_state["run_eval"] = True
            st.success("Profile saved! Head to the **Results** tab to see your evaluation.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CONVERTER
# ══════════════════════════════════════════════════════════════════════════════
with tab2:

    # ── Converter ──
    st.markdown('<div class="section-card"><div class="section-title">🔢 Marks ↔ CGPA Converter</div>', unsafe_allow_html=True)
    conv_mode = st.selectbox("Conversion Mode", [
        "Percentage → CGPA (out of 10)",
        "Percentage → GPA (out of 4)",
        "CGPA (out of 10) → Percentage",
        "GPA (out of 4) → Percentage",
        "CGPA (out of 10) → GPA (out of 4)",
        "GPA (out of 4) → CGPA (out of 10)",
    ])

    col_in, col_out = st.columns(2)

    def pct_to_gpa4(p):
        if p >= 93: return 4.0
        elif p >= 90: return 3.7
        elif p >= 87: return 3.3
        elif p >= 83: return 3.0
        elif p >= 80: return 2.7
        elif p >= 77: return 2.3
        elif p >= 73: return 2.0
        elif p >= 70: return 1.7
        elif p >= 67: return 1.3
        elif p >= 63: return 1.0
        elif p >= 60: return 0.7
        else: return 0.0

    with col_in:
        if "Percentage" in conv_mode.split("→")[0]:
            conv_val = st.number_input("Enter Percentage (%)", 0.0, 100.0, 75.0, 0.1)
        elif "out of 10" in conv_mode.split("→")[0]:
            conv_val = st.number_input("Enter CGPA (out of 10)", 0.0, 10.0, 7.5, 0.1)
        else:
            conv_val = st.number_input("Enter GPA (out of 4)", 0.0, 4.0, 3.0, 0.1)

    with col_out:
        if conv_mode == "Percentage → CGPA (out of 10)":
            result = round(conv_val / 9.5, 2)
            label = "CGPA (out of 10)"
            note = "CBSE formula: CGPA = % ÷ 9.5"
            prog = result / 10
        elif conv_mode == "Percentage → GPA (out of 4)":
            result = pct_to_gpa4(conv_val)
            label = "GPA (out of 4)"
            note = "US GPA scale approximation"
            prog = result / 4
        elif conv_mode == "CGPA (out of 10) → Percentage":
            result = round(conv_val * 9.5, 1)
            label = "Equivalent Percentage (%)"
            note = "CBSE formula: % = CGPA × 9.5"
            prog = result / 100
        elif conv_mode == "GPA (out of 4) → Percentage":
            result = round((conv_val / 4) * 100, 1)
            label = "Equivalent Percentage (%)"
            note = "Proportional approximation"
            prog = result / 100
        elif conv_mode == "CGPA (out of 10) → GPA (out of 4)":
            result = round((conv_val / 10) * 4, 2)
            label = "GPA (out of 4)"
            note = "Proportional conversion"
            prog = result / 4
        else:
            result = round((conv_val / 4) * 10, 2)
            label = "CGPA (out of 10)"
            note = "Proportional conversion"
            prog = result / 10

        st.metric(label=label, value=str(result))
        st.progress(min(prog, 1.0))
        st.caption(f"ℹ️ {note}")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Grade Reference Table ──
    st.markdown('<div class="section-card"><div class="section-title">📊 Grade Reference Table</div>', unsafe_allow_html=True)
    import pandas as pd
    grade_data = {
        "Percentage": ["90–100%", "80–90%", "70–80%", "60–70%", "50–60%", "40–50%", "<40%"],
        "CGPA /10":   ["9.0–10.0", "8.0–9.0", "7.0–8.0", "6.0–7.0", "5.0–6.0", "4.0–5.0", "<4.0"],
        "GPA /4":     ["3.7–4.0", "3.3–3.7", "3.0–3.3", "2.7–3.0", "2.3–2.7", "2.0–2.3", "<2.0"],
        "Grade / Class": [
            "O / Distinction with Honours",
            "A+ / Distinction",
            "A / First Class",
            "B+ / Second Class Upper",
            "B / Second Class",
            "C / Pass Class",
            "F / Fail"
        ]
    }
    st.dataframe(pd.DataFrame(grade_data), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Cutoff Quick-Check ──
    st.markdown('<div class="section-card"><div class="section-title">🎯 Cutoff Quick-Check</div>', unsafe_allow_html=True)
    st.caption("Enter your percentage and see which tier of colleges you qualify for.")

    cc1, cc2 = st.columns(2)
    with cc1:
        cutoff_pct = st.number_input("Your Percentage", 0.0, 100.0, 75.0, 0.5, key="cutoff_pct")
    with cc2:
        cutoff_domain = st.selectbox("Domain", [
            "Engineering", "Medicine (MBBS)", "Commerce / MBA", "Law", "Arts & Humanities"
        ])

    CUTOFFS = {
        "Engineering": [
            ("IIT (JEE Advanced)",              98,  "🥇"),
            ("NIT / IIIT (JEE Main)",           85,  "✅"),
            ("VIT / Manipal / SRM",             75,  "🔵"),
            ("State Govt Engineering Colleges", 60,  "🔵"),
            ("Management Quota / Private",      40,  "🟣"),
        ],
        "Medicine (MBBS)": [
            ("AIIMS / JIPMER",                  99,  "🥇"),
            ("Government MBBS (NEET)",          90,  "✅"),
            ("Deemed Medical Colleges",         75,  "🔵"),
            ("Private MBBS Colleges",           60,  "🔵"),
            ("BAMS / BHMS / BDS",               45,  "🟣"),
        ],
        "Commerce / MBA": [
            ("IIM (CAT 99%ile)",                95,  "🥇"),
            ("XLRI / FMS / MDI",                88,  "✅"),
            ("NMIMS / Symbiosis / JBIMS",       80,  "🔵"),
            ("B.Com Hons — DU / Christ",        90,  "✅"),
            ("Private B-Schools",               55,  "🟣"),
        ],
        "Law": [
            ("NLSIU / NALSAR (CLAT top ranks)", 95,  "🥇"),
            ("Top NLUs",                        88,  "✅"),
            ("DU Law / Symbiosis Law",          80,  "🔵"),
            ("State Law Universities",          60,  "🔵"),
            ("Private Law Colleges",            45,  "🟣"),
        ],
        "Arts & Humanities": [
            ("DU — Miranda / Stephens / ARSD",  95,  "🥇"),
            ("JNU / BHU / Hyderabad Univ.",     85,  "✅"),
            ("Christ / Symbiosis / Ashoka",     75,  "🔵"),
            ("Jadavpur / Presidency Univ.",     70,  "✅"),
            ("State Central Universities",      55,  "🟣"),
        ],
    }

    for label, cutoff, icon in CUTOFFS[cutoff_domain]:
        meets = cutoff_pct >= cutoff
        gap   = cutoff - cutoff_pct
        color = "#34d399" if meets else "#f87171"
        bg    = "rgba(52,211,153,0.08)" if meets else "rgba(248,113,113,0.06)"
        border= "rgba(52,211,153,0.3)"  if meets else "rgba(248,113,113,0.15)"
        status = f"✓ You qualify (cutoff ≈{cutoff}%)" if meets else f"Needs ≈{cutoff}% — you're {gap:.1f}% short"
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {border};border-radius:10px;
                    padding:10px 14px;margin-bottom:6px;display:flex;align-items:center;gap:10px;">
            <span style="font-size:1rem;">{icon}</span>
            <div>
                <div style="font-size:0.88rem;font-weight:500;color:{'#34d399' if meets else '#e8f0fe'};">{label}</div>
                <div style="font-size:0.75rem;color:{color};margin-top:2px;">{status}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RESULTS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:

    if "run_eval" not in st.session_state or not st.session_state.get("run_eval"):
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">🎓</div>
            <p style="color:#8fa3c0;font-size:1rem;">
                Fill in your profile in the <strong style="color:#e8f0fe;">Profile & Interests</strong> tab
                and click <strong style="color:#4f9eff;">Evaluate My Profile with AI</strong> to see your results here.
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        p = st.session_state["profile"]

        # Build prompt
        prompt = f"""You are FuturePath, an expert Indian college admission counselor. A student needs detailed guidance.

STUDENT PROFILE:
- Name: {p['name']}
- Status: {p['grade']}
- Score: {p['score']} ({p['score_type']}) ≈ {p['pct_equiv']:.1f}% equivalent
- Home State: {p['state']}
- Budget: {p['budget']}
- Category: {p['category']}
- Preferred Location: {p['location_pref']}
- Interests & Goals: {p['interests']}
- Entrance Exams: {p['exams'] or 'None mentioned'}
- Achievements: {p['extras'] or 'None mentioned'}

Provide a detailed, structured JSON response ONLY (no markdown, no extra text) with this exact structure:
{{
  "field": "the main field/career path you recommend",
  "tier": "Excellent|Good|Moderate|Developing",
  "tierColor": "#34d399|#4f9eff|#f5c842|#f87171",
  "summary": "2-3 sentence personalized profile summary mentioning their name",
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "gaps": ["area to work on 1", "area to work on 2"],
  "colleges": [
    {{
      "name": "College Name",
      "location": "City, State",
      "tier": "Tier 1|Tier 2|Tier 3",
      "type": "Govt|Private|Deemed|Central Univ",
      "approxFees": "₹X LPA",
      "cutoff": "approx cutoff or exam required",
      "why": "1 sentence why this fits this student",
      "tags": ["tag1", "tag2"]
    }}
  ],
  "roadmap": ["Step 1: ...", "Step 2: ...", "Step 3: ...", "Step 4: ...", "Step 5: ..."],
  "examsToTarget": ["Exam 1 — brief note", "Exam 2 — brief note"],
  "scholarships": ["Scholarship 1", "Scholarship 2", "Scholarship 3"],
  "careerPaths": ["Career path 1", "Career path 2", "Career path 3"],
  "aiAdvice": "3-4 sentences of personalized, honest, warm advice directly to {p['name']}"
}}

Give 8-10 REAL Indian colleges specific to the student's field, score, budget and location preference.
Make the advice genuinely helpful and specific. Do not add any text outside the JSON."""

        client = anthropic.Anthropic()

        with st.spinner("AI is analysing your profile…"):
            try:
                message = client.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=2500,
                    messages=[{"role": "user", "content": prompt}]
                )
                raw = message.content[0].text.strip()
                # Strip markdown fences if present
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                d = json.loads(raw)
                st.session_state["result"] = d
                st.session_state["run_eval"] = False
            except Exception as e:
                st.error(f"Error calling AI: {e}")
                st.stop()

        if "result" not in st.session_state:
            st.stop()

    if "result" in st.session_state:
        d = st.session_state["result"]
        p = st.session_state["profile"]

        TIER_COLORS = {
            "Excellent": ("#34d399", "rgba(52,211,153,0.12)", "rgba(52,211,153,0.35)"),
            "Good":      ("#4f9eff", "rgba(79,158,255,0.12)", "rgba(79,158,255,0.35)"),
            "Moderate":  ("#f5c842", "rgba(245,200,66,0.12)", "rgba(245,200,66,0.35)"),
            "Developing":("#f87171", "rgba(248,113,113,0.12)","rgba(248,113,113,0.35)"),
        }
        tc, tbg, tborder = TIER_COLORS.get(d.get("tier","Good"), TIER_COLORS["Good"])

        # ── Profile Summary Card ──
        st.markdown(f"""
        <div style="background:{tbg};border:1px solid {tborder};border-radius:14px;padding:1.5rem;margin-bottom:1.2rem;">
            <div style="display:flex;align-items:center;gap:14px;margin-bottom:1rem;">
                <div style="background:{tc}22;border:2px solid {tc}44;border-radius:12px;
                            padding:10px 16px;text-align:center;flex-shrink:0;">
                    <div style="font-family:'Sora',sans-serif;font-size:1.3rem;font-weight:700;color:{tc};">
                        {p['score']}
                    </div>
                    <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.08em;color:{tc}aa;">
                        {p['score_type'].split('(')[0].strip()}
                    </div>
                </div>
                <div>
                    <div style="font-family:'Sora',sans-serif;font-size:1.1rem;font-weight:600;color:#e8f0fe;">
                        {p['name']}
                    </div>
                    <span style="background:{tc}22;color:{tc};font-family:'Sora',sans-serif;
                                 font-size:0.72rem;font-weight:600;padding:3px 10px;border-radius:20px;
                                 display:inline-block;margin:4px 0;">
                        {d.get('tier','')} Profile
                    </span>
                    <div style="font-size:0.82rem;color:#8fa3c0;">
                        Recommended Field: <strong style="color:#e8f0fe;">{d.get('field','')}</strong>
                    </div>
                </div>
            </div>
            <p style="font-size:0.88rem;color:#8fa3c0;line-height:1.75;margin:0;">{d.get('summary','')}</p>
        </div>
        """, unsafe_allow_html=True)

        # ── Strengths & Gaps ──
        col_s, col_g = st.columns(2)
        with col_s:
            st.markdown('<div class="section-card"><div class="section-title">✅ Strengths</div>', unsafe_allow_html=True)
            for s in d.get("strengths", []):
                st.markdown(f'<div style="font-size:0.85rem;color:#8fa3c0;padding:3px 0;display:flex;gap:8px;"><span style="color:#34d399;">✓</span>{s}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_g:
            st.markdown('<div class="section-card"><div class="section-title">📈 Areas to Improve</div>', unsafe_allow_html=True)
            for g in d.get("gaps", []):
                st.markdown(f'<div style="font-size:0.85rem;color:#8fa3c0;padding:3px 0;display:flex;gap:8px;"><span style="color:#f5c842;">!</span>{g}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── College List ──
        st.markdown('<div class="section-card"><div class="section-title">🏛 Recommended Colleges</div>', unsafe_allow_html=True)
        for i, c in enumerate(d.get("colleges", []), 1):
            tier_tag_cls = "tag-gold" if c.get("tier") == "Tier 1" else ("tag-green" if c.get("tier") == "Tier 2" else "")
            extra_tags = "".join([f'<span class="tag">{t}</span>' for t in c.get("tags", [])])
            st.markdown(f"""
            <div class="college-card">
                <div style="display:flex;align-items:flex-start;gap:10px;">
                    <span class="college-rank">#{i}</span>
                    <div style="flex:1;">
                        <div class="college-name">{c.get('name','')}</div>
                        <div class="college-meta">{c.get('location','')} &nbsp;|&nbsp; {c.get('type','')} &nbsp;|&nbsp; {c.get('approxFees','')}</div>
                        <div class="college-why">{c.get('why','')}</div>
                        <div class="college-meta">Cutoff: {c.get('cutoff','')}</div>
                        <div style="margin-top:6px;">
                            <span class="tag {tier_tag_cls}">{c.get('tier','')}</span>
                            {extra_tags}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Roadmap ──
        st.markdown('<div class="section-card"><div class="section-title">🗺 Your Roadmap</div>', unsafe_allow_html=True)
        for i, step in enumerate(d.get("roadmap", []), 1):
            st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:10px;">
                <div style="min-width:26px;height:26px;background:rgba(79,158,255,0.15);border-radius:50%;
                            display:flex;align-items:center;justify-content:center;
                            font-size:0.7rem;font-weight:700;color:#4f9eff;font-family:'Sora',sans-serif;flex-shrink:0;">
                    {i}
                </div>
                <div style="font-size:0.88rem;color:#8fa3c0;line-height:1.6;padding-top:3px;">{step}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Exams / Scholarships / Careers ──
        col_e, col_sc, col_cp = st.columns(3)
        with col_e:
            st.markdown('<div class="section-card"><div class="section-title" style="font-size:0.88rem;">📝 Target Exams</div>', unsafe_allow_html=True)
            for e in d.get("examsToTarget", []):
                st.markdown(f'<div style="font-size:0.78rem;color:#8fa3c0;padding:5px 0;border-bottom:1px solid rgba(99,160,255,0.1);">{e}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_sc:
            st.markdown('<div class="section-card"><div class="section-title" style="font-size:0.88rem;">💰 Scholarships</div>', unsafe_allow_html=True)
            for s in d.get("scholarships", []):
                st.markdown(f'<div style="font-size:0.78rem;color:#8fa3c0;padding:5px 0;border-bottom:1px solid rgba(99,160,255,0.1);">{s}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_cp:
            st.markdown('<div class="section-card"><div class="section-title" style="font-size:0.88rem;">🚀 Career Paths</div>', unsafe_allow_html=True)
            for cp in d.get("careerPaths", []):
                st.markdown(f'<div style="font-size:0.78rem;color:#8fa3c0;padding:5px 0;border-bottom:1px solid rgba(99,160,255,0.1);">{cp}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── AI Advice ──
        st.markdown(f"""
        <div class="section-card">
            <div class="ai-label">✦ Personalised AI Advice</div>
            <div class="ai-advice-box">{d.get('aiAdvice','')}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("← Edit Profile & Re-evaluate"):
            st.session_state.pop("result", None)
            st.session_state["run_eval"] = False
            st.rerun()
