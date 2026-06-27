# 🤖 Multi-Agent AI System — Claude API

> A multi-agent AI system where specialized Claude agents collaborate to answer complex questions through task decomposition, research, analysis, and synthesis.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude%20API-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 Overview

This project implements a **multi-agent AI pipeline** using the Anthropic Claude API. Instead of a single AI answering everything, four specialized agents collaborate:

```
User Question
     │
     ▼
┌─────────────────┐
│  Coordinator    │  ← Breaks question into subtasks
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌─────────┐
│Research│ │Analyst  │  ← Specialist agents work in parallel
└────┬───┘ └────┬────┘
     │           │
     └─────┬─────┘
           ▼
      ┌─────────┐
      │ Writer  │  ← Synthesizes final answer
      └─────────┘
           │
           ▼
    Final Answer
```

---

## 🧠 Agents

| Agent | Role |
|---|---|
| **Coordinator** | Analyzes the question and creates a plan with subtasks |
| **Researcher** | Gathers relevant facts and background information |
| **Analyst** | Identifies patterns, evaluates trade-offs, draws insights |
| **Writer** | Synthesizes everything into a clear final answer |

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/janachamma/multi-agent-claude.git
cd multi-agent-claude
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Anthropic API key
```bash
# Windows
set ANTHROPIC_API_KEY=your-api-key-here

# Mac/Linux
export ANTHROPIC_API_KEY=your-api-key-here
```

### 4. Run the system
```bash
python agents.py
```

### 5. Ask a question!
```
💬 Your question: What are the key challenges in deploying AI on edge devices?

📋 STEP 1: Coordinator analyzing question...
🤖 [Researcher Agent] Working on: Gather facts about edge AI deployment...
🤖 [Analyst Agent] Working on: Analyze challenges and trade-offs...
✍️  STEP 3: Writer synthesizing final answer...

📊 FINAL ANSWER
...comprehensive answer from all 3 agents...
⏱️  Completed in 12 seconds by 3 agents
```

---

## 📁 Project Structure

```
multi-agent-claude/
├── agents.py              # Main multi-agent pipeline
├── requirements.txt       # Dependencies
├── conversation_log.json  # Auto-generated conversation history
└── README.md             # This file
```

---

## 💡 Key Concepts Demonstrated

- **Task Decomposition** — Breaking complex questions into manageable subtasks
- **Agent Specialization** — Each agent has a specific role and system prompt
- **Context Propagation** — Agents build on each other's outputs
- **Agentic Workflows** — Autonomous multi-step reasoning pipeline
- **Prompt Engineering** — Carefully crafted system prompts per agent
- **JSON-structured outputs** — Coordinator returns structured task plans

---

## 🔧 Customization

You can easily add new agents by adding to the `AGENTS` dictionary:

```python
AGENTS["fact_checker"] = {
    "name": "Fact Checker Agent",
    "role": "Verify claims and flag potential inaccuracies.",
    "system": "You are a Fact Checker Agent. Your job is to..."
}
```

---

## 👩‍💻 Author

**Jana Chamma**  
AI/ML Engineer | LLM Systems | Computer Vision  
[LinkedIn](https://www.linkedin.com/in/jana-chamma-26b7212b3/) | [Portfolio](https://janachamma.github.io/)

---

## 📄 License

MIT License — feel free to use and adapt.
