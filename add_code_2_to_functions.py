import json
import time
import os
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

MODEL = "o4-mini-2025-04-16"
JSON_FILE = "functions.json"
MAX_WORKERS = 10  # Tune this based on your API rate limits

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_code_2(task, code_1, function_name, input_desc, output_desc):
    prompt = f"""
You are a Python expert. Given the following function, write a new function with the SAME signature and behavior, but using a DIFFERENT approach or style. Do NOT copy or trivially reformat the code. Use a different algorithm, built-in, or style. The function must be named {function_name} and match the input/output described.

Task: {task}
Input: {input_desc}
Output: {output_desc}

# Original implementation:
{code_1}

# Respond ONLY in this JSON format (no explanation):
{{
  \"code_2\": \"<your new function code here, as a Python function>\"
}}
"""
    messages = [
        {"role": "system", "content": "You are a Python expert generating alternative function implementations."},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    content = response.choices[0].message.content.strip()
    try:
        if content.startswith("```json"):
            content = content.split("```json", 1)[1].split("```", 1)[0].strip()
        elif content.startswith("```"):
            content = content.split("```", 1)[1].split("```", 1)[0].strip()
        code_json = json.loads(content)
        code_2 = code_json["code_2"]
    except Exception as e:
        print("⚠️ Could not parse JSON, using raw content. Error:", e)
        code_2 = content
    return code_2

def update_json_file(tasks):
    with open(JSON_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def process_task(idx, task):
    code_2 = get_code_2(
        task=task["task"],
        code_1=task["code_1"],
        function_name=task["function_name"],
        input_desc=task["input"],
        output_desc=task["output"]
    )
    return idx, code_2

def main():
    with open(JSON_FILE, "r") as f:
        tasks = json.load(f)
    # Find indices of tasks missing code_2
    to_update = [(i, task) for i, task in enumerate(tasks) if "code_1" in task and "code_2" not in task]
    if not to_update:
        print("No tasks needed updating.")
        return
    print(f"Processing {len(to_update)} tasks needing code_2...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_task, idx, task): idx for idx, task in to_update}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Generating code_2"):
            idx, code_2 = future.result()
            tasks[idx]["code_2"] = code_2
            update_json_file(tasks)  # Write after each update for crash safety
            time.sleep(0.5)  # Polite delay to avoid hammering the API
    print("✅ Updated functions.json with code_2 for missing tasks.")

if __name__ == "__main__":
    main() 