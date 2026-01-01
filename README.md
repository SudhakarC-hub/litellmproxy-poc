# PDF Summarizer Agent with LiteLLM Proxy

A FastAPI-based PDF summarizer using Google ADK agents with LiteLLM proxy for unified LLM access.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (for LiteLLM proxy)
- Gemini API key (get from https://aistudio.google.com/app/apikey)

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Environment

Create/update `.env` file:

```bash
# LiteLLM Proxy Configuration
LITELLM_MASTER_KEY=sk-1234
LITELLM_SALT_KEY=sk-1234
LITELLM_PROXY_URL=http://localhost:4000

# Model Selection (any model configured in proxy)
MODEL_NAME=gemini-flash

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
MAX_FILE_SIZE_MB=10


### 3. Start LiteLLM Proxy

```bash
# Start proxy with Docker Compose
docker compose up -d

# Verify proxy is running
curl http://localhost:4000/health

# Check available models
curl http://localhost:4000/models -H "Authorization: Bearer sk-1234"
```

**Proxy URLs:**
- API: http://localhost:4000
- Admin UI: http://localhost:4000/ui
- Prometheus: http://localhost:9090

### 4. Start Backend Server

```bash
# Activate virtual environment
source venv/bin/activate

# Start server
uvicorn backend.main:app --reload
```

Server runs on: http://localhost:8000

### 5. Test the Application

**Option A: Using Swagger UI**
1. Visit http://localhost:8000/docs
2. Click on `/upload` endpoint
3. Upload a PDF file
4. Get summary response

**Option B: Using curl**
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@your_document.pdf"
```

## 📋 LiteLLM Proxy Setup Guide

### Step 1: Configure Models

Edit `config.yaml` to define available models:

```yaml
model_list:
  # Ollama Models (self-hosted)
  - model_name: mistral
    litellm_params:
      model: ollama_chat/mistral
      api_base: http://localhost:11434
  
  # Gemini Models
  - model_name: gemini-flash
    litellm_params:
      model: gemini/gemini-2.5-flash-lite
  
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
```

### Step 2: Start Proxy Services

```bash
# Start all services (proxy, database, prometheus)
docker compose up -d

# View logs
docker compose logs -f litellm

# Stop services
docker compose down
```

### Step 3: Verify Proxy Configuration

```bash
# Test health endpoint
curl http://localhost:4000/health

# List available models
curl http://localhost:4000/models \
  -H "Authorization: Bearer sk-1234"

# Test chat completion
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-flash",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Step 4: Configure ADK Agent

The agent is configured in `agent/agent.py`:

```python
from google.adk.models import LiteLlm
from google.adk.agents import Agent

pdf_summarizer_agent = Agent(
    model=LiteLlm(
        model=f"openai/{MODEL_NAME}",  # Uses OpenAI-compatible format
        api_base=proxy_config["proxy_url"],
        api_key=proxy_config["api_key"]
    ),
    name="pdf_summarizer_agent",
    # ... agent configuration
)
```

**Key Points:**
- Use `openai/` prefix for model name (e.g., `openai/gemini-flash`)
- Point to proxy URL (`http://localhost:4000`)
- Use master key for authentication
- API keys managed in proxy, not in application code

### Step 5: Switch Models

To use a different model, update `MODEL_NAME` in `.env`:

```bash
# Use Gemini Flash
MODEL_NAME=gemini-flash

# Use Ollama Mistral
MODEL_NAME=mistral
```

Restart the backend server after changing models.

## 🔧 Troubleshooting

### Docker Daemon Not Running

If you get `Cannot connect to the Docker daemon`:

**Solution:**
1. Start Docker Desktop application
2. Wait for Docker to fully start (check the Docker icon in menu bar)
3. Verify Docker is running: `docker ps`
4. Then run: `docker compose up -d`

### Proxy Won't Start

```bash
# Check if ports are in use
lsof -ti:4000 | xargs kill -9  # Kill process on port 4000
lsof -ti:8000 | xargs kill -9  # Kill process on port 8000

# Check Docker logs
docker compose logs litellm
docker compose logs db
```

### Missing Dependencies

If you get `ModuleNotFoundError: No module named 'backoff'`:

```bash
pip install 'litellm[proxy]'
```

### Ollama Models Not Working

Ensure Ollama is running:

```bash
# Start Ollama
ollama serve

# Pull model
ollama pull mistral

# Test model
ollama run mistral "Hello"
```

### Gemini API Errors

1. Verify API key is valid at https://aistudio.google.com/
2. Check `.env` has `GEMINI_API_KEY` set
3. Restart proxy: `docker compose restart litellm`

## 📁 Project Structure

```
pdf_summary_adk_agent/
├── agent/
│   ├── agent.py           # ADK agent configuration
│   └── proxy_config.py    # Proxy connection settings
├── backend/
│   ├── main.py           # FastAPI application
│   └── pdf_extractor.py  # PDF text extraction
├── config.yaml           # LiteLLM model configuration
├── docker-compose.yml    # Proxy services
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔑 Key Features

- **Unified LLM Access**: Single API for multiple LLM providers (Gemini, Ollama, etc.)
- **API Key Management**: Centralized key management in proxy
- **Monitoring**: Built-in Prometheus metrics and admin UI
- **OpenAI Compatible**: Standard OpenAI API format for all models
- **Easy Model Switching**: Change models via environment variable

## 📚 API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

### Upload PDF
```bash
POST http://localhost:8000/upload
Content-Type: multipart/form-data

file: <PDF file>
```

**Response:**
```json
{
  "summary": "Generated summary text...",
  "page_count": 5,
  "file_name": "document.pdf"
}
```

## 🔗 Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Google ADK Documentation](https://google.github.io/adk/)
- [Gemini API](https://ai.google.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📝 License

MIT License
