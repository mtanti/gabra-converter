@echo off

call conda activate venv\ || pause && exit /b

cd bin
call pyinstaller --clean --onefile --name gabra_converter run_gabra_converter.py
cd ..
