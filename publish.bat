del /S /Q  dist\*.*
RMDIR "build" /S /Q

python setup.py bdist_wheel && twine upload dist/*

pause