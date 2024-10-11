def decode_tile_data(data):
    # Extract tile ID (lower 16 bits)
    tile_id = data & 0xFFFF

    # Extract atlas coordinates
    atlas_x = (data >> 16) & 0xFF
    atlas_y = (data >> 24) & 0xFF

    return tile_id, (atlas_x, atlas_y)


# Example usage:
tile_data_1 = 65537
tile_data_2 = 65542

tile_id_1, atlas_coords_1 = decode_tile_data(tile_data_1)
print(f"Tile 1 ID: {tile_id_1}, Atlas Coordinates: {atlas_coords_1}")

tile_id_2, atlas_coords_2 = decode_tile_data(tile_data_2)
print(f"Tile 2 ID: {tile_id_2}, Atlas Coordinates: {atlas_coords_2}")