.PHONY: clean lint pre-commit pyspec pyinstaller deps

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install pre-commit hooks
pre-commit:
	pre-commit install

## Delete all artifacts
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*egg-info" -exec rm -r {} \;
	rm -rf build/ dist/

## Lint using pre-commit
lint:
	pre-commit run --all-files

## Install dependencies for development
deps:
	pip install --upgrade -r src/client/requirements.txt

## Make pyinstaller spec file
pyspec:
	pyi-makespec --paths=src/client/ --windowed --onefile --name palms src/client/gui.py

## Build executable with pyinstaller
pyinstaller:
	pyinstaller palms.spec
