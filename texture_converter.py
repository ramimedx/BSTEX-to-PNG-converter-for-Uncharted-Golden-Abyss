import os
import sys
import subprocess

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        return os.path.dirname(os.path.abspath(__file__))

def find_noesis(script_dir):
    valid_names = {"noesis.exe", "noesis64.exe", "Noesis.exe", "Noesis64.exe"}
    
    for root, dirs, files in os.walk(script_dir):
        for filename in files:
            if filename.lower() in valid_names:
                return os.path.join(root, filename)
            
    fallback = r"C:\Program Files\Noesis\noesis.exe"
    if os.path.isfile(fallback):
        return fallback
        
    return None

def process_and_convert_textures(directory, noesis_path, default_dir):
    directory = directory.strip('"\'')
    
    if not directory:
        directory = default_dir

    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    print(f"\n--- Scanning directory & subfolders: {os.path.abspath(directory)} ---")
    
    processed_count = 0
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            base_name = os.path.splitext(filename)[0]
            gxt_path = os.path.join(root, base_name + ".gxt")
            png_path = os.path.join(root, base_name + ".png")
            
            try:
                # Read the first 36 bytes to inspect magic bytes (signatures)
                with open(file_path, "rb") as f:
                    header = f.read(36)
                
                # Check if it's already a GXT file by looking for 'GXT' magic bytes at offset 0
                if header[:3] == b'GXT':
                    gxt_path = file_path
                    print(f"[1/2] Verified GXT signature: {os.path.relpath(file_path, directory)}")
                
                # Check if it has a 32-byte wrapper with 'GXT' starting at offset 32
                elif len(header) >= 36 and header[32:35] == b'GXT':
                    with open(file_path, "rb") as f:
                        data = f.read()
                    
                    modified_data = data[32:]
                    with open(gxt_path, "wb") as f:
                        f.write(modified_data)
                        
                    print(f"[1/2] Stripped 32-byte header (GXT detected at offset 32): {os.path.relpath(file_path, directory)}")
                else:
                    # Skip files that don't match known texture signatures
                    continue

                # Convert .gxt to .png using Noesis via console mode (?cmode)
                result = subprocess.run(
                    [noesis_path, "?cmode", gxt_path, png_path, "-nopause"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0 and os.path.exists(png_path):
                    print(f"[2/2] Converted to PNG: {base_name}.png\n")
                    processed_count += 1
                else:
                    print(f"Warning: Noesis couldn't convert {filename}. Output: {result.stderr or result.stdout}\n")
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print(f"Done! Successfully processed {processed_count} file(s) to PNG.")

if __name__ == "__main__":
    print("=== Texture Converter ===")
    
    script_dir = get_base_dir()
    noesis_exe_path = find_noesis(script_dir)
    
    if not noesis_exe_path:
        print("\nError: Could not find 'noesis.exe' or 'noesis64.exe'.")
        print("Please place Noesis in the same folder (or a subfolder) as this tool.")
    else:
        print(f"Found Noesis at: {noesis_exe_path}\n")
        user_input = input(f"Paste folder path (or press enter to use tool's folder):\n> ")
        process_and_convert_textures(user_input, noesis_exe_path, script_dir)
    
    input("\nPress Enter to close this window...")
