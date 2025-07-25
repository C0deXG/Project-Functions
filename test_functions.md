# test_functions.py

This script tests both the original (`code_1`) and alternative (`code_2`) implementations for each task in `functions.json`.

## Purpose
- Ensures correctness and consistency of all generated functions.
- Provides automated, model-assisted test case generation and validation.

## How it Works
- For each task, generates test cases using Gemini (Google Generative AI).
- Dynamically executes both `code_1` and `code_2` on each test case.
- Compares outputs to expected results and records pass/fail status.
- Saves all test results to `arguments.json` for later analysis.

## Usage
```bash
python test_functions.py
```

## Notes
- Requires a valid Google Generative AI API key (should be set via environment variable or .env file).
- Do not commit API keys to version control. 