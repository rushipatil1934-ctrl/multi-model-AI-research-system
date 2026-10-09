# ResearchMind - Multi-Agent AI Research System

ResearchMind is an AI-powered research assistant that automates the complete research workflow using multiple specialized AI agents. Instead of relying on a single LLM for every task, the system coordinates dedicated agents to search the web, extract information, generate structured research reports, and independently evaluate the quality of the generated content.


## Features

- Multi-agent architecture powered by LangChain
- Live web search using Tavily API
- Web scraping for extracting detailed information
- AI-generated structured research reports
- Independent AI critic that reviews and scores reports
- Downloadable Markdown reports
- Clean and responsive Streamlit interface

---

## Multi-Agent Pipeline

The application consists of four specialized agents:

### 1. Search Agent
- Searches the web for recent and reliable information
- Retrieves relevant sources using Tavily Search

### 2. Reader Agent
- Visits the retrieved URLs
- Scrapes and extracts useful information from web pages

### 3. Writer Chain
- Organizes the collected research
- Generates a professional research report including:
  - Introduction
  - Key Findings
  - Conclusion
  - Sources

### 4. Critic Chain
- Reviews the generated report
- Assigns a quality score
- Highlights strengths
- Suggests improvements

---

## Tech Stack

### AI & LLM
- LangChain
- Mistral AI

### Backend
- Python

### Frontend
- Streamlit

### Search & Scraping
- Tavily API
- BeautifulSoup
- Requests

## Project Structure

```text
.
├── app.py                 # Streamlit frontend
├── agents.py              # Multi-agent configuration
├── tools.py               # Search and scraping tools
├── requirements.txt
├── .env
├── README.md
└── assets/
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/Multi-agent-research-system.git

cd Multi-agent-research-system
```

### Create Virtual Environment

Using uv

```bash
uv venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux/Mac

```bash
source .venv/bin/activate
```

---

### Install Dependencies

```bash
uv pip install -r requirements.txt
```

or

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```env
MISTRAL_API_KEY=your_mistral_api_key

TAVILY_API_KEY=your_tavily_api_key
```

---

## Run the Application

```bash
streamlit run app.py
```

---

## Example Workflow

1. Enter a research topic.
2. Search Agent finds recent information.
3. Reader Agent extracts content from the retrieved websites.
4. Writer Chain generates a detailed report.
5. Critic Chain evaluates the report.
6. Download the report as a Markdown file.

---

## Screenshots

### Multi-Agent Pipeline

Shows the coordinated workflow where multiple AI agents collaborate to perform research.

### Research Report

Generated report containing structured findings and cited sources.

### Critic Review

AI-generated evaluation including strengths, improvement suggestions, and overall quality score.

---

## Future Improvements

- PDF export
- Citation formatting (APA/IEEE)
- Streaming agent responses
- Memory-enabled agents
- Parallel agent execution
- RAG support with vector databases
- Support for multiple LLM providers
- Research history and saved reports

---

## Learning Outcomes

This project helped me gain practical experience with:

- Multi-Agent Systems
- LangChain Agents
- Tool Calling
- Prompt Engineering
- LLM Orchestration
- Web Search Integration
- Web Scraping
- Streamlit Development
- Python Project Deployment
- API Integration
- Environment Variable Management

---

## Author

**Rushikesh patil**


---

## License

This project is intended for educational and portfolio purposes.
