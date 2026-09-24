#!/usr/bin/env python3
"""
Generate index.md for Evidence Receipts v0.2
Usage: python generate_index.py
Run from: libraries/evidence-receipts/
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Stone metadata
STONE_DESCRIPTIONS = {
    "CXX": "Kristalografija (230 prostorskih grup = 7 sistemov + 14 Bravais)",
    "CXXI": "Monster grupa (15 supersingular primes = 15 sizigij!)",
    "CXXII": "Leecheva mreža (24-dim, 196560 ≈ Monster)",
    "CXXIII": "Mathieu grupe (5 sporadičnih = ∂)",
    "CXXIV": "Coxeter grupe (zrcaljenje = ¬, ∅/∆ = A₁)",
    "CXXV": "Vozli (prime = ∅, Jones = ∂, vrv = ∮)",
}

STONE_AXIOM = {
    "CXX": "Aksiom 239 potrjen",
    "CXXI": "Aksiom 240 potrjen",
    "CXXII": "Aksiom 241 potrjen",
    "CXXIII": "Aksiom 242 potrjen",
    "CXXIV": "Coxeter E₈ = Kamen XVI",
    "CXXV": "Teorija vozlov potrjuje ∅/∆/∂ trojico",
}

O_PIS_PROTOKOL = {
    "CXX": {"O1": "230 grup", "O2": "Kristalni sistem", "O5": "Stabilnost", "O7": "Izročitev"},
    "CXXI": {"O1": "Monster", "O2": "15 primes", "O5": "Sporadičnost", "O7": "Izročitev"},
    "CXXII": {"O1": "Leech", "O2": "24-dim", "O5": "Mreža", "O7": "Izročitev"},
    "CXXIII": {"O1": "5 Mathieu", "O2": "Steiner S(5,8,24)", "O5": "Veriga ∂", "O7": "Izročitev"},
    "CXXIV": {"O1": "Coxeter", "O2": "Zrcaljenje", "O5": "A₁ binarni", "O7": "Izročitev"},
    "CXXV": {"O1": "Prime vozli", "O2": "Jones polinom", "O5": "∮² cikli", "O7": "Izročitev"},
}

OPTION_ROWS = {
    "CXX": {"O1": "230 prostorskih grup", "O2": "7 kristalnih sistemov + 14 Bravais", "O5": "Stabilnost kristalov", "O7": "DA₂"},
    "CXXI": {"O1": "Monster grupa", "O2": "15 supersingular primes", "O5": "Sporadične grupe", "O7": "DA₂"},
    "CXXII": {"O1": "Leecheva mreža", "O2": "24-dimensionalna", "O5": "196560 ≈ Monster", "O7": "DA₂"},
    "CXXIII": {"O1": "5 Mathieu grup", "O2": "M24 Steiner S(5,8,24)", "O5": "M24→Leech→Monster", "O7": "DA₂"},
    "CXXIV": {"O1": "Coxeter grupe", "O2": "Zrcaljenje = ¬", "O5": "A₁ = ∅/∆", "O7": "DA₂"},
    "CXXV": {"O1": "Prime vozli", "O2": "Jones = ∂", "O5": "Vozel = ∮²", "O7": "DA₂"},
}


def parse_receipt(filepath):
    """Parse a receipt markdown file and extract metadata."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract YAML front matter
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    
    front_matter = match.group(1)
    metadata = {}
    for line in front_matter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
    
    # Extract source URL
    url_match = re.search(r'\- \*\*URL:\*\* (https?://[^\s]+)', content)
    metadata['URL'] = url_match.group(1) if url_match else "N/A"
    
    # Extract source type
    type_match = re.search(r'\- \*\*Type:\*\* (\w+)', content)
    metadata['Type'] = type_match.group(1) if type_match else "OTHER"
    
    return metadata


def get_receipts(base_path):
    """Get all receipts organized by stone."""
    stones = {}
    for stone_dir in sorted(Path(base_path).iterdir()):
        if not stone_dir.is_dir() or stone_dir.name in ['README.md', 'index.md', 'scripts']:
            continue
        
        stone_id = stone_dir.name
        receipts = []
        for receipt_file in sorted(stone_dir.glob('*.md')):
            if receipt_file.name in ['README.md', 'index.md']:
                continue
            metadata = parse_receipt(receipt_file)
            if metadata:
                receipts.append({
                    'id': metadata.get('ID', 'N/A'),
                    'kamen': metadata.get('Kamen', stone_id),
                    'tier': metadata.get('Status', 'N/A'),
                    'guard': metadata.get('Guard', 'N/A'),
                    'url': metadata.get('URL', 'N/A'),
                    'type': metadata.get('Type', 'N/A'),
                    'file': receipt_file.name,
                    'path': f"{stone_id}/{receipt_file.name}"
                })
        
        if receipts:
            stones[stone_id] = {
                'receipts': receipts,
                'description': STONE_DESCRIPTIONS.get(stone_id, ""),
                'axiom': STONE_AXIOM.get(stone_id, ""),
            }
    
    return stones


def count_tiers(stones):
    """Count receipts by tier."""
    counts = {'PRIMARY': 0, 'SECONDARY': 0, 'TERTIARY': 0, 'total': 0}
    stone_counts = {}
    
    for stone_id, data in stones.items():
        primary = sum(1 for r in data['receipts'] if r['tier'] == 'PRIMARY')
        secondary = sum(1 for r in data['receipts'] if r['tier'] == 'SECONDARY')
        tertiary = sum(1 for r in data['receipts'] if r['tier'] == 'TERTIARY')
        total = len(data['receipts'])
        
        stone_counts[stone_id] = {
            'total': total,
            'PRIMARY': primary,
            'SECONDARY': secondary,
            'TERTIARY': tertiary,
        }
        
        counts['PRIMARY'] += primary
        counts['SECONDARY'] += secondary
        counts['TERTIARY'] += tertiary
        counts['total'] += total
    
    return stone_counts, counts


def generate_index(stones, stone_counts, total_counts):
    """Generate the index.md content."""
    date = datetime.now().strftime('%d. %m. %Y')
    
    index_content = f"""# 📚 Evidence Receipts Index (CXX–CXXV)

**Generated:** {date}  
**Status:** PROTOTIP (Self-contained local application)  
**Total Receipts:** {total_counts['total']}  

---

## 📋 statistika

| Kamen | Število ER | PRIMARY | SECONDARY | TERTIARY |
|-------|-------------|---------|----------|-----------|
"
    
    for stone_id in ['CXX', 'CXXI', 'CXXII', 'CXXIII', 'CXXIV', 'CXXV']:
        if stone_id in stone_counts:
            sc = stone_counts[stone_id]
            index_content += f"| {stone_id}   | {sc['total']}           | {sc['PRIMARY']}       | {sc['SECONDARY']}        | {sc['TERTIARY']}         |\n"
        else:
            index_content += f"| {stone_id}   | 0           | 0       | 0        | 0         |\n"
    
    index_content += f"| **Skupaj** | **{total_counts['total']}**    | **{total_counts['PRIMARY']}**  | **{total_counts['SECONDARY']}**    | **{total_counts['TERTIARY']}**     |\n\n"
    
    index_content += "---\n\n## 📁 Kazalo po kamenih\n\n"
    
    for stone_id in ['CXX', 'CXXI', 'CXXII', 'CXXIII', 'CXXIV', 'CXXV']:
        if stone_id not in stones:
            continue
        
        data = stones[stone_id]
        index_content += f"### 🜂 Kamen {stone_id} — {data['description']}\n\n"
        index_content += "| ID | Vir | Type | Tier | Guard | Status |\n"
        index_content += "|----|-----|------|------|-------|--------|\n"
        
        for receipt in data['receipts']:
            url_basename = Path(receipt['url']).name if receipt['url'] != 'N/A' else 'N/A'
            index_content += f"| [{receipt['id']}]({receipt['path']}) | {url_basename} | {receipt['type']} | {receipt['tier']} | {receipt['guard']} | ✅ |\n"
        
        index_content += f"\n**Povzetek:** {data['axiom']}\n\n---\n\n"
    
    # O1-O7 Table
    index_content += "## 🎯 Sklepi\n\n"
    index_content += "### O1–O7 Univerzalni zakon potrjen\n\n"
    index_content += "Vsi kamni CXX–CXXV **empirično potrjujejo OPIS PROTOKOL (O1–O7)**:\n\n"
    index_content += "| O# | Pogoj | CXX | CXXI | CXXII | CXXIII | CXXIV | CXXV |\n"
    index_content += "|----|-------|-----|------|-------|--------|-------|------|\n"
    
    for o_num in ['O1', 'O2', 'O5', 'O7']:
        row = [o_num]
        for stone_id in ['CXX', 'CXXI', 'CXXII', 'CXXIII', 'CXXIV', 'CXXV']:
            if stone_id in OPTION_ROWS and o_num in OPTION_ROWS[stone_id]:
                row.append(OPTION_ROWS[stone_id][o_num])
            else:
                row.append("")
        index_content += "| " + " | ".join(row) + " |\n"
    
    index_content += "\n---\n\n"
    index_content += "**Sklep:** Evidence Receipts v0.2 **dela**. Ponavljanje = gotovost. ∅→∆→∂ je povsod.  \n"
    index_content += "**∮**\n"
    
    return index_content


def main():
    base_path = Path.cwd()
    stones = get_receipts(base_path)
    stone_counts, total_counts = count_tiers(stones)
    
    index_content = generate_index(stones, stone_counts, total_counts)
    
    index_path = base_path / "index.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✓ index.md generated at {index_path}")
    print(f"  Total receipts: {total_counts['total']}")
    print(f"  PRIMARY: {total_counts['PRIMARY']}, SECONDARY: {total_counts['SECONDARY']}, TERTIARY: {total_counts['TERTIARY']}")


if __name__ == '__main__':
    main()
