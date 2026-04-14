del /S /Q  dist\*.*
RMDIR "build" /S /Q

python -m build && twine upload dist/* --repository testpypi

pause
