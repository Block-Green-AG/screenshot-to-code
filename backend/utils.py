import copy
import json
import os
from datetime import datetime


def pprint_prompt(prompt_messages):
    print(json.dumps(truncate_data_strings(prompt_messages), indent=4))


def truncate_data_strings(data):
    # Deep clone the data to avoid modifying the original object
    cloned_data = copy.deepcopy(data)

    if isinstance(cloned_data, dict):
        for key, value in cloned_data.items():
            # Recursively call the function if the value is a dictionary or a list
            if isinstance(value, (dict, list)):
                cloned_data[key] = truncate_data_strings(value)
            # Truncate the string if it it's long and add ellipsis and length
            elif isinstance(value, str):
                cloned_data[key] = value[:40]
                if len(value) > 40:
                    cloned_data[key] += "..." + f" ({len(value)} chars)"

    elif isinstance(cloned_data, list):
        # Process each item in the list
        cloned_data = [truncate_data_strings(item) for item in cloned_data]

    return cloned_data



def write_logs(prompt_messages, completion):
    # Get the logs path from environment, default to the current working directory
    logs_path = os.environ.get("LOGS_PATH", os.getcwd())

    # Create run_logs directory if it doesn't exist within the specified logs path
    logs_directory = os.path.join(logs_path, "run_logs")
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    print("Writing to logs directory:", logs_directory)

    # Generate a unique filename using the current timestamp within the logs directory
    filename = datetime.now().strftime(f"{logs_directory}/messages_%Y%m%d_%H%M%S.json")

    # Write the messages dict into a new file for each run
    with open(filename, "w") as f:
        f.write(json.dumps({"prompt": prompt_messages, "completion": completion}))

def extract_source_code(markdown_text):
    """
    Extracts the source code from a markdown string.

    :param markdown_text: A string that contains markdown text
    :return: The extracted source code
    """
    # Splitting the markdown text into lines
    lines = markdown_text.split('\n')

    # Checking if the markdown contains code blocks
    if any('```' in line for line in lines):
        code = []
        code_block = False
        for line in lines:
            if line.startswith('```'):
                # Toggle the code block flag
                code_block = not code_block
                # Skip the line that only contains '```'
                continue
            if code_block:
                code.append(line)
        return '\n'.join(code)
    else:
        # If there are no code blocks, the entire text is considered as code
        return markdown_text

