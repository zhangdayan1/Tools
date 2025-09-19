import os

# Combine files
output_files = ["output_1.csv", "output_2.csv", "output_3.csv", "output_4.csv", "output_5.csv"]
combined_file = "output.csv"

# Combine the files using the cat equivalent
with open(combined_file, "w") as outfile:
    for idx, fname in enumerate(output_files):
        with open(fname, "r") as infile:
            for line in infile:
                # If it's not the first file, skip the header
                if idx > 0 and line.startswith("Run Index"):
                    continue
                outfile.write(line)

# Deduplicate lines starting with 'Run Index' (only keep the first occurrence)
with open(combined_file, "r") as file:
    lines = file.readlines()

seen = False
with open(combined_file, "w") as file:
    for line in lines:
        if line.startswith("Run Index"):
            if seen:
                continue  # Skip subsequent headers
            seen = True  # Mark header as seen
        file.write(line)

print(f"Combined and cleaned file saved as: {combined_file}")
