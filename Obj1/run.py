#!/usr/bin/env python3
"""
Glavni run script za sistem ∅→∆→∂→∮
Enotno vmesnik za vso avtomatizacijo
"""

import sys
import subprocess
from pathlib import Path

# Barve za izpis
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header(text):
    """Izpiši naslov"""
    print(f"\n{Colors.CYAN}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.END}")


def print_success(text):
    """Izpiši uspeh"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    """Izpiši napako"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_info(text):
    """Izpiši informacijo"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def print_warning(text):
    """Izpiši opozorilo"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def run_command(cmd, cwd=None):
    """Zaženi ukaz in vrni rezultat"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            shell=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def show_help():
    """Pokaži pomoč"""
    print_header("POMOČ - SISTEM ∅→∆→∂→∮")
    print(f"{Colors.BOLD}UPORABA:{Colors.END}")
    print(f"  python run.py [UKAZ] [ARGUMENTI]")
    print()
    print(f"{Colors.BOLD}UKAZI:{Colors.END}")
    print(f"  {Colors.CYAN}generate{Colors.END} [n] [naslov] [opis]  - Generiraj nov kamen")
    print(f"  {Colors.CYAN}generate-batch{Colors.END} [n]             - Generiraj n novih kamnov")
    print(f"  {Colors.CYAN}verify{Colors.END}                      - Preveri vse kamne")
    print(f"  {Colors.CYAN}index{Colors.END}                       - Zgradi indeks")
    print(f"  {Colors.CYAN}search{Colors.END} [query]              - Išči v dokumentih")
    print(f"  {Colors.CYAN}build{Colors.END}                       - Zgradi vsa (EXE + indeks)")
    print(f"  {Colors.CYAN}stats{Colors.END}                       - Pokaži statistiko")
    print(f"  {Colors.CYAN}clean{Colors.END}                       - Počisti zacasne datoteke")
    print(f"  {Colors.CYAN}gui{Colors.END}                         - Zaženi GUI")
    print(f"  {Colors.CYAN}help{Colors.END}        /h              - Pokaži pomoč")
    print()
    print(f"{Colors.BOLD}PRIMERI:{Colors.END}")
    print(f"  python run.py generate 120 'Krog' 'zapis kot cikel'")
    print(f"  python run.py generate-batch 5")
    print(f"  python run.py search '∅→∆'")
    print(f"  python run.py build")
    print()


def generate_stone(args):
    """Generiraj nov kamen"""
    if len(args) < 3:
        print_error("Manjkajo argumenti: run.py generate [številka] [naslov] [opis]")
        return False
    
    stone_id = args[0]
    naslov = args[1]
    opis = args[2]
    tema = args[3] if len(args) > 3 else None
    
    cmd = f"python tools.py generate {stone_id} \"{naslov}\" \"{opis}\""
    if tema:
        cmd += f" \"{tema}\""
    
    print_info(f"Generiram kamen {stone_id}: {naslov}...")
    success, stdout, stderr = run_command(cmd)
    
    if success:
        print_success(f"Kamen {stone_id} ustvarjen!")
        print(stdout)
    else:
        print_error(f"Napaka: {stderr}")
    
    return success


def generate_batch(args):
    """Generiraj več kamnov"""
    if len(args) < 1:
        print_error("Manjka argument: run.py generate-batch [številka]")
        return False
    
    count = int(args[0])
    
    print_info(f"Generiram {count} novih kamnov...")
    cmd = f"python auto_generate.py"
    success, stdout, stderr = run_command(cmd)
    
    if success:
        print_success(f"Generiranih {count} kamnov!")
        print(stdout)
    else:
        print_error(f"Napaka: {stderr}")
    
    return success


def verify_all():
    """Preveri vse kamne"""
    print_info("Preverjam vse kamne...")
    cmd = "python tools.py verify"
    success, stdout, stderr = run_command(cmd)
    
    if success:
        print_success("Preverjanje uspešno!")
        print(stdout)
    else:
        print_error(f"Napaka: {stderr}")
    
    return success


def build_index():
    """Zgradi indeks"""
    print_info("Gradim indeks...")
    cmd = "python indexer.py"
    success, stdout, stderr = run_command(cmd)
    
    if success:
        print_success("Indeks zgrajen!")
        print(stdout)
    else:
        print_error(f"Napaka: {stderr}")
    
    return success


def search_query(args):
    """Išči v dokumentih"""
    if len(args) < 1:
        print_error("Manjka argument: run.py search [poizvedba]")
        return False
    
    query = ' '.join(args)
    print_info(f"Iščem: '{query}'...")
    
    cmd = f"python -c \"from indexer import search; results = search('{query}'); " \
           f"[print(f'  {{r[\"title\"]}} ({{r[\"score\"]}})') for r in results]\""
    
    success, stdout, stderr = run_command(cmd)
    
    if success:
        if stdout.strip():
            print_success(f"Najdenih {len(stdout.strip().split(chr(10)))} rezultatov:")
            print(stdout)
        else:
            print_warning("Ni rezultatov")
    else:
        print_error(f"Napaka: {stderr}")
    
    return success


def build_all():
    """Zgradi vsa"""
    print_header("GRADNJA VSEGA")
    
    # Generiraj nove kamne
    print_info("1. Generiram nove kamne...")
    run_command("python auto_generate.py")
    
    # Preveri vse
    print_info("2. Preverjam kamne...")
    verify_all()
    
    # Zgradi indeks
    print_info("3. Gradim indeks...")
    build_index()
    
    # Zgradi EXE
    print_info("4. Gradim GUI...")
    run_command("python build.py")
    
    print_success("Vsa gradnja uspešna!")
    return True


def show_stats():
    """Pokaži statistiko"""
    print_info("Prikazujem statistiko...")
    cmd = "python db_manager.py statistika"
    success, stdout, stderr = run_command(cmd)
    
    if success:
        print(stdout)
    else:
        print_error(f"Napaka: {stderr}")
    
    return success


def clean():
    """Počisti zacasne datoteke"""
    print_info("Čistim zacasne datoteke...")
    cmd = "python build.py"  # build.py že počisti
    success, stdout, stderr = run_command(cmd)
    
    if success:
        print_success("Počisceno!")
    else:
        print_error(f"Napaka: {stderr}")
    
    return success


def run_gui():
    """Zaženi GUI"""
    print_info("Zaženem GUI...")
    
    # Preveri, ali obstaja EXE
    exe_path = Path("dist/Sistem_∅→∆→∂→∮.exe")
    if exe_path.exists():
        print_success(f"Zaženem: {exe_path}")
        run_command(f'start "" "{exe_path}"')
    else:
        print_warning("EXE ne obstaja, zgradim...")
        build_all()
        if exe_path.exists():
            run_command(f'start "" "{exe_path}"')
        else:
            print_error("EXE ni bil ustvarjen")
    
    return True


def main():
    """Glavais funkcija"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    args = sys.argv[2:]
    
    commands = {
        'generate': generate_stone,
        'generate-batch': generate_batch,
        'g': generate_batch,
        'verify': lambda _: verify_all(),
        'v': lambda _: verify_all(),
        'index': lambda _: build_index(),
        'i': lambda _: build_index(),
        'search': search_query,
        's': search_query,
        'build': lambda _: build_all(),
        'b': lambda _: build_all(),
        'stats': lambda _: show_stats(),
        'st': lambda _: show_stats(),
        'clean': lambda _: clean(),
        'c': lambda _: clean(),
        'gui': lambda _: run_gui(),
        'help': show_help,
        'h': show_help,
        '?': show_help
    }
    
    if command in commands:
        commands[command](args)
    else:
        print_error(f"Neveljaven ukaz: {command}")
        show_help()


if __name__ == "__main__":
    main()
