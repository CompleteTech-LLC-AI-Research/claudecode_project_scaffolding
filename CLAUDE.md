# Test Scaffolding Project Guide

## Commands
```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run all tests
pytest

# Run specific test
pytest tests/test_main.py::TestClassName::test_function_name

# Linting
flake8 src/ tests/
black src/ tests/
isort src/ tests/
mypy src/ tests/
```

## Code Style Guidelines
- Python 3.8+ compatibility
- Use type hints for all function parameters and return values
- Imports order: stdlib → third-party → local modules
- DocStrings for all modules, classes, and functions
- Classes use PascalCase, functions/variables use snake_case
- Use Pydantic models for data validation
- Write pytest tests for all functionality
- Use explicit exception handling with meaningful messages
- JSON for configuration files