"""
File : secondary_data_processing.py
Author : Daniel Kortesmaa
Description : Loads the topic jsons from preliminary_data_processing.py and filters out posts and comments based on arbitrary logic (post score > 50 && comment score > 1 && message isn't deleted). These are then saved as separate files.
"""
import json, os


# Get the parent directory of the script's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

#Raw data location
previous_data_dir = os.path.join(parent_dir, 'data/processed1')
#Processed
processed_data_dir = os.path.join(parent_dir, 'data/processed2')
#Make the processed data folder if it doesn't exist.
if not os.path.exists(processed_data_dir):
    os.makedirs(processed_data_dir)

# Test the function
file_names = os.listdir(previous_data_dir)

for file_name in file_names:
    # Check if the file is a JSON file
    if file_name.endswith('.json'):
        # Construct the full path to the file
        file_path = os.path.join(previous_data_dir, file_name)
        
        # Load the JSON data from the file
        with open(file_path, 'r') as file:
            data = json.load(file)

            # Extract values
            title = data["title"]
            author = data["author"]
            created_utc = data["created_utc"]
            url = data["url"]
            score = data["score"]

            if score >= 50:
                filtered_data = {
                    "title": title,
                    "comments": []
                }

                # Append suitable comments
                comments = data["comments"]
                for comment in comments:
                    comment_id = comment["comment_id"]
                    parent_id = comment["parent_id"]
                    author = comment["author"]
                    body = comment["body"]
                    created_utc = comment["created_utc"]
                    upvotes = comment["upvotes"]
                    downvotes = comment["downvotes"]
                    if upvotes >= 2 and body != "[removed]":
                        filtered_comment = {
                            "comment_id": comment_id,
                            "parent_id": parent_id,
                            "body": body
                        }
                        filtered_data["comments"].append(filtered_comment)

                    output_file = os.path.join(processed_data_dir, file_name)

                    with open(output_file, 'w') as f:
                        json.dump(filtered_data, f, indent=4)
