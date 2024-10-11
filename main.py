import os
import re
from id_mapping import *


tile_data_for_mapping_gd43 = [0, 0, 0, 1, 10, 0, 2, 5, 0, 3, 3, 0, 4, 4, 0, 5, 6, 0, 6, 1, 0, 7, 1, 1, 8, 1, 2, 9, 1, 3, 10, 7, 0,
                  11, 2, 0, 12, 9, 0, 13, 8, 0, 65542, 1, 1, 65543, 65537, 1, 65544, 131073, 1, 65545, 196609, 1, 65546,
                  7, 1, 65547, 65538, 0, 65549, 8, 1, 131078, 1, 2, 131079, 65537, 2, 131080, 131073, 2, 131081, 196609,
                  2, 131082, 7, 2, 131083, 131074, 0, 131085, 8, 2, 196614, 1, 3, 196615, 65537, 3, 196616, 131073, 3,
                  196617, 196609, 3, 196619, 196610, 0]
tile_data_for_mapping_gd35 = [0, 0, 0, 1, 17, 0, 2, 19, 0, 3, 14, 0, 4, 15, 0, 5, 18, 0, 6, 1, 0, 7, 1, 1, 8, 1, 2, 9, 1, 3, 10, 11,
                  0, 11, 21, 0, 12, 16, 0, 13, 13, 0, 65542, 1, 65536, 65543, 1, 65537, 65544, 1, 65538, 65545, 1,
                  65539, 65546, 11, 65536, 65547, 21, 1, 65549, 13, 65536, 131078, 1, 131072, 131079, 1, 131073, 131080,
                  1, 131074, 131081, 1, 131075, 131082, 11, 131072, 131083, 21, 2, 131085, 13, 131072, 196614, 1,
                  196608, 196615, 1, 196609, 196616, 1, 196610, 196617, 1, 196611, 196619, 21, 3]


def replace_gd35_with_gd43_tile_data_in_dir(root_folder):
    """
    Recursively processes all files in the given directory, converting Godot 3.5 tile data to 4.3 format.

    :param directory: The root directory to search for files.
    """
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file.endswith(('.tscn', '.tres', '.txt', '.gd', '.cfg')):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    modified = False

                    new_lines = []
                    for line in lines:
                        if 'tile_data = PoolIntArray' in line:
                            numbers = re.findall(r'-?\d+', line)
                            tile_data_gd35 = list(map(int, numbers))
                            id_mapping = map_tile_ids_between_formats(tile_data_for_mapping_gd35, tile_data_for_mapping_gd43)

                            tile_data_gd43 = convert_tile_data_using_mapping(tile_data_gd35, id_mapping)
                            tile_data_gd43_string = "format = 2\n" + format_tile_data_as_string(tile_data_gd43)

                            new_lines.append(tile_data_gd43_string + '\n')
                            modified = True
                        else:
                            new_lines.append(line)

                    if modified:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(new_lines)
                        print(f"Updated file: {file_path}")
                        return

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")


home_dir = os.path.expanduser("~") 
project_dir = home_dir + "/git/test_1"
replace_gd35_with_gd43_tile_data_in_dir(project_dir)