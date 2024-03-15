import os
import shutil

# Define the source directory
source_directory = "/root/nuclei-templates/"

# Define the destination directory
destination_directory = "/root/nuclei-temp/"

# Define the list of severity levels to filter
allowed_severity_levels = ["low", "unknown", "medium", "high", "critical"]

# Function to check if a file has allowed severity level
def has_allowed_severity_level(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        for severity_level in allowed_severity_levels:
            if severity_level in content:
                return True
    return False

# Walk through the source directory
for root, dirs, files in os.walk(source_directory):
    for file in files:
        file_path = os.path.join(root, file)
        if file.endswith(".yaml") and has_allowed_severity_level(file_path):
            # Create destination directory if it doesn't exist
            os.makedirs(destination_directory, exist_ok=True)
            # Copy the file to the destination directory
            shutil.copy(file_path, destination_directory)
            print(f"Copied '{file}' to '{destination_directory}'.")

print("Done.")
