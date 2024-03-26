#!/bin/bash
set -e

conda shell.bash activate venv/

cd bin
pyinstaller --clean --onefile --name gabra_converter run_gabra_converter.py
cd ..

call python -m build
call python -m twine upload dist/*
