#!/usr/bin/env python3
import os
import zlib
import base64
import urllib.request
import glob

# Paths
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PUML_DIR = os.path.join(WORKSPACE_ROOT, '_files', 'uml', 'plantUml')
OUT_DIR = os.path.join(WORKSPACE_ROOT, 'assets', 'images', 'uml', 'plantUml')

def encode_plantuml(text):
    """Compress and encode the PlantUML text for the Kroki API."""
    compressed = zlib.compress(text.encode('utf-8'), 9)
    return base64.urlsafe_b64encode(compressed).decode('utf-8').rstrip('=')

def main():
    if not os.path.exists(PUML_DIR):
        print(f"Directory not found: {PUML_DIR}")
        print("Please create the directory and add some .puml files.")
        return

    os.makedirs(OUT_DIR, exist_ok=True)
    puml_files = glob.glob(os.path.join(PUML_DIR, '*.puml'))
    
    if not puml_files:
        print(f"No .puml files found in {PUML_DIR}")
        return
        
    print(f"Found {len(puml_files)} .puml file(s). Starting conversion...")
    
    for puml_file in puml_files:
        basename = os.path.basename(puml_file)
        name_only = os.path.splitext(basename)[0]
        out_file = os.path.join(OUT_DIR, f"{name_only}.svg")
        
        with open(puml_file, 'r', encoding='utf-8') as f:
            text = f.read()
            
        encoded = encode_plantuml(text)
        url = f"https://kroki.io/plantuml/svg/{encoded}"
        
        print(f"Converting: {basename}...")
        try:
            # Fetch the SVG from Kroki API
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                svg_data = response.read()
                
            # Save the SVG
            with open(out_file, 'wb') as f:
                f.write(svg_data)
            print(f"  -> Saved successfully to: assets/images/{name_only}.svg")
            
        except Exception as e:
            print(f"  -> Error converting {basename}: {e}")

if __name__ == '__main__':
    main()
