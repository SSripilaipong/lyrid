test:
	pytest -m "not integration" tests/

test-integration:
	pytest -m "integration" tests/

release:
	rm -rf ./dist/ | exit 0
	python setup.py sdist
	twine upload ./dist/*