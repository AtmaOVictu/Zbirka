@echo off
chcp 65001 >nul
echo ============================================================
echo  SISTEM 0-1-0-1 - Zagon
echo ============================================================
echo.
echo  Izberi moznost:
echo  1. Zagni GUI (priporoceno)
echo  2. Generiraj nov kamen
echo  3. Generiraj vec kamnov
echo  4. Preveri vse kamne
echo  5. Zgradi vsa (EXE + indeks + baza)
echo  6. Prikazi statistiko
echo  7. Iskanje v dokumentih
echo  8. Prikazi pomoc
echo.
set /p choice=Vnesi stevilko (1-8):

if "%choice%"=="1" goto gui
if "%choice%"=="2" goto generate_single
if "%choice%"=="3" goto generate_batch
if "%choice%"=="4" goto verify
if "%choice%"=="5" goto build
if "%choice%"=="6" goto stats
if "%choice%"=="7" goto search
if "%choice%"=="8" goto help

goto end

:gui
echo.
echo Zazenem GUI...
cd %~dp0
start "" "dist\Sistem.exe"
goto end

:generate_single
set /p num=Vnesi stevilko kamna (npr 121):
set /p title=Vnesi naslov (npr Krog):
set /p desc=Vnesi opis (npr zapis kot cikel):
python tools_enhanced.py %num% "%title%" "%desc%"
goto end

:generate_batch
set /p count=Koliko kamnov naj generiram?:
python auto_generate.py %count%
goto end

:verify
echo.
echo Preverjam vse kamne...
python tools.py verify
goto end

:build
echo.
echo Zgradim vsa...
python run.py build
goto end

:stats
echo.
echo Statistika sistema...
python db_manager.py statistika
goto end

:search
set /p query=Vnesi poizvedbo (npr povratna zanka):
python -c "from indexer import search; results = search('%query%'); [print(f'  {r[\"title\"]} ({r[\"score\"]})') for r in results[:5]]"
goto end

:help
echo.
python run.py help
goto end

:end
echo.
echo ============================================================
echo  Koncano!
echo ============================================================
pause
