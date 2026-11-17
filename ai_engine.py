import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:latest"
GEMINI_MODEL = "gemini-3.8-flash"


def _build_prompt(goal, target_date, daily_hours, level, preferences):
    return f"""
You are an educational study-planning assistant.

Create a realistic, clear study plan using the student's information below.
Do not claim that you have created calendar events or sent reminders.
Do not invent syllabus topics beyond the student's stated goal.
Break the work into dated or sequential study sessions where possible.
Include learning, practice, revision, short breaks, and a final self-check.
Keep the workload within the student's available daily study time.
If the target date is today or has passed, explain that the timeline needs review.

STUDENT DETAILS
Study goal: {goal}
Target date: {target_date}
Available study time: {daily_hours} hours per day
Current level: {level}
Additional preferences: {preferences or "None provided"}

FORMAT
1. Brief understanding of the goal
2. Day-wise study schedule (topic, activity, approximate duration)
3. Practice and revision strategy
4. Potential workload risks or assumptions
5. A short checklist the student can follow

Use simple, student-friendly language.
"""


def _generate_with_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY was not found. Check the .env file in the project folder."
        )

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")
        return response.text
    finally:
        client.close()


def _generate_with_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=240
        )
        response.raise_for_status()
        result = response.json().get("response", "").strip()
        if not result:
            raise RuntimeError("Ollama returned an empty response.")
        return result
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Cannot connect to Ollama. Open Ollama on your computer and "
            "check that the llama3.2:latest model is installed."
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "Ollama took too long to respond. Try a shorter study request."
        ) from exc


def generate_study_plan(
    goal,
    target_date,
    daily_hours,
    level,
    preferences="",
    provider="Gemini"
):
    prompt = _build_prompt(
        goal, target_date, daily_hours, level, preferences
    )

    if provider == "Gemini":
        return _generate_with_gemini(prompt), "Gemini"

    if provider == "Ollama (local)":
        return _generate_with_ollama(prompt), "Ollama (local)"

    if provider == "Automatic fallback (Ollama → Gemini)":
        try:
            return _generate_with_ollama(prompt), "Ollama (local)"
        except Exception as ollama_error:
            try:
                return _generate_with_gemini(prompt), "Gemini (fallback)"
            except Exception as gemini_error:
                raise RuntimeError(
                    "Both providers failed. "
                    f"Ollama error: {ollama_error} | "
                    f"Gemini error: {gemini_error}"
                ) from gemini_error

    raise ValueError("Unknown AI provider selected.")


def generate_ai_text(prompt, provider="Gemini"):
    """Generate text using the selected provider or automatic fallback."""
    if provider == "Gemini":
        return _generate_with_gemini(prompt), "Gemini"
    if provider == "Ollama (local)":
        return _generate_with_ollama(prompt), "Ollama (local)"
    if provider == "Automatic fallback (Ollama → Gemini)":
        try:
            return _generate_with_ollama(prompt), "Ollama (local)"
        except Exception as ollama_error:
            try:
                return _generate_with_gemini(prompt), "Gemini (fallback)"
            except Exception as gemini_error:
                raise RuntimeError(
                    f"Both AI providers failed. Ollama: {ollama_error}; "
                    f"Gemini: {gemini_error}"
                ) from gemini_error
    raise ValueError("Unknown AI provider selected.")
