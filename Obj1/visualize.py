#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visualize.py - Vizualizacija mreže kamnov
==========================================
Funkcije:
- DOT → PNG (z Graphviz)
- DOT → SVG
- DOT → HTML (interaktivni)
- HTML vizualizacija (z PyVis)

Zahtevano:
- Graphviz (za PNG/SVG)
- pip install pyvis (za HTML)
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime

DATA_DIR = Path.cwd()
DOT_FILE = DATA_DIR / "mreza.dot"
PNG_FILE = DATA_DIR / "mreza.png"
SVG_FILE = DATA_DIR / "mreza.svg"
HTML_FILE = DATA_DIR / "mreza.html"


def dot_to_png(dot_file: str = str(DOT_FILE), png_file: str = str(PNG_FILE)):
    """Pretvori DOT datoteko v PNG (z Graphviz dot)"""
    import shutil
    if not os.path.exists(dot_file):
        print("❌ Datoteka mreza.dot ne obstaja!")
        print("Ustvari: python tools.py dot")
        return None
    try:
        subprocess.run(['dot', '-Tpng', dot_file, '-o', png_file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Ustvarjen: {png_file}")
        return png_file
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Graphviz (dot) ni nameščen!")
        print("Namestitev: https://graphviz.org/download/")
        return None


def dot_to_svg(dot_file: str = str(DOT_FILE), svg_file: str = str(SVG_FILE)):
    """Pretvori DOT datoteko v SVG"""
    if not os.path.exists(dot_file):
        print("❌ Datoteka mreza.dot ne obstaja!")
        print("Ustvari: python tools.py dot")
        return None
    try:
        subprocess.run(['dot', '-Tsvg', dot_file, '-o', svg_file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Ustvarjen: {svg_file}")
        return svg_file
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Graphviz (dot) ni nameščen!")
        print("Namestitev: https://graphviz.org/download/")
        return None


def dot_to_html_pyvis():
    """Ustvari interaktivni HTML graf z PyVis"""
    try:
        from pyvis.network import Network
        import json
        
        # Naloži podatke iz JSON
        with open(DATA_DIR / "database.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        kamni = data.get('kamni', {})
        
        # Ustvari mrežo
        net = Network(
            height="750px",
            width="100%",
            bgcolor="#2e3440",
            font_color="#e0e0e0",
            directed=True,
            notebook=False
        )
        
        # Dodaj vozlišča (kamne)
        for kamen_id, kamen_data in kamni.items():
            net.add_node(
                kamen_id,
                label=f"{kamen_id}\n{kamen_data.get('naslov', '')[:20]}",
                title=f"{kamen_id}: {kamen_data.get('naslov', '')}",
                color={
                    'CVII': '#88c0d0',
                    'CVIII': '#81a1c1',
                    'CIX': '#5e81ac',
                    'CX': '#bf616a',
                    'CXI': '#d08770',
                    'CXII': '#ebcb8b',
                    'CXIII': '#a3be8c'
                }.get(kamen_id, '#ffffff')
            )
        
        # Dodaj povezave (predlagane)
        povezave = [
            ('CVII', 'CVIII'), ('CVII', 'CIX'), ('CVII', 'CX'),
            ('CVIII', 'CIX'), ('CVIII', 'CX'), ('CVIII', 'CXI'),
            ('CIX', 'CX'), ('CIX', 'CXII'), ('CIX', 'CXIII'),
            ('CX', 'CXI'), ('CX', 'CXII'), ('CX', 'CXIII'),
            ('CXI', 'CXII'), ('CXI', 'CXIII'),
            ('CXII', 'CXIII')
        ]
        for src, tgt in povezave:
            net.add_edge(src, tgt, color='#4c566a', width=1)
        
        # Shrani HTML
        net.save_graph(str(HTML_FILE))
        print(f"✅ Ustvarjen: {HTML_FILE}")
        print(f"   Odpri v brskalniku: file://{HTML_FILE}")
        return HTML_FILE
        
    except ImportError:
        print("❌ PyVis ni nameščen!")
        print("Namestitev: pip install pyvis")
        return None
    except Exception as e:
        print(f"❌ Napaka: {str(e)}")
        return None


def generate_all_visualizations():
    """Generira vse vizualizacije (PNG, SVG, HTML)"""
    print("🎨 Generiram vizualizacije...")
    print("=" * 60)
    
    # DOT → PNG
    png_result = dot_to_png()
    if png_result:
        print(f"   ✅ PNG: {png_result}")
    else:
        print("   ⚠️  PNG: Graphviz ni nameščen (neobvezno)")
    
    # DOT → SVG
    svg_result = dot_to_svg()
    if svg_result:
        print(f"   ✅ SVG: {svg_result}")
    else:
        print("   ⚠️  SVG: Graphviz ni nameščen (neobvezno)")
    
    # HTML (PyVis)
    html_result = dot_to_html_pyvis()
    if html_result:
        print(f"   ✅ HTML: {html_result}")
    else:
        print("   ⚠️  HTML: PyVis ni nameščen (neobvezno)")
    
    print("=" * 60)
    print("✅ Vizualizacije končane!")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Uporaba visualize.py:")
        print("=" * 60)
        print("  png       - DOT → PNG")
        print("  svg       - DOT → SVG")
        print("  html      - Interaktivni HTML (PyVis)")
        print("  all       - Vse vizualizacije")
        print("=" * 60)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'png':
        dot_to_png()
    elif command == 'svg':
        dot_to_svg()
    elif command == 'html':
        dot_to_html_pyvis()
    elif command == 'all':
        generate_all_visualizations()
    else:
        print(f"Neznan ukaz: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
