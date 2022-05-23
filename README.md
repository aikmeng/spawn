# Spawn

The purpose of this program is to generate test files of variety content type.

## Build Instructions

* Create a python environment shell running Poetry command: `poetry shell`
* Check by running `which python` to ensure python is running from shell environment.
* Resolve program dependencies by running Poetry command: `poetry install`

## Program Execution

* Generate 4 sparse/empty binary files with size 1024 B
  * `poetry run python spawn -t 1 -c 4 -s 1024`  
* Generate 3 binary files with random data with size 10 KB
  * `poetry run python spawn -t 2 -c 3 -s 10240`
* Generate 2 text files with random letters with size 10 MB
  * `poetry run python spawn -t 3 -c 2 -s 10485760`
* Generate 1 text file with random sentences with line count 5
  * `poetry run python spawn -t 4 -c 1 -s 5`