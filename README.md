# StudySpace AI – Personal AI-Powered Study Assistant

## Project Overview
StudySpace AI is an AI-powered personal study assistant designed to help students organize their academic activities, plan study schedules, monitor learning progress, and improve their preparation through AI-based learning support.

## Features
- Dashboard with study progress overview
- Study task management
- Subject and syllabus tracking
- Daily study tracker
- AI-powered study planner
- AI study chatbot
- Automatic quiz generation
- Smart flashcards
- Exam countdown
- Weekly study analytics
- Achievement tracking
- Focus timer

## Technology Stack
- Python
- Streamlit
- SQLite
- Google Gemini API
- Ollama (local LLM)

## Project Structure
- `app.py` – Main Streamlit application
- `database.py` – Core database operations
- `ai_engine.py` – AI provider integration
- `study_features_db.py` – Additional study feature database operations

## Installation and Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the required dependencies:

   `python -m pip install -r requirements.txt`

4. Create a `.env` file in the project folder and add your Gemini API key:

   `GEMINI_API_KEY=your_api_key_here`

5. Start the application:

   `python -m streamlit run app.py`

## AI Providers
StudySpace AI supports Google Gemini for cloud-based AI generation and Ollama for local AI generation.

## Database
SQLite is used to store study tasks, subjects, syllabus topics, study sessions, quiz results, flashcards, and exam information.

## Project Purpose
The project demonstrates how AI agents and Python-based application logic can support personalized student learning and academic planning.

## Author
Student Project – AI Agents
