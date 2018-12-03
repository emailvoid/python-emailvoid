all:

publish:
	python setup.py register sdist upload

.PHONY: all publish
