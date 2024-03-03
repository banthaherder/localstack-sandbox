bucket-up:
	python tools/s3_manager.py --create sure-thing

bucket-down:
	python tools/s3_manager.py --delete sure-thing

run_janitor:
	python src/main.py

lint:
	black src/main.py tools/*.py
