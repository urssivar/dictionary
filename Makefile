# Auto-detect Python: use venv if it exists, otherwise system python
PYTHON := $(shell test -d venv && echo venv/bin/python3 || echo python3)

.PHONY: genid validate export

genid:
	@$(PYTHON) scripts/tools/generate_id.py

validate:
	@$(PYTHON) scripts/validate.py

export:
	@$(PYTHON) scripts/export.py
