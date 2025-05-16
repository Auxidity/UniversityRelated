# For the sake of this exercise, we assume that consent has been given when the data has been collected
# The data is then stored as is somewhere locally, and the scripts responsibility is to transform it to GDPR compliant version
# To avoid overcomplicating the exercise, instead of creating a db that the data is stored to, the data is stored to another file instead
#
# For limitation of purpose, data and storage clause in GDPR, we do not make decisions if some of the data provided in example is unneeded. One could argue that contact information is not neccesary,
# however I am not making that decision here since I do not know for a fact that it is unneccesary.
#
# Data protection and data subject rights are assumed to be handled outside this exercise, since we're only tasked with privacy related transformations.
#


import json
import uuid
from cryptography.fernet import Fernet
import os

def generate_key():
    return Fernet.generate_key()

def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data.encode()).decode()


# For the sake of this exercise, the encryption & decryption key is stored locally for entire exercise. Other alternatives would exist, such as generating a database and assigning unique key for each entry (as done in exercise 4_5)

key_file = 'encryption_key.key'
if not os.path.exists(key_file):
    key = generate_key()
    with open(key_file, 'wb') as f:
        f.write(key)
else:
    with open(key_file, 'rb') as f:
        key = f.read()

# Read the initial data from the JSON file. This would normally be an API call for the data or something else, but for simplicitys sake we are reading a file.
with open('data.json', 'r') as f:
    data = json.load(f)

# Pseudonymize the data
def pseudonymize(value):
    return str(uuid.uuid4())  # Generate a unique identifier

# Create a mapping for pseudonymization
pseudonym_mapping = {}

# Pseudonymize and encrypt sensitive data
pseudonym_mapping[data['Person']['first_name']] = pseudonymize(data['Person']['first_name'])
data['Person']['first_name'] = encrypt_data(pseudonym_mapping[data['Person']['first_name']], key)

pseudonym_mapping[data['Person']['last_name']] = pseudonymize(data['Person']['last_name'])
data['Person']['last_name'] = encrypt_data(pseudonym_mapping[data['Person']['last_name']], key)

pseudonym_mapping[data['Person']['SSN']] = pseudonymize(data['Person']['SSN'])
data['Person']['SSN'] = encrypt_data(pseudonym_mapping[data['Person']['SSN']], key)

pseudonym_mapping[data['Person']['date-of-birth']] = pseudonymize(data['Person']['date-of-birth'])
data['Person']['date-of-birth'] = encrypt_data(pseudonym_mapping[data['Person']['date-of-birth']], key)

pseudonym_mapping[data['Contact_info']['street_address']] = pseudonymize(data['Contact_info']['street_address'])
data['Contact_info']['street_address'] = encrypt_data(pseudonym_mapping[data['Contact_info']['street_address']], key)

pseudonym_mapping[data['Contact_info']['phone_number']] = pseudonymize(data['Contact_info']['phone_number'])
data['Contact_info']['phone_number'] = encrypt_data(pseudonym_mapping[data['Contact_info']['phone_number']], key)

# Store the encrypted data in destination file (should be a db)
# Note: This file is not FULLY encrypted, its only the pseudonymized values that are encrypted, representing how they would be stored in the db.
with open('encrypted_data.json', 'w') as f:
    json.dump(data, f)

# Store the pseudonym mapping. In this case, we are just storing it to another file, but normally this would be done through a db aswell. This file is entirely encrypted.
# For the sake of simplicity, we are using the same key, but it would have its own key stored in same db that has the other encryption keys and fetched from there in reality.
encrypted_mapping = encrypt_data(json.dumps(pseudonym_mapping), key)
with open('pseudonym_mapping.json', 'w') as f:
    f.write(encrypted_mapping)

print("Sensitive data pseudonymized and encrypted successfully.")

#Function for accessing the encrypted data in its pseudonymized form
def retrieve_and_decrypt_pseudonymized():
    with open('encrypted_data.json', 'r') as f:
        stored_data = json.load(f)

    for field in ['first_name', 'last_name', 'SSN', 'date-of-birth']:
        stored_data['Person'][field] = decrypt_data(stored_data['Person'][field], key)

    for field in ['street_address', 'phone_number']:
        stored_data['Contact_info'][field] = decrypt_data(stored_data['Contact_info'][field], key)

    print("Decrypted pseudonymized data for use:\n", stored_data)

#Function for accessing the encrypted data in its non-pseudonymized form for GDPR compliance (Requirement as data holder so that we can delete the data when user requests it)
#For simplicitys sake, I won't implement removing the entry, but that would be part of the GDPR compliance aswell. 
#Implementation would just iterate over pseudonym mapping for a match in name and possibly other fields such as SSN (since there might be duplicates on name alone), and then delete entire entry based on the match from db
def retrieve_and_decrypt_non_pseudonymized():
    with open('encrypted_data.json', 'r') as f:
        stored_data = json.load(f)

    with open('pseudonym_mapping.json', 'r') as f:
        encrypted_mapping = f.read()
        pseudonym_mapping = json.loads(decrypt_data(encrypted_mapping, key))
    
    reverse_mapping = {v: k for k, v in pseudonym_mapping.items()}

    for field in ['first_name', 'last_name', 'SSN', 'date-of-birth']:
        pseudonymized_value = decrypt_data(stored_data['Person'][field], key)
        stored_data['Person'][field] = reverse_mapping.get(pseudonymized_value, pseudonymized_value)

    for field in ['street_address', 'phone_number']:
        pseudonymized_value = decrypt_data(stored_data['Contact_info'][field], key)
        stored_data['Contact_info'][field] = reverse_mapping.get(pseudonymized_value, pseudonymized_value)

    print("\nDecrypted non-pseudonymized data for use:", stored_data)

if __name__=="__main__":
    retrieve_and_decrypt_pseudonymized()
    retrieve_and_decrypt_non_pseudonymized()
