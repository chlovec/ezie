Python tests:
Update output_dir to match the output path test files will be written to.
coverage run -m pytest
coverage report -m

Docker:
docker build -t ezie-tests .
docker run --rm ezie-tests
