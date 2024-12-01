import json
import pandas as pd
import sys

# Load the JSON data
with open('data.json', 'r') as json_file:
    json_data = json.load(json_file)

# Get the run index from the input parameter
if len(sys.argv) < 2:
    print("Please provide a run index as an input parameter.")
    sys.exit(1)
run_index = int(sys.argv[1])

# Perform the transformations
fields = ['dl', 'lsh', 'pss', 'ss', 'htc', 'lcss', 'lvb', 'appstr', 'lvql', 'bps', 'boi', 'propri', 'prosec', 'bos', 'pld', 'gas', 'imgld', 'rmld', 'ep']
extracted_data = {field: json_data['ei']['at'].get(field) or json_data['ei']['bt'].get(field) for field in fields}
gsi_fields = ['gsi.1']
extracted_gsi_data = {field: json_data['ei']['at']['gsi'].get(field) for field in gsi_fields}
extracted_mdload_data = json_data["ei"]["at"]["mdload"]
extracted_df_data = json_data["ei"]["at"]["df"]

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

# Parse regular EPT metrics data
for field, values in extracted_data.items():
    if isinstance(values, list):
        match field:
            case "ep":
                table_data["Metric Name"].append("Time To First Byte")
            case "dl":
                table_data["Metric Name"].append("Static Html Start Loading")
            case "lsh":
                table_data["Metric Name"].append("Load Static Html")            
            case "bps":
                table_data["Metric Name"].append("Bootstrap POST Request Sent")
            case "pss":
                table_data["Metric Name"].append("Prepare Start Session")
            case "ss":
                table_data["Metric Name"].append("Start Session")
            case "htc":
                table_data["Metric Name"].append("Handle TsConfig")            
            case "lcss":
                table_data["Metric Name"].append("Load Css") 
            case "lvb":
                table_data["Metric Name"].append("Load ViewerBootstrap Module") 
            case "appstr":
                table_data["Metric Name"].append("Application Startup") 
            case "lvql":
                table_data["Metric Name"].append("Load JS Mobules For Bootstrap")            
            case "boi":
                table_data["Metric Name"].append("BootstrapSession onInitial Callback")                   
            case "bos":
                table_data["Metric Name"].append("BootstrapSession onSecondaryAction Callback")            
            case "imgld":
                table_data["Metric Name"].append("Image Tiles Load")            
            case "propri":
                table_data["Metric Name"].append("Process Bootstrap Primary Payload")
            case "prosec":
                table_data["Metric Name"].append("Process Bootstrap Secondary Payload")
            case "pld":
                table_data["Metric Name"].append("Progressive Load")
            case "gas":
                table_data["Metric Name"].append("Get Acceleration State for View")
            case "rmld":
                table_data["Metric Name"].append("Extra Time of Async Module Load after Image Tiles Load")
            case _:
                table_data["Metric Name"].append(field)
        table_data["Start Time"].append(values[0])
        table_data["End Time"].append(values[2])
        table_data["Elapsed Time"].append(values[1])

# Parse GetSessionInfo data
for field, values in extracted_gsi_data.items():
    if isinstance(values, list):
        match field:
            case "gsi.1":
                table_data["Metric Name"].append("Get Session Info 1")
            case "gsi.2":
                table_data["Metric Name"].append("Get Session Info 2")
            case "gsi.3":
                table_data["Metric Name"].append("Get Session Info 3")
            case "gsi.4":
                table_data["Metric Name"].append("Get Session Info 4")
            case _:
                table_data["Metric Name"].append(field)
        table_data["Start Time"].append(values[0])
        table_data["End Time"].append(values[2])
        table_data["Elapsed Time"].append(values[1])

# Parse async module load data
start_time_of_mdload = min(item[0] for item in extracted_mdload_data.values())
end_time_of_mdload = max(sum(item) for item in extracted_mdload_data.values())
table_data["Metric Name"].append("Async Module Load")
table_data["Start Time"].append(start_time_of_mdload)
table_data["End Time"].append(end_time_of_mdload)
table_data["Elapsed Time"].append(end_time_of_mdload - start_time_of_mdload)

# Parse download font data
start_time_of_df = min(item[0] for item in extracted_df_data.values())
end_time_of_df = max(sum(item) for item in extracted_df_data.values())
table_data["Metric Name"].append("Download Fonts")
table_data["Start Time"].append(start_time_of_df)
table_data["End Time"].append(end_time_of_df)
table_data["Elapsed Time"].append(end_time_of_df - start_time_of_df)

df = pd.DataFrame(table_data)

# Add 'Run Index' as the first column
df.insert(0, 'Run Index', run_index)

# Sort the DataFrame by 'Start Time' in ascending order
df = df.sort_values(by=["Start Time", "End Time"], ascending=[True, True]).reset_index(drop=True)

# Save the table
output_file = f'output_{run_index}.csv'
df.to_csv(output_file, index=False)
