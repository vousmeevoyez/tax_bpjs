clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

tests:
	python -m unittest discover

coverage:
	coverage run --source tax_bpjs -m unittest discover