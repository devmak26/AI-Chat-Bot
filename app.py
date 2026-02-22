import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from pymongo import MongoClient 
from datetime import datetime,timezone
from fastapi import FastAPI, HTTPException
import logging
import traceback
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")
mongo_uri=os.getenv("MONGO_URI")

client=MongoClient(mongo_uri)
db=client["chatbot"]
collection=db["users"]

app=FastAPI()

class ChatRequest(BaseModel):
    user_id:str
    question:str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,

)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI study assistant. Answer clearly and simply."),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{question}"),
    ]
)

 
llm = ChatGroq(api_key= groq_api_key, model="openai/gpt-oss-20b")
chain = prompt | llm



def get_history(user_id):
    chats = collection.find({"user_id": user_id}).sort("timestamp", 1)
    history = []

    for chat in chats:
        # Normalize history items to a list of dicts with role/content
        history.append({"role": chat.get("role"), "content": chat.get("message")})

    return history
@app.get("/")
def home():
    return {"message":"welcome to the study chat bot"}

@app.post("/chat")

def chat(request:ChatRequest):
    logger = logging.getLogger("uvicorn.error")

    try:
        history = get_history(request.user_id)
        result = chain.invoke({"history": history, "question": request.question})

        # Robust extraction of text from result
        content = None
        if hasattr(result, "content"):
            content = result.content
        elif isinstance(result, dict):
            content = result.get("content") or result.get("text") or result.get("answer")
        else:
            content = getattr(result, "text", None)

        if content is None:
            try:
                content = str(result)
            except Exception:
                content = ""

        collection.insert_one({
            "user_id": request.user_id,
            "role": "user",
            "message": request.question,
            "timestamp": datetime.now(timezone.utc)
        })

        collection.insert_one({
            "user_id": request.user_id,
            "role": "assistant",
            "message": content,
            "timestamp": datetime.now(timezone.utc)
        })

        return {"result": content}

    except Exception as e:
        logger.exception("Error handling /chat request: %s", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")
