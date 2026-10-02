UV ?= uv
CONFIG ?= config.json
MYPY_FLAGS = --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint lint-strict test package

# Create .venv, install the dev tools (uv.lock), then the local wheels
# (42 MLX + assigned A-Maze-ing package) if they are in wheels/.
install:
	$(UV) sync
	@if ls wheels/*.whl >/dev/null 2>&1; then \
		$(UV) pip install wheels/*.whl; \
	else \
		echo "Tip: put the MLX wheel and the assigned maze package in wheels/"; \
	fi

run:
	$(UV) run python pac-man.py $(CONFIG)

debug:
	$(UV) run python -m pdb pac-man.py $(CONFIG)

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache build dist
	rm -f highscores.json.tmp

lint:
	$(UV) run flake8 .
	$(UV) run mypy . $(MYPY_FLAGS)

lint-strict:
	$(UV) run flake8 .
	$(UV) run mypy . --strict

test:
	$(UV) run pytest -q

package:
	$(UV) run pyinstaller --noconfirm pacman.spec
