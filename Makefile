# Auto-detect Python: use venv if it exists, otherwise system python
PYTHON := $(shell test -d venv && echo venv/bin/python3 || echo python3)

.PHONY: id validate export

id:
	@$(PYTHON) -c "from nanoid import generate; print(generate())"

validate:
	@$(PYTHON) scripts/validate.py $(L)

export:
	@$(PYTHON) scripts/export.py
