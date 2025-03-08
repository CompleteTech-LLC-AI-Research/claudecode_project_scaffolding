#!/usr/bin/env python3
"""
Script to reorganize the generated files into a more cohesive structure.
"""
import os
import sys
import shutil
from pathlib import Path

# Define source and target directories
SOURCE_DIR = "/Users/completetech/test_scaffolding/output/demo_csv_utility"
TARGET_DIR = "/Users/completetech/test_scaffolding/output/real_csv_utility"

def create_target_structure():
    """Create the target directory structure."""
    # Ensure target directory exists
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    # Create subdirectories
    subdirs = ["core", "operations", "utils", "cli", "tests", "docs"]
    for subdir in subdirs:
        os.makedirs(os.path.join(TARGET_DIR, subdir), exist_ok=True)

def move_files():
    """Move files from source to target structure."""
    # Dictionary mapping source paths to target directories
    path_mapping = {
        "csv_utility/core": "core",
        "csv_utility/operations": "operations",
        "csv_utility/utils": "utils",
        "csv_utility/cli": "cli",
        "csv_utility/tests": "tests",
        "csv_utility/docs": "docs"
    }
    
    # Move README.md to the root
    if os.path.exists(os.path.join(SOURCE_DIR, "README.md")):
        shutil.copy(
            os.path.join(SOURCE_DIR, "README.md"),
            os.path.join(TARGET_DIR, "README.md")
        )
    
    # Move files based on mapping
    for source_path, target_subdir in path_mapping.items():
        source_dir = os.path.join(SOURCE_DIR, source_path)
        target_dir = os.path.join(TARGET_DIR, target_subdir)
        
        # Skip if source directory doesn't exist
        if not os.path.exists(source_dir):
            continue
            
        # Move all files in the directory
        for filename in os.listdir(source_dir):
            source_file = os.path.join(source_dir, filename)
            target_file = os.path.join(target_dir, filename)
            
            # Only copy files, not directories
            if os.path.isfile(source_file):
                shutil.copy(source_file, target_file)
                print(f"Copied {source_file} to {target_file}")

def main():
    """Main entry point."""
    print(f"Reorganizing files from {SOURCE_DIR} to {TARGET_DIR}")
    
    # Create target structure
    create_target_structure()
    
    # Move files
    move_files()
    
    print("Reorganization complete!")

if __name__ == "__main__":
    main()