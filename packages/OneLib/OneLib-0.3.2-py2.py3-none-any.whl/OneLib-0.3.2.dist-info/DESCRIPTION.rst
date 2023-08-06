python setup.py bdist_wheel --universal

twine upload dist/*
---
install:
> pip3 install --upgrade  -i https://pypi.org/simple/ OneLib


---
updates:
    2018-10-25 12:01 
    v0.3.2 add SimpleTimer


