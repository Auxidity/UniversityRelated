#Debug file

"""
import subprocess
import os
import shutil

# Get the parent directory of the script's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
src_dir = os.path.join(parent_dir, 'src/')
output_dir = os.path.join(parent_dir, 'data/output')
db_dir = os.path.join(parent_dir, 'data/db')


db_insert_script = os.path.join(src_dir, 'db_insertion.py')
db_create_training_data = os.path.join(src_dir, 'db_create_training_data.py')

# Remove placeholder directories if they exist (cleanup in case they do exist and you're inspecting previous run)
placeholder_dirs = [os.path.join(parent_dir, 'data/db'), os.path.join(parent_dir, 'data/output')]
for dir_path in placeholder_dirs:
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)


if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

subprocess.run(['python3', db_insert_script])
subprocess.run(['python3', db_create_training_data])
"""