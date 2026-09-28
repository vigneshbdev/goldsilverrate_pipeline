# 🪙 Gold & Silver Rate Agent

An **Agentic AI-powered gold and silver rate publishing pipeline** that automatically collects the latest Chennai gold and silver rates, validates the data, generates social-media content, reviews the post, renders an Instagram image, and publishes it automatically.

The project is designed as a practical demonstration of **Agentic AI, LLM tool calling, structured outputs, multi-provider LLM abstraction, automation, and API integration**.

---

## ✨ What This Project Does

The pipeline automates the complete journey from **live market data → Instagram post**.

```text
                    ┌─────────────────────┐
                    │   GitHub Actions    │
                    │  Scheduled Trigger  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  LiveChennai Data   │
                    │      Scraper        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Gold Rate Agent   │
                    │                     │
                    │ LLM + Tool Calling  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Structured Data   │
                    │   GoldSilverRate    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              ▼                                 ▼
     ┌─────────────────┐              ┌─────────────────┐
     │  Caption Agent  │              │   Post Renderer │
     │                 │              │                 │
     │ LLM Generated   │              │ Pillow Template │
     │ Instagram Text  │              │                 │
     └────────┬────────┘              └────────┬────────┘
              │                                │
              └────────────────┬───────────────┘
                               ▼
                    ┌─────────────────────┐
                    │    Review Agent     │
                    │                     │
                    │ Validate Post Data │
                    └──────────┬──────────┘
                               │
                         Approved?
                         /       \
                       NO         YES
                       │           │
                       ▼           ▼
                     STOP     ┌──────────────┐
                              │  Cloudinary  │
                              └──────┬───────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │  Instagram   │
                              │     API      │
                              └──────────────┘
```

---

# 🚀 Key Features

* 📊 Live Chennai gold & silver rate extraction
* 🤖 LLM-powered agent workflow
* 🔧 LLM tool calling
* 🧱 Tool Registry architecture
* 📦 Pydantic structured outputs
* 🔄 Multiple LLM provider support
* ⚡ Groq support through OpenAI-compatible API
* 🌐 OpenRouter support
* 💻 Ollama support for local models
* 🧠 Provider-independent `BaseLLM` abstraction
* ✍️ AI-generated Instagram captions
* 🔍 Automated post review
* 🎨 Pillow-based image rendering
* ☁️ Cloudinary image hosting
* 📱 Instagram Graph API publishing
* ⏰ GitHub Actions scheduling
* 🔐 GitHub Secrets for credentials
* 🛑 Validation to prevent publishing stale/invalid rates

---

# 🧠 Agentic Architecture

The project intentionally separates **deterministic application logic** from **LLM reasoning**.

```text
                         User / Scheduler
                                │
                                ▼
                         Orchestration
                                │
                                ▼
                           Agent Layer
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
       GoldRateAgent      CaptionAgent       ReviewAgent
             │                  │                  │
             └──────────────────┼──────────────────┘
                                │
                                ▼
                           Tool Registry
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
          Gold Rate Tool                 Publishing Tools
                 │
                 ▼
            LiveChennai
```

The agents are not directly coupled to a specific LLM provider.

Instead:

```text
Agent
  ↓
BaseLLM
  ↓
LLMFactory
  ↓
Provider
```

This allows the same agent to work with different LLM providers.

---

# 🔌 Multi-LLM Provider Architecture

The project uses an abstraction layer so agents do not depend directly on OpenAI, Groq, OpenRouter, or Ollama.

```text
                     BaseLLM
                        │
                        ▼
                   LLMFactory
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
      Groq          OpenRouter         Ollama
        │               │                │
        └───────────────┼────────────────┘
                        │
                 OpenAI-compatible
                    interface
```

### Supported Providers

| Provider               | Purpose                          |
| ---------------------- | -------------------------------- |
| Groq                   | Fast cloud inference             |
| OpenRouter             | Access to multiple models        |
| Ollama                 | Local LLM experimentation        |
| OpenAI-compatible APIs | Extensible provider architecture |

Provider selection is controlled through environment configuration.

```env
LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-20b
```

The agents don't need to change when switching providers.

---

# 🔧 Tool Calling

The Gold Rate Agent uses an LLM tool call to retrieve the latest rate.

Example tool:

```text
get_latest_gold_and_silver_rates
```

The LLM determines that current rates are required and requests the tool.

```text
User Request
     │
     ▼
GoldRateAgent
     │
     ▼
LLM
     │
     │ tool call
     ▼
Gold Rate Tool
     │
     ▼
LiveChennai
     │
     ▼
GoldSilverRate
```

The tool result is then supplied back to the LLM for structured processing.

---

# 📦 Structured Data

The pipeline uses Pydantic models instead of passing loosely structured dictionaries between agents.

```python
class RateDiff(BaseModel):
    rate: float
    diff: float


class GoldSilverRate(BaseModel):
    date: date
    gold22KRate: RateDiff
    gold24KRate: RateDiff
    silverRate: RateDiff
```

Example:

```json
{
  "date": "2026-09-25",
  "gold22KRate": {
    "rate": 14010,
    "diff": 10
  },
  "gold24KRate": {
    "rate": 15284,
    "diff": 11
  },
  "silverRate": {
    "rate": 250,
    "diff": 0
  }
}
```

This provides validation and a consistent contract between components.

---

# ✍️ Caption Generation

The Caption Agent receives validated rate data and generates a concise Instagram caption.

Example structure:

```text
📅 Gold & Silver Rates — 25 Sep 2026

🟡 22K Gold: ₹14,010/g
📈 +₹10

✨ 24K Gold: ₹15,284/g
📈 +₹11

⚪ Silver: ₹250/g
➡️ No change

Stay updated with daily Chennai gold & silver rates!
```

The agent is instructed not to invent prices or provide financial advice.

---

# 🎨 Image Generation

The post image is rendered deterministically using **Pillow**.

LLMs are responsible for language and reasoning.

Python is responsible for:

* Rate formatting
* Numeric calculations
* Data mapping
* Image positioning
* Template rendering

This keeps the visual output predictable.

```text
GoldSilverRate
      │
      ▼
PostData
      │
      ▼
Pillow Renderer
      │
      ▼
Instagram Image
```

---

# 🔍 Review Agent

Before publishing, the Review Agent validates the generated post.

The review stage helps prevent:

* Incorrect rates
* Missing data
* Invalid captions
* Incorrect dates
* Incomplete post content

```text
Generated Post
      │
      ▼
Review Agent
      │
      ├── rejected → STOP
      │
      └── approved → PUBLISH
```

---

# ☁️ Image Hosting

Generated images are uploaded to **Cloudinary** before being published.

```text
Pillow
  │
  ▼
Generated PNG
  │
  ▼
Cloudinary
  │
  ▼
Public Image URL
  │
  ▼
Instagram API
```

---

# 📱 Instagram Publishing

After the post passes validation:

```text
Review Approved
       │
       ▼
Upload Image
       │
       ▼
Cloudinary URL
       │
       ▼
Instagram Media Container
       │
       ▼
Publish
```

The Instagram credentials are never stored in source code.

---

# ⏰ Automated Scheduling

The project can run automatically through GitHub Actions.

Example schedule:

```text
10:30 AM IST
     │
     ▼
Morning rate check
     │
     ▼
Generate & publish
```

And:

```text
6:30 PM IST
     │
     ▼
Evening rate check
     │
     ▼
Publish only if newer rate is available
```

The exact schedule can be configured in:

```text
.github/workflows/gold-rate.yml
```

The scraper should validate that the source contains the current day's rate before publishing.

---

# 🔐 Configuration

Create a local `.env` file:

```env
LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-20b

GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_API_KEY=

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

INSTAGRAM_ACCESS_TOKEN=
INSTAGRAM_USER_ID=
```

### GitHub Actions

Production credentials should be stored as GitHub repository secrets:

```text
GROQ_API_KEY
CLOUDINARY_CLOUD_NAME
CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET
INSTAGRAM_ACCESS_TOKEN
INSTAGRAM_USER_ID
```

Never commit `.env`.

---

# 📁 Project Structure

```text
post_goldrate/
│
├── .github/
│   └── workflows/
│       └── gold-rate.yml
│
├── src/
│   │
│   ├── agents/
│   │   ├── gold_rate_agent.py
│   │   ├── caption_agent.py
│   │   └── review_agent.py
│   │
│   ├── llm/
│   │   ├── base.py
│   │   ├── config.py
│   │   ├── factory.py
│   │   │
│   │   └── providers/
│   │       └── openai_provider.py
│   │
│   ├── models/
│   │   ├── gold_silver_rate.py
│   │   └── post_data.py
│   │
│   ├── tools/
│   │   ├── tool_definitions.py
│   │   ├── tool_executor.py
│   │   └── ...
│   │
│   ├── services/
│   │   ├── renderer.py
│   │   └── post_pipeline.py
│   │
│   └── main.py
│
├── tests/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🛠️ Tech Stack

| Technology          | Usage                                |
| ------------------- | ------------------------------------ |
| Python              | Core application                     |
| Pydantic            | Data validation & structured outputs |
| OpenAI SDK          | Common LLM client interface          |
| Groq                | Cloud LLM inference                  |
| OpenRouter          | Multi-model LLM access               |
| Ollama              | Local LLM inference                  |
| BeautifulSoup       | Web scraping                         |
| Pillow              | Image rendering                      |
| Cloudinary          | Image hosting                        |
| Instagram Graph API | Publishing                           |
| GitHub Actions      | Automation                           |
| PostgreSQL          | Future agent memory/storage          |

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone <your-repository-url>

cd post_goldrate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure environment

```bash
cp .env.example .env
```

Add your API credentials.

## 4. Run the pipeline

```bash
python -m src.main
```

---

# 🧪 Development Mode

For local development, you can run individual components.

### Test Gold Rate Agent

```bash
python -m src.agents.gold_rate_agent
```

### Test Caption Agent

```bash
python -m src.agents.caption_agent
```

### Test the complete pipeline

```bash
python -m src.main
```

---

# 🧭 Design Principles

This project follows several important Agentic AI design principles.

### 1. LLMs reason, Python validates

Use the LLM for:

* Tool selection
* Planning
* Natural language
* Caption generation
* Review reasoning

Use Python for:

* Calculations
* Validation
* Data transformation
* API calls
* Image rendering
* Business rules

---

### 2. Agents communicate through contracts

Instead of passing arbitrary dictionaries or strings:

```text
Agent → Pydantic Model → Agent
```

This makes the system easier to test and maintain.

---

### 3. Providers are replaceable

Agents should never contain:

```python
OpenAI(...)
```

or:

```python
Groq(...)
```

Instead:

```python
self.llm = LLMFactory.create()
```

This keeps the business logic independent from the model provider.

---

### 4. Fail safely

The pipeline should stop instead of publishing incorrect information.

```text
Invalid rate
     ↓
STOP

Stale rate
     ↓
STOP

Review rejected
     ↓
STOP

Only approved data
     ↓
PUBLISH
```

---

# 🔮 Roadmap

The project is being developed incrementally to explore production-style Agentic AI architecture.

### Completed / In Progress

* [x] Live gold/silver rate scraper
* [x] Gold Rate Agent
* [x] LLM tool calling
* [x] Structured Pydantic output
* [x] Caption Agent
* [x] Review Agent
* [x] Pillow image rendering
* [x] Cloudinary integration
* [x] Instagram publishing
* [x] LLM provider abstraction
* [x] Groq integration
* [x] OpenRouter integration
* [x] Ollama integration
* [x] GitHub Actions automation

### Planned

* [ ] Tool Registry
* [ ] Generic Orchestrator Agent
* [ ] Execution Plan / Plan Executor
* [ ] Agent memory
* [ ] PostgreSQL state management
* [ ] Retry & failure handling
* [ ] Human-in-the-loop approval
* [ ] MCP integration
* [ ] LangGraph implementation
* [ ] Langfuse observability
* [ ] Agent execution dashboard
* [ ] Automated tests
* [ ] Production deployment

---

# 🎯 Why This Project?

This project is more than an automated Instagram poster.

It is a practical exploration of how to build **production-oriented Agentic AI systems**.

The architecture demonstrates:

```text
LLM
 +
Tool Calling
 +
Structured Outputs
 +
Agents
 +
Tool Registry
 +
Provider Abstraction
 +
Automation
 +
External APIs
 +
Validation
 +
Observability
```

The long-term goal is to evolve this from a simple scheduled pipeline into a **general-purpose agentic content automation system**.

---

# 👨‍💻 Author

**Vignesh B**

Senior Software Engineer | Python | GenAI | Agentic AI | AWS

---

## ⭐ Project Philosophy

> Build small. Validate everything. Let the LLM reason where reasoning is useful, and let deterministic code handle what must be correct.
