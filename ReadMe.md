Python tests:
coverage run -m pytest
coverage report -m

Docker:
docker build -t ezie-tests .
docker run --rm ezie-tests
https://github.com/pytest-dev/pytest/discussions/8270