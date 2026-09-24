#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MARKERJI_EXTENDED - Univerzalni simbolski register za SISTEM ∅→∆→∂→∮
====================================================================
Avtor: Luka + Vibe
Datum: 19. 9. 2026

Vsebina:
- Vsi markerji sistema z opisom
- Funkcije za preverjanje in zamenjavo
- Konverzija med oblikami

Uporaba:
    from markerji_extended import MARKERJI, verify_markers, replace_markers
    
    # Prikaži vse markerje
    for marker, desc in MARKERJI.items():
        print(f"{marker}: {desc}")
    
    # Preveri, ali tekst vsebuje markerje
    text = "∅→∆→∂→∮"
    found = verify_markers(text)
    
    # Zamenjaj markerje (npr. za HTML)
    html_text = replace_markers(text, format='html')
"""

# ============================================================================
# OSNOVNI MARKERJI (∅→∆→∂→∮)
# ============================================================================

MARKERJI = {
    # Osnovni markerji sistema
    '\u2205': {'ime': 'Praznina', 'opis': 'Izvor, nič, prazen prostor', 'kategorija': 'osnovni', 'unicode': 'U+2205', 'html': '&empty;', 'latex': '\emptyset'},
    '\u2206': {'ime': 'Razlika', 'opis': 'Prehod, sprememba, razlika med stanji', 'kategorija': 'osnovni', 'unicode': 'U+2206', 'html': '&Delta;', 'latex': '\Delta'},
    '\u2202': {'ime': 'Vprašanje', 'opis': 'Rez, vprašanje, ločitev, delitev', 'kategorija': 'osnovni', 'unicode': 'U+2202', 'html': '&part;', 'latex': '\partial'},
    '\u222e': {'ime': 'Povratek', 'opis': 'Cikel, povratek, zaključek, integrala', 'kategorija': 'osnovni', 'unicode': 'U+222E', 'html': '&int;', 'latex': '\oint'},
    
    # Razširjeni markerji
    '\u29ef': {'ime': 'Tiheon', 'opis': 'Molk, praznina, ničnost kot izpolnjenost', 'kategorija': 'tiheon', 'unicode': 'U+29EF', 'html': None, 'latex': None},
    '\u27e1': {'ime': 'Resonanca', 'opis': 'Odziv, resonanca, sozvočje', 'kategorija': 'resonanca', 'unicode': 'U+27E1', 'html': None, 'latex': None},
    '\u2297': {'ime': 'Križ', 'opis': 'Križišče, produkt, presečišče', 'kategorija': 'operacije', 'unicode': 'U+2297', 'html': '&otimes;', 'latex': '\otimes'},
    '\u2298': {'ime': 'Prazni krog', 'opis': 'Prazna operacija, ničelna operacija', 'kategorija': 'operacije', 'unicode': 'U+2298', 'html': '&odot;', 'latex': '\odot'},
    '\u22a2': {'ime': 'Izpeljava', 'opis': 'Logična izpeljava, posledica', 'kategorija': 'logika', 'unicode': 'U+22A2', 'html': '&vdash;', 'latex': '\vdash'},
    '\u27c1': {'ime': 'Krog', 'opis': 'Zaprt cikel, celota', 'kategorija': 'geometrija', 'unicode': 'U+27C1', 'html': None, 'latex': None},
    '\u21af': {'ime': 'Strelca navzdol', 'opis': 'Usmerjenost, smer', 'kategorija': 'smeri', 'unicode': 'U+21AF', 'html': None, 'latex': None},
    
    # Pečati in potrditve
    'DA\u2082': {'ime': 'Pečat DA₂', 'opis': 'Potrditev, izročitev, sklenjen dogovor', 'kategorija': 'pečati', 'unicode': 'DA2', 'html': 'DA<sub>2</sub>', 'latex': 'DA_2'},
    '\u2611': {'ime': 'Kvadrat', 'opis': 'Pečat, potrditev, checkbox', 'kategorija': 'pečati', 'unicode': 'U+2611', 'html': '&radio;', 'latex': '\square'},
    '\u2713': {'ime': 'Križec', 'opis': 'Potrjeno, DA', 'kategorija': 'pečati', 'unicode': 'U+2713', 'html': '&check;', 'latex': '\checkmark'},
    '\u2717': {'ime': 'Križ', 'opis': 'Zavrtnjeno, NE', 'kategorija': 'pečati', 'unicode': 'U+2717', 'html': '&cross;', 'latex': '\times'},
    
    # Smeri in prehodi
    '\u2205\u2191': {'ime': 'Odprava', 'opis': 'Odstranitev, prekinitev, uničenje', 'kategorija': 'smeri', 'unicode': 'U+2205 U+2191', 'html': '&empty;&uarr;', 'latex': '\emptyset\uparrow'},
    '\u2205\u2193': {'ime': 'Vrnitev v praznino', 'opis': 'Reset, ponastavitev, povratek k izvoru', 'kategorija': 'smeri', 'unicode': 'U+2205 U+2193', 'html': '&empty;&darr;', 'latex': '\emptyset\downarrow'},
    '\u2206\u2192': {'ime': 'Prehod naprej', 'opis': 'Napredek, razvoj, rast', 'kategorija': 'smeri', 'unicode': 'U+2206 U+2192', 'html': '&Delta;&rarr;', 'latex': '\Delta\rightarrow'},
    '\u2206\u2190': {'ime': 'Prehod nazaj', 'opis': 'Povratek, razgradnja, zmanjšanje', 'kategorija': 'smeri', 'unicode': 'U+2206 U+2190', 'html': '&Delta;&larr;', 'latex': '\Delta\leftarrow'},
    
    '\u2202\u2191': {'ime': 'Vprašanje v viško dimenzijo', 'opis': 'Abstrakcija, generalizacija', 'kategorija': 'dimenzije', 'unicode': 'U+2202 U+2191', 'html': '&part;&uarr;', 'latex': '\partial\uparrow'},
    '\u2202\u2193': {'ime': 'Vprašanje v globino', 'opis': 'Konkretizacija, specializacija', 'kategorija': 'dimenzije', 'unicode': 'U+2202 U+2193', 'html': '&part;&darr;', 'latex': '\partial\downarrow'},
    '\u222e\u2192': {'ime': 'Cikel naprej', 'opis': 'Iteracija, ponavljanje', 'kategorija': 'cikli', 'unicode': 'U+222E U+2192', 'html': '&int;&rarr;', 'latex': '\oint\rightarrow'},
    
    # Matematični in logični simboli
    '\u2260': {'ime': 'Ne enako', 'opis': 'Negacija, razlika', 'kategorija': 'matematika', 'unicode': 'U+2260', 'html': '&ne;', 'latex': '\neq'},
    '\u2261': {'ime': 'Enako', 'opis': 'Identiteta, enakost', 'kategorija': 'matematika', 'unicode': 'U+2261', 'html': '&equiv;', 'latex': '\equiv'},
    '\u2208': {'ime': 'Pripada', 'opis': 'Element množice', 'kategorija': 'množice', 'unicode': 'U+2208', 'html': '&isin;', 'latex': '\in'},
    '\u2209': {'ime': 'Ne pripada', 'opis': 'Ni element množice', 'kategorija': 'množice', 'unicode': 'U+2209', 'html': '&notin;', 'latex': '\notin'},
    '\u2286': {'ime': 'Podmnožica', 'opis': 'Hierarhija, vsebovanost', 'kategorija': 'množice', 'unicode': 'U+2286', 'html': '&sube;', 'latex': '\subseteq'},
    '\u2288': {'ime': 'Nadmnožica', 'opis': 'Vsebovanje', 'kategorija': 'množice', 'unicode': 'U+2288', 'html': '&supe;', 'latex': '\supseteq'},
    '\u2229': {'ime': 'Presek', 'opis': 'Skupni del', 'kategorija': 'operacije', 'unicode': 'U+2229', 'html': '&cap;', 'latex': '\cap'},
    '\u222a': {'ime': 'Unija', 'opis': 'Združitev', 'kategorija': 'operacije', 'unicode': 'U+222A', 'html': '&cup;', 'latex': '\cup'},
    
    # Grški črke (za matematiko)
    '\u0394': {'ime': 'Delta', 'opis': 'Razlika, prehod', 'kategorija': 'grske', 'unicode': 'U+0394', 'html': '&Delta;', 'latex': '\Delta'},
    '\u03a9': {'ime': 'Omega', 'opis': 'Celota, končnost', 'kategorija': 'grske', 'unicode': 'U+03A9', 'html': '&Omega;', 'latex': '\Omega'},
    '\u03b1': {'ime': 'Alpha', 'opis': 'Začetek, izvor', 'kategorija': 'grske', 'unicode': 'U+03B1', 'html': '&alpha;', 'latex': '\alpha'},
    '\u03c9': {'ime': 'omega', 'opis': 'Končni rezultat', 'kategorija': 'grske', 'unicode': 'U+03C9', 'html': '&omega;', 'latex': '\omega'},
    
    # Specijalni simboli za sistem
    '\u25c8': {'ime': 'Sneg', 'opis': 'Belenje, razpad, postopno uničenje', 'kategorija': 'sistem', 'unicode': 'U+25C8', 'html': None, 'latex': None},
    '\u25cb': {'ime': 'Krog', 'opis': 'Celota, enotnost', 'kategorija': 'sistem', 'unicode': 'U+25CB', 'html': '&circ;', 'latex': '\circ'},
    '\u25a1': {'ime': 'Kvadrat', 'opis': 'Stabilnost, trdnost', 'kategorija': 'sistem', 'unicode': 'U+25A1', 'html': '&squf;', 'latex': '\square'},
    '\u25b3': {'ime': 'Zvezda', 'opis': 'Odločitev, usmerjenost', 'kategorija': 'sistem', 'unicode': 'U+25B3', 'html': None, 'latex': None},
    '\u25b2': {'ime': 'Triangel navzgor', 'opis': 'Rast, razvoj', 'kategorija': 'sistem', 'unicode': 'U+25B2', 'html': '&blacktriangleright;', 'latex': None},
    '\u25bc': {'ime': 'Triangel navzdol', 'opis': 'Pad, zmanjšanje', 'kategorija': 'sistem', 'unicode': 'U+25BC', 'html': '&blacktriangledown;', 'latex': None},
}

# ============================================================================
# FUNKCIJE
# ============================================================================

def verify_markers(text: str, required: list = None) -> dict:
    """
    Preveri, kateri markerji so prisotni v tekstu.
    
    Args:
        text: Vhodni tekst
        required: Seznam zahtevanih markerjev (če None, preveri vse)
    
    Returns:
        dict: {'found': list, 'missing': list, 'all_found': bool}
    """
    if required is None:
        required = list(MARKERJI.keys())
    
    found = [m for m in required if m in text]
    missing = [m for m in required if m not in text]
    
    return {
        'found': found,
        'missing': missing,
        'all_found': len(missing) == 0
    }


def replace_markers(text: str, format: str = 'html', mapping: dict = None) -> str:
    """
    Zamenjaj markerje z ustreznimi kodi za izbran format.
    
    Args:
        text: Vhodni tekst
        format: 'html', 'latex', 'unicode', ali 'name'
        mapping: Custom mapping (če None, uporabi MARKERJI)
    
    Returns:
        str: Tekst z zamenjanimi markerji
    """
    if mapping is None:
        mapping = MARKERJI
    
    result = text
    
    for marker, info in mapping.items():
        replacement = info.get(format)
        if replacement:
            result = result.replace(marker, replacement)
    
    return result


def get_markers_by_category(category: str = None) -> dict:
    """
    Vrni markerje po kategoriji.
    
    Args:
        category: Ime kategorije (osnovni, tiheon, operacije, itd.)
    
    Returns:
        dict: {marker: info}
    """
    if category is None:
        return MARKERJI
    
    return {m: info for m, info in MARKERJI.items() if info.get('kategorija') == category}


def get_marker_info(marker: str) -> dict:
    """
    Vrni informacije o markerju.
    
    Args:
        marker: Simbol markerja
    
    Returns:
        dict: Informacije o markerju
    """
    return MARKERJI.get(marker, {'error': 'Marker ne obstaja'})


def list_all_markers() -> list:
    """
    Vrni seznam vseh markerjev.
    
    Returns:
        list: Seznam markerjev
    """
    return list(MARKERJI.keys())


def count_markers_in_text(text: str) -> dict:
    """
    Preštej pojavitve markerjev v tekstu.
    
    Args:
        text: Vhodni tekst
    
    Returns:
        dict: {marker: count}
    """
    counts = {}
    for marker in MARKERJI.keys():
        counts[marker] = text.count(marker)
    return counts


def validate_text(text: str, required_markers: list = None) -> dict:
    """
    Validiraj tekst glede na zahtevane markerje.
    
    Args:
        text: Vhodni tekst
        required_markers: Seznam zahtevanih markerjev
    
    Returns:
        dict: {'valid': bool, 'missing': list, 'counts': dict}
    """
    if required_markers is None:
        required_markers = ['\u2205', '\u2206', '\u2202', '\u222e']
    
    result = verify_markers(text, required_markers)
    counts = count_markers_in_text(text)
    
    return {
        'valid': result['all_found'],
        'missing': result['missing'],
        'counts': counts
    }


def to_html(text: str) -> str:
    """
    Pretvori tekst v HTML z ustreznimi entitetami.
    
    Args:
        text: Vhodni tekst
    
    Returns:
        str: HTML tekst
    """
    return replace_markers(text, 'html')


def to_latex(text: str) -> str:
    """
    Pretvori tekst v LaTeX z ustreznimi komandami.
    
    Args:
        text: Vhodni tekst
    
    Returns:
        str: LaTeX tekst
    """
    return replace_markers(text, 'latex')


def format_for_display(text: str, format: str = 'html') -> str:
    """
    Formatiraj tekst za prikaz.
    
    Args:
        text: Vhodni tekst
        format: 'html', 'latex', ali 'unicode'
    
    Returns:
        str: Formatiran tekst
    """
    if format == 'html':
        return to_html(text)
    elif format == 'latex':
        return to_latex(text)
    else:
        return text


# ============================================================================
# UPORABA
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("MARKERJI_EXTENDED - Univerzalni simbolski register")
    print("=" * 60)
    
    # Prikaži vse markerje
    print("\n📚 VSI MARKERJI:")
    print("-" * 60)
    for marker, info in MARKERJI.items():
        print(f"  {marker} - {info['ime']} ({info['kategorija']}): {info['opis']}")
    
    print("\n" + "=" * 60)
    print("FUNKCIJE:")
    print("-" * 60)
    print("  verify_markers(text) - Preveri prisotnost markerjev")
    print("  replace_markers(text, format) - Zamenjaj markerje")
    print("  get_markers_by_category(category) - Markerji po kategoriji")
    print("  to_html(text) - Pretvori v HTML")
    print("  to_latex(text) - Pretvori v LaTeX")
    print("=" * 60)
