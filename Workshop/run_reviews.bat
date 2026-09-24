@echo off
rem SODBA #002 discharge — run all receipts with your own eyes.
rem Each PASS is a receipt UNTIL you have seen it run here. Double-click me.
cd /d D:OntoProjektCanvasMinstralWorkshop
echo ============================================
echo RECEIPT 1/4: the lattice (107 letters)
echo ============================================
python phonetic_coordinates_full.py
echo.
echo ============================================
echo RECEIPT 2/4: the APD runtime
echo ============================================
python apd_engine-py-apd-runtime-for-love-cage-deliverable-2.py
echo.
echo ============================================
echo RECEIPT 3/4: the finiteness layer
echo ============================================
python wordlist_validator.py
echo.
echo ============================================
echo RECEIPT 4/4: the cockpit (smoke)
echo ============================================
python obj2_cockpit.py --smoke
echo.
echo ============================================
echo RECEIPT 5/5: the lexicon core (Cut 3)
echo ============================================
python lexicon_core.py
echo.
echo Reviews complete. Any FAIL above is a scar, not a surprise.
pause
