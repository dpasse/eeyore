lint:
	pylint src/eeyore

test:
	pytest -v -s

style:
	pycodestyle src/eeyore

mypy:
	mypy src/eeyore

build:
	python3 setup.py sdist
	python3 setup.py bdist_wheel
