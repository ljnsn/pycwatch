PROJECTS := $(notdir $(wildcard workspaces/*))


.clean-venv:
	rm -rf .venv

.venv:
	poetry config virtualenvs.create true --local
	poetry install --sync

init: .clean-venv .venv

test-%: .venv
	poetry install --sync --with $*
	poetry run bash scripts/test.sh $*

tests: .venv $(addprefix test-, $(PROJECTS))

test-isolated-%: .venv
	poetry install --sync --only $*,$*-test
	poetry run bash scripts/test.sh $*
