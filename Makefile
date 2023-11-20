# Install the dependencies and install pre commit
.PHONY: install
install:
	@pip3 install -r requirements.txt
	@pre-commit install

# Run Pre-Commit
.PHONY: precommit
pre-commit:
	@pre-commit install -f
	@pre-commit run --all

# Start the game
.PHONY: start
start:
	@python3 main.py
