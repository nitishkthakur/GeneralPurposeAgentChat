"""Agent module using LangChain with MCP tools."""

import os
from typing import List, Dict, Any, Optional

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

from mcp_tools.filesystem import filesystem_tools
from mcp_tools.search import search_tools


class Agent:
    """General purpose agent with MCP tools."""

    SYSTEM_PROMPT = """You are a helpful AI assistant with access to filesystem and search tools.
You can help users with tasks like:
- Reading and writing files
- Navigating directories
- Searching for files and content
- General programming assistance

When using tools, explain what you're doing and provide clear results.
Be concise but thorough in your responses."""

    def __init__(self, model_name: Optional[str] = None):
        """Initialize the agent with MCP tools.

        Args:
            model_name: The model to use (e.g., 'openai:gpt-4', 'anthropic:claude-3-5-sonnet-20241022').
                       Defaults to environment variable MODEL_NAME or 'openai:gpt-4o-mini'.
        """
        self.model_name = model_name or os.getenv("MODEL_NAME", "openai:gpt-4o-mini")

        # Combine all MCP tools
        self.tools = filesystem_tools + search_tools

        # Initialize the model
        self._model = None
        self._agent = None
        self._init_agent()

    def _init_agent(self):
        """Initialize the chat model and agent."""
        try:
            # Use init_chat_model from LangChain
            self._model = init_chat_model(self.model_name)

            # Create the agent with tools using create_react_agent
            self._agent = create_react_agent(
                self._model,
                tools=self.tools,
            )
        except Exception as e:
            print(f"Warning: Failed to initialize agent: {e}")
            self._agent = None

    def is_ready(self) -> bool:
        """Check if the agent is ready to process messages."""
        return self._agent is not None

    def get_tool_names(self) -> List[str]:
        """Get the names of available tools."""
        return [tool.name for tool in self.tools]

    async def invoke(self, messages: List[Dict[str, str]]) -> str:
        """Invoke the agent with a list of messages.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.

        Returns:
            The agent's response as a string.
        """
        if not self.is_ready():
            return "Error: Agent is not initialized. Please check your API keys."

        try:
            # Convert messages to LangChain format
            langchain_messages = [SystemMessage(content=self.SYSTEM_PROMPT)]

            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")

                if role == "user":
                    langchain_messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    langchain_messages.append(AIMessage(content=content))
                elif role == "system":
                    langchain_messages.append(SystemMessage(content=content))

            # Invoke the agent
            result = await self._agent.ainvoke({"messages": langchain_messages})

            # Extract the final response
            if "messages" in result:
                # Get the last AI message
                for msg in reversed(result["messages"]):
                    if isinstance(msg, AIMessage):
                        return msg.content

            return "I apologize, but I couldn't generate a response."

        except Exception as e:
            return f"Error processing request: {str(e)}"
