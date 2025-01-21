#!/usr/bin/env python3
import os
import openai
import pathlib


openai.api_key = os.environ["OPENAI_API_KEY"]

def main():
    changed_files_raw = os.getenv("CHANGED_FILES", "").strip()
    if not changed_files_raw:
        print("No changed files detected.")
        return
    changed_files = changed_files_raw.split()
    for changed_file in changed_files:
        if not changed_file.endswith(".py"):
            continue
        doc_path = docs_path_for(changed_file)
        code_content = read_file(changed_file)

        if not os.path.exists(doc_path):
            doc_content = generate_new_doc(changed_file, code_content)
            write_file(doc_path, doc_content)
            print(f"Created docs for {changed_file} at {doc_path}")
        else:
            existing_doc = read_file(doc_path)
            updated_doc = update_existing_doc(changed_file, code_content, existing_doc)
            write_file(doc_path, updated_doc)
            print(f"Updated docs for {changed_file} at {doc_path}")

def docs_path_for(changed_file):

    p = pathlib.Path(changed_file)
    return str(pathlib.Path("docs") / p.with_suffix(".md"))

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_new_doc(filename, code_content):
    prompt = f"""
You are an AI that writes architecture documentation for code.
The code file is {filename}.

TASK:
1. Summarize what the file does.
2. List the key classes, functions, or methods, including parameters.
3. Provide a standard 'Architecture Overview' section at the top, then a 'Detailed Explanation' section.
4. Write in Markdown format.

Here is the code:
\"\"\"
{code_content}
\"\"\"
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    doc_text = response["choices"][0]["message"]["content"]
    return doc_text

def update_existing_doc(filename, code_content, existing_doc):
    prompt = f"""
We have an existing Markdown doc for the file '{filename}'. Here it is:

Existing Doc:
\"\"\"
{existing_doc}
\"\"\"

The code has been updated. Here's the new code:
\"\"\"
{code_content}
\"\"\"

TASK:
1. Update or refine the existing doc to reflect any new or changed classes, functions, or logic.
2. At the top, provide a short "Change summary" that describes what's new/changed.
3. Keep the same general format (Markdown).
4. Remove anything that is no longer valid, add details for anything new.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    updated_text = response["choices"][0]["message"]["content"]
    return updated_text

if __name__ == "__main__":
    main()
