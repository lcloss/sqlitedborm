Remove-Item build -Force -Recurse
Remove-Item dist -Force -Recurse
Python3 setup.py sdist bdist_wheel