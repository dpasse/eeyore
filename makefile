all: style mypy lint test

lint:
	pylint src/eeyore

test:
	pytest -v -s

style:
	pycodestyle src/eeyore

mypy:
	mypy src/eeyore