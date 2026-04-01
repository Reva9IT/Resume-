from flask import Flask, request, jsonify
from resume_generator import create_docx, create_pdf
import requests

app = Flask(__name__)


def generate_with_ollama(prompt):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data)
    return response.json()["response"]


@app.route("/")
def home():
    return "Backend with LLM is running!"


@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    data = request.get_json()

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    links = data.get("links", "")
    education = data.get("education", "")
    skills = data.get("skills", "")
    projects = data.get("projects", "")
    experience = data.get("experience", "")
    achievements = data.get("achievements", "")
    role = data.get("role", "")

    prompt = f"""
    You are a professional resume writer.

    Write a short professional summary.

    Skills: {skills}
    Projects: {projects}
    Experience: {experience}
    Role: {role}

    Keep it concise and ATS-friendly.
    """

    summary = generate_with_ollama(prompt)

    resume_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "links": links,
        "education": education,
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "achievements": achievements,
        "role": role,
        "summary": summary
    }

    docx_file = create_docx(resume_data)
    pdf_file = create_pdf(resume_data)

    return jsonify({
        "message": "Resume created successfully",
        "preview": summary,
        "docx": docx_file,
        "pdf": pdf_file
    })


#if __name__ == "__main__":
   # app.run(debug=True)
