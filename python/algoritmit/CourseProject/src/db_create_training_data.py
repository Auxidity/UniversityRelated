"""
File : db_create_training_data.py
Author : Daniel Kortesmaa
Description : Creates formatted yaml file for training a RASA chatbot from sqlite db
"""

import sqlite3

def fetch_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT intent, example, response FROM training_data ORDER BY rowid")
    data = cursor.fetchall()
    return data

def create_yaml_file(data, output_file):
    with open(output_file, 'w') as file: #Custom yaml dump since the format gets broken inbetween source | db | output pipeline
        file.write('version: "2.0"\n\n')
        file.write("nlu:\n")
        for row in data:
            intent, example, response = row
            file.write("  - intent: {}\n".format(intent))
            file.write("    examples: |\n")
            for line in example.splitlines():
                file.write("      {}\n".format(line))
            file.write("    response:\n")
            response_lines = response.splitlines()
            if response_lines:
                file.write("       {}\n".format(response_lines[0]))
                for resp_line in response_lines[1:]:
                    file.write("       {}\n".format(resp_line))
                file.write("\n")


def main():
    # Connect to SQLite database
    conn = sqlite3.connect('data/db/chatbot_training_data.db')

    # Fetch all data from the table
    data = fetch_data(conn)

    # Close connection
    conn.close()

    # Create a single YAML file containing all the data
    create_yaml_file(data, 'data/output/training_data.yaml')

if __name__ == "__main__":
    main()
