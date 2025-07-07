# 🚦 Usage Guide

This guide will help you set up, configure, and use **PromptedCode** for AI-powered coding interview practice.

---

## 1. Prerequisites

- Python 3.13+
- Node.js 18+
- Conda (recommended)
- Hugging Face account
- Clerk account
- Ngrok (for webhook testing)

---

## 2. Installation

### Backend

```bash
conda create -n llm-codegen python=3.13
conda activate llm-codegen
pip install -r backend/requirements.txt
cd backend
huggingface-cli login
python server.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 3. Configuration

- **Backend:** Create a `.env` file with Clerk API keys, JWT secret, Hugging Face token, etc.
- **Frontend:** Create a `.env` file with your Clerk publishable key.

---

## 4. Using the App

1. **Sign in** with Clerk.
2. **Generate a challenge:** Select difficulty and click "Generate Challenge".
3. **Solve the challenge:** Choose an answer and submit.
4. **View feedback:** See if you were correct and get an explanation.
5. **Track history:** Review past challenges in the History panel.
6. **Check quota:** Daily challenge quota resets every 24 hours.

---

## 5. Customization

- **Change LLM:** Edit `ai_generator.py` to use a different Hugging Face model.
- **Add features:** Extend React components or FastAPI routes as needed.

---

## 6. Troubleshooting

- **Apple Silicon:** Use MPS device and float16 for PyTorch (see README).
- **Auth issues:** Double-check Clerk keys and frontend/backend `.env` files.
- **Model errors:** Ensure Hugging Face login and correct model name.

---

## 7. More Help

- See the [FAQ](faq.md) or [open an issue](https://github.com/ethanvillalovoz/llm-coding-challenge-generator/issues).
