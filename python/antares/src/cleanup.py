import os

def cleanup_session_files():
    current_dir = os.getcwd()
    for file_name in os.listdir(current_dir):
        if file_name.endswith(".session"):
            file_path = os.path.join(current_dir, file_name)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

def cleanup_user_data():
    current_dir = os.getcwd()
    for file in os.listdir(current_dir):
        if file == "user_data.json":
            file_path = os.path.join(current_dir, file)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

if __name__ == "__main__":
    cleanup_session_files()
    cleanup_user_data()


"""
+358    4
045 123 6666    3+3+4 = 10

"""