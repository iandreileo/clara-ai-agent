# Clara - AI Agent for resume building

With Clara you can define resume sections and fields, and API calls to your database and Clara will help your users to fill their sections while talking with the agent.

A FastAPI-based application that leverages AI to create resumes through a conversational interface, powered by LangChain, OpenAI, and PostgreSQL.

## Features

- 💬 Conversational AI interface
- 📝 Resume section management
  - Personal Information
  - Work Experience
  - Education
- 🔄 Edit and update capabilities
- 📚 Conversation history tracking
- 🗄️ PostgreSQL data persistence
- 🐳 Docker containerization
- 🏥 Health monitoring
- 🔒 Bearer token authentication

## Prerequisites

- Docker and Docker Compose
- OpenAI API key
- PostgreSQL database
- Python 3.9+ (for local development)

## Setup

### Environment Variables

Clone `.env.template` to create your `.env` file:

```bash
cp .env.template .env
```

### Docker Deployment (Recommended)

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Configure `.env` file

3. Launch containers:

```bash
docker-compose up -d
```

Access the application at `http://localhost:8000`

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Reference

### Chat Endpoints

| Method | Endpoint        | Description              |
| ------ | --------------- | ------------------------ |
| POST   | `/api/v1/chat/` | Send message to AI agent |

### Health Check

- GET `/api/v1/health/` - Application health status

## Authentication

Use Bearer token authentication:

```
Authorization: Bearer <your-token>
```

## Customization

### Adding Custom Sections and Fields

1. Edit or create new classes in `app/api/v1/models.py`
2. Update `settings.RESUME_SECTIONS` with the new section names
3. Create corresponding tools in `app/tools/resume_tools.py` for each section

Example:

```python
# models.py
class CustomSection(BaseModel):
    title: str
    description: str

# settings.py
RESUME_SECTIONS = [..., "custom_section"]

# resume_tools.py
@tool
async def save_custom_Section(section: CustomSection, *, config: RunnableConfig) -> str:
    """Saves the education custom section of the resume."""
```

## Preview with Streamlit

By default, Streamlit is enable and you can simulate a chat using the port "8501".

You can disable the Streamlit by removing it from the Docker files.
