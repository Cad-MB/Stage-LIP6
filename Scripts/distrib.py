import os
import shutil
import random

def distribute_json_files(path, num_repositories):
    # Create directories if they don't exist
    for i in range(1, num_repositories + 1):
        dir_name = f"github_sat_{i}"
        os.makedirs(os.path.join(path, dir_name), exist_ok=True)

    # List all files in the specified path
    files = os.listdir(path)
    random.shuffle(files)

    for file in files:
        # Check if the file is a JSON file
        if file.endswith('.json'):
            # Select a random destination directory
            dest_dir = random.randint(1, num_repositories)
            dest_dir_name = f"github_sat_{dest_dir}"
            src_path = os.path.join(path, file)
            dest_path = os.path.join(path, dest_dir_name, file)

            # Move the file to the corresponding directory
            shutil.move(src_path, dest_path)
            print(f"Moved '{file}' to '{dest_dir_name}' directory.")

if __name__ == "__main__":
    source_path = r"C:\Users\Surface\Documents\LIP6\Stage-LIP6\dataGenDataset\github\sat"
    num_repositories = 14
    distribute_json_files(source_path, num_repositories)
