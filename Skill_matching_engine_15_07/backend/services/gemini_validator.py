from google import genai
from dotenv import load_dotenv
import os
import json
import time

load_dotenv("../supabase_database/.env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MAX_RETRIES = 3


def fallback_validation(skills):
    """
    Fallback used when Gemini is unavailable.
    Keeps the application running.
    """

    known_languages = {
        "python", "java", "c", "c++", "c#", "javascript",
        "typescript", "php", "go", "rust", "kotlin", "swift"
    }

    known_frameworks = {
        "django", "flask", "fastapi", "react", "angular",
        "vue", "spring", "spring boot",
        "langgraph", "llamaindex"
    }

    known_tools = {
        "git", "github", "docker", "postman", "mysql",
        "mongodb", "supabase", "colab", "vs code",
        "vscode", "aws", "jira"
    }

    result = {
        "languages": [],
        "frameworks": [],
        "tools": [],
        "invalid_skills": []
    }

    for skill in skills:

        s = skill.lower().strip()

        if s in known_languages:
            result["languages"].append(s)

        elif s in known_frameworks:
            result["frameworks"].append(s)

        elif s in known_tools:
            result["tools"].append(s)

        else:
            result["invalid_skills"].append(s)

    return result

# prompt changed to handel speling mistake by drashti 09-07-2026 start
def validate_skills(skills):

    print("GEMINI CALLED")

    prompt = f"""
You are a strict software technology validation engine.

Skills may contain spelling mistakes, typos, missing letters, or
merged/split words (e.g. "fasi api" instead of "FastAPI",
"javvaa" instead of "Java", "jyupeter nootbook" instead of
"Jupyter Notebook").

Step 1: For each skill, first try to correct it to the closest
real, known programming language, framework, or developer tool
name — even if the spelling is very wrong — as long as it clearly
resembles a real technology.

Step 2: Classify the CORRECTED skill name into exactly one category.

Step 3: Store the CORRECTED name in that category, not the
original misspelled text.

Only place a skill in "invalid_skills" if, after attempting
correction, it still does not resemble any real technology.

Examples:
- "fasi api" -> corrected to "FastAPI" -> goes in frameworks
- "javvaa" -> corrected to "Java" -> goes in languages
- "jyupeter nootbook" -> corrected to "Jupyter Notebook" -> goes in tools
- "asdkfj123" -> no real technology resembles this -> goes in invalid_skills

Return ONLY JSON.

Schema:

{{
    "languages": [],
    "frameworks": [],
    "tools": [],
    "invalid_skills": []
}}

Skills:
{skills}
"""

    delay = 2

    for attempt in range(MAX_RETRIES):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            text = response.text.strip()

            text = text.replace("```json", "")
            text = text.replace("```", "")

            return json.loads(text)

        except Exception as e:

            print(f"Gemini attempt {attempt + 1} failed:")
            print(e)

            if attempt < MAX_RETRIES - 1:
                time.sleep(delay)
                delay *= 2

    print("Using fallback validation.")

    return fallback_validation(skills)

# prompt changed to handel speling mistake by drashti 09-07-2026 end
