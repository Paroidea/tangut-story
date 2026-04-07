import os
import glob
import subprocess

# Paths relative to the script's new location in "assets/figure"
SEARCH_PATTERN = "*.mermaid"
PUPPETEER_CONFIG = os.path.join("..", "..", "..", "puppeteer_config.json")
MERMAID_CONFIG = "mermaid_config.json"

def run_mmdc_conversion():
    # Find all .mermaid files in the current directory
    mermaid_files = glob.glob(SEARCH_PATTERN)
    
    if not mermaid_files:
        print(f"No mermaid files found in the current directory.")
        return

    for file_path in mermaid_files:
        # Get filename without extension
        file_name = os.path.basename(file_path)
        base_name_only, _ = os.path.splitext(file_name)
        
        # Split by '+' to determine target directory and new filename
        parts = base_name_only.split('+')
        
        if len(parts) >= 2:
            target_dir = os.path.join("..", "..", "static", "images", parts[0])
            new_filename = "_".join(parts[1:])
            output_file = os.path.join(target_dir, f"{new_filename}.svg")
            
            # Create folder if it doesn't exist
            os.makedirs(target_dir, exist_ok=True)
        else:
            # Fallback for files without '+'
            output_file = f"{base_name_only}.svg"

        # Skip if target is newer than source
        if os.path.exists(output_file):
            if os.path.getmtime(output_file) > os.path.getmtime(file_path):
                print(f"Skipping: {output_file} is up to date.")
                continue

        # Build and run the command
        command = [
            "mmdc",
            "-i", file_path,
            "-o", output_file,
            "-p", PUPPETEER_CONFIG,
            "-c", MERMAID_CONFIG
        ]
        
        print(f"Converting: {file_path} -> {output_file}")
        
        try:
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error converting {file_path}: {e}")
        except FileNotFoundError:
            print("Error: 'mmdc' command not found. Please ensure mermaid-cli is installed.")
            return

    print("Process complete.")

if __name__ == "__main__":
    run_mmdc_conversion()
