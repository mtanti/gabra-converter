@echo off

call conda activate venv\ || pause && exit /b

echo #########################################
echo mypy
for /f %%F in ('dir *.py /b') do (
    echo ..checking %%F
    call python -m mypy %%F || pause && exit /b
)
echo ..checking gabra_converter
call python -m mypy gabra_converter\ || pause && exit /b
echo ..checking tools
call python -m mypy tools\ || pause && exit /b
echo.

echo #########################################
echo pylint
for /f %%F in ('dir *.py /b') do (
    echo ..checking %%F
    call python -m pylint %%F || pause && exit /b
)
echo ..checking gabra_converter
call python -m pylint gabra_converter\ || pause && exit /b
echo ..checking tools
call python -m pylint tools\ || pause && exit /b
echo.

echo #########################################
echo api documentation
call python tools\api_doc_maker.py || pause && exit /b
echo.

echo #########################################
echo project validation
call python tools\validate_project.py || pause && exit /b
echo.

echo #########################################
echo sphinx
cd docs
call make html || cd .. && pause && exit /b
cd ..
echo.

echo #########################################
echo unittest
cd gabra_converter\tests
call python -m unittest || cd ..\.. && pause && exit /b
cd ..\..
echo.
