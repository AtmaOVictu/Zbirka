#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ustvari ikono za SISTEM ∅→∆→∂→∮
Instructions:
1. Install PIL: pip install Pillow
2. Run: python create_icon.py
3. ICO file will be created as icon.ico
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Size for icon (multiple sizes for .ico format)
sizes = [16, 24, 32, 48, 64, 128, 256]
output_path = os.path.join(os.path.dirname(__file__), "icon.ico")

# Colors
bg_color = (46, 52, 64)  # #2e3440
primary_color = (136, 192, 208)  # #88c0d0
text_color = (224, 224, 224)  # #e0e0e0

# Create a list of images for the ICO file
images = []

for size in sizes:
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw background circle
    draw.ellipse([(0, 0), (size-1, size-1)], fill=(bg_color[0], bg_color[1], bg_color[2], 255))
    
    # Draw the ∅→∆→∂→∮ symbols in a circle
    # Calculate positions
    center = size // 2
    radius = size // 3
    
    # Symbols and their positions
    symbols = ['∅', '∆', '∂', '∮']
    angles = [45, 135, 225, 315]  # degrees
    
    # Try to use a font that supports these symbols
    try:
        font = ImageFont.truetype("Segoe UI Symbol", size // 4)
    except:
        try:
            font = ImageFont.truetype("Arial Unicode MS", size // 4)
        except:
            font = ImageFont.load_default()
    
    for i, symbol in enumerate(symbols):
        angle_rad = (angles[i] - 90) * (3.14159 / 180)  # Convert to radians and offset
        x = center + radius * 0.7 * (i % 2 * 2 - 1)  # Alternate sides
        y = center + radius * 0.7 * ((i // 2) * 2 - 1)
        
        # Draw symbol
        draw.text((x - size//16, y - size//16), symbol, font=font, fill=primary_color)
    
    # Add a small center circle
    if size > 32:
        draw.ellipse([(center - size//10, center - size//10), 
                      (center + size//10, center + size//10)], 
                     fill=primary_color)
    
    images.append(img)

# Save as ICO file
try:
    images[0].save(output_path, format='ICO', sizes=[(s, s) for s in sizes])
    print(f"✅ ICO file created: {output_path}")
    print(f"   Sizes: {sizes}")
except Exception as e:
    # Fallback: save as PNG
    png_path = output_path.replace('.ico', '.png')
    images[-1].save(png_path, format='PNG')
    print(f"⚠️  Could not create ICO, saved as PNG: {png_path}")
    print(f"   Error: {e}")
