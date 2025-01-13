#!/usr/bin/env python3
import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

def main():
    changed_files_raw = os.getenv("CHANGED_FILES", "").strip()
    if not changed_files_raw:
        print("No changed files detected.")
        return

    # For simplicity, assume only 1 changed file or 
    # handle them all in a single combined prompt.
    changed_files = changed_files_raw.split()
    print(f"Changed files: {changed_files}")

    # Example prompt:
    prompt = f"""
    Please read the content of the changed files (list: {changed_files})
    and generate a short summary or comment. 
    We are demonstrating GPT-4-based processing here.
    """

    # Prepare the content. In a real scenario, you'd read the file content
    # and feed it into the prompt. For demonstration, we'll keep it simpler.
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    # Call GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    gpt_output = response["choices"][0]["message"]["content"]

    # Write GPT output to a file
    output_path = "GPT_SUMMARY.md"
    with open(output_path, "w") as f:
        f.write("# GPT-4 Summary\n\n")
        f.write(gpt_output.strip())

    print(f"GPT output written to {output_path}")

if __name__ == "__main__":
    main()
