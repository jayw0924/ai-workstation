# Autonomous Research Agent

Automatically searches the web, analyzes sources, and generates comprehensive research reports.

## Features

- 🔍 Web search using DuckDuckGo
- 📄 Automatic content scraping from sources
- 🤖 AI-powered analysis with Claude
- 📝 Markdown report generation
- 📚 Auto-saves to knowledge base
- 🎯 Source citations and synthesis

## Usage
```bash
cd research-agent
source ../ai-env/bin/activate

# Run research on a topic
python research_agent.py "Your research topic here"
```

## Examples
```bash
# Research vector databases
python research_agent.py "What are the latest developments in vector databases?"

# Research AI techniques
python research_agent.py "How does retrieval augmented generation work?"

# Research any topic
python research_agent.py "Best practices for Python async programming"
```

## Output

Reports are saved to:
- `research_outputs/` - Local output directory
- `../markdown-rag/data/markdown/research_reports/` - Knowledge base (run ingest to add)

## How It Works

1. **Search**: Queries DuckDuckGo for relevant articles
2. **Scrape**: Retrieves full content from top sources
3. **Analyze**: Claude analyzes and synthesizes findings
4. **Report**: Generates structured markdown report with citations
5. **Save**: Stores locally and in knowledge base

## Report Structure

- Executive summary with key findings
- Synthesis across all sources
- Source citations
- Full source list with URLs
- Methodology notes

---

*Part of the AI Workstation suite*
