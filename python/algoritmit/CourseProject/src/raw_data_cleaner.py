"""
File : raw_data_cleaner.py
Author : Daniel Kortesmaa
Description : Automated process of running each script sequentially resulting in creation of singular training data for RASA chatbot. Comment parts out based on need for inspecting steps.
"""

#Files that require further attention (due to chatgpt limitations) are under data/reformat. Theres a few ways to go about them, either manually fixing them or run them through chatgpt until the format is acceptable for sqlite.
#Also there is a potential need to verify the data being inserted into db further.. Some weird stuff passes every now and then (i.e.  response topic starts with ?.. Issue lies with passing it through chatgpt and it doesn't get caught \
#when inserting to db since it is "technically" valid, sometimes... Hallucination issue with AI.) Potential solution is to double or triple check outputs through AI to lessen the amount of reformatted crap, but it increases \
#cost (API calls arent free) & time spent. It isn't entirely error free solution either. Better error handler on data injection is also an option, but creating a robust one without false positives is a lot of work. I decided against \
#making one for now, as it was fairly rare occurance.


#Note: A bit of an ugly solution in terms of space management, \
        #but it is a viable lazy solution if you don't deal with massive amounts of data at once, and add the data to database at constant intervals. Massive amounts of data will probably also result in too many API calls leading to \
        #timeouts possibly, lessening the need for the solution to be space efficient.

import subprocess
import os
import shutil

# Relevant directories initialized
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
src_dir = os.path.join(parent_dir, 'src/')
output_dir = os.path.join(parent_dir, 'data/output')
db_dir = os.path.join(parent_dir, 'data/db')

# Define paths to the scripts
preliminary_script = os.path.join(src_dir, 'preliminary_data_processing.py')
secondary_script = os.path.join(src_dir, 'secondary_data_processing.py')
tertiary_script = os.path.join(src_dir, 'tertiary_data_processing.py')
yamlifier_script = os.path.join(src_dir, 'yamlifier.py')
db_insert_script = os.path.join(src_dir, 'db_insertion.py')
db_create_training_data = os.path.join(src_dir, 'db_create_training_data.py')

# Remove placeholder directories if they exist (cleanup in case they do exist and you're inspecting previous run)
placeholder_dirs = [os.path.join(parent_dir, 'data/processed1'), os.path.join(parent_dir, 'data/processed2')]
for dir_path in placeholder_dirs:
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

# Run the json related scripts sequentially
subprocess.run(['python3', preliminary_script])
subprocess.run(['python3', secondary_script])
subprocess.run(['python3', tertiary_script])

#Run the yamlifier process 
subprocess.run(['python3', yamlifier_script])

# Remove db and output dirs to ensure clean slate output. Comment out if you wish to append to db instead. Output should be deleted just in case though. Final solution is to merge this with the above dir deletion once theres nothing that\
#we potentially want to inspect post run
placeholder_dirs = [os.path.join(parent_dir, 'data/db'), os.path.join(parent_dir, 'data/output')]
for dir_path in placeholder_dirs:
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

#Make directories for output and db. They are wiped on each run currently, and the sqlite3 scripts don't create these by themselves.
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

#Run the script to add yaml files into db, and creating one big training data yaml file out of the db. If you only wish to append to db, comment out 2nd subprocess
subprocess.run(['python3', db_insert_script])
subprocess.run(['python3', db_create_training_data])

#Cleanup of excess directories.
placeholder_dirs = [os.path.join(parent_dir, 'data/processed1'), os.path.join(parent_dir, 'data/processed2', os.path.join(parent_dir, 'data/yaml'))] #, os.path.join(parent_dir, 'data/yaml'
for dir_path in placeholder_dirs:
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)


