.PHONY: clean lint pre-commit

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

## Lint using pre-commit
lint:
	pre-commit run --all-files
