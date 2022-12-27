#!/bin/bash
set -e

source venv/bin/activate

echo "#########################################"
for FNAME in `find -maxdepth 1 -name "*.py"`
do
    echo "..checking $FNAME"
    python -m mypy $FNAME
done
echo "..checking gabra_converter"
python -m mypy gabra_converter/
echo "..checking tools"
python -m mypy tools/
echo ""

echo "#########################################"
echo "pylint"
for FNAME in `find -maxdepth 1 -name "*.py"`
do
    echo "..checking $FNAME"
    python -m pylint $FNAME
done
echo "..checking gabra_converter"
python -m pylint gabra_converter/
echo "..checking tools"
python -m pylint tools/
echo ""

echo "#########################################"
echo "api documentation"
python tools/api_doc_maker.py
echo ""

echo "#########################################"
echo "project validation"
python tools/validate_project.py
echo ""

echo "#########################################"
echo "sphinx"
cd docs
make html
cd ..
echo ""

echo "#########################################"
echo "unittest"
cd gabra_converter/tests
python -m unittest
cd ../..
echo ""
