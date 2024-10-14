import os
import re

from id_mapping import *

## for pixifrmer
# tile_data_for_mapping_gd43 = [
#     0, 0, 0, 1, 10, 0, 2, 5, 0, 3, 3, 0, 4, 4, 0, 5, 6, 0, 6, 1, 0, 7, 1, 1, 8, 1, 2, 9, 1, 3, 10, 7, 0, 11, 2, 0, 12,
#     9, 0, 13, 8, 0, 65542, 1, 1, 65543, 65537, 1, 65544, 131073, 1, 65545, 196609, 1, 65546, 7, 1, 65547, 65538, 0,
#     65549, 8, 1, 131078, 1, 2, 131079, 65537, 2, 131080, 131073, 2, 131081, 196609, 2, 131082, 7, 2, 131083, 131074, 0,
#     131085, 8, 2, 196614, 1, 3, 196615, 65537, 3, 196616, 131073, 3, 196617, 196609, 3, 196619, 196610, 0]
# tile_data_for_mapping_gd35 = [
#     0, 0, 0, 1, 17, 0, 2, 19, 0, 3, 14, 0, 4, 15, 0, 5, 18, 0, 6, 1, 0, 7, 1, 1, 8, 1, 2, 9, 1, 3, 10, 11, 0, 11, 21, 0, 12, 16, 0, 13, 13, 0, 65542, 1, 65536, 65543, 1, 65537, 65544, 1, 65538, 65545, 1, 65539, 65546, 11, 65536, 65547, 21, 1, 65549, 13, 65536, 131078, 1, 131072, 131079, 1, 131073, 131080, 1, 131074, 131081, 1, 131075, 131082, 11, 131072, 131083, 21, 2, 131085, 13, 131072, 196614, 1, 196608, 196615, 1, 196609, 196616, 1, 196610, 196617, 1, 196611, 196619, 21, 3
# ]

tile_data_for_mapping_gd35 = [ 0, 11, 0, 1, 11, 1, 2, 11, 2, 3, 11, 3, 4, 11, 4, 5, 11, 5, 6, 11, 6, 7, 11, 7, 8, 11, 8, 9, 11, 9, 10, 11, 10, 11, 11, 11, 65536, 11, 65536, 65537, 11, 65537, 65538, 11, 65538, 65539, 11, 65539, 65540, 11, 65540, 65541, 11, 65541, 65542, 11, 65542, 65543, 11, 65543, 65544, 11, 65544, 65545, 11, 65545, 65546, 11, 65547, 65547, 11, 131072, 131072, 11, 131073, 131073, 11, 131074, 131074, 11, 131075, 131075, 11, 131076, 131076, 11, 131077, 131077, 11, 131078, 131078, 11, 131079, 131079, 11, 131080, 131080, 11, 131081, 131081, 11, 131082, 131082, 11, 131083, 131083, 11, 196608, 196608, 11, 196609, 196609, 11, 196610, 196610, 11, 196611, 196611, 11, 196612, 196612, 11, 196613, 196613, 11, 196614, 196614, 11, 196615, 196615, 11, 196616, 196616, 11, 196617, 196617, 11, 196618, 196618, 11, 196619 ]
tile_data_for_mapping_gd43 = [0, 0, 0, 1, 65536, 0, 2, 131072, 0, 3, 196608, 0, 4, 262144, 0, 5, 327680, 0, 6, 393216, 0, 7, 458752, 0, 8, 524288, 0, 9, 589824, 0, 10, 655360, 0, 11, 720896, 0, 65536, 0, 1, 65537, 65536, 1, 65538, 131072, 1, 65539, 196608, 1, 65540, 262144, 1, 65541, 327680, 1, 65542, 393216, 1, 65543, 458752, 1, 65544, 524288, 1, 65545, 589824, 1, 65546, 720896, 1, 65547, 0, 2, 131072, 65536, 2, 131073, 131072, 2, 131074, 196608, 2, 131075, 262144, 2, 131076, 327680, 2, 131077, 393216, 2, 131078, 458752, 2, 131079, 524288, 2, 131080, 589824, 2, 131081, 655360, 2, 131082, 720896, 2, 131083, 0, 3, 196608, 65536, 3, 196609, 131072, 3, 196610, 196608, 3, 196611, 262144, 3, 196612, 327680, 3, 196613, 393216, 3, 196614, 458752, 3, 196615, 524288, 3, 196616, 589824, 3, 196617, 655360, 3, 196618, 720896, 3]

def update_tile_data_in_files(directory):
    """
    Recursively processes all files in the given directory, converting Godot 3.5 tile data to 4.3 format.

    :param directory: The root directory to search for files.
    """
    for subdir, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file.endswith(('.tscn', '.tres', '.txt', '.gd', '.cfg')):
                process_file_for_tile_data_conversion(file_path)


def process_file_for_tile_data_conversion(file_path):
    """
    Processes a single file and replaces Godot 3.5 tile data with Godot 4.3 tile data if applicable.

    :param file_path: The path to the file to be processed.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        modified = False
        new_lines = []

        for line in lines:
            if 'tile_data = PoolIntArray' in line:
                # Extract tile data from the line
                numbers = re.findall(r'-?\d+', line)
                tile_data_gd35 = list(map(int, numbers))

                # Create a mapping and convert tile data
                id_mapping = map_tile_ids_between_formats(tile_data_for_mapping_gd35, tile_data_for_mapping_gd43)
                tile_data_gd43 = convert_tile_data_using_mapping(tile_data_gd35, id_mapping)

                # Generate new tile data string for the file
                tile_data_gd43_string = "format = 2\n" + format_tile_data_as_string(tile_data_gd43)
                new_lines.append(tile_data_gd43_string + '\n')
                modified = True
            else:
                new_lines.append(line)

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Updated file: {file_path}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


# Example usage
home_dir = os.path.expanduser("~")
project_dir = os.path.join(home_dir, "git/jomtry")
update_tile_data_in_files(project_dir)
