@echo off
chcp 65001 >nul
title SISTEM 0-1-0-1
color 0A
echo ============================================================
echo   SISTEM 0-1-0-1 - Zagon
 echo ============================================================
echo.
echo  Izberi:
echo  1. Zagni GUI
 echo  2. Generiraj nov kamen
echo  3. Generiraj 5 kamnov
 echo  4. Preveri vse
 echo  5. Zgradi vsa
echo  6. Statistika
 echo  7. Iskanje
 echo  8. Pomoc
 echo  9. Izhod
echo.
set /p choice=Izberi (1-9):

if "%choice%"=="1" goto gui
if "%choice%"=="2" goto gen1
if "%choice%"=="3" goto gen5
if "%choice%"=="4" goto verify
if "%choice%"=="5" goto build
if "%choice%"=="6" goto stats
if "%choice%"=="7" goto search
if "%choice%"=="8" goto help
if "%choice%"=="9" goto end

goto end

:gui
cd /d/OntoProjekt/CanvasMinstral/Obj1
start "" "dist\Sistem.exe"
goto end

:gen1
cd /d/OntoProjekt/CanvasMinstral/Obj1
set /p num=Stevilka (npr 121):
set /p title=Naslov (npr Krog):
set /p desc=Opis (npr zapis kot cikel):
python tools_enhanced.py %num% "%title%" "%desc%"
pause
goto end

:gen5
cd /d/OntoProjekt/CanvasMinstral/Obj1
python auto_generate.py
pause
goto end

:verify
cd /d/OntoProjekt/CanvasMinstral/Obj1
python tools.py verify
pause
goto end

:build
cd /d/OntoProjekt/CanvasMinstral/Obj1
python run.py build
pause
goto end

:stats
cd /d/OntoProjekt/CanvasMinstral/Obj1
python db_manager.py statistika
pause
goto end

:search
cd /d/OntoProjekt/CanvasMinstral/Obj1
set /p query=Poizvedba:
python -c "from indexer import search; results = search('%query%'); [print(f'  {r[\"title\"]} ({r[\"score\"]})') for r in results[:5]]"
pause
goto end

:help
cd /d/OntoProjekt/CanvasMinstral/Obj1
python run.py help
pause
goto end

:end
echo.
echo Konec.
