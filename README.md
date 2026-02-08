# 🧹 AI Data Cleaning

> A multi-agent system that cleans dirty datasets automatically using Groq's high-speed inference.

## 🚀 Overview

Data cleaning is the most time-consuming part of Data Science. **AI Data Cleaning** automates this process using a **Manager-Worker Agent Architecture**.

Instead of hardcoded rules, this system uses Large Language Models (LLMs) to intelligently analyze your specific dataset, plan a cleaning strategy, and write/execute Python code to fix issues like missing values, inconsistent formats, and outliers.

## ✨ Key Features

* **🤖 Multi-Agent Orchestration:**
    * **Manager Agent:** Analyzes the dataset schema and creates a strategic, step-by-step cleaning plan.
    * **Worker Agent:** Writes, executes, and verifies Python code for each step.
* **❤️‍🩹 Self-validating Code Execution:** If the Worker's code fails (e.g., syntax error or data type mismatch), it automatically analyzes the error, rewrites the code, and retries until successful.
* **⚡ Powered by Groq:** Uses Llama 3 models on Groq LPUs for near-instant analysis and code generation.
* **🔒 Sandboxed Execution:** Code is executed in a controlled local environment to ensure state persistence across steps.
* **📂 Dynamic Adaptability:** Works on *any* dataset (Finance, Healthcare, E-commerce) by dynamically generating logic based on the data provided.

## 📂 Project Structure

```text
ai_data_cleaner/
├── agents/                  # The Agent Brains
│   ├── __init__.py
│   ├── manager.py           # Planner: Analyzes data & generates tasks
│   └── worker.py            # Executor: Writes & runs Python code
├── app.py                   # Main Streamlit Application (UI)
├── requirements.txt         # Python Dependencies
├── .env                     # API Keys configuration
└── README.md                # Documentation

Installation & Setup
1. Clone the Repository

``` git clone [https://github.com/yourusername/ai-data-cleaning-swarm.git](https://github.com/yourusername/ai-data-cleaning-swarm.git)
cd ai-data-cleaning-swarm```

2. Create a Virtual Environment

``` python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate```

3. Install Dependencies

``` pip install -r requirements.txt ```

4. Configuration
You will need a Groq API Key. Enter it in the Streamlit Sidebar when running the app:

Usage

1. Run the Application:

``` streamlit run app.py ```

2. Workflow:

  Upload: Drag and drop your messy CSV or Excel file.
  Plan: Click "Analyze & Plan Strategy". The Manager Agent will inspect your data and list the necessary cleaning steps.
  Execute: Click "Execute". Watch as the Worker Agent picks up each task, writes the code, and applies it to your data in real-time.
  Download: Once finished, download your perfectly cleaned dataset.

How It Works (The Architecture)

  Ingestion: The app loads your file into a Pandas DataFrame.
  The Manager: We feed the dataframe schema (column names, types, non-null counts) to the Manager Agent. It returns a structured JSON plan (e.g., 1. Drop nulls in 'Age', 2. Standardize 'Date' column).
  The Loop: The app iterates through this plan.
  The Worker: For each step, the Worker Agent receives the current state of the dataframe and the instruction. It generates Python code.
  Execution & Self-Correction: The code is executed. If a Python error occurs, the system captures the traceback, feeds it back to the Worker, and requests a fix immediately.

Future Roadmap

  Guardrails Integration: Implementing strict output validation to prevent hallucinations.
  LangGraph Orchestration: Moving to a graph-based state machine for more complex non-linear workflows.
  Data Quality Report: Generating a PDF report showing "Before vs After" statistics.

