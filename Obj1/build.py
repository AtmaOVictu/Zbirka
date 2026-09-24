#!/usr/bin/env python3
"""
Build script za sistem ∅→∆→∂→∮
Ponovna gradnja vseh komponent sistema
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Konfiguracija
PROJECT_DIR = Path(__file__).parent
DIST_DIR = PROJECT_DIR / "dist"
BUILD_DIR = PROJECT_DIR / "build"
SPEC_FILE = PROJECT_DIR / "sistem_gui.spec"


def clean():
    """Počisti prejšnje gradnje"""
    print("🧹 Čiščenje...")
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
        print(f"   Izbrisana mapa: {DIST_DIR}")
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        print(f"   Izbrisana mapa: {BUILD_DIR}")
    
    # Izbriši .pyc in __pycache__
    for root, dirs, files in os.walk(PROJECT_DIR):
        for f in files:
            if f.endswith('.pyc'):
                os.remove(os.path.join(root, f))
        for d in dirs:
            if d == '__pycache__':
                shutil.rmtree(os.path.join(root, d))
    print("   ✅ Počisceno")


def install_dependencies():
    """Namesti odvisnosti"""
    print("\n📦 Nameščanje odvisnosti...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    if result.returncode == 0:
        print("   ✅ Odvisnosti nameščene")
    else:
        print(f"   ⚠️  Opomnik: {result.stderr}")
    return result.returncode == 0


def build_exe():
    """Zgradi izvršljivo datoteko"""
    print("\n🏗️ Gradnja GUI izvršljive datoteke...")
    
    # Preveri, ali spec datoteka obstaja
    if not SPEC_FILE.exists():
        print(f"   ❌ Spec datoteka {SPEC_FILE} ne obstaja")
        return False
    
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", str(SPEC_FILE), "--clean", "--noconfirm"],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    
    if result.returncode == 0:
        print("   ✅ GUI zgrajen")
        # Preveri, ali je EXE ustvarjen
        exe_files = list(DIST_DIR.glob("*.exe"))
        if exe_files:
            print(f"   📁 Izvršljiva datoteka: {exe_files[0].name}")
        return True
    else:
        print(f"   ❌ Napaka pri gradnji: {result.stderr}")
        return False


def build_documentation():
    """Zgradi dokumentacijo"""
    print("\n📚 Gradnja dokumentacije...")
    
    # Generiraj mrežo povezav
    print("   Generiram mrežo povezav...")
    result = subprocess.run(
        [sys.executable, "visualize.py"],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    print(f"   {result.stdout}")
    
    # Posodobi statistiko
    print("   Posodabljam statistiko sistema...")
    result = subprocess.run(
        [sys.executable, "db_manager.py", "statistika"],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    print(f"   {result.stdout}")
    
    return True


def verify_build():
    """Preveri, ali je gradnja uspešna"""
    print("\n✅ Preverjanje gradnje...")
    
    # Preveri, ali EXE obstaja
    if not DIST_DIR.exists():
        print("   ❌ Mapa 'dist' ne obstaja")
        return False
    
    exe_files = list(DIST_DIR.glob("*.exe"))
    if not exe_files:
        print("   ❌ Ni izvršljive datoteke")
        return False
    
    print(f"   ✅ Izvršljiva datoteka: {exe_files[0]}")
    
    # Preveri kamne
    stones = list(PROJECT_DIR.glob("*resnicami-rozetni-kamni-*.md"))
    print(f"   ✅ Številka kamnov: {len(stones)}")
    
    # Preveri baza
    if (PROJECT_DIR / "database.json").exists():
        print("   ✅ Baza podatek: database.json")
    if (PROJECT_DIR / "sistem.db").exists():
        print("   ✅ SQLite baza: sistem.db")
    
    return True


def create_shortcut():
    """Ustvari bljižnjico na namizje"""
    print("\n🔗 Ustvarjam bljižnjico...")
    
    import ctypes
    from ctypes import wintypes
    
    try:
        # Najdi EXE
        exe_files = list(DIST_DIR.glob("*.exe"))
        if not exe_files:
            print("   ❌ Ni izvršljive datoteke")
            return False
        
        target = str(exe_files[0].absolute())
        
        # Pot do namizja
        desktop = Path(os.path.expanduser("~")) / "Desktop" / "Sistem_∅→∆→∂→∮.lnk"
        
        # Ustvari bljižnjico (Windows)
        if sys.platform == "win32":
            shell = ctypes.windll.shell32
            
            # Ustvari .lnk datoteko
            with open(desktop, "w") as f:
                pass
            
            # Nastavi cilj
            shell.SHCreateShortcutW(
                str(desktop),
                target,
                None,
                None,
                0
            )
            print(f"   ✅ Bljižnjica ustvarjena: {desktop}")
        else:
            print("   ⚠️  Bljižnjica podprta samo na Windows")
        
        return True
    except Exception as e:
        print(f"   ⚠️  Napaka pri ustvarjanju bljižnjice: {e}")
        return False


def main():
    print("=" * 60)
    print("BUILD SCRIPT ZA SISTEM ∅→∆→∂→∮")
    print("=" * 60)
    
    # Čiščenje
    clean()
    
    # Nameščanje odvisnosti
    install_dependencies()
    
    # Gradnja EXE
    build_exe()
    
    # Gradnja dokumentacije
    build_documentation()
    
    # Preverjanje
    if verify_build():
        # Ustvari bljižnjico
        create_shortcut()
        
        print("\n" + "=" * 60)
        print("✅ GRADNJA USPEŠNA!")
        print("=" * 60)
        print("\n📁 Izvršljiva datoteka se nahaja v:")
        print(f"   {DIST_DIR.absolute()}")
        print("\n🚀 Za zagon:")
        print(f"   1. Odpri: {DIST_DIR / 'Sistem_∅→∆→∂→∮.exe'}")
        print(f"   2. ali dvoklikni bljižnjico na namizju")
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ GRADNJA NEUSPEŠNA")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
