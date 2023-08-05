
**SETUP ENV**
1. sudo pip install virtualenv
2. virtualenv --no-site-packages VIRTUAL
3. source VIRTUAL/bin/activate
4. pip install -r requirements.txt

**DEPLOYING**
https://packaging.python.org/tutorials/packaging-projects/
1. python setup.py sdist
2. python -m twine upload dist/*