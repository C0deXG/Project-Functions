# function-reqest.py

This script uses GPT-4o to generate a Python function implementation for each task in `tasks.json` and saves the results to `functions.json`.

## Purpose
- Automates the process of turning task descriptions into working Python functions.

## How it Works
- Reads all tasks from `tasks.json`.
- For each task not already in `functions.json`, prompts GPT-4o to generate a function.
- Saves each function (with its name and code) to `functions.json`.
- Uses asyncio and aiofiles for efficient, concurrent API calls and file writes.

## Usage
```bash
python function-reqest.py
```

## Notes
- Requires a valid OpenAI API key (should be set via environment variable or .env file).
- Do not commit API keys to version control. 