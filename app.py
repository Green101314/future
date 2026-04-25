import streamlit as st
import json
import anthropic
import pandas as pd

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

# ─── Logic & Tabs ──────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋 Profile & Interests", "🔢 Converter", "🎯 Results"])

# ─── TAB 1: PROFILE ────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-card"><div class="section-title">👤 Your Academic Profile</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Arjun Sharma", key="name_input")
        grade = st.selectbox("Current Status", ["After 12th / Class 12", "After UG (Bachelors)", "After PG (Masters)", "After Diploma"])
        score_type = st.selectbox("Score Type", ["Percentage (%)", "CGPA (out of 10)", "CGPA (out of 4)"])
    with col2:
        state = st.selectbox("Home State", ["Delhi / NCR", "Maharashtra", "Tamil Nadu", "Karnataka", "Telangana", "Uttar Pradesh", "West Bengal", "Gujarat", "Other"])
        budget = st.selectbox("Annual Budget", ["Low — Govt", "Medium — Up to ₹3–5 LPA", "High — ₹5–15 LPA", "Premium — No limit"])
        category = st.selectbox("Category", ["General", "OBC", "SC", "ST", "EWS"])

    if score_type == "Percentage (%)":
        score_val = st.slider("Percentage", 0.0, 100.0, 75.0)
        pct_equiv = score_val
    elif score_type == "CGPA (out of 10)":
        score_val = st.slider("CGPA (/10)", 0.0, 10.0, 7.5)
        pct_equiv = score_val * 9.5
    else:
        score_val = st.slider("GPA (/4)", 0.0, 4.0, 3.0)
        pct_equiv = (score_val / 4) * 100

    location_pref = st.selectbox("Location Preference", ["No preference", "North India", "South India", "West India", "East India", "Home state only"])
    interests = st.text_area("Your Goals & Interests", placeholder="Describe what you want to study...", height=120)
    exams = st.text_input("Exams Given/Planned", placeholder="JEE, CAT, NEET, CUET...")
    extras = st.text_area("Extra Achievements")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("✦ Evaluate My Profile with AI", type="primary"):
        if not interests.strip():
            st.warning("Please tell us about your interests first!")
        else:
            # Prepare profile for session state
            st.session_state["profile"] = {
                "name": name or "Student",
                "grade": grade,
                "score": score_val,
                "score_type": score_type,
                "pct_equiv": pct_equiv,
                "state": state,
                "budget": budget,
                "category": category,
                "location_pref": location_pref,
                "interests": interests,
                "exams": exams,
                "extras": extras
            }

            # API Integration
            try:
                # Note: 'claude-3-5-sonnet-20241022' is the correct current model name
                client = anthropic.Anthropic() 
                
                system_prompt = "You are FuturePath, an expert Indian college admission consultant. You provide accurate, realistic, and encouraging college advice."
                
                user_prompt = f"""
                Provide a JSON response for this student profile:
                Profile: {st.session_state["profile"]}

                The JSON must strictly follow this structure:
                {{
                  "field": "string",
                  "tier": "Excellent|Good|Moderate|Developing",
                  "tierColor": "#34d399|#4f9eff|#f5c842|#f87171",
                  "summary": "string",
                  "strengths": ["string"],
                  "gaps": ["string"],
                  "colleges": [
                    {{ "name": "string", "location": "string", "tier": "Tier 1|2|3", "type": "string", "approxFees": "string", "cutoff": "string", "why": "string", "tags": ["string"] }}
                  ],
                  "roadmap": ["string"],
                  "examsToTarget": ["string"],
                  "scholarships": ["string"],
                  "careerPaths": ["string"],
                  "aiAdvice": "string"
                }}
                Ensure the colleges are REAL Indian institutions based on their budget and score. Return ONLY JSON.
                """

                with st.spinner("FuturePath AI is analyzing your career path..."):
                    message = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=3000,
                        messages=[{"role": "user", "content": user_prompt}]
                    )
                    
                    # Clean and Parse JSON
                    res_text = message.content[0].text.strip()
                    if "```json" in res_text:
                        res_text = res_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in res_text:
                        res_text = res_text.split("```")[1].split("```")[0].strip()
                    
                    st.session_state["result"] = json.loads(res_text)
                    st.success("Analysis complete! Switch to the Results tab.")
                    st.rerun()

            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ─── TAB 2: CONVERTER ─────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-card"><div class="section-title">🔢 Quick Grade Converter</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        input_type = st.radio("Convert From", ["Percentage", "CGPA (/10)", "GPA (/4)"])
        val = st.number_input("Value", 0.0, 100.0, 75.0)
    with c2:
        if input_type == "Percentage":
            st.metric("CGPA (/10)", f"{val/9.5:.2f}")
            st.metric("GPA (/4)", f"{(val/100)*4:.2f}")
        elif input_type == "CGPA (/10)":
            st.metric("Percentage", f"{val*9.5:.1f}%")
            st.metric("GPA (/4)", f"{(val/10)*4:.2f}")
        else:
            st.metric("Percentage", f"{(val/4)*100:.1f}%")
            st.metric("CGPA (/10)", f"{(val/4)*10:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── TAB 3: RESULTS ───────────────────────────────────────────────────────────
with tab3:
    if "result" not in st.session_state:
        st.info("👋 Please fill in your profile and click 'Evaluate' to see your personalized report.")
    else:
        res = st.session_state["result"]
        prof = st.session_state["profile"]
        
        # Header / Tier Card
        st.markdown(f"""
        <div style="background:{res.get('tierColor', '#4f9eff')}22; border: 1px solid {res.get('tierColor', '#4f9eff')}; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.2rem;">
            <div style="color:{res.get('tierColor', '#4f9eff')}; font-weight: 700; text-transform: uppercase; font-size: 0.8rem; margin-bottom: 0.5rem;">
                {res.get('tier')} PROFILE • {res.get('field')}
            </div>
            <h2 style="margin:0; color:#e8f0fe;">Analysis for {prof['name']}</h2>
            <p style="color:#8fa3c0; margin-top:10px; line-height:1.6;">{res.get('summary')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Strengths & Gaps
        s_col, g_col = st.columns(2)
        with s_col:
            st.markdown('<div class="section-card"><div class="section-title">✅ Key Strengths</div>', unsafe_allow_html=True)
            for s in res.get("strengths", []): st.write(f"• {s}")
            st.markdown('</div>', unsafe_allow_html=True)
        with g_col:
            st.markdown('<div class="section-card"><div class="section-title">📈 Areas to Improve</div>', unsafe_allow_html=True)
            for g in res.get("gaps", []): st.write(f"• {g}")
            st.markdown('</div>', unsafe_allow_html=True)

        # College Recommendations
        st.markdown('<div class="section-card"><div class="section-title">🏛 Recommended Colleges</div>', unsafe_allow_html=True)
        for i, coll in enumerate(res.get("colleges", []), 1):
            st.markdown(f"""
            <div class="college-card">
                <span class="college-rank">#{i}</span>
                <span class="college-name">{coll['name']}</span>
                <div class="college-meta">{coll['location']} | {coll['type']} | {coll['approxFees']}</div>
                <div class="college-why"><b>Why:</b> {coll['why']}</div>
                <div style="margin-top:8px;">
                    <span class="tag tag-gold">{coll['tier']}</span>
                    {' '.join([f'<span class="tag">{t}</span>' for t in coll.get('tags', [])])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Roadmap
        st.markdown('<div class="section-card"><div class="section-title">🗺 Career Roadmap</div>', unsafe_allow_html=True)
        for i, step in enumerate(res.get("roadmap", []), 1):
            st.write(f"**Step {i}:** {step}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Bottom Row
        c_e, c_s = st.columns(2)
        with c_e:
            st.markdown('<div class="section-card"><div class="section-title">📝 Target Exams</div>', unsafe_allow_html=True)
            for e in res.get("examsToTarget", []): st.write(f"• {e}")
            st.markdown('</div>', unsafe_allow_html=True)
        with c_s:
            st.markdown('<div class="section-card"><div class="section-title">💰 Scholarships</div>', unsafe_allow_html=True)
            for s in res.get("scholarships", []): st.write(f"• {s}")
            st.markdown('</div>', unsafe_allow_html=True)

        # AI Advice
        st.markdown(f"""
        <div class="section-card">
            <div class="ai-label">✦ Personal Counsel from FuturePath</div>
            <div class="ai-advice-box">{res.get('aiAdvice')}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Reset Analysis"):
            for key in ["result", "profile"]:
                if key in st.session_state: del st.session_state[key]
            st.rerun()
