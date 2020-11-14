#!/bin/sh

# Format, Lint, Test (FLT)
black . \
&& isort . \
&& flake8 \
&& pytest
