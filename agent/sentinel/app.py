from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel, Field

from config import HOST, PORT
from memory import init_db, save_message, get_recent_messages
from model import LocalModel

app = FastAPI(title="Local Chatbot Server")
model = LocalModel()


class ChatRequest(BaseModel):
    session_id: str | None = Field(default=None)
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    session_id = req.session_id or str(uuid4())

    save_message(session_id, "user", req.message)
    history = get_recent_messages(session_id)
    reply = model.generate(req.message, history)
    save_message(session_id, "assistant", reply)

    return ChatResponse(session_id=session_id, reply=reply)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
