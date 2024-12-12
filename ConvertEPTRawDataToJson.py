import json
import sys
import re

def convert_to_json(input_string):
    # Replace unquoted keys with quoted keys
    fixed = re.sub(r'(\{|,)(\s*)([a-zA-Z_][a-zA-Z0-9_]*)(\s*):', r'\1 "\3":', input_string)

    # Step 2: Add quotes around unquoted string values (but not numbers, booleans, or null)
    fixed = re.sub(r':\s*([a-zA-Z0-9_\-]+)(?=\s*[,}])', r': "\1"', fixed)

    # Fix empty values (like sid:)
    fixed = re.sub(r':\s*,', r': "",', fixed)

    # Handle embedded JSON strings properly
    fixed = re.sub(r'":\s*"{', r'": {', fixed)
    fixed = re.sub(r'}",', r'},', fixed)

    return fixed

# Get the run index from the input parameter
if len(sys.argv) < 2:
    print("Please provide raw data file as input parameters")
    sys.exit(1)
raw_data_file = str(sys.argv[1])

# Load the JSON data
with open(raw_data_file, 'r') as file:
    raw_data = file.read()

# Convert to correct Json format
json_data = json.loads(convert_to_json(raw_data))

print(json.dumps(json_data, indent=4))
