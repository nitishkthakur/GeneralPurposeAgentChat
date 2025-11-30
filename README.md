# GeneralPurposeAgentChat

A Claude Code-like general purpose AI agent accessible through a modern web interface. Built with LangChain, FastAPI, and Material Design.

## Features

- 🤖 **AI-Powered Chat**: Intelligent conversation with access to powerful tools
- 📁 **Filesystem Tools**: Read, write, list, and manage files and directories
- 🔍 **Search Tools**: Search for files and content across directories
- 🎨 **Modern UI**: Material Design with deep blue theme using Alpine.js
- 🔌 **MCP Architecture**: Modular tool organization for easy extension

## Project Structure

```
├── backend/
│   ├── mcp_tools/           # MCP tool servers
│   │   ├── __init__.py
│   │   ├── filesystem.py    # File operations tools
│   │   └── search.py        # Search tools
│   ├── agent.py             # LangChain agent with tools
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/
│   └── index.html           # Single-page UI with Alpine.js
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key or Anthropic API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/GeneralPurposeAgentChat.git
cd GeneralPurposeAgentChat
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API key
```

4. Start the server:
```bash
python main.py
```

5. Open your browser to http://localhost:8000

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `MODEL_NAME` | Model to use (format: `provider:model`) | `openai:gpt-4o-mini` |

### Supported Models

- OpenAI: `openai:gpt-4o-mini`, `openai:gpt-4o`, `openai:gpt-4-turbo`
- Anthropic: `anthropic:claude-3-5-sonnet-20241022`, `anthropic:claude-3-opus-20240229`

## Available Tools

### Filesystem Tools
- `read_file`: Read contents of a file
- `write_file`: Write content to a file
- `list_directory`: List directory contents
- `create_directory`: Create a new directory
- `delete_file`: Delete a file
- `get_file_info`: Get file metadata

### Search Tools
- `search_files`: Search for files by pattern
- `search_in_file`: Search for text in a file
- `search_in_directory`: Search text across files
- `regex_search`: Search with regular expressions

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve the frontend UI |
| GET | `/health` | Health check |
| POST | `/chat` | Send a message to the agent |
| GET | `/tools` | List available tools |

## Development

### Adding New Tools

1. Create a new file in `backend/mcp_tools/`:
```python
from langchain_core.tools import tool

@tool
def my_tool(param: str) -> str:
    """Tool description."""
    return "result"

my_tools = [my_tool]
```

2. Import and add to `mcp_tools/__init__.py`
3. Import in `agent.py` and add to the tools list

## Technology Stack

- **Frontend**: HTML, CSS, Alpine.js, Material Design
- **Backend**: Python, FastAPI, LangChain, LangGraph
- **AI**: OpenAI GPT or Anthropic Claude via `init_chat_model`

## License

MIT