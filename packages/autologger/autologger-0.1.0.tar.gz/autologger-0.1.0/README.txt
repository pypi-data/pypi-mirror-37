Autologger




python setup.py sdist bdist_wheel
pip install --upgrade twine
twine upload --repository-url https://pypi.org/legacy/ dist/*
