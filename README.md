# 🚀 Multi-Agent Research System

<p align="center">
  <img src="assets/banner.png" alt="Multi Agent Research System Banner" width="100%">
</p>

<p align="center">
  <strong>An AI-powered Multi-Agent Research System built with LangChain, LangGraph, OpenAI, Tavily Search, and BeautifulSoup.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/OpenAI-GPT-green?style=for-the-badge&logo=openai">
  <img src="https://img.shields.io/badge/LangChain-LCEL-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/LangGraph-Multi--Agent-purple?style=for-the-badge">
</p>

---

## 🌟 Overview

This project is a **production-ready Multi-Agent Research System** designed to perform deep web research using multiple AI agents working collaboratively.

Instead of relying on a single LLM call, the system creates specialized agents that:

🔍 Search the web using Tavily

🌐 Extract and clean web content using BeautifulSoup

🧠 Analyze information with OpenAI models

📑 Generate structured research reports

🔄 Coordinate through ReAct reasoning and LangGraph workflows

⚡ Execute efficiently using LCEL Runnable pipelines

---

## 🏗️ Architecture

<p align="center">
  <img src="assets/architecture.png" alt="Architecture Diagram" width="900">
</p>

### Agent Workflow

User Query
↓
Research Agent
↓
Tavily Search Tool
↓
Web Scraper Agent
↓
BeautifulSoup Extraction
↓
Analysis Agent
↓
Report Generator
↓
Final Research Report

---

## ✨ Features

### 🤖 Multi-Agent Collaboration

* Research Agent
* Web Scraping Agent
* Analysis Agent
* Report Generation Agent

### 🔍 Advanced Search

* Tavily Search Integration
* Real-time Web Research
* Multi-source Information Gathering

### 🌐 Intelligent Web Scraping

* BeautifulSoup Extraction
* HTML Cleaning
* Content Processing

### 🧠 AI-Powered Analysis

* OpenAI GPT Models
* ReAct Reasoning
* Structured Research Output

### ⚡ Modern LangChain Stack

* LangChain
* LangGraph
* LCEL Pipelines
* Runnable Architecture

---

## 🛠️ Tech Stack

| Technology    | Purpose             |
| ------------- | ------------------- |
| Python        | Core Development    |
| OpenAI API    | LLM Intelligence    |
| LangChain     | Agent Framework     |
| LangGraph     | Agent Orchestration |
| Tavily        | Web Search          |
| BeautifulSoup | Web Scraping        |
| Pydantic      | Structured Outputs  |

---

## 📂 Project Structure

```bash
multi-agent-research/
│
├── agents.py
│   
├── tools.py
│   
├── pipeline.py
│   
├── tools.py
│
├── requirements.txt
├── .env
└── app.py
```

---

## 🚀 Getting Started

### Clone Repository

```bash
git clone https://github.com/your-username/multi-agent-research.git

cd multi-agent-research
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

```env
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

### Run Project

```bash
python main.py
```

---

## 📊 Example Output

```text
Query:
"Latest developments in AI Agents"

Research Agent:
✓ Search completed

Scraper Agent:
✓ Extracted 12 sources

Analysis Agent:
✓ Generated insights

Report Agent:
✓ Created final report

Status: SUCCESS
```

---

## 🎯 Future Improvements

* Memory-enabled agents
* Vector Database Integration
* RAG Pipelines
* Multi-Modal Research
* PDF Report Generation
* Agent Performance Monitoring
* Streamlit Dashboard

---

## 🤝 Contributing

Contributions are welcome!

If you'd like to improve this project, feel free to fork the repository and submit a pull request.

---

## ⭐ Support

If you found this project useful:

🌟 Star the repository

🍴 Fork the project

📢 Share it with others

---

<p align="center">
  Built with ❤️ using OpenAI, LangChain, LangGraph, Tavily, and Python.
</p>
