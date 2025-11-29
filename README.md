# Annie — A Personal AI Assistant  
### Multi-Agent System | Google AI Agents Capstone Project

**Author:** H. Nilsankar Singha  
**Project Type:** Google AI Agents Course — Capstone Submission  
**Tech Stack:** Python, Google ADK, Gemini 2.5 Flash, Multi-Agent Architecture  

---

## Overview
Annie is a custom-built personal AI assistant designed using Google’s AI Agent Development Kit (ADK).  
The system features:

- A **main assistant agent** with creator verification, personality rules, and memory.
- A **technical agent** specializing in debugging, MERN stack, Python, OOP, and code reasoning.
- A **memory service** with automatic saving and loading.
- A complete **evaluation suite** validating authentication, memory, and technical reasoning.
- A **CLI chat interface** powered by Google ADK Runner.

This project is part of the official capstone requirement for the Google AI Agents course.

---

## Steps for running the app 

 1. create venv and activate (Windows)
python -m venv venv
venv\Scripts\activate

 2. install
pip install -r requirements.txt

 3. create .env (main directory)
 
GOOGLE_API_KEY=your_api_key_here

 4. run the CLI assistant
python main.py

 5. run the evaluation suite
python evaluation/eval_runner.py
