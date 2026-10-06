import streamlit as st
import sqlite3
import os
import pandas as pd
from dotenv import load_dotenv
from google import genai


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Internship Tracker",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# LOAD GEMINI API KEY
# =========================================================

load_dotenv(".env")

api_key = os.getenv("GEMINI_API_KEY")

client = None

if api_key:
    client = genai.Client(api_key=api_key)


# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect(
    "internships.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS internships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    skills TEXT,
    location TEXT,
    link TEXT,
    status TEXT
)
""")

conn.commit()


# =========================================================
# TITLE
# =========================================================

st.title("🎓 AI Internship Tracker")

st.write(
    "Track internships and find the best opportunities "
    "based on your skills."
)


# =========================================================
# SIDEBAR - ADD INTERNSHIP
# =========================================================

st.sidebar.header("➕ Add Internship")

company = st.sidebar.text_input(
    "Company"
)

role = st.sidebar.text_input(
    "Internship Role"
)

skills = st.sidebar.text_input(
    "Required Skills",
    placeholder="Python, SQL, Pandas"
)

location = st.sidebar.text_input(
    "Location"
)

link = st.sidebar.text_input(
    "Application Link",
    placeholder="https://example.com"
)

status = st.sidebar.selectbox(
    "Status",
    [
        "Not Applied",
        "Applied",
        "Interview",
        "Selected",
        "Rejected"
    ]
)


# =========================================================
# ADD INTERNSHIP
# =========================================================

if st.sidebar.button("Add Internship"):

    if company.strip() and role.strip():

        cursor.execute("""
        INSERT INTO internships
        (company, role, skills, location, link, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            company.strip(),
            role.strip(),
            skills.strip(),
            location.strip(),
            link.strip(),
            status
        ))

        conn.commit()

        st.sidebar.success(
            "Internship added successfully!"
        )

        st.rerun()

    else:

        st.sidebar.warning(
            "Company and Internship Role are required."
        )


# =========================================================
# GET INTERNSHIPS
# =========================================================

cursor.execute("""
SELECT *
FROM internships
ORDER BY id DESC
""")

data = cursor.fetchall()


# =========================================================
# DISPLAY INTERNSHIPS
# =========================================================

st.header("📋 My Internships")

if data:

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Company",
            "Role",
            "Skills",
            "Location",
            "Link",
            "Status"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No internships added yet. "
        "Add an internship using the sidebar."
    )


# =========================================================
# SKILL MATCHING FUNCTION
# =========================================================

def calculate_skill_match(
    student_skills,
    internship_skills
):

    student_list = [
        skill.strip().lower()
        for skill in student_skills.split(",")
        if skill.strip()
    ]

    internship_list = [
        skill.strip().lower()
        for skill in internship_skills.split(",")
        if skill.strip()
    ]

    matching_skills = []

    for skill in internship_list:

        if skill in student_list:
            matching_skills.append(skill)

    missing_skills = []

    for skill in internship_list:

        if skill not in student_list:
            missing_skills.append(skill)

    if len(internship_list) > 0:

        match_percentage = (
            len(matching_skills)
            / len(internship_list)
        ) * 100

    else:

        match_percentage = 0

    return (
        matching_skills,
        missing_skills,
        round(match_percentage, 2)
    )


# =========================================================
# AI INTERNSHIP MATCHER
# =========================================================

st.header("🤖 AI Internship Matcher")

user_skills = st.text_area(
    "Enter your skills",
    placeholder=(
        "Example: Python, SQL, Pandas, "
        "Machine Learning, Streamlit"
    )
)


# Keep matches available throughout the app
matches = []


# =========================================================
# FIND BEST MATCHES
# =========================================================

if st.button("🔍 Find Best Internship Matches"):

    if not user_skills.strip():

        st.warning(
            "Please enter your skills."
        )

    elif not data:

        st.warning(
            "Please add some internships first."
        )

    else:

        for row in data:

            internship_id = row[0]
            company_name = row[1]
            internship_role = row[2]
            required_skills = row[3] or ""
            internship_location = row[4] or ""
            application_link = row[5] or ""
            internship_status = row[6]

            (
                matching_skills,
                missing_skills,
                match_percentage
            ) = calculate_skill_match(
                user_skills,
                required_skills
            )

            matches.append({
                "ID": internship_id,
                "Company": company_name,
                "Role": internship_role,
                "Location": internship_location,
                "Match %": match_percentage,
                "Matching Skills": ", ".join(
                    matching_skills
                ),
                "Missing Skills": ", ".join(
                    missing_skills
                ),
                "Status": internship_status,
                "Link": application_link
            })

        # Sort by highest match
        matches = sorted(
            matches,
            key=lambda x: x["Match %"],
            reverse=True
        )

        st.subheader(
            "🎯 Best Internship Matches"
        )

        for internship in matches:

            st.markdown("---")

            st.subheader(
                f"🏢 {internship['Company']} - "
                f"{internship['Role']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Match",
                    f"{internship['Match %']}%"
                )

            with col2:

                st.write("📍 Location")

                st.write(
                    internship["Location"]
                    or "Not specified"
                )

            with col3:

                st.write("📌 Status")

                st.write(
                    internship["Status"]
                )

            st.write(
                "✅ **Matching Skills:**",
                internship["Matching Skills"]
                if internship["Matching Skills"]
                else "None"
            )

            st.write(
                "❌ **Missing Skills:**",
                internship["Missing Skills"]
                if internship["Missing Skills"]
                else "None"
            )

            if internship["Link"]:

                st.link_button(
                    "🔗 Apply",
                    internship["Link"]
                )


# =========================================================
# GEMINI AI CAREER ADVICE
# =========================================================

st.header("🧠 AI Career Advice")

if st.button("🤖 Get AI Career Advice"):

    if not user_skills.strip():

        st.warning(
            "Please enter your skills in the "
            "AI Internship Matcher section first."
        )

    elif not data:

        st.warning(
            "Please add internships first."
        )

    elif not api_key:

        st.error(
            "Gemini API key not found. "
            "Please add GEMINI_API_KEY to key.env."
        )

    else:

        # Calculate matches again so this button
        # works independently
        advice_matches = []

        for row in data:

            internship_id = row[0]
            company_name = row[1]
            internship_role = row[2]
            required_skills = row[3] or ""
            internship_location = row[4] or ""
            application_link = row[5] or ""
            internship_status = row[6]

            (
                matching_skills,
                missing_skills,
                match_percentage
            ) = calculate_skill_match(
                user_skills,
                required_skills
            )

            advice_matches.append({
                "Company": company_name,
                "Role": internship_role,
                "Location": internship_location,
                "Match %": match_percentage,
                "Matching Skills": ", ".join(
                    matching_skills
                ),
                "Missing Skills": ", ".join(
                    missing_skills
                ),
                "Status": internship_status
            })

        advice_matches = sorted(
            advice_matches,
            key=lambda x: x["Match %"],
            reverse=True
        )

        internship_text = ""

        for internship in advice_matches:

            internship_text += f"""
Company: {internship['Company']}
Role: {internship['Role']}
Location: {internship['Location']}
Match Percentage: {internship['Match %']}%
Matching Skills: {internship['Matching Skills']}
Missing Skills: {internship['Missing Skills']}
Status: {internship['Status']}

"""

        prompt = f"""
You are an AI internship career assistant.

Student skills:
{user_skills}

Internship matching results:
{internship_text}

Give simple career advice.

For the best internships explain:

1. Which internship is the best
2. Why it matches the student's skills
3. What skills are missing
4. Which missing skills the student should learn first
5. Give a short recommendation

Use simple language suitable for a college student.
"""

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.subheader(
                "💡 AI Recommendation"
            )

            st.write(
                response.text
            )

        except Exception as e:

            st.error(
                f"AI Error: {e}"
            )


# =========================================================
# STATISTICS
# =========================================================

st.header("📊 Internship Statistics")

cursor.execute("""
SELECT status, COUNT(*)
FROM internships
GROUP BY status
""")

stats = cursor.fetchall()

if stats:

    stats_df = pd.DataFrame(
        stats,
        columns=[
            "Status",
            "Count"
        ]
    )

    st.bar_chart(
        stats_df.set_index("Status")
    )

else:

    st.info(
        "Statistics will appear after "
        "adding internships."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "🎓 AI Internship Tracker | "
    "Built with Python, Streamlit, SQLite and Gemini AI"
)