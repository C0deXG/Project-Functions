from openai import OpenAI
import json
import os
import time

# === Settings ===
API_KEY = "openai_api_key"
MODEL = "o4-mini-2025-04-16"
OUTPUT_FILE = "tasks.json"
MAX_TASKS = 1000  # stop when this many unique tasks exist

# === Initialize OpenAI client ===
client = OpenAI(api_key=API_KEY)

# === Ensure the file exists ===
if not os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "w") as f:
        json.dump([], f)

# === Loop until we reach max tasks ===
while True:
    with open(OUTPUT_FILE, "r") as f:
        existing_tasks = json.load(f)
        existing_names = {task["task"].lower().strip() for task in existing_tasks}

    if len(existing_tasks) >= MAX_TASKS:
        print(f"🎯 Goal reached: {len(existing_tasks)} unique tasks in {OUTPUT_FILE}")
        break

    # Build exclusion list
    exclusion_list = "\n".join(f"- {task['task']}" for task in existing_tasks)

    # Messages to instruct the model
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant generating simple Python programming tasks for beginners. "
                "Each task must follow this format exactly:\n\n"
                "Task: [Short Task Name]\nInput: [Describe the input type(s)]\nOutput: [Describe the output]\n\n"
                "Tasks must be easy and practical — like basic math, string manipulation, lists, loops, etc."
            )
        },
        {
            "role": "user",
            "content": (
                f"The following tasks have already been used:\n{exclusion_list}\n\n"
                "Now generate 10 completely new and unique programming tasks. "
                "Avoid any task with the same purpose as above, even if the wording is different. "
                "Use the format strictly: Task / Input / Output. Don't add explanation or notes."
            )
        }
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        raw_text = response.choices[0].message.content
        print("🆕 Generated:\n", raw_text, "\n")

        # Parse tasks
        new_tasks = []
        for block in raw_text.strip().split("Task: ")[1:]:
            lines = block.strip().split("\n")
            try:
                name = lines[0].strip()
                input_ = lines[1].replace("Input:", "").strip()
                output = lines[2].replace("Output:", "").strip()
                if name.lower() not in existing_names:
                    new_tasks.append({
                        "task": name,
                        "input": input_,
                        "output": output
                    })
            except (IndexError, ValueError):
                continue

        # Save new tasks
        if new_tasks:
            with open(OUTPUT_FILE, "r+") as f:
                data = json.load(f)
                data.extend(new_tasks)
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()

            print(f"✅ Added {len(new_tasks)} new tasks. Total now: {len(existing_tasks) + len(new_tasks)}\n")
        else:
            print("⚠️ No new unique tasks detected. Retrying...\n")

        time.sleep(2)  # polite delay to avoid overloading the API

    except Exception as e:
        print("❌ Error:", str(e))
        break
