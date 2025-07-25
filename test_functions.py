import json
import google.generativeai as genai
import re
import os
import time

# Setup Gemini
genai.configure(api_key="AIzaSyB-IfzI3HDmpcdrHiR3S3hMfwCAW4TvhqI")
model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite	")

# Load functions.json
with open("functions.json", "r") as f:
    functions = json.load(f)

# Load or initialize arguments.json
all_arguments = {}
if os.path.exists("arguments.json"):
    try:
        with open("arguments.json", "r") as f:
            all_arguments = json.load(f)
    except json.JSONDecodeError:
        print("⚠️  WARNING: arguments.json is corrupted. Starting fresh.")

# === Helpers ===

def generate_test_cases(task, code):
    prompt = f"""You are a Python tester.

Task: {task}

Function:
{code}

Generate 3 valid test cases in this format:
[
  {{ "inputs": [...], "expected": ... }},
  ...
]
Return only the JSON array.
"""
    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = re.sub(r"^```json|^```|```$", "", raw.strip(), flags=re.MULTILINE).strip()
        return json.loads(raw)
    except Exception as e:
        print(f"Parsing failed or quota hit. Error: {e}")
        print("Raw response:\n", response.text if 'response' in locals() else "")
        return []

def run_function(code: str, function_name: str, inputs):
    try:
        context = {}
        exec(code, context)
        func = context[function_name]
        return func(*inputs)
    except Exception as e:
        return f"ERROR: {str(e)}"

def normalize(val, expected_type=None):
    try:
        if isinstance(val, str) and expected_type in [complex, list, tuple] and "j" in val:
            return complex(val)
    except:
        pass

    if isinstance(val, complex):
        return {"real": round(val.real, 5), "imag": round(val.imag, 5)}

    if isinstance(val, (list, tuple)):
        return [normalize(v) for v in val]

    if isinstance(val, dict) and "real" in val and "imag" in val:
        return {"real": round(val["real"], 5), "imag": round(val["imag"], 5)}

    if isinstance(val, float):
        return round(val, 5)

    if isinstance(val, str) and expected_type == int:
        return len(val)

    return val

def safe_json(obj):
    if isinstance(obj, complex):
        return {"real": obj.real, "imag": obj.imag}
    if isinstance(obj, set):
        return list(obj)
    return str(obj)

# === Resume point ===
start_task = "Quadratic Equation Solver"
found_start = False

# === Main Loop ===
for entry in functions:
    task = entry["task"]
    name = entry["function_name"]
    code1 = entry["code_1"]
    code2 = entry["code_2"]

    if not found_start:
        if task == start_task:
            found_start = True
        else:
            continue

    print(f"\n=== Task: {task} ===")

    test_cases = generate_test_cases(task, code1)
    if not test_cases:
        continue  # skip if failed

    all_arguments[task] = []

    for i, case in enumerate(test_cases):
        inputs = case["inputs"]
        expected = case["expected"]

        result1 = run_function(code1, name, inputs)
        result2 = run_function(code2, name, inputs)

        passed1 = normalize(result1, type(expected)) == normalize(expected)
        passed2 = normalize(result2, type(expected)) == normalize(expected)

        status1 = "-OK" if passed1 else f"❌ Got {result1}"
        status2 = "-Ok" if passed2 else f"❌ Got {result2}"

        print(f"Test Case {i+1}: Inputs={inputs}, Expected={expected}")
        print(f" - code_1: {status1}")
        print(f" - code_2: {status2}")

        all_arguments[task].append({
            "inputs": inputs,
            "expected": expected,
            "code_1_result": result1,
            "code_1_pass": passed1,
            "code_2_result": result2,
            "code_2_pass": passed2
        })

        # Save after every test case
        with open("arguments.json", "w") as f:
            json.dump(all_arguments, f, indent=2, default=safe_json)
