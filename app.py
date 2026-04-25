import streamlit as st

# Setup the page
st.set_page_config(page_title="Student AI Consultant", page_icon="🎓")

# Header
st.title("🎓 FuturePath: The Student AI Consultant")
st.write("Helping you find the right college without the expensive fees.")

# Question Section
st.header("Step 1: Tell us about yourself")
name = st.text_input("Enter your full name")
grade = st.selectbox("Current Status", ["After 12th", "After UG (Bachelors)", "After PG (Masters)"])
marks = st.number_input("Enter your latest percentage or CGPA", min_value=0, max_value=100, value=85)
budget = st.selectbox("Preferred Annual Budget", ["Low (Government)", "Medium (Private-Budget)", "High (Premium Private)"])
interest = st.selectbox("Your Field of Interest", ["Engineering", "Medicine", "Arts", "Commerce/MBA", "Law"])

# The "Logic" Button
if st.button("Evaluate My Profile"):
    st.divider()
    st.subheader(f"Recommendations for {name}")
    
    # Simple logic for your prototype
    if marks >= 90:
        st.success("🎯 Top Tier Match: Your marks are excellent for Tier 1 Universities.")
        st.write("**Suggested:** IITs / NITs (via JEE) or Top-tier Law/Medical Schools.")
        st.info("💡 Next Step: Prepare for Entrance Exams immediately.")
    elif marks >= 75:
        st.success("✅ Solid Match: You qualify for several high-ranking private & state universities.")
        st.write("**Suggested:** VIT, Manipal, or State-level Merit Seats.")
        st.info("💡 Next Step: Check CUET or VITEEE application dates.")
    else:
        st.success("🌟 Potential Match: Focus on entrance exams to boost your profile.")
        st.write("**Suggested:** Amity University, LPU, or specialized skill-based colleges.")
        st.info("💡 Next Step: Focus on Building a Portfolio or a strong Interview.")
