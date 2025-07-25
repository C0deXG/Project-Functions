# generate_tasks_to_json.py

This script uses OpenAI to generate new, unique beginner-friendly programming tasks and appends them to `tasks.json`.

## Purpose
- Expands the dataset of programming tasks for function synthesis and diversity analysis.

## How it Works
- Reads existing tasks from `tasks.json`.
- Prompts OpenAI to generate 10 new tasks at a time, avoiding duplicates.
- Each task includes a name, input description, and output description.
- Appends new tasks to `tasks.json`.
- Stops when a set maximum number of unique tasks is reached.

## Usage
```bash
python generate_tasks_to_json.py
```

## Notes
- Requires a valid OpenAI API key (should be set via environment variable or .env file).
- Do not commit API keys to version control. 