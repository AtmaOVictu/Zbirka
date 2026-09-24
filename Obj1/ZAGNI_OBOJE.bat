@echo off
chcp 65001 >nul
SETLOCAL EnableDelayedExpansion

:: ============================================================================
:: ZAGNI_OBOJE.BAT - Zaženi GUI + Zgradi EXE
:: SISTEM \u2205\u2206\u2202\u222e v2.0
:: Avtor: Luka + Vibe
:: Datum: 19. 9. 2026
:: ============================================================================

echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║   ZAGNI_OBOJE: GUI + EXE                                        ║
echo  ║   SISTEM \u2205\u2206\u2202\u222e v2.0                                 ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.

:: Preveri, ali smo v pravilni mapi
SET "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo.
echo  🎯 CILJ: Zaženi GUI + Zgradi EXE

:: ============================================================================
:: KORAK 1: Preveri in namesti zahtevane knjižnjice
:: ============================================================================

echo.
echo  ─────────────────────────────────────────────────────────────────
echo  📦 KORAK 1/4: Preverjanje in nameščanje knjižnic...
echo  ─────────────────────────────────────────────────────────────────
echo.

:: Preveri PySide6
python -m pip show PySide6 >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  📥 Nameščam PySide6...
    pip install PySide6
    echo.
)

:: Preveri Pillow (za ikono)
python -m pip show Pillow >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  📥 Nameščam Pillow (za ikono)...
    pip install Pillow
    echo.
)

:: Preveri markdown2 (za PDF)
python -m pip show markdown2 >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  📥 Nameščam markdown2 (za PDF izvoz)...
    pip install markdown2
    echo.
)

:: Preveri PyInstaller (za EXE)
python -m pip show pyinstaller >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  📥 Nameščam PyInstaller (za EXE)...
    pip install pyinstaller
    echo.
)

echo  ✅ Vse knjižnjice so nameščene!

:: ============================================================================
:: KORAK 2: Ustvari ikono
:: ============================================================================

echo.
echo  ─────────────────────────────────────────────────────────────────
echo  🎨 KORAK 2/4: Ustvarjam ikono...
echo  ─────────────────────────────────────────────────────────────────
echo.

IF NOT EXIST icon.ico (
    python create_icon.py
    echo.
) ELSE (
    echo  ℹ️  Ikonica že obstaja: icon.ico
)

:: ============================================================================
:: KORAK 3: Zaženi GUI
:: ============================================================================

echo.
echo  ─────────────────────────────────────────────────────────────────
echo  🚀 KORAK 3/4: Zažnem GUI aplikacijo...
echo  ─────────────────────────────────────────────────────────────────
echo.
echo  ⏳ GUI se bo odprl v novem oknu...
echo  ⏳ Če se ne odpre avtomatsko, ročno zaženi:
echo  ⏳   python sistem_gui_v2.py
echo.

:: Odpri GUI v novem oknu
start python sistem_gui_v2.py

:: Počakaj 3 sekunde, da se GUI odpre
timeout /t 3 /nobreak >nul

:: ============================================================================
:: KORAK 4: Zgradi EXE (v ozadju)
:: ============================================================================

echo.
echo  ─────────────────────────────────────────────────────────────────
echo  📦 KORAK 4/4: Gradim EXE (v ozadju)...
echo  ─────────────────────────────────────────────────────────────────
echo.

:: Zgradi EXE
pyinstaller Sistem_v2.spec --clean --onefile --windowed

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo  ✅ EXE uspešno zgrajen!
    echo  📁 Lokacija: dist\Sistem_v2.exe
    echo.
    echo  🏃 Če hočeš zažeti EXE ročno:
    echo  🏃   start dist\Sistem_v2.exe
) ELSE (
    echo.
    echo  ⚠️  Napaka pri gradnji EXE
    echo  💡 Poskusi ročno: pyinstaller Sistem_v2.spec --clean --onefile --windowed
)

:: ============================================================================
:: ZAKLJUČEK
:: ============================================================================

echo.
echo  ─────────────────────────────────────────────────────────────────
echo  🎉 ZAKLJUČEK
echo  ─────────────────────────────────────────────────────────────────
echo.
echo  ✅ GUI aplikacija je odprta
echo  ✅ EXE se gradi v ozadju

echo.
echo  📌 KAJ NARDITI:
echo  ─────────────────────────────────────────────────────────────────
echo  1. V GUI generiraj nov kamen (npr. CXIV - Labirint)
echo  2. Preveri T1-T4 za vse dokumente
  3. Uredi obstoječe dokumente
  4. Išči po dokumentih
  5. Izvozi v PDF/ZIP
  6. Če se EXE zgradi: start dist\Sistem_v2.exe

echo.
echo  📚 DOKUMENTACIJA:
echo  ─────────────────────────────────────────────────────────────────
echo  • PRIROČNIK_GUI_v2.md - Kompleten priročnik
  • POVZETEK_IZBOLJŠAV_v2.md - Seznam vseh izboljšav
  • build_and_run.bat - Interaktivni menu

echo.
echo  🎯 SISTEM \u2205\u2206\u2202\u222e v2.0 JE PRIPRAVLJEN! 🚀
echo.

ENDLOCAL
