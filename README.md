# Generating Diverse Python Function Implementations for the Same Task Using AI and Program Synthesis

## Overview
This project leverages Large Language Models (LLMs) and program synthesis to generate multiple, diverse Python function implementations for the same programming task. The goal is to produce not only correct but also stylistically and algorithmically diverse solutions for each task, enabling applications in pedagogy, code obfuscation, optimization, robustness, and LLM evaluation.

## Key Features
- **Task Dataset**: 600+ beginner-friendly programming tasks (e.g., GCD, CSV parsing, password generation).
- **Function Generation**: Uses GPT models to generate 2–5 unique implementations per task.
- **Automated Testing**: Unit tests for correctness, edge cases, and performance.
- **Diversity Analysis**: Compares implementations using AST, token, and algorithmic metrics.
- **Evaluation**: Cross-model verification and reporting.

## Applications
- **Teaching**: Showcases multiple ways to solve the same problem.
- **Security**: Diverse code makes reverse-engineering harder.
- **Optimization**: Enables selection of the most efficient solution.
- **Robustness**: Multiple implementations increase reliability.
- **LLM Evaluation**: Tests AI's ability to generate diverse, correct code.

---

## Project Workflow
1. **Task Generation**: `generate_tasks_to_json.py` uses OpenAI to create new programming tasks and saves them to `tasks.json`.
2. **Function Synthesis**: `function-reqest.py` (typo: should be `function-request.py`) uses GPT-4o to generate a Python function for each task in `tasks.json`, saving results to `functions.json`.
3. **Alternative Solution Generation**: `add_code_2_to_functions.py` generates a second, stylistically different implementation (`code_2`) for each function using OpenAI, updating `functions.json`.
4. **Testing**: `test_functions.py` generates test cases, runs both implementations, and validates outputs, saving results to `arguments.json`.
5. **Reporting**: Results and statistics are summarized in `code_2_testing_report.md`.

---

## File-by-File Documentation

### Data Files
- **tasks.json**: List of programming tasks with input/output specs.
- **functions.json**: Main dataset; for each task, stores the function name, `code_1` (original), and `code_2` (alternative) implementations.
- **arguments.json**: Stores generated test cases and results for each function (auto-generated; ignored by git).

### Scripts
- **generate_tasks_to_json.py**: Uses OpenAI to generate new, unique programming tasks and appends them to `tasks.json`.
- **function-reqest.py**: For each task in `tasks.json`, generates a Python function using GPT-4o and saves it to `functions.json`.
- **add_code_2_to_functions.py**: For each function in `functions.json` missing a `code_2`, generates a diverse alternative implementation using OpenAI.
- **test_functions.py**: Generates test cases, runs both implementations, and validates outputs, saving results to `arguments.json`.
- **code_2_testing_report.md**: Project report and summary of the testing process and results.

### Other
- **requirements.txt**: Python dependencies for all scripts.
- **.gitignore**: Excludes sensitive/generated files and local folders from git.

### Extra (Unrelated)
- **None-Projec/generate_session.py**: Telegram/Docx scraping utility. Not part of the main workflow.

---

## Setup & Installation
1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up API keys**:
   - Create a `.env` file or export your OpenAI and Google API keys as environment variables.
   - Remove hardcoded keys from scripts before pushing to GitHub!

---

## Usage
- **Generate tasks**:
  ```bash
  python generate_tasks_to_json.py
  ```
- **Generate function implementations**:
  ```bash
  python function-reqest.py
  ```
- **Generate alternative solutions**:
  ```bash
  python add_code_2_to_functions.py
  ```
- **Test all functions**:
  ```bash
  python test_functions.py
  ```

---

## Results & Findings
- 92% of GPT-generated functions passed all unit tests.
- Diversity saturates after 3–4 solutions per task.
- Gemini model struggled with structured output.
- Confirmed applications in teaching, code generation, and optimization.

---

## Notes & Recommendations
- **Security**: Never commit API keys. Use `.env` and `.gitignore`.
- **Data files**: `arguments.json` and `functions.json` are large and auto-generated; do not version control.
- **Unrelated scripts**: `None-Projec/generate_session.py` is not part of the main workflow.
