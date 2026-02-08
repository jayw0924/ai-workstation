# AI Workstation - Knowledge Base RAG System

> Multi-format document ingestion and semantic search powered by Claude AI and ChromaDB

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Features

- **Multi-Format Support**: Ingest Markdown, PDF, and web pages
- **Smart Chunking**: Intelligent text splitting with configurable overlap
- **Vector Search**: Semantic search using ChromaDB embeddings
- **AI-Powered Q&A**: Claude Sonnet 4 integration with context-aware answers
- **Source Citations**: Full transparency with document sources and similarity scores
- **Dual Interface**: Both CLI and beautiful web UI
- **Persistent Storage**: ChromaDB with automatic embedding generation

## 📋 Prerequisites

- Python 3.12+
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- 2GB+ RAM recommended
- Linux/macOS (tested on Fedora 41)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/jay0924/ai-workstation.git
cd ai-workstation
```

### 2. Create Virtual Environment
```bash
python3.12 -m venv ai-env
source ai-env/bin/activate  # On Windows: ai-env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Anthropic API key
nano .env
```

Your `.env` should look like:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

## 📚 Usage

### Adding Documents
```bash
cd markdown-rag

# Add Markdown files
cp /path/to/your/docs/*.md data/markdown/

# Add PDF files
cp /path/to/your/pdfs/*.pdf data/pdf/

# Add web URLs to scrape
echo "https://docs.example.com" >> data/urls.txt
```

### Ingesting Documents
```bash
# Run enhanced ingestion (MD, PDF, web scraping with chunking)
python ingest_enhanced.py
```

This will:
- Load all markdown files from `data/markdown/`
- Load all PDFs from `data/pdf/`
- Scrape URLs from `data/urls.txt`
- Split documents into smart chunks (1000 chars, 200 overlap)
- Generate embeddings and store in ChromaDB

### Querying via CLI

**Interactive Mode:**
```bash
python query_enhanced.py
```

**Single Question:**
```bash
python query_enhanced.py "How do I configure the API?"
```

### Querying via Web Interface
```bash
# Start web server
python web_app.py

# Open browser to:
# http://localhost:5000
```

**Features:**
- Beautiful gradient UI
- Real-time search
- Source cards with similarity scores
- File type badges (Markdown, PDF, Web)
- Responsive design

## 🏗️ Project Structure
```
ai-workstation/
├── markdown-rag/              # Main RAG system
│   ├── ingest_enhanced.py     # Document ingestion with chunking
│   ├── query_enhanced.py      # CLI query interface
│   ├── web_app.py            # Flask web interface
│   ├── templates/
│   │   └── index.html        # Web UI
│   ├── data/
│   │   ├── markdown/         # Your .md files
│   │   ├── pdf/             # Your .pdf files
│   │   └── urls.txt         # URLs to scrape
│   └── chroma_db/           # Vector database (gitignored)
├── docs/                     # Documentation
├── test_chromadb.py         # ChromaDB test script
├── test_claude.py           # Claude API test script
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
└── README.md              # This file
```

## 🔧 Configuration

### Chunking Parameters

Edit `ingest_enhanced.py`:
```python
chunk_size=1000      # Characters per chunk
chunk_overlap=200    # Overlap between chunks
```

### Search Results

Edit `query_enhanced.py` or `web_app.py`:
```python
n_results=5  # Number of chunks to retrieve
```

## 🧪 Testing

### Test ChromaDB Connection
```bash
python test_chromadb.py
```

### Test Claude API
```bash
python test_claude.py
```

## 📊 How It Works

1. **Document Ingestion**
   - Documents are loaded from `data/` folders
   - Text is split into overlapping chunks
   - Embeddings are generated automatically
   - Stored in ChromaDB with metadata

2. **Semantic Search**
   - User query is embedded
   - ChromaDB finds similar document chunks
   - Returns top N matches with similarity scores

3. **AI-Powered Answers**
   - Relevant chunks are sent to Claude as context
   - Claude generates comprehensive answer
   - Sources are cited with file names and chunks

## 🎯 Use Cases

- **Technical Documentation**: Search internal wikis, API docs, setup guides
- **Research**: Query across papers, articles, reports
- **Knowledge Management**: Company policies, procedures, training materials
- **Personal Notes**: Searchable second brain for markdown notes

## 🔐 Security Notes

- **Never commit `.env`** - Contains your API keys
- **Never commit `data/`** - Your personal documents
- **Never commit `chroma_db/`** - Your vector database
- All sensitive files are in `.gitignore`

## 🤝 Contributing

Feel free to fork, improve, and submit PRs!

## 📝 License

MIT License - feel free to use for personal or commercial projects

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com) - Claude AI
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [LangChain](https://www.langchain.com/) - Text splitting utilities
- [Flask](https://flask.palletsprojects.com/) - Web framework

## 📧 Contact

GitHub: [@jay0924](https://github.com/jay0924)

---

**Built with ❤️ on Fedora Linux**

## 🔬 Research Agent

**Location:** `research-agent/`

Autonomous agent that researches topics by searching the web, analyzing sources, and generating comprehensive reports.

### Quick Start
```bash
cd research-agent
python research_agent.py "Your research topic"
```

**Features:**
- Web search and content scraping
- AI-powered synthesis with Claude
- Automatic report generation
- Source citations
- Saves to knowledge base

See [research-agent/README.md](research-agent/README.md) for details.
