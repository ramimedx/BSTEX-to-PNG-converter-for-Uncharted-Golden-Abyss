# BSTEX & GXT to PNG Texture Converter for Uncharted: Golden Abyss

A portable, recursive Python tool designed to batch convert proprietary game texture files (`.bstex` and `.gxt`) into standard `.png` format. It features automatic magic byte detection to safely strip proprietary wrappers and leverages *Noesis* (Credit to Rich Whitehouse) for GPU texture decoding. This has been tested only with game files belonging to **Uncharted: Golden Abyss PS Vita** game, but the tool may be updated to fulfill your specific game needs, modifying the script to handle the specific header of your file.

## Prerequisites
Because standard Python libraries cannot decode proprietary GPU formats like PVRTC-II (`PVRTII4BPP`), this tool requires **Noesis** by Rich Whitehouse.

1. Download [Noesis](https://richwhitehouse.com/index.php?content=inc_projects.php&showproject=91).
2. Place `noesis.exe` (or `noesis64.exe`) inside the `Noesis/` folder next to the script, or right next to the executable.

## Usage
1. Place the script (or compiled `.exe`) and Noesis in your working environment.
2. Open `process_textures.py` (or run it via terminal).
3. Paste the path to the folder containing your game textures when prompted (or press Enter to use the script's current directory).
