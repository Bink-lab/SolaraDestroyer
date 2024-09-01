import os
import time
import ctypes
import sys

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

# Function to count all files in the directory with a timer
def count_files_with_timer(root_dir):
    start_time = time.time()
    total_files = 0

    for root, dirs, files in os.walk(root_dir):
        total_files += len(files)
        
        # Calculate the elapsed time
        current_time = time.time()
        elapsed_time = int(current_time - start_time)

        # Print the elapsed time on the same line
        print(f"\rAnalyze time: {elapsed_time} seconds", end="")
    
    print()  # Move to the next line after completion
    return total_files, elapsed_time

# Function to scan for files with 'solara' in the filename
def scan_for_solara_files(root_dir):
    found_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Scanned: {file_path}")
            if "solara" in file.lower():
                found_files.append((file, file_path))
                print(f"Found! {file_path} (a file with the word 'solara' in it)")
    return found_files

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
    
    print("Analyzing the total amount of files...")
    total_files, elapsed_time = count_files_with_timer(root_dir)
    print(f"\nFound {total_files} files in {elapsed_time} seconds!")

    # Use a standard input instead of keyboard.wait to avoid skipping inputs
    input("\nPress Enter to start the scanning process...")
    print("\nStaring the scanning process...")
    time.sleep(2)

    found_files = scan_for_solara_files(root_dir)

    # Display the number of files found
    print(f"\nTotal files found with 'solara' in the name: {len(found_files)}")

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
        print("No files with 'solara' in the filename were found.")

if __name__ == "__main__":
    main()
