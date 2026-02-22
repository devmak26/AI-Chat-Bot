🤖 AI Chat Bot

An AI-powered chatbot built using FastAPI, LangChain, and Groq API.
This chatbot provides intelligent, real-time responses and is deployed on Render.

🚀 Live Demo

👉 https://ai-chat-bot-1-r2yk.onrender.com/docs

✨ Features

💬 Real-time AI conversation

🧠 Powered by LangChain + Groq LLM

⚡ FastAPI backend

🔐 Secure API key handling with .env

🌐 Deployed on Render

📜 Interactive API documentation (Swagger UI)

🛠️ Tech Stack

Python

FastAPI

LangChain

Groq API

Uvicorn

Render (Deployment)

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/devmak26/AI-Chat-Bot.git
cd AI-Chat-Bot
2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Setup environment variables

Create a .env file and add:

GROQ_API_KEY=your_api_key_here
5️⃣ Run the application
uvicorn app:app --reload
📡 API Endpoints
🔹 Chat Endpoint
POST /chat

Example JSON body:

{
  "message": "Hello AI"
}
🔹 API Documentation
GET /docs

Swagger UI available at:

👉 https://ai-chat-bot-1-r2yk.onrender.com/docs

📦 Deployment

Deployed on Render using:

uvicorn app:app --host 0.0.0.0 --port $PORT
👨‍💻 Author

Dev Makwana
GitHub: https://github.com/devmak26
