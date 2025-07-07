# 🏗️ Architecture

This document provides an overview of the architecture for **PromptedCode**.

---

## System Overview

PromptedCode is a full-stack web application for AI-powered coding interview prep. It consists of:

- **Frontend:** React SPA (Single Page Application)
- **Backend:** FastAPI (Python)
- **AI/ML:** Hugging Face Transformers (Meta-Llama-3-8B-Instruct)
- **Database:** SQLite (via SQLAlchemy ORM)
- **Authentication:** Clerk

---

## High-Level Diagram

```mermaid
graph TD
    A[User] -->|Browser| B[React Frontend]
    B -->|REST API| C[FastAPI Backend]
    C -->|Prompt| D[LLM (Hugging Face)]
    C -->|ORM| E[SQLite DB]
    B -->|Auth| F[Clerk]
```

---

## Data Flow

1. **User** interacts with the React frontend (e.g., clicks "Generate Challenge").
2. **Frontend** sends a REST API request to the FastAPI backend.
3. **Backend** authenticates the user (via Clerk) and processes the request.
4. **Backend** sends a prompt to the LLM (Hugging Face) to generate a coding challenge.
5. **LLM** returns a challenge, which the backend stores in the database and returns to the frontend.
6. **Frontend** displays the challenge and updates the UI.

---

## Backend Structure

- `server.py`: FastAPI entrypoint
- `src/app.py`: FastAPI app instance and routes
- `src/ai_generator.py`: LLM integration and prompt logic
- `src/database/`: SQLAlchemy models and DB utilities
- `src/routes/`: API endpoints (challenge, webhooks)
- `src/utils.py`: Helper functions

---

## Frontend Structure

- `src/`: React source code
  - `auth/`: Authentication components (Clerk)
  - `challenge/`: Challenge generator and MCQ UI
  - `history/`: Challenge history panel
  - `layout/`: Layout and navigation
  - `utils/`: API hooks and helpers

---

## Deployment

- **Backend:** Python 3.13+, Conda, FastAPI, Hugging Face
- **Frontend:** Node.js 18+, Vite, React
- **Auth:** Clerk
- **Dev Tools:** Ngrok for local webhook testing

---

## Extensibility

- Swap out LLMs by editing `ai_generator.py`
- Add new endpoints in `src/routes/`
- Extend UI with new React components
