#!/bin/sh

# Format, Lint, Test (FLT)
black . \
&& isort . \
&& flake8 \
&& docker-compose build && docker-compose run server sh -c '
  cat dev.requirements.txt | grep pytest | xargs pip install
  pytest
'
