#!/usr/bin/env python3
import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

def main():
    changed_files_raw = os.getenv("CHANGED_FILES", "").strip()
    if not changed_files_raw:
        print("No changed files detected.")
        return

    changed_files = changed_files_raw.split()
    print(f"Changed files: {changed_files}")

    # Example prompt
    prompt = f"Summarize the changes in the files: {changed_files}"

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    gpt_output = response["choices"][0]["message"]["content"]

    output_path = "GPT_SUMMARY.md"
    with open(output_path, "w") as f:
        f.write("# GPT-4 Summary\n\n")
        f.write(gpt_output.strip())

    print(f"GPT output written to {output_path}")

if __name__ == "__main__":
    main()
