# PDF Summarizer Agent

A local PDF summarization system powered by **Google Agent Development Kit (ADK)**, **FastAPI**, and **Ollama** with the Mistral model. Upload PDFs through a modern web interface and get AI-generated summaries instantly.

## 🌟 Features

- **Modern Web Interface**: Beautiful, responsive UI with drag-and-drop file upload
- **Local LLM Processing**: Uses Ollama with Mistral model for privacy and speed
- **Google ADK Integration**: Leverages ADK for robust agent orchestration
- **FastAPI Backend**: High-performance REST API with automatic documentation
- **Real-time Processing**: Instant PDF text extraction and summarization
- **Mac M5 Optimized**: Designed for Apple Silicon with 24GB RAM

## 📋 Prerequisites

- **Python 3.11+** (installed in virtual environment)
- **Ollama** (for local LLM hosting)
- **Mac M5** with 24GB RAM (or similar hardware)

## 🚀 Installation

### 1. Install Ollama

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the Mistral model
ollama pull mistral
```

### 2. Set Up the Project

```bash
# Clone or navigate to the project directory
cd /Users/sudhakarchigurupati/ADKProject/pdf_summary_adk_agent

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

The `.env` file is already configured with default settings:

```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=mistral
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
MAX_FILE_SIZE_MB=10
```

Modify these values if needed.

## 🎯 Usage

### Start Ollama

First, ensure Ollama is running:

```bash
# Start Ollama server
ollama serve
```

Keep this terminal open.

### Start the Backend

In a new terminal:

```bash
# Navigate to project directory
cd /Users/sudhakarchigurupati/ADKProject/pdf_summary_adk_agent

# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`

### Open the Frontend

**Option 1: Direct File Access**
- Open `frontend/index.html` directly in your browser

**Option 2: Local Server (Recommended)**
```bash
# In a new terminal, navigate to frontend directory
cd /Users/sudhakarchigurupati/ADKProject/pdf_summary_adk_agent/frontend

# Start a simple HTTP server
python -m http.server 3000
```

Then open `http://localhost:3000` in your browser.

### Using the Application

1. **Upload PDF**: Drag and drop a PDF file or click "Browse Files"
2. **Generate Summary**: Click "Generate Summary" button
3. **View Results**: Read the AI-generated summary
4. **Copy or Restart**: Copy the summary or process another PDF

## 📁 Project Structure

```
pdf_summary_adk_agent/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   └── pdf_extractor.py     # PDF text extraction utility
├── agent/
│   ├── __init__.py
│   ├── agent.py             # ADK agent implementation
│   └── ollama_config.py     # Ollama configuration
├── frontend/
│   ├── index.html           # Web interface
│   ├── styles.css           # Styling
│   └── script.js            # Frontend logic
├── .env                     # Environment configuration
├── .gitignore              # Git ignore patterns
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔌 API Documentation

### Endpoints

#### `GET /`
Root endpoint with API information.

**Response:**
```json
{
  "message": "PDF Summarizer Agent API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "pdf-summarizer-agent"
}
```

#### `POST /upload`
Upload a PDF and generate a summary.

**Request:**
- Content-Type: `multipart/form-data`
- Body: PDF file (max 10MB)

**Response:**
```json
{
  "summary": "AI-generated summary text...",
  "page_count": 5,
  "file_name": "document.pdf"
}
```

**Error Response:**
```json
{
  "detail": "Error message"
}
```

### Interactive API Docs

Visit `http://localhost:8000/docs` for Swagger UI documentation.

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.11+
- **Agent Framework**: Google ADK
- **LLM**: Ollama (Mistral model)
- **PDF Processing**: PyMuPDF (fitz)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Server**: Uvicorn (ASGI)

## 🔧 Troubleshooting

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
killall ollama
ollama serve
```

### Model Not Found

```bash
# List available models
ollama list

# Pull Mistral model
ollama pull mistral
```

### Backend Errors

```bash
# Check backend logs
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### CORS Issues

If the frontend can't connect to the backend:
- Ensure backend is running on `http://localhost:8000`
- Check browser console for errors
- Verify `script.js` has correct `API_BASE_URL`

## 🎨 Features Highlights

### Modern UI/UX
- Dark mode with glassmorphism effects
- Smooth animations and transitions
- Responsive design for all screen sizes
- Drag-and-drop file upload
- Real-time progress indicators

### Robust Error Handling
- File type validation (PDF only)
- File size limits (10MB default)
- Comprehensive error messages
- Graceful fallback mechanisms

### Performance Optimizations
- Async/await for non-blocking operations
- Temporary file cleanup
- Efficient text extraction
- Optimized for Mac M5 hardware

## 📝 License

This project is open source and available for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📧 Support

For issues or questions, please open an issue in the repository.

## 🛑 Stopping Servers

When you're done using the application, you can stop all running servers:

### Stop Backend Server

If running in foreground (with `--reload`):
```bash
# Press CTRL+C in the terminal where uvicorn is running
```

If running in background or need to force stop:
```bash
# Find and kill the uvicorn process
pkill -f "uvicorn backend.main:app"

# Or find the process ID and kill it
ps aux | grep uvicorn
kill <PID>
```

### Stop Frontend Server

If you started a Python HTTP server:
```bash
# Press CTRL+C in the terminal where the server is running
```

Or force stop:
```bash
# Kill Python HTTP server on port 3000
lsof -ti:3000 | xargs kill -9

# Or for port 3001
lsof -ti:3001 | xargs kill -9
```

### Stop Ollama

```bash
# Stop Ollama server
killall ollama

# Or use pkill
pkill -f ollama
```

### Stop All Servers at Once

```bash
# Stop all related processes
pkill -f "uvicorn backend.main:app"
pkill -f "http.server"
killall ollama

# Verify all stopped
ps aux | grep -E "uvicorn|http.server|ollama"
```

### Deactivate Virtual Environment

```bash
# When done, deactivate the Python virtual environment
deactivate
```

## 🔧 ADK Integration Troubleshooting

This section documents common issues encountered when integrating Google ADK with Ollama and their solutions.

### Issue 1: Import Path Error

**Error:**
```
ModuleNotFoundError: No module named 'google.adk.llms'
```

**Solution:**
The correct import path for LiteLlm is:
```python
from google.adk.models import LiteLlm  # ✅ Correct
# NOT: from google.adk.llms import LiteLlm  # ❌ Wrong
```

### Issue 2: Missing Session Service

**Error:**
```
Runner.__init__() missing 1 required keyword-only argument: 'session_service'
```

**Solution:**
ADK Runner requires a session service for managing conversation state:
```python
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
runner = Runner(
    app_name="your_app",
    agent=your_agent,
    session_service=session_service  # Required!
)
```

### Issue 3: Missing App Name

**Error:**
```
Either app or both app_name and agent must be provided
```

**Solution:**
When providing an agent to Runner, you must also provide `app_name`:
```python
runner = Runner(
    app_name="pdf_summarizer",  # Required when using agent
    agent=pdf_summarizer_agent,
    session_service=session_service
)
```

### Issue 4: Incorrect Message Format

**Error:**
```
Runner.run() takes 1 positional argument but 2 were given
```

**Solution:**
Don't pass a string directly. Use `types.Content` format:
```python
from google.genai import types

# ❌ Wrong
response = runner.run(prompt_string)

# ✅ Correct
new_message = types.Content(
    role='user',
    parts=[types.Part(text=prompt_string)]
)
response = runner.run(
    user_id="user_id",
    session_id="session_id",
    new_message=new_message
)
```

### Issue 5: Session Not Found

**Error:**
```
ValueError: Session not found: session_id
```

**Solution:**
You must create the session before using it:
```python
# Create session first
await session_service.create_session(
    app_name="pdf_summarizer",
    user_id="user_id",
    session_id="session_id"
)

# Then run the agent
async for event in runner.run_async(
    user_id="user_id",
    session_id="session_id",
    new_message=new_message
):
    # Process events
```

### Issue 6: Async/Await Required (Critical!)

**Error:**
Session still not found even after calling `create_session()`

**Root Cause:**
`create_session()` is an **async** function. If you don't `await` it, the session is never actually created.

**Solution:**
Always use `await` with async ADK methods:
```python
# ❌ Wrong - session never created
session_service.create_session(app_name, user_id, session_id)

# ✅ Correct - properly awaited
await session_service.create_session(app_name, user_id, session_id)

# Also use run_async instead of run
async for event in runner.run_async(...):  # ✅ Correct
    # Process events
```

### Complete Working Pattern

Here's the complete pattern that works:

```python
import uuid
from google.adk.agents import Agent
from google.adk.models import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

async def generate_summary(text: str) -> str:
    # 1. Create session service
    session_service = InMemorySessionService()
    
    # 2. Generate unique IDs
    user_id = "pdf_user"
    session_id = f"session_{uuid.uuid4().hex[:8]}"
    app_name = "pdf_summarizer"
    
    # 3. Create session (async!)
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    # 4. Create Runner
    runner = Runner(
        app_name=app_name,
        agent=your_agent,
        session_service=session_service
    )
    
    # 5. Format message
    new_message = types.Content(
        role='user',
        parts=[types.Part(text=text)]
    )
    
    # 6. Run agent (async!)
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=new_message
    ):
        if hasattr(event, 'content') and event.content:
            if hasattr(event.content, 'parts'):
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_text += part.text
    
    return response_text
```

### Key Takeaways

1. **Import Path**: Use `google.adk.models.LiteLlm`
2. **Session Service**: Always required for Runner
3. **App Name**: Required when providing an agent
4. **Message Format**: Use `types.Content` with role and parts
5. **Session Creation**: Must create session before use
6. **Async/Await**: Critical - `await create_session()` and use `run_async()`
7. **Event Processing**: Iterate through events to collect response

---

**Built with ❤️ using Google ADK, FastAPI & Ollama**
