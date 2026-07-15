import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Path to supabase_database/.env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(BASE_DIR)
)

ENV_PATH = os.path.join(
    PROJECT_ROOT,
    "supabase_database",
    ".env"
)

# Load .env
load_dotenv(ENV_PATH)

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Gemini Model
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# Extract Required Skills
# add two parameters for technologies and tools_and_ide to the get_required_skills function call, as they are already included in the prompt for Gemini and also change the prompt . inshort change whole def function henil 9/7/2026
def get_required_skills(
    task_name: str,
    description: str,
    technologies: str = "",
    tools_ide: str = ""
):
    """
    Extract and normalize required technical skills using Gemini.
    """

    prompt = f"""
You are an expert Software Project Manager and Technical Recruiter.

Your job is to identify ONLY the mandatory technical skills required to complete the given task.

Use ALL of the following information.

Task Name:
{task_name}

Description:
{description}

Technologies Entered By User:
{technologies}

Tools & IDE Entered By User:
{tools_ide}

Instructions:

1. Consider ALL FOUR inputs together before deciding the required skills.

2. Correct spelling mistakes and normalize technology names to their industry-standard names.

Examples:
- Fast APi → FastAPI
- fast api → FastAPI
- react js → React
- node js → Node.js
- mongo db → MongoDB
- my sql → MySQL
- postgressql → PostgreSQL
- git hub → GitHub
- vs cod → VS Code
- visual studio code → VS Code
- pychrm → PyCharm

3. Remove duplicate skills.

4. Return ONLY the skills that are actually required to complete the task.

5. If the task explicitly mentions only one or two technologies, return only those technologies unless another core technical skill is clearly essential.

6. Add a core technical skill ONLY if it is directly implied by the task and is necessary for successful completion.

Examples:
- FastAPI + JWT → Add REST API
- Django CRUD Application → Add CRUD
- Tableau Dashboard → Add Dashboard Development

Do NOT add unnecessary implied skills.

Examples:
- React → Do NOT automatically add JavaScript.
- MySQL → Do NOT automatically add SQL.
- Docker → Do NOT automatically add Linux.
- VS Code → Do NOT add Programming.

7. Include only technical skills such as:
- Programming Languages
- Frameworks
- Libraries
- Databases
- APIs
- Cloud Platforms
- DevOps Tools
- Version Control Tools
- IDEs
- Required Development Technologies

8. Do NOT include:
- Soft Skills
- Best Practices
- Design Principles
- Nice-to-have Skills
- Generic Software Engineering Concepts
- Broad Domains
- Future Learning Topics
- Certifications

9. There is NO minimum number of skills.

10. Usually return between 1 and 7 skills, depending on the task.

11. Return ONLY valid JSON.

Output Format:

{{
    "required_skills": [
        "FastAPI",
        "JWT",
        "REST API"
    ]
}}

Return ONLY valid JSON.
Do not explain.
Do not use markdown.
Do not include any text before or after the JSON.
"""
    #  add multiple exceptions to handle errors in Gemini response and return empty list of required_skills henil 9/7/2026
    try:
        response = model.generate_content(prompt)

        result = response.text.strip()

        # Remove markdown if Gemini returns it
        result = (
            result.replace("```json", "")
                  .replace("```", "")
                  .strip()
        )

        data = json.loads(result)

        if not isinstance(data, dict):
            return {
                "required_skills": []
            }

        skills = data.get("required_skills", [])

        if not isinstance(skills, list):
            skills = []

        # Remove duplicates while preserving order
        cleaned_skills = []
        seen = set()

        for skill in skills:
            if not isinstance(skill, str):
                continue

            skill = skill.strip()

            if skill.lower() not in seen:
                seen.add(skill.lower())
                cleaned_skills.append(skill)

        return {
            "required_skills": cleaned_skills
        }

    except json.JSONDecodeError:
        return {
            "required_skills": []
        }

    except Exception as e:
        print("Gemini Error:", e)

        return {
            "required_skills": []
        }