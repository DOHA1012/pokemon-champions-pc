import zipfile
import re
import os
import sys
import struct

apk_path = "base.apk"
ico_path = "pokemon_icon.ico"

print("Opening APK...")
with zipfile.ZipFile(apk_path, 'r') as z:
    namelist = z.namelist()
    
    # Filter for potential launcher icons
    candidates = []
    for name in namelist:
        if name.endswith('.png') and ('ic_launcher' in name or 'app_icon' in name or 'icon' in name):
            if 'foreground' not in name and 'background' not in name:
                candidates.append(name)
                
    if not candidates:
        candidates = [name for name in namelist if name.endswith('.png') and 'icon' in name.lower()]

    if not candidates:
        print("No icon candidate found!")
        sys.exit(1)
        
    print(f"Found {len(candidates)} candidates. Selecting the highest resolution...")
    
    def sort_key(name):
        if 'xxxhdpi' in name:
            return 6
        elif 'xxhdpi' in name:
            return 5
        elif 'xhdpi' in name:
            return 4
        elif 'hdpi' in name:
            return 3
        elif 'mdpi' in name:
            return 2
        elif 'ldpi' in name:
            return 1
        return 0

    candidates.sort(key=sort_key, reverse=True)
    best_candidate = candidates[0]
    print(f"Selected icon: {best_candidate}")
    
    # Extract PNG bytes
    png_bytes = z.read(best_candidate)
    
    # Convert PNG bytes to ICO format
    ico_header = struct.pack("<HHH", 0, 1, 1)
    
    width = 0
    height = 0
    if len(png_bytes) > 24 and png_bytes[12:16] == b"IHDR":
        width, height = struct.unpack(">II", png_bytes[16:24])
        print(f"PNG dimensions: {width}x{height}")
        
    ico_w = 0 if width >= 256 else width
    ico_h = 0 if height >= 256 else height
    
    png_size = len(png_bytes)
    offset = 6 + 16
    
    directory_entry = struct.pack("<BBBBHHII", ico_w, ico_h, 0, 0, 1, 32, png_size, offset)
    
    with open(ico_path, "wb") as f:
        f.write(ico_header)
        f.write(directory_entry)
        f.write(png_bytes)
        
    print(f"Successfully created ICO file at: {ico_path}")
