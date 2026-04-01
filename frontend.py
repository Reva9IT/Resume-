import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Builder", layout="centered")

st.markdown("""
<style>
body { background-color: #1e2d24; color: #f5f5dc; }
h1, h2 { color: #d6e5b1; }
.stButton>button {
    background-color: #556b2f;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Resume Builder")

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
links = st.text_input("LinkedIn / GitHub")

education = st.text_area("Education")
skills = st.text_area("Skills (comma separated)")
projects = st.text_area("Projects (comma separated)")
experience = st.text_area("Experience")
achievements = st.text_area("Achievements")
role = st.text_input("Target Role")

if st.button("Generate Resume"):
    if not name or not skills or not role:
        st.warning("Fill required fields")
    else:
        response = requests.post(
            "http://127.0.0.1:5000/generate-resume",
            json={
                "name": name,
                "email": email,
                "phone": phone,
                "links": links,
                "education": education,
                "skills": skills,
                "projects": projects,
                "experience": experience,
                "achievements": achievements,
                "role": role
            }
        )

        result = response.json()

        st.subheader("Summary")
        st.write(result["preview"])

        with open("resume.docx", "rb") as f:
            st.download_button("Download DOCX", f)

        with open("resume.pdf", "rb") as f:
            st.download_button("Download PDF", f)