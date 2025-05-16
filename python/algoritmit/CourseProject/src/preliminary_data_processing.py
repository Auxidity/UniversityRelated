"""
File : preliminary_data_processing.py
Author : Daniel Kortesmaa
Description : Splits the raw data jsons into separate topics and creates a separate file for each topic
"""

import json, os, io, datetime

# Get the parent directory of the script's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

#Raw data location
raw_data_dir = os.path.join(parent_dir, 'data/raw')

processed_data_dir = os.path.join(parent_dir, 'data/processed1')

#Make the processed data folder if it doesn't exist.
if not os.path.exists(processed_data_dir):
    os.makedirs(processed_data_dir)


#Splits data to topics  
def split_data(data, filename):
    """Split data into separate files."""
    for post in data:        
        # Write post data along with comments to a file
        post_filename = increment_filename(filename)
        generate_file(post_filename, post)

#Helper function for naming based on what will get loaded
def increment_filename(filename):
    base, ext = os.path.splitext(filename)
    parts = base.split('_')
    if len(parts) < 2:
        return None  # Invalid filename format
    prefix = '_'.join(parts[:-1])  # Exclude the last part (file format extension)
    processed_suffix = parts[-1] + '_processed'  # Include '_processed' in the suffix
    counter = 1
    
    while True:
        new_filename = f"{prefix}_{processed_suffix}{counter}{ext}"
        if not os.path.exists(os.path.join(processed_data_dir, new_filename)):
            return new_filename
        counter += 1

        
# Generates output files
def generate_file(data_filename, data):
    new_filename = increment_filename(data_filename)
    output_file = os.path.join(processed_data_dir, new_filename)
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)





file_names = os.listdir(raw_data_dir)

for file_name in file_names:
    # Check if the file is a JSON file
    if file_name.endswith('.json'):
        # Construct the full path to the file
        file_path = os.path.join(raw_data_dir, file_name)
        
        # Load the JSON data from the file
        with open(file_path, 'r') as file:
            data = json.load(file)
            split_data(data, file_name)