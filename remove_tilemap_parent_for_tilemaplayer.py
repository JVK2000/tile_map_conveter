import os
import re


def process_godot_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Regex patterns to find TileMap and TileMapLayer nodes
    tilemap_pattern = re.compile(r'\[node name="TileMap" parent="\." instance=ExtResource\("(\d+)"\)\]')
    tilemaplayer_pattern = re.compile(r'\[node name="(\w+)" type="TileMapLayer" parent="TileMap"\]')

    new_lines = []
    tilemap_instance = None
    layer_name = None
    inside_tilemaplayer = False

    for line in lines:
        # Find the TileMap node and extract its instance number
        tilemap_match = tilemap_pattern.match(line)
        if tilemap_match:
            tilemap_instance = tilemap_match.group(1)
            continue  # Remove the TileMap node by skipping the line

        # Find the TileMapLayer node and capture the layer name
        tilemaplayer_match = tilemaplayer_pattern.match(line)
        if tilemaplayer_match:
            layer_name = tilemaplayer_match.group(1)
            inside_tilemaplayer = True
            # Replace the type and parent, and use the TileMap instance
            new_lines.append(f'[node name="{layer_name}" parent="." instance=ExtResource("{tilemap_instance}")]\n')
            continue

        # Process TileMapLayer data until the next node or section
        if inside_tilemaplayer:
            if line.startswith('['):  # A new section begins, so exit the TileMapLayer processing
                inside_tilemaplayer = False
            # else:
                # Append lines related to TileMapLayer node data
            new_lines.append(line)
        else:
            # Add lines that are not affected by TileMap or TileMapLayer processing
            new_lines.append(line)

    # Write the modified lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(new_lines)


def process_directory(directory):
    # Iterate through all files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.tscn'):  # Process only Godot scene files
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}...")
                process_godot_file(file_path)


if __name__ == "__main__":
    # Change the directory path to the folder containing your Godot scene files
    directory_path = r'C:\Users\josef\git\pixiformer\pixiformer\levels'
    process_directory(directory_path)
