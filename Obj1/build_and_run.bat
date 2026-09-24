@echo off
chcp 65001 >nul
SETLOCAL EnableDelayedExpansion

:: ============================================================================
:: BUILD AND RUN SCRIPT - SISTEM ∅→∆→∂→∮ v2.0
:: Avtor: Luka + Vibe
:: Datum: 19. 9. 2026
:: ============================================================================

echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║   SISTEM ∅→∆→∂→∮ v2.0 - Build & Run Script                    ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.

:: Preveri, ali smo v pravilni mapi
SET "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: ============================================================================
:: MENU
:: ============================================================================

:menu
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║                    SISTEM ∅→∆→∂→∮ v2.0                            ║
echo  ╠══════════════════════════════════════════════════════════════════╣
echo  ║  1.  🚀 ZAGON GUI APLIKACIJE (Python)                          ║
echo  ║  2.  📦 BUILD EXE (PyInstaller)                                  ║
echo  ║  3.  🏃 ZAGON EXE (dist/Sistem_v2.exe)                           ║
echo  ║  4.  🔄 BUILD & RUN (Avtomatsko)                                ║
echo  ║  5.  🧪 TEST VSEH DOKUMENTOV                                      ║
echo  ║  6.  📊 STATISTIKA SISTEMA                                        ║
echo  ║  7.  🔍 ISKI V DOKUMENTIH                                        ║
echo  ║  8.  📝 GENERIRAJ NOV KAMEN                                      ║
echo  ║  9.  ✅ PREVERI T1-T4                                             ║
echo  ║ 10.  ❌ IZBRISI DIST IMENIK                                       ║
echo  ║ 11.  💾 IZVOZI VSE V ZIP                                          ║
echo  ║ 12.  ℹ️  POMOČ                                                  ║
echo  ║  0.   🚪 IZHOD                                                  ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.

SET /P "CHOICE=Enter choice (0-12): "

IF "%CHOICE%"=="1" GOTO run_gui
IF "%CHOICE%"=="2" GOTO build_exe
IF "%CHOICE%"=="3" GOTO run_exe
IF "%CHOICE%"=="4" GOTO build_and_run
IF "%CHOICE%"=="5" GOTO test_documents
IF "%CHOICE%"=="6" GOTO show_stats
IF "%CHOICE%"=="7" GOTO search_documents
IF "%CHOICE%"=="8" GOTO generate_kamen
IF "%CHOICE%"=="9" GOTO verify_t1t4
IF "%CHOICE%"=="10" GOTO clean_dist
IF "%CHOICE%"=="11" GOTO export_zip
IF "%CHOICE%"=="12" GOTO show_help
IF "%CHOICE%"=="0" GOTO exit_script

echo.
echo  ❌ NEVELJAVNA IZBIRA: %CHOICE%
echo.
pause
GOTO menu

:: ============================================================================
:: 1. Zagon GUI Aplikacije (Python)
:: ============================================================================
:run_gui
cls
echo.
echo  🚀 ZAGON GUI APLIKACIJE
echo  ─────────────────────────────────────────────────────────────────
echo.

python sistem_gui_v2.py

GOTO menu

:: ============================================================================
:: 2. Build EXE
:: ============================================================================
:build_exe
cls
echo.
echo  📦 BUILD EXE z PyInstaller
echo  ─────────────────────────────────────────────────────────────────
echo.

:: Preveri, ali je PyInstaller nameščen
python -m pip show pyinstaller >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  ⚠️  PyInstaller ni nameščen!
    echo  Namestitev: pip install pyinstaller
    echo.
    pause
    GOTO menu
)

echo  📦 Gradnja Sistem_v2.exe...
echo.

:: Ustvari ikono (če ne obstaja)
IF NOT EXIST icon.ico (
    echo  🎨 Ustvarjam ikono...
    python create_icon.py
    echo.
)

:: Zagon PyInstaller
pyinstaller Sistem_v2.spec --clean --onefile --windowed

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo  ✅ EXE uspešno zgrajen!
    echo  Lokacija: dist\Sistem_v2.exe
) ELSE (
    echo.
    echo  ❌ Napaka pri gradnji EXE
)

echo.
pause
GOTO menu

:: ============================================================================
:: 3. Zagon EXE
:: ============================================================================
:run_exe
cls
echo.
echo  🏃 ZAGON EXE
echo  ─────────────────────────────────────────────────────────────────
echo.

IF EXIST dist\Sistem_v2.exe (
    echo  🏃 Zagonym Sistem_v2.exe...
    start /d dist\Sistem_v2.exe
) ELSE (
    echo  ❌ dist\Sistem_v2.exe ne obstaja!
    echo  Najprej zgradi EXE (izberi 2)
)

echo.
pause
GOTO menu

:: ============================================================================
:: 4. Build & Run (Avtomatsko)
:: ============================================================================
:build_and_run
cls
echo.
echo  🔄 BUILD & RUN (Avtomatsko)
echo  ─────────────────────────────────────────────────────────────────
echo.

:: Preveri in namesti PyInstaller
python -m pip show pyinstaller >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  📦 Nameščam PyInstaller...
    pip install pyinstaller
    echo.
)

:: Ustvari ikono
IF NOT EXIST icon.ico (
    echo  🎨 Ustvarjam ikono...
    python create_icon.py
    echo.
)

:: Zgradi EXE
echo  📦 Gradim Sistem_v2.exe...
pyinstaller Sistem_v2.spec --clean --onefile --windowed

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo  ✅ EXE uspešno zgrajen!
    echo.
    echo  🏃 Zagonym Sistem_v2.exe...
    start /d dist\Sistem_v2.exe
) ELSE (
    echo.
    echo  ❌ Napaka pri gradnji EXE
)

echo.
pause
GOTO menu

:: ============================================================================
:: 5. Test vseh dokumentov
:: ============================================================================
:test_documents
cls
echo.
echo  🧪 TEST VSEH DOKUMENTOV (T1-T4)
echo  ─────────────────────────────────────────────────────────────────
echo.

python tools.py verify

echo.
pause
GOTO menu

:: ============================================================================
:: 6. Statistika sistema
:: ============================================================================
:show_stats
cls
echo.
echo  📊 STATISTIKA SISTEMA
echo  ─────────────────────────────────────────────────────────────────
echo.

python db_manager.py statistika

echo.
pause
GOTO menu

:: ============================================================================
:: 7. Išči v dokumentih
:: ============================================================================
:search_documents
cls
echo.
echo  🔍 ISKI V DOKUMENTIH
echo  ─────────────────────────────────────────────────────────────────
echo.

SET /P "SEARCH_TERM=Vnesi iskalni izraz (npr. ∅ ∆ ∂ ∮): "
IF "%SEARCH_TERM%"=="" GOTO menu

echo.
echo  Iščem: %SEARCH_TERM%
echo.

python -c "from markerji_extended import *; import os; results = []; [results.append(f'{f} (v{i+1}): {line.strip()}') for f in os.listdir('.') if f.endswith('.md') for i, line in enumerate(open(f, 'r', encoding='utf-8').read().split('\n')) if '%SEARCH_TERM%' in line]; print('\n'.join(results)) if results else print('Ni ujemanj')"

echo.
pause
GOTO menu

:: ============================================================================
:: 8. Generiraj nov kamen
:: ============================================================================
:generate_kamen
cls
echo.
echo  📝 GENERIRAJ NOV KAMEN
echo  ─────────────────────────────────────────────────────────────────
echo.

SET /P "KAMEN_NUM=Vnesi številko kamna (npr. 114): "
IF "%KAMEN_NUM%"=="" GOTO menu

SET /P "KAMEN_TITLE=Vnesi naslov (npr. Labirint): "
IF "%KAMEN_TITLE%"=="" GOTO menu

SET /P "KAMEN_DESC=Vnesi opis (npr. zapis kot pot): "
IF "%KAMEN_DESC%"=="" GOTO menu

echo.
echo  📝 Generiram kamen CROMAN(%KAMEN_NUM%) - %KAMEN_TITLE%
echo.

python tools.py generate %KAMEN_NUM% "%KAMEN_TITLE%" "%KAMEN_DESC%"

echo.
pause
GOTO menu

:: ============================================================================
:: 9. Preveri T1-T4
:: ============================================================================
:verify_t1t4
cls
echo.
echo  ✅ PREVERI T1-T4
echo  ─────────────────────────────────────────────────────────────────
echo.

python preveri_0124.py

echo.
pause
GOTO menu

:: ============================================================================
:: 10. Izbrisi DIST imenik
:: ============================================================================
:clean_dist
cls
echo.
echo  ❌ IZBRISI DIST IMENIK
echo  ─────────────────────────────────────────────────────────────────
echo.

IF EXIST dist\ (
    echo  ⚠️  Brisanje dist/ imenika...
    rmdir /s /q dist
    echo  ✅ Imenik dist/ izbrisan
) ELSE (
    echo  ℹ️  Imenik dist/ ne obstaja
)

echo.
pause
GOTO menu

:: ============================================================================
:: 11. Izvozi vse v ZIP
:: ============================================================================
:export_zip
cls
echo.
echo  💾 IZVOZI VSE V ZIP
echo  ─────────────────────────────────────────────────────────────────
echo.

SET /P "ZIP_NAME=Vnesi ime ZIP datoteke (npr. sistem_backup): "
IF "%ZIP_NAME%"=="" SET "ZIP_NAME=sistem_backup_%DATE:~-4,4%%DATE:~-7,2%%DATE:~-10,2%"

python -c "import zipfile, glob, os; zipf = zipfile.ZipFile('%ZIP_NAME%.zip', 'w', zipfile.ZIP_DEFLATED); [zipf.write(f, f) for f in glob.glob('*resnicami-rozetni-kamni-*.md') + ['database.json', 'sistem.db', 'STANJE-SISTEMA-POLNO-18092026.md', 'PRIROCNIK.md'] if os.path.exists(f)]; print('✅ Izvožen: %ZIP_NAME%.zip')"

echo.
pause
GOTO menu

:: ============================================================================
:: 12. Pomoč
:: ============================================================================
:show_help
cls
echo.
echo  ℹ️  POMOČ - SISTEM ∅→∆→∂→∮ v2.0
echo  ─────────────────────────────────────────────────────────────────
echo.
echo  OSNOVNE FUNKCIJE:
echo  ─────────────────────────────────────────────────────────────────
echo.
echo  1. ZAGON GUI
   - Grafična aplikacija z vsi funkcijami
   - Preprosto uporabniško vmesnik
   - Podpora vseh markerjev

echo.
echo  2. BUILD EXE
   - Ustvari samostojno Windows aplikacijo
   - Potreben: PyInstaller (pip install pyinstaller)
   - Izhod: dist/Sistem_v2.exe

echo.
echo  3. ZAGON EXE
   - Zaženi že zgrajen EXE
   - Hitro in preprosto

echo.
echo  4. BUILD & RUN
   - Avtomatsko zgradi in zaženi EXE
   - Idealno za hitro testiranje

echo.
echo  TEHNIČNE ZAHTEVE:
echo  ─────────────────────────────────────────────────────────────────
echo  - Python 3.10 ali novejši
  - PySide6: pip install PySide6
  - PyInstaller: pip install pyinstaller (za build)
  - markdown2: pip install markdown2 (za PDF izvoz)
  - Graphviz: za PNG vizualizacijo (opcijsko)

echo.
echo  DATOTEKE:
echo  ─────────────────────────────────────────────────────────────────
echo  - sistem_gui_v2.py - Glavna GUI aplikacija
  - Sistem_v2.spec - PyInstaller specifikacija
  - icon.ico - Ikonica aplikacije
  - database.json - Baza podatkov
  - sistem.db - SQLite baza
  - *resnicami-rozetni-kamni-*.md - Kamni
  - tools.py - Orodja
  - db_manager.py - Upravljanje baze
  - markerji_extended.py - Simbolski register
  - create_icon.py - Ustvari ikono

echo.
echo  POVEZAVE:
echo  ─────────────────────────────────────────────────────────────────
echo  - Dokumentacija: PREDLAGE-ZA-KONSISTENTNO-RAZLAGANJE.md
  - Prikaz sistema: STANJE-SISTEMA-POLNO-18092026.md
  - Priročnik: PRIROCNIK.md

echo.
pause
GOTO menu

:: ============================================================================
:: IZHOD
:: ============================================================================
:exit_script
cls
echo.
echo  🚪 IZHOD
echo  ─────────────────────────────────────────────────────────────────
echo.
echo  Hvala, da uporabljaš SISTEM ∅→∆→∂→∮ v2.0!
echo.
echo.
ENDLOCAL
