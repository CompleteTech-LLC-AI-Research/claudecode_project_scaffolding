# Project Scaffolding Examples

This directory contains examples demonstrating how to use the scaffolding system.

## Directory Structure

- `basic_demos/`: Simple example scripts showing basic scaffolding features
  - `meta_prompt_optimization.py`: Demonstrates meta-prompt optimization
  - `simple_project.py`: Shows how to use scaffolding for a basic project
  - `test_config.json`: Example configuration file

- `cli_tool_generator/`: Complete demo application for generating project scaffolding
  - `example_config.json`: Configuration for the CSV utility demo
  - `generate.py`: Main generator script
  - `reorganize.py`: Script for reorganizing generated code
  - `generated/`: Generated output from running the demo
    - `real_csv_utility/`: Complete generated CSV utility application

## Getting Started

To run the basic examples:
```bash
cd examples/basic_demos
python simple_project.py
# or
python meta_prompt_optimization.py
```

To run the CLI tool generator demo:
```bash
cd examples/cli_tool_generator
python generate.py
```

The generated output will be placed in the `generated/` directory.