#!/usr/bin/env python3
"""
Example of generating a multi-file/folder project for a CSV processing utility.
This example demonstrates how to use the scaffolding system to create
a more complex and realistic project structure.
"""
import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.main import ScaffoldConfig, TierConfig, PromptTemplate
from src.pipeline import PipelineProcessor


class FileStructureGenerator:
    """Generator for creating a file structure based on a project structure."""
    
    def __init__(self, config: ScaffoldConfig, output_dir=None):
        """Initialize with a scaffold config."""
        self.config = config
        self.structure = config.variables.get("structure", {})
        self.base_dir = output_dir or f"./output/{config.project_name}"
        
    def create_file_structure(self):
        """Create the directory and file structure."""
        os.makedirs(self.base_dir, exist_ok=True)
        
        # Process the structure recursively
        self._process_structure(self.structure, self.base_dir)
        
        print(f"File structure created at {self.base_dir}")
        
    def _process_structure(self, structure, current_path):
        """
        Recursively process the structure dictionary to create directories and files.
        
        Args:
            structure: The structure dictionary or list
            current_path: The current path to create items in
        """
        if isinstance(structure, dict):
            # Process directories
            for dir_name, contents in structure.items():
                dir_path = os.path.join(current_path, dir_name)
                os.makedirs(dir_path, exist_ok=True)
                self._process_structure(contents, dir_path)
        elif isinstance(structure, list):
            # Process files
            for file_name in structure:
                file_path = os.path.join(current_path, file_name)
                # Create an empty file
                with open(file_path, 'w') as f:
                    f.write("")
                    
                # Store the relative path for prompt generation
                rel_path = os.path.relpath(file_path, self.base_dir)
                print(f"Created file: {rel_path}")


def load_example_config() -> ScaffoldConfig:
    """Load the example configuration."""
    config_path = os.path.join(os.path.dirname(__file__), "example_config.json")
    
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    
    # Convert tier configs
    if 'tiers' in config_data:
        tiers = {}
        for tier_name, tier_data in config_data['tiers'].items():
            if 'prompt_template' in tier_data:
                template_data = tier_data.pop('prompt_template')
                tier_data['prompt_template'] = PromptTemplate(**template_data)
            tiers[tier_name] = TierConfig(**tier_data)
        config_data['tiers'] = tiers
        
    return ScaffoldConfig(**config_data)


def mock_file_content_generation(file_path: str, config: ScaffoldConfig) -> str:
    """
    Generate mock content for files based on the file path.
    In a real implementation, this would call the LLM.
    
    Args:
        file_path: The path to the file
        config: The scaffold config
        
    Returns:
        Mock content for the file
    """
    # Get the filename and directory from the path
    filename = os.path.basename(file_path)
    dirname = os.path.dirname(file_path)
    
    # Add a header comment with file location info
    location_info = f"# File: {file_path}\n# Part of the {config.project_name} project\n\n"
    
    # Simple mocking based on file type and name
    if filename.endswith(".py"):
        if filename.startswith("test_"):
            return f"""#!/usr/bin/env python3
\"\"\"
Tests for {filename[5:-3]} module.
\"\"\"
import unittest
from unittest.mock import patch, MagicMock

class Test{filename[5:-3].capitalize()}(unittest.TestCase):
    \"\"\"Test suite for {filename[5:-3]} functionality.\"\"\"
    
    def setUp(self):
        \"\"\"Set up test fixtures.\"\"\"
        pass
        
    def test_basic_functionality(self):
        \"\"\"Test basic functionality.\"\"\"
        self.assertTrue(True)
        
if __name__ == "__main__":
    unittest.main()
"""
        else:
            return f"""#!/usr/bin/env python3
\"\"\"
{filename[:-3].replace('_', ' ').title()} module for CSV utility.

Part of the {config.project_name} project.
\"\"\"
import csv
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class {filename[:-3].replace('_', ' ').title().replace(' ', '')}:
    \"\"\"
    {filename[:-3].replace('_', ' ').title()} class implementation.
    \"\"\"
    
    def __init__(self):
        \"\"\"Initialize the {filename[:-3].replace('_', ' ')} component.\"\"\"
        logger.debug(f"Initializing {filename[:-3].replace('_', ' ')}")
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        \"\"\"
        Process the provided data.
        
        Args:
            data: The input data to process
            
        Returns:
            Processed data
        \"\"\"
        return data
"""
    elif filename.endswith(".md"):
        return f"""# {filename[:-3].title()}

## Overview

This document provides information about the {config.project_name} project.

## Description

{config.description}

## Features

{chr(10).join(['- ' + feature for feature in config.variables.get('features', [])])}
"""
    else:
        return f"# {filename}\n\nGenerated content for {file_path}"


def generate_project(output_dir=None):
    """
    Generate the CSV utility project.
    
    Args:
        output_dir: Optional directory to output the project to
    """
    print("Loading example configuration...")
    config = load_example_config()
    
    # Create an organized output directory structure
    project_dir = output_dir or f"./generated/{config.project_name}"
    
    # Clean up previous output if it exists
    if os.path.exists(project_dir):
        print(f"Cleaning up previous output at {project_dir}...")
        shutil.rmtree(project_dir)
    
    # Create the file structure
    print("Creating file structure...")
    generator = FileStructureGenerator(config, project_dir)
    generator.create_file_structure()
    
    # Get the list of files to generate content for
    base_dir = generator.base_dir
    all_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, base_dir)
            all_files.append(rel_path)
    
    print(f"Generating content for {len(all_files)} files...")
    
    # Override the execute_prompt method to generate mock content
    original_execute = config._execute_prompt
    
    def mock_execute_prompt(prompt, output_format):
        if "Generate the file " in prompt:
            file_path = prompt.split("Generate the file ")[1].split(" for a project")[0]
            return mock_file_content_generation(file_path, config)
        else:
            # For README generation or other prompts
            return mock_file_content_generation("README.md", config)
            
    config._execute_prompt = mock_execute_prompt
    
    # Process each file
    for file_path in all_files:
        # Directly call the mock generator for simplicity
        # In a real scenario, you'd use the full prompting system
        content = mock_file_content_generation(file_path, config)
        
        # Write the content to the file
        with open(os.path.join(base_dir, file_path), 'w') as f:
            f.write(content)
            
    # Generate README.md separately using the readme_generation tier
    if "readme_generation" in config.tiers and config.tiers["readme_generation"].enabled:
        result = config.process_tier("readme_generation")
        
        # Write the README.md
        with open(os.path.join(base_dir, "README.md"), 'w') as f:
            f.write(result)
    
    print(f"Project generation complete! Check {base_dir} for the generated files.")
    

if __name__ == "__main__":
    # Set testing mode
    os.environ["SCAFFOLD_TESTING"] = "1"
    
    # Generate the project
    generate_project()