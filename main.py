import base64
import struct

origin_4_3_data = "AAAAAAAADQAAAAAAAAABAAAADQABAAAAAAAAAAEADQAAAAEAAAABAAEADQABAAEAAAACAAAADQACAAAAAAACAAEADQACAAEAAAAHAAEADQADAAEAAAAHAAAADQADAAEAAAAKAAAADQADAAEAAAAKAAEADQADAAEAAAAJAAEADQADAAEAAAAIAAEADQADAAEAAAAIAAAADQADAAEAAAAJAAAADQADAAEAAAALAAEADQADAAEAAAALAAAADQADAAEAAAD+//7/DQAAAAAAAAD+//3/DQAAAAAAAAD9//3/DQAAAAAAAAD9//7/DQAAAAAAAAA="


def decode(encoded_data):
    binary_data = base64.b64decode(encoded_data)
    #print(f"Length of binary data: {len(binary_data)} bytes")

    try:
        decoded_values = struct.iter_unpack('<H', binary_data)  # 16-bit unsigned integers
        #decoded_values = struct.iter_unpack('<B', binary_data)  # 8-bit unsigned integers (bytes)
        decoded_list = [value[0] for value in decoded_values]
        decoded_list.pop(0)

        if False:
            print("Decoded values:")
            print(decoded_list)
            print("size:")
            print(len(decoded_list)/6)
            group_size = 6
            num_groups = len(decoded_list) // group_size

            for i in range(num_groups):
                print(f"Tile {i + 1}: {decoded_list[i * group_size:(i + 1) * group_size]}")

        return decoded_list

    except struct.error as e:
        print(f"Struct unpack error: {e}")


"""
first value of the entire string is 0
then every 6 values is for one tile.
the first is the 
the

[0, 0, 13, 0, 0, 0]

-> [coord_x, coord_y, source_id, tile_map_x_cord, tile_map_y_cord, alternative_tile]
[tile_map_x_cord, tile_map_y_cord, source_id, coord_x, coord_y, alternative_tile]

"""
[0,
 1, 0, 1, 4, 1, 0,
 2, 0, 1, 4, 1, 0,
 1, 1, 1, 4, 2, 0,
 2, 1, 1, 4, 2, 0
 ]



## for godot 3.5

tile_data = [1, 0, 0, 2, 0, 1, 65537, 0, 65536, 65538, 0, 65537]
index_data = tile_data[::3]
alt_data = tile_data[2::3]
print(tile_data)
print(alt_data)


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


pos_data = tile_data[::3]
source_data = tile_data[1::3]
tile_map_pos_data = tile_data[2::3]
tile_map_data_4_3 = [0]
size = 32
region = ( 96, 32, 64, 64 )

for i in range(len(tile_data) // 3):
    pos = decode_tile_position(pos_data[i])
    coord_x = pos[0]
    coord_y = pos[1]

    source_id = source_data[i] + 1

    tile_map_pos = decode_tile_position(tile_map_pos_data[i])
    tile_map_x_cord = tile_map_pos[0] + region[0] // size
    tile_map_y_cord = tile_map_pos[1] + region[1] // size
    print(tile_map_pos)

    alt_tile = 0

    tile_map_data_4_3.append(coord_x)
    tile_map_data_4_3.append(coord_y)
    tile_map_data_4_3.append(source_id)
    tile_map_data_4_3.append(tile_map_x_cord)
    tile_map_data_4_3.append(tile_map_y_cord)
    tile_map_data_4_3.append(0)


def encode(decoded_list):
    binary_data = bytearray()

    # Repack the values exactly as they were unpacked
    for value in decoded_list:
        packed_value = struct.pack('<H', value)  # Pack the 16-bit value back
        binary_data.extend(packed_value)

    # Now, convert the binary data back to base64
    encoded_data = base64.b64encode(binary_data).decode('utf-8')

    return encoded_data


#print("origin: ", origin_4_3_data)
#print("decoded: ", decode(origin_4_3_data))
#print("encoded: ", encode(decode(origin_4_3_data)))
#print(origin_4_3_data == encode(decode(origin_4_3_data)))

#print("tile_map_data: ", encode())

print("tile_map_data_4_3: ", tile_map_data_4_3)
print("tile_map_data_4_3_encoded: ", encode(tile_map_data_4_3))


a = [0, 0, 1, 0, 0, 0, 1, 0, 4, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 4, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 4, 0, 2, 0, 0, 0, 2, 0, 1, 0, 1, 0, 4, 0, 2, 0, 0, 0]
print(a[::2])