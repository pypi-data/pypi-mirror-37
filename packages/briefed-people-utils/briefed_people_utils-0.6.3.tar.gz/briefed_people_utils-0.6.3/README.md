This project is for supporting serverless apps collecting publicly available
data and sending that data to https://Briefed.eu. 

python3 setup.py sdist bdist_wheel
twine upload dist/* -r pypi
