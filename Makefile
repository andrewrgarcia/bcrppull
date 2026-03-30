PYTHON := uv run python

START ?= 1950-01
END ?= 2025-01
LIMIT ?= None


build:
	$(PYTHON) scripts/build.py --start $(START) --end $(END)

test:
	$(PYTHON) scripts/build.py --start $(START) --end $(END) --limit $(LIMIT)

run-pull:
	LIMIT=$(LIMIT) $(PYTHON) scripts/run_pull.py

inspect:
	LIMIT=$(LIMIT) $(PYTHON) scripts/analyze.py

test-match:
	LIMIT=$(LIMIT) $(PYTHON) scripts/test_ipc_match.py

# --------------------------------------------------
# Clean
# --------------------------------------------------
clean:
	rm -rf data/raw/*
	rm -rf .bcrpy_cache/*