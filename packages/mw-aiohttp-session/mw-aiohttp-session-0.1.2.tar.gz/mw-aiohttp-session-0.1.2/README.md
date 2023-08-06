###产生分发包
``
python setup.py sdist
twine upload dist/*
``
###产生分发包
``
python setup.py build
``

###安装方式

2. python setup.py install
3. pip install mw-aiohttp-session --upgrade