setup:
	python3 setup.py sdist bdist_wheel

upload:
	rm dist/*
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

upload-test:
	rm dist/*
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

init:
	pip install -r requirements.txt

test:
	py.test tests

.PHONY: init test
