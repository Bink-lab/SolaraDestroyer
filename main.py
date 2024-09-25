import os
import time
import ctypes
import sys
import requests

print(""" $$$$$$\   $$$$$$\  $$\        $$$$$$\  $$$$$$$\   $$$$$$\        $$$$$$$$\ $$\   $$\  $$$$$$\  $$\   $$\ $$$$$$$$\ $$$$$$$\  
$$  __$$\ $$  __$$\ $$ |      $$  __$$\ $$  __$$\ $$  __$$\       $$  _____|$$ |  $$ |$$  __$$\ $$ | $$  |$$  _____|$$  __$$\ 
$$ /  \__|$$ /  $$ |$$ |      $$ /  $$ |$$ |  $$ |$$ /  $$ |      $$ |      $$ |  $$ |$$ /  \__|$$ |$$  / $$ |      $$ |  $$ |
\$$$$$$\  $$ |  $$ |$$ |      $$$$$$$$ |$$$$$$$  |$$$$$$$$ |      $$$$$\    $$ |  $$ |$$ |      $$$$$  /  $$$$$\    $$$$$$$  |
 \____$$\ $$ |  $$ |$$ |      $$  __$$ |$$  __$$< $$  __$$ |      $$  __|   $$ |  $$ |$$ |      $$  $$<   $$  __|   $$  __$$< 
$$\   $$ |$$ |  $$ |$$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |      $$ |      $$ |  $$ |$$ |  $$\ $$ |\$$\  $$ |      $$ |  $$ |
\$$$$$$  | $$$$$$  |$$$$$$$$\ $$ |  $$ |$$ |  $$ |$$ |  $$ |      $$ |      \$$$$$$  |\$$$$$$  |$$ | \$$\ $$$$$$$$\ $$ |  $$ |
 \______/  \______/ \________|\__|  \__|\__|  \__|\__|  \__|      \__|       \______/  \______/ \__|  \__|\________|\__|  \__|
                                                                                                                              
                                                                                                                              
                                                                                                                              """)

# Function to check if the script is running as an administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to load skip folders from a GitHub URL
def load_skip_folders(github_url='https://raw.githubusercontent.com/bink-lab/solaradestroyer/main/skip_folders.txt'):
    try:
        response = requests.get(github_url)
        response.raise_for_status()  # Raise an error for bad responses
        return [os.path.normcase(line.strip()) for line in response.text.splitlines() if line.strip()]
    except Exception as e:
        print(f"Error reading skip folders from GitHub: {e}")
        return []

# Function to scan for 'solara' in filenames and contents (for files < 10MB)
def scan_for_solara_files(root_dir, skip_folders, max_size_mb=10):
    found_files = []
    large_files = []

    for root, dirs, files in os.walk(root_dir):
        # Normalize the current directory path to lowercase
        normalized_root = os.path.normcase(root)
        
        # Skip directories listed in skip_folders
        if any(normalized_root.startswith(os.path.normcase(skip_folder)) for skip_folder in skip_folders):
            continue  # Skip without printing
        
        for file in files:
            file_path = os.path.join(root, file)
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # File size in MB
            print(f"Scanned: {file_path}")
            
            # Check if 'solara' is in the filename (case-insensitive)
            if "solara" in file.lower():
                found_files.append((file, file_path))
                print(f"Found in filename! {file_path} (a file with the word 'solara' in it)")

            # Scan the contents of files smaller than max_size_mb
            if file_size_mb <= max_size_mb:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        if 'solara' in f.read().lower():
                            found_files.append((file, file_path))
                            print(f"Found in content! {file_path} (a file with 'solara' inside)")
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}")
            else:
                large_files.append((file, file_path, file_size_mb))

    return found_files, large_files


# Function to save found files to a text file
def save_to_txt(found_files, output_file):
    with open(output_file, 'w') as f:
        f.write("---- FOUND FILES ----\n\n")
        for file_name, file_path in found_files:
            f.write(f"Filename: {file_name}\n")
            f.write(f"Path: {file_path}\n\n")
    print(f"Results saved to {output_file}")

# Function to delete found files
def delete_files(found_files):
    for _, file_path in found_files:
        try:
            os.remove(file_path)
            print(f"\nDeleted: {file_path}")
        except Exception as e:
            print(f"\nFailed to delete {file_path}: {e}")

def main():
    # Check if running as administrator
    if not is_admin():
        print("This program is not being run as an administrator. It is recommended to run as an administrator.")
        choice = input("Do you wish to continue? (y/n): ").strip().lower()
        if choice != 'y':
            sys.exit("Exiting program. Please run as administrator.")
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal

    root_dir = "C:\\"
    
    # Load skip folders from GitHub
    skip_folders = load_skip_folders()

    print("\nStarting the scanning process...")
    time.sleep(2)

    found_files, large_files = scan_for_solara_files(root_dir, skip_folders)

    # Display the number of files found
    print(f"\nTotal files found with 'solara' in the name or content: {len(found_files)}")
    print(f"Total large files skipped: {len(large_files)}")

    if found_files:
        save_choice = input("Would you like to save the found files to a .txt file? (y/n): ").strip().lower()
        if save_choice == 'y':
            output_file = "found_solara_files.txt"
            save_to_txt(found_files, output_file)
        
        delete_choice = input("\nWould you like to delete the found files? (y/n): ").strip().lower()
        if delete_choice == 'y':
            print(f"\nDeleting {len(found_files)} files...")
            delete_files(found_files)
            print("\nAll found files have been deleted!")
            input("Press Enter to exit...")
    else:
        print("No files with 'solara' in the filename or content were found.")

if __name__ == "__main__":
    main()
