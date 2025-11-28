# 🌱 Sprout

An AI-powered CLI tool that helps your commits grow! Analyzes git history and generates intelligent commit messages, PR descriptions, and code insights.

## Features (Planned)

- 🤖 AI-generated commit messages from git diff
- 🔍 Find similar past changes using RAG
- 📝 Automatic PR descriptions with context
- 👥 Smart reviewer suggestions
- 🚨 Code smell detection

## Tech Stack

- **LLM**: Groq API with Llama 3.1 70B
- **Vector DB**: ChromaDB for embeddings
- **Code Parser**: Tree-sitter
- **CLI**: Python with Rich and Click

## Setup

1. Clone this repository
2. Create virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Add Groq API key to `.env` file

## Usage (Coming Soon!)
```bash
sprout commit          # Generate commit message
sprout similar         # Find similar past changes
sprout pr              # Generate PR description
sprout review          # Suggest reviewers
```

## Development Status

🌱 **Phase 1**: Basic commit message generation (In Progress)

## Project Structure
```
sprout/
├── src/
│   ├── core/          # Main business logic
│   └── utils/         # Helper functions
├── tests/             # Unit tests
├── docs/              # Documentation
└── README.md
```

Made with Love by Akchhya