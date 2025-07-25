import json
import os
import asyncio
from openai import AsyncOpenAI
import aiofiles

openai.api_key = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key="openai_api_key")

functions_file = "functions.json"


if not os.path.exists(functions_file):
    with open(functions_file, "w") as f:
        json.dump([], f)


try:
    with open(functions_file, "r") as f:
        functions = json.load(f)
except json.JSONDecodeError:
    functions = []

existing_task_names = {func["task"] for func in functions}

# load tasks here
with open("tasks.json", "r") as f:
    tasks = json.load(f)

tasks_to_process = [task for task in tasks if task["task"] not in existing_task_names]

semaphore = asyncio.Semaphore(5)
lock = asyncio.Lock()

async def save_function(function_entry):
    async with lock:
        try:
            async with aiofiles.open(functions_file, "r+") as f:
                try:
                    f_data = await f.read()
                    data = json.loads(f_data) if f_data else []
                except Exception:
                    data = []

                data.append(function_entry)
                await f.seek(0)
                await f.write(json.dumps(data, indent=2))
                await f.truncate()
        except Exception as e:
            print(f"Error saving function for task: {function_entry['task']}\n{e}")

async def generate_function(task):
    async with semaphore:
        prompt = (
            f"Task: {task['task']}\n"
            f"Input: {task['input']}\n"
            f"Output: {task['output']}\n\n"
            "Write a Python function that accomplishes this task. "
            "Return ONLY valid JSON in this format:\n"
            "{\n"
            '  "function_name": "your_function_name",\n'
            '  "code": "def your_function(...):\\n    # Your code here"\n'
            "}"
        )

        try:
            response = await client.chat.completions.create(
                model="o4-mini-2025-04-16",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes Python functions and responds only in JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            function_data = json.loads(content)

            function_entry = {
                "task": task["task"],
                "input": task["input"],
                "output": task["output"],
                "function_name": function_data["function_name"],
                "code": function_data["code"]
            }

            await save_function(function_entry)

            print(f"Saved function for task: {task['task']}")

        except Exception as e:
            print(f"Error generating function for task: {task['task']}\n{e}")

async def main():
    await asyncio.gather(*(generate_function(task) for task in tasks_to_process))

if __name__ == "__main__":
    asyncio.run(main())
