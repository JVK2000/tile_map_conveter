def map_tile_ids_between_formats(tile_data_gd35, tile_data_gd43):
    """
    Map tile IDs from the Godot 3.5 format to the Godot 4.3 format.

    :param tile_data_gd35: List of tile data from Godot 3.5.
    :param tile_data_gd43: List of tile data from Godot 4.3.
    :return: A dictionary mapping tiles from the 3.5 format to their corresponding tiles in the 4.3 format.
    """
    num_tiles = len(tile_data_gd35) // 3

    # Extract positions, tile IDs, and alternate data for both formats
    num_gd35_tile_pos = tile_data_gd35[::3]
    num_gd43_tile_pos = tile_data_gd43[::3]
    num_gd35_tile_ids = tile_data_gd35[1::3]
    num_gd43_tile_ids = tile_data_gd43[1::3]
    num_gd35_tile_alt = tile_data_gd35[2::3]
    num_gd43_tile_alt = tile_data_gd43[2::3]

    id_map = {}
    for i in range(num_tiles):
        # Find the corresponding tile position in the 4.3 data
        gd43_i = num_gd43_tile_pos.index(num_gd35_tile_pos[i])

        # Create tuple pairs for the tile IDs and alternate data
        gd35_tuple = (num_gd35_tile_ids[i], num_gd35_tile_alt[i])
        gd45_tuple = (num_gd43_tile_ids[gd43_i], num_gd43_tile_alt[gd43_i])

        # Map the Godot 3.5 tile data to the 4.3 tile data
        id_map[gd35_tuple] = gd45_tuple

    return id_map


def convert_tile_data_using_mapping(tile_data, id_mapping):
    """
    Convert Godot 3.5 tile data to Godot 4.3 format using a mapping of tile IDs.

    :param tile_data: List of tile data from the Godot 3.5 format.
    :param id_mapping: Dictionary mapping tile data pairs from 3.5 to 4.3 format.
    :return: Updated list of tile data where the mapped values are replaced.
    """
    updated_lst = tile_data.copy()

    # Iterate over the tile data in chunks of 3 (position, ID, alternate data)
    for i in range(0, len(tile_data), 3):
        # Get the tile ID and alternate data
        tile_data_1 = tile_data[i + 1]
        tile_data_2 = tile_data[i + 2]

        # Check if the pair is in the mapping, and replace it if found
        if (tile_data_1, tile_data_2) in id_mapping:
            # Get the new mapped value
            new_tile_data_1, new_tile_data_2 = id_mapping[(tile_data_1, tile_data_2)]
            updated_lst[i + 1] = new_tile_data_1
            updated_lst[i + 2] = new_tile_data_2

    return updated_lst


def format_tile_data_as_string(tile_data):
    """
    Format a list of tile data into a string for use in a Godot scene file.

    :param tile_data: List of integers representing the tile data.
    :return: A formatted string representing the tile data in Godot's PackedInt32Array format.
    """
    list_str = ', '.join(map(str, tile_data))
    return f"layer_0/tile_data = PackedInt32Array( {list_str} )"
