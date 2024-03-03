bucket-up:
	python tools/s3_manager.py --create sure-thing

bucket-down:
	python tools/s3_manager.py --delete sure-thing

run-janitor:
	python src/main.py

bundle:
	cd src && zip -r lambda_function.zip ./

lint:
	black src/main.py tools/*.py
