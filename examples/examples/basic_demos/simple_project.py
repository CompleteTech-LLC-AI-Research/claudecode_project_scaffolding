#!/usr/bin/env python3
"""
Example usage of the prompt scaffolding system for a simple project.
"""
import os
import sys
import json

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import PipelineProcessor, create_pipeline_config


def main():
    """Create and process a simple project configuration."""
    # Create a configuration for a simple CLI tool
    config = create_pipeline_config(
        project_name="cli_tool",
        concept="A command-line tool for converting CSV files to JSON",
        language="python",
        description="Simple utility for data conversion",
        additional_vars={
            "features": [
                "CSV parsing with headers",
                "JSON output with formatting options",
                "Error handling for malformed input",
                "Progress reporting for large files"
            ]
        }
    )
    
    # Enable the file generation tier
    config.tiers["file_generation"].enabled = True
    
    # Create the pipeline processor
    processor = PipelineProcessor(config)
    
    # Process the pipeline starting from the initial tier
    results = processor.process_pipeline("initial")
    
    # Create an output directory
    output_dir = "./generated/cli_tool"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the outputs
    processor.save_outputs(output_dir, create_files=True)
    
    print(f"Project scaffolding completed. Check {output_dir} for results.")


if __name__ == "__main__":
    main()