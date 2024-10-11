import os

def replace_tile_data_lines(root_folder, replacement_line):
    """
    Iterates through all files in the root_folder and its subfolders,
    searches for lines containing 'tile_data', and replaces those lines
    with the replacement_line.

    Parameters:
    - root_folder: The path to the folder to search.
    - replacement_line: The line that will replace any line containing 'tile_data'.
    """

    # Walk through all subdirectories and files
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(subdir, file)

            # Process only files with specific extensions (e.g., .tscn, .tres)
            if file.endswith(('.tscn', '.tres', '.txt', '.gd', '.cfg')):

                try:
                    # Read the file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    # Flag to check if any replacement happened
                    replaced = False

                    # Replace lines containing 'tile_data'
                    new_lines = []
                    for line in lines:
                        if 'tile_data' in line:
                            new_lines.append(replacement_line + '\n')
                            replaced = True
                        else:
                            new_lines.append(line)

                    # Write the modified content back to the file if replacements were made
                    if replaced:
                        # Create a backup of the original file
                        backup_path = file_path + '.bak'
                        os.rename(file_path, backup_path)

                        # Write the new content to the original file path
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(new_lines)

                        print(f"Updated file: {file_path}")

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

# Example usage:
root_folder = '/path/to/your/folder'  # Replace with the path to your folder
replacement_line = 'tile_data = [ ]'  # Replace with your desired replacement line

replace_tile_data_lines(root_folder, replacement_line)