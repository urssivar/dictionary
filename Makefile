# Auto-detect Python: use venv if it exists, otherwise system python
PYTHON := $(shell test -d venv && echo venv/bin/python3 || echo python3)

.PHONY: new validate export

new:
	@$(PYTHON) scripts/new.py $(W)

validate:
	@$(PYTHON) scripts/validate.py $(L)

export:
	@$(PYTHON) scripts/export.py
