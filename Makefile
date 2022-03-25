lint:
	mypy .
	black .
	pylint src

tests:
	pytest . -v


test-coverage:
	pytest --cov-report term-missing --cov=src .

pip-compile:
	pip-compile requirements.in

pip-sync:
	pip-sync requirements.txt

docker-build:
	docker build -t nate-td .

docker-run:
	docker run -p 80:80 nate-td

docker-run:
	docker run -p 80:80 nate-td 

docker-run-tests:
	docker run --entrypoint "pytest" nate-td . 