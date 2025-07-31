from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# Create the FastAPI app
app = FastAPI()

# Enable CORS for all origins (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ ROOT ROUTE (Fix for 404 error)
@app.get("/")
async def root():
    return {"message": "SynAgent API is running 🚀"}

# Data model for the incoming POST /ask request
class Message(BaseModel):
    question: str

# Main assistant route
@app.post("/ask")
async def ask_question(message: Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are SynAgent's helpful AI assistant. Answer questions about SynAgent services, pricing, capabilities, and benefits in a friendly and professional tone."},
                {"role": "user", "content": message.question}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
