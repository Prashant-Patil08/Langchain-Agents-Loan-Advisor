# Loan Advisor Agent Learning Lab

## Overview
A practical LangChain agent learning project with Streamlit UI.

## Features
- Tool calling
- Agent loop
- Structured output
- Thread memory
- Middleware
- Gemini model integration

## Concepts Covered
- Loop understanding
- Structured output
- Context engineering
- Memory and thread state
- Middleware

## Run
streamlit run app.py

## Screenshot
![Loan-Advisor-Agent](D:\Langchain-Agents\assets\image.png)

A clean, VS Code friendly LangChain learning project that teaches the most important agent concepts in one place:

- Agent loop
- Tools
- Structured output
- Memory and thread state
- Middleware
- Streamlit UI

This project **does not include RAG** on purpose. The goal is to help you learn agent fundamentals before adding retrieval or moving to LangGraph.

---

## What you will learn

### 1. Agent loop
The agent receives a user message, decides which tool to call, sees the tool result, and keeps looping until it can finish.

### 2. Tools
This project includes:
- EMI calculator
- affordability checker
- loan comparison
- max safe loan estimator
- interest-rate hint tool

### 3. Structured output
The final answer is returned as a validated schema, not messy text.

### 4. Memory and thread state
The app uses `InMemorySaver` and a `thread_id` so follow-up questions work naturally inside the same session.

### 5. Middleware
The app uses custom middleware for:
- console logging
- tool selection based on the latest user question

### 6. Basic UI
A Streamlit chat interface makes the project easy to run and inspect.

---

## Project structure

```text
loan_agent_learning_project/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── .streamlit/
│   └── config.toml
├── .vscode/
│   └── launch.json
│
└── src/
    ├── __init__.py
    ├── agent.py
    ├── config.py
    ├── finance.py
    ├── model.py
    ├── service.py
    ├── utils.py
    ├── middleware/
    │   ├── __init__.py
    │   ├── logging_middleware.py
    │   └── tool_selector.py
    ├── schemas/
    │   ├── __init__.py
    │   └── recommendation.py
    └── tools/
        ├── __init__.py
        └── loan_tools.py
```

---

## Setup

### 1. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add environment variables

Create a `.env` file from `.env.example`.

```bash
copy .env.example .env
```

Update `.env`:

```env
GOOGLE_API_KEY=your_google_api_key_here
MODEL_NAME=gemini-2.5-flash
APP_TITLE=Loan Advisor Agent Learning Lab
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## How to use it

Try this learning flow in one chat session:

1. `My salary is 80000`
2. `Existing EMI is 12000`
3. `Can I afford a 20 lakh loan at 9% for 20 years?`
4. `Compare 20 lakh at 9% for 10 years vs 20 years`
5. `What is a safe loan amount for me at 9% for 20 years?`

This sequence helps you observe memory, structured output, and tool use.

---

## What to observe while learning

### Agent loop
Watch your terminal output. Middleware logs each model call and tool call.

### Memory
Use the same session and ask follow-up questions. Then click **Start new learning session** to create a new `thread_id` and notice how memory resets.

### Structured output
The UI renders a clean result with:
- summary
- affordability status
- risk level
- recommended action
- reasons
- follow-up questions

### Middleware
Notice that the tool selector tries to reduce tool confusion by exposing a smaller relevant set of tools based on the latest question.

---

## Key files explained

### `src/agent.py`
Builds the agent with:
- Gemini model
- LangChain tools
- structured output schema
- memory checkpointer
- middleware

### `src/tools/loan_tools.py`
Defines the business tools used by the agent.

### `src/finance.py`
Contains deterministic financial logic. This is important because numeric business logic should live in tools or utility functions, not in the model.

### `src/middleware/logging_middleware.py`
Logs model and tool calls to the terminal so you can see the runtime behavior.

### `src/middleware/tool_selector.py`
Shows a practical context-engineering idea: only expose a smaller relevant tool subset for the current question.

### `src/schemas/recommendation.py`
Defines the structured response schema returned by the agent.

---

## Recommended experiments

### Experiment 1: remove memory
Comment out `checkpointer=InMemorySaver()` and test follow-up questions again.

### Experiment 2: remove middleware
Comment out the middleware list and observe the difference in logs and tool selection.

### Experiment 3: remove structured output
Comment out `response_format=LoanAdvice` and observe how messy the final response becomes.

### Experiment 4: weaken tool descriptions
Change the tool docstrings to vague names and see how tool choice becomes worse.

These four experiments will teach you more than reading theory alone.

---

## How to upload to GitHub

```bash
git init
git add .
git commit -m "Initial loan advisor agent learning project"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

---

## Good next step after this project

After you understand this project deeply, the next upgrade path is:

1. Add retrieval as a tool
2. Add direct routing for document questions vs reasoning questions
3. Add persistent checkpointer
4. Move the orchestration into LangGraph

That path will feel natural once you fully understand the current project.
