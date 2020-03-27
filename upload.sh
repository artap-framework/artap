if [ -d "dist" ]; then rm -Rf "dist"; fi
if [ -d "build" ]; then rm -Rf "build"; fi
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -u artap -p SAdkjf-+*5132
