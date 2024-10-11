import os
import re
import base64
import struct



def decode_tile_position(encoded_index):
    # Extract the X coordinate (lower 16 bits)
    x = encoded_index & 0xFFFF
    if x >= 32768:  # Handle negative values for X
        x -= 65536

    # Extract the Y coordinate (upper 16 bits)
    y = (encoded_index >> 16) & 0xFFFF
    if y >= 32768:  # Handle negative values for Y
        y -= 65536

    return (x, y)


print(decode_tile_position(65537))
print(decode_tile_position(131073))
print(decode_tile_position(196609))


def gd35_to_43(tile_data_gd_3_5, region_data):
    pos_data = tile_data_gd_3_5[::3]
    source_data = tile_data_gd_3_5[1::3]
    tile_map_pos_data = tile_data_gd_3_5[2::3]
    tile_map_data_4_3 = [0]
    size = 32

    for i in range(len(tile_data_gd_3_5) // 3):
        pos = decode_tile_position(pos_data[i])
        coord_x = pos[0]
        coord_y = pos[1]

        source_id = source_data[i]

        tile_map_pos = decode_tile_position(tile_map_pos_data[i])
        tile_map_x_cord = tile_map_pos[0] + region_data[source_id][0] // size
        tile_map_y_cord = tile_map_pos[1] + region_data[source_id][1] // size

        alt_tile = 0

        tile_map_data_4_3.append(coord_x)
        tile_map_data_4_3.append(coord_y)
        tile_map_data_4_3.append(source_id)
        tile_map_data_4_3.append(tile_map_x_cord)
        tile_map_data_4_3.append(tile_map_y_cord)
        tile_map_data_4_3.append(alt_tile)

    return tile_map_data_4_3


def encode(decoded_list):
    binary_data = bytearray()

    # Repack the values exactly as they were unpacked
    for value in decoded_list:
        packed_value = struct.pack('<H', value)  # Pack the 16-bit value back
        binary_data.extend(packed_value)

    # Now, convert the binary data back to base64
    encoded_data = base64.b64encode(binary_data).decode('utf-8')

    return encoded_data


def extract_region_data(file_path):
    region_dict = {}
    region_pattern = re.compile(r"(\d+)/region = Rect2\(\s*(-?\d+),\s*(-?\d+),\s*(\d+),\s*(\d+)\s*\)")
    if file_path.endswith(('.tscn', '.tres', '.txt', '.gd', '.cfg')):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                match = region_pattern.match(line)
                if match:
                    index = int(match.group(1))
                    x, y, w, h = map(int, match.group(2, 3, 4, 5))
                    region_dict[index] = (x, y, w, h)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    return region_dict


def add_line_after_tile_data(root_folder):
    """
    Iterates through all files in the root_folder and its subfolders,
    searches for lines containing 'tile_data', and adds the new_line
    right after the matching line.

    Parameters:
    - root_folder: The path to the folder to search.
    - new_line: The line that will be added after any line containing 'tile_data'.
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

                    # Flag to check if any addition happened
                    modified = False

                    # Prepare new list of lines
                    new_lines = []
                    for line in lines:
                        new_lines.append(line)
                        if 'tile_data = PoolIntArray' in line or 'tile_data = PackedInt32Array' in line:

                            numbers = re.findall(r'-?\d+', line)
                            tile_data_godot_3_5 = list(map(int, numbers))
                            print(tile_data_godot_3_5)

                            region_data = extract_region_data(file_path)
                            print("region data: ", region_data)

                            tile_data_godot_4_3_list = gd35_to_43(tile_data_godot_3_5, region_data)
                            print(tile_data_godot_4_3_list)
                            tile_data_godot_4_3 = encode(tile_data_godot_4_3_list)

                            print("tile_data_godot_4_3: ", tile_data_godot_4_3)
                            tile_data_godot_4_3 = 'layer_0/tile_data = PackedByteArray("' + tile_data_godot_4_3 + '")'
                            print("tile_data_godot_4_3: ", tile_data_godot_4_3)
                            # tile_data_godot_4_3 = "hej"
                            # Add the new line directly after 'tile_data' line
                            new_lines.append(tile_data_godot_4_3 + '\n')
                            modified = True

                    # Write the modified content back to the file if any modifications were made
                    if modified:

                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(new_lines)

                        print(f"Updated file: {file_path}")

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")


# Example usage:
root_folder = r'C:\Users\josef\Documents\tilemap_3.5_c2'  # Replace with the path to your folder

add_line_after_tile_data(root_folder)