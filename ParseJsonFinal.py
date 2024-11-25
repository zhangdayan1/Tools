import json
import pandas as pd

# Load the JSON data
with open('data.json', 'r') as json_file:
    json_data = json.load(json_file)

# Perform the transformations
fields = ['dl', 'lsh', 'pss', 'ss', 'htc', 'lcss', 'lvql', 'bps', 'boi', 'propri', 'prosec', 'bos', 'pld', 'imgld', 'rmld', 'ep']
extracted_data = {field: json_data['ei']['at'].get(field) or json_data['ei']['bt'].get(field) for field in fields}
gsi_fields = ['gsi.1']
extracted_gsi_data = {field: json_data['ei']['at']['gsi'].get(field) for field in gsi_fields}

print(extracted_gsi_data)

# Adjust the 'ep' and 'dl' fields to be arrays with a first element of 0, second as the original value, and third as their sum
if 'ep' in extracted_data and isinstance(extracted_data['ep'], (int, float)):
    extracted_data['ep'] = [0, extracted_data['ep'], extracted_data['ep'] + 0]
if 'dl' in extracted_data and isinstance(extracted_data['dl'], (int, float)):
    extracted_data['dl'] = [0, extracted_data['dl'], extracted_data['dl'] + 0]
if 'lsh' in extracted_data and isinstance(extracted_data['lsh'], (int, float)):
    extracted_data['lsh'] = [0, extracted_data['lsh'], extracted_data['lsh'] + 0]

for key, value in extracted_data.items():
    if isinstance(value, list):
        value.append(value[0] + value[1])
# Add gsi data
for key, value in extracted_gsi_data.items():
    if isinstance(value, list):
        value.append(value[0] + value[1])
    
extracted_data["EPT"] = [json_data["t"] - json_data["e"], json_data["e"], json_data["t"]]

# Convert to a DataFrame
table_data = {
    "Metric Name": [],
    "Start Time": [],
    "End Time": [],
    "Elapsed Time": []
}
for field, values in extracted_data.items():
    if isinstance(values, list):
        table_data["Metric Name"].append(field)
        table_data["Start Time"].append(values[0])
        table_data["End Time"].append(values[2])
        table_data["Elapsed Time"].append(values[1])
for field, values in extracted_gsi_data.items():
    if isinstance(values, list):
        table_data["Metric Name"].append(field)
        table_data["Start Time"].append(values[0])
        table_data["End Time"].append(values[2])
        table_data["Elapsed Time"].append(values[1])

df = pd.DataFrame(table_data)

# Sort the DataFrame by 'Start Time' in ascending order
df = df.sort_values(by=["Start Time", "End Time"], ascending=[True, True]).reset_index(drop=True)

# Save the table
df.to_csv('converted_table.csv', index=False)

