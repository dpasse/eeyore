lint:
	pylint src/eeyore_nlp

test:
	pytest -v -s

style:
	pycodestyle src/eeyore_nlp

mypy:
	mypy src/eeyore_nlp

build:
	python3 setup.py sdist
	python3 setup.py bdist_wheel

install:
	( \
		python3 -m venv envs/venv; \
		source envs/venv/bin/activate; \
		python3 -m pip install --upgrade pip; \
		pip install -r requirements.txt; \
		pip install wheel; \
		python3 -m spacy download en_core_web_sm; \
	)

setup-spacy-models:
	python3 -m spacy download en_core_web_sm; \

clean-build:
	rm -R ./src/eeyore_nlp.egg-info/* || true
	rmdir ./src/eeyore_nlp.egg-info || true
	rm -R ./dist/* || true
	rmdir ./dist/ || true
	rm -R ./build/* || true
	rmdir ./build/ || true

clean-venv:
	rm -R ./envs/venv/* || true
	rmdir ./envs/venv || true

clean-cache:
	rm -R ./.mypy_cache || true
	rmdir ./.mypy_cache || true
	rm -R ./.pytest_cache || true
	rmdir ./.pytest_cache || true
