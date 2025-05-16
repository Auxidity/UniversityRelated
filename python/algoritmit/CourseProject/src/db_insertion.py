"""
File : db_insertion.py
Author : Daniel Kortesmaa
Description : Creates a db if one doesn't exist and then adds yaml data into it.
"""

import yaml
import sqlite3
import os, shutil

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS training_data (
                        intent TEXT,
                        example TEXT,
                        response TEXT
                    )''')
    conn.commit()

def insert_data(conn, yaml_files):
    cursor = conn.cursor()
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r') as file:
                yaml_data = yaml.safe_load(file)
                for intent_data in yaml_data.get('nlu', []):
                    intent = intent_data.get('intent')
                    example = intent_data.get('examples', '')
                    response = intent_data.get('response', '')
                    cursor.execute("INSERT INTO training_data (intent, example, response) VALUES (?, ?, ?)",
                        (intent, example, response))

                    examples = yaml_data.get('examples', {})
                    for intent, example_list in examples.items():
                        for example in example_list:    
                            cursor.execute("UPDATE training_data SET example = ? WHERE intent = ?",
                                        (example, intent))
                
                responses = yaml_data.get('responses', {})
                for intent, response_list in responses.items():
                    # Convert the list of responses to a multi-line YAML string. Above solution on examples doesn't work for responses
                    response_yaml = yaml.dump({intent: response_list})
                    cursor.execute("UPDATE training_data SET response = ? WHERE intent = ?",
                                       (response_yaml, intent))
            conn.commit()
        except Exception as e: #Move any exception under reformat for further analysis. Not handled currently in any way
            print(f"Error: {e}")
            reformat_dir = os.path.join(parent_dir, 'data/reformat')
            os.makedirs(reformat_dir, exist_ok=True)
            shutil.move(yaml_file, os.path.join(reformat_dir, os.path.basename(yaml_file)))
            continue


def main(directory):
    # Get list of YAML files in directory
    yaml_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.yaml')]

    # Connect to SQLite database
    conn = sqlite3.connect('data/db/chatbot_training_data.db')

    # Create table if not exists
    create_table(conn)

    # Insert data from YAML files into table
    insert_data(conn, yaml_files)

    # Close connection
    conn.close()

if __name__ == "__main__":
    # Get the parent directory of the script's directory
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    yaml_dir = os.path.join(parent_dir, 'data/yaml')
    main(yaml_dir)
