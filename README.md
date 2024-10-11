# TileMap Godot Version Converter

A tool to convert TileMaps from Godot 3.5 to Godot 4.3.

After conversion, the TileMaps in Godot 4.3 must be manually converted to TileMapLayers.

## Steps to Convert

1. **Duplicate the project**  
   Create two project copies, one for Godot 3.5 and one for Godot 4.3. The 4.3 project will be used to create references to tiles. Godot's internal version converter will automatically remove the TileMap data from the 4.3 project. Therefore this project will later be removed. 

2. **Set up the TileMap in both projects**  
   - Create a TileMap and place all the tiles (auto tiles included) in both the Godot 3.5 and Godot 4.3 projects. You may need to fix the TileSet for the 4.3 project.
   - Ensure the tiles are positioned identically in both projects.   
   - **Important:** Use `TileMap`, not `TileMapLayer`, in the Godot 4.3 project.
   ![Screenshot 2024-10-11 at 21.44.21.png](Screenshot%202024-10-11%20at%2021.44.21.png)

3. **Extract tile data**  
   - Open the scene file in a text editor (e.g., VS Code).  
   - Copy the numbers from the `tile_data` parameter under the TileMap node in the Godot 3.5 project.  
   - Add these numbers to the `tile_data_for_mapping_gd35` variable in `main.py`.  
   - Similarly, copy the `tile_data` from the Godot 4.3 project and add it to the `tile_data_for_mapping_gd43` variable in `main.py`.

4. **Specify project directory**  
   Set the path of the Godot 3.5 project in the `project_dir` variable in `main.py`.

5. **Run the script**  
   After setting up the tile data and project directory, run the script to perform the conversion.

6. **Final conversion to Godot 4.3**  
   After the script completes, you can now convert the Godot 3.5 project to Godot 4.3.