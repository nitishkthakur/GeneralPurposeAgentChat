"""Main FastAPI application for the General Purpose Agent Chat."""

import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from agent import Agent

# Load environment variables
load_dotenv()

# Get absolute paths
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(
    title="General Purpose Agent Chat",
    description="A Claude Code-like general purpose agent with MCP tools",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
agent = Agent()


class Message(BaseModel):
    """A chat message."""

    role: str = Field(..., description="The role of the message sender (user or assistant)")
    content: str = Field(..., description="The content of the message")


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    message: str = Field(..., description="The user's message")
    conversation_history: List[Message] = Field(
        default_factory=list, description="Previous conversation history"
    )


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""

    response: str = Field(..., description="The agent's response")
    conversation_history: List[Message] = Field(
        ..., description="Updated conversation history"
    )


@app.get("/")
async def root():
    """Serve the main HTML page."""
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(str(index_path))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent_ready": agent.is_ready()}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message and return the agent's response."""
    try:
        # Build messages from history
        messages = []
        for msg in request.conversation_history:
            messages.append({"role": msg.role, "content": msg.content})

        # Add the current user message
        messages.append({"role": "user", "content": request.message})

        # Get response from agent
        response = await agent.invoke(messages)

        # Build updated conversation history
        updated_history = request.conversation_history + [
            Message(role="user", content=request.message),
            Message(role="assistant", content=response),
        ]

        return ChatResponse(response=response, conversation_history=updated_history)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List available tools."""
    return {"tools": agent.get_tool_names()}


# Mount static files for frontend
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
