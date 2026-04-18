# 📚 AI Library Management System
A lightweight Flask + Vanilla JS library manager with AI recommendations powered by Ollama (Llama 3.1).

## 🚀 Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Start Ollama: `OLLAMA_ORIGINS="*" ollama serve`
3. Pull model: `ollama pull llama3.1`
4. Run backend: `python server.py`
5. Open `index.html` in your browser.

## 📁 Dataset
Place your CSV in the root as `BooksDatasetClean.csv` with columns:
`Title, Authors, Description, Category, Publisher, Publish Date (Month), Publish Date (Year), quantity_available`