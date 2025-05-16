"""
File : tertiary_data_processing.py
Author : Daniel Kortesmaa
Description : Creates parent - child format for each topic and its comments from secondary_data_processing.py's output
"""

import os, json

# Get the parent directory of the script's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

#Raw data location
previous_data_dir = os.path.join(parent_dir, 'data/processed2')
#Processed
processed_data_dir = os.path.join(parent_dir, 'data/processed')
#Make the processed data folder if it doesn't exist.
if not os.path.exists(processed_data_dir):
    os.makedirs(processed_data_dir)

def create_comment_chain(comment, comments, chain):
    chain.append(comment)
    children = [c for c in comments if c['parent_id'] == comment['comment_id']]
    for child in children:
        create_comment_chain(child, comments, chain)

def split_comments(data):
    title = data['title']
    comments = data['comments']
    
    # Initialize dictionaries to store comments by their comment_id
    comments_dict = {comment['comment_id']: comment for comment in comments}
    
    # Initialize a list to keep track of processed comments
    processed_comments = set()
    
    # Initialize a list to store output data
    output_data = []
    
    # Iterate through comments to create output
    for comment in comments:
        if comment['comment_id'] not in processed_comments:
            if comment['parent_id'] is None:
                conversation = {'title': title, 'comment': comment['body'], 'responses': []}
                chain = []
                create_comment_chain(comment, comments, chain)
                processed_comments.update(c['comment_id'] for c in chain)
                for c in chain[1:]:
                    conversation['responses'].append(c['body'])
                output_data.append(conversation)
    
    return output_data


file_names = os.listdir(previous_data_dir)
for file_name in file_names:
    
    # Check if the file is a JSON file
    if file_name.endswith('.json'):
        # Construct the full path to the file
        file_path = os.path.join(previous_data_dir, file_name)
        
        # Load the JSON data from the file
        with open(file_path, 'r') as file:
            data = json.load(file)
            output_data = split_comments(data)

            output_file = os.path.join(processed_data_dir, file_name)
            with open(output_file, 'w') as f:
                json.dump(output_data, f, indent=4)