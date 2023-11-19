.PHONY: install
install:
	@echo ">>> Install Dependencies ..."
	@pip3 install -r requirements.txt
	@pre-commit install


# Run Pre-Commit
.PHONY: precommit
pre-commit:
	@echo "Running Pre-Commit..."
	@pre-commit install -f
	@pre-commit run --all
