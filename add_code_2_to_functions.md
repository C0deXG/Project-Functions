# add_code_2_to_functions.py

This script generates a second, stylistically different implementation (`code_2`) for each programming task in `functions.json` using OpenAI's API.

## Purpose
- Ensures each task has at least two diverse solutions: the original (`code_1`) and an alternative (`code_2`).
- Promotes code diversity for pedagogy, robustness, and LLM evaluation.

## How it Works
- Reads `functions.json` and finds tasks missing `code_2`.
- For each, prompts OpenAI to generate a new function with the same signature and behavior but a different algorithm or style.
- Updates `functions.json` after each new solution for crash safety.
- Uses multithreading for speed and politeness delays to respect API rate limits.

## Usage
```bash
python add_code_2_to_functions.py
```

## Notes
- Requires a valid OpenAI API key (should be set via environment variable or .env file).
- Do not commit API keys to version control. 