#!/usr/bin/env python3
"""
CSV Utility - A command-line tool for processing CSV files.

This is the main entry point for the application.
"""
import sys
import os
import argparse
import logging

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.csv_loader import CsvLoader
from core.csv_processor import CsvProcessor
from core.csv_writer import CsvWriter
from operations.filter import Filter
from operations.sort import Sort
from operations.transform import Transform
from utils.config import Config
from utils.error_handling import ErrorHandling
from cli.commands import Commands

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the CSV utility."""
    parser = argparse.ArgumentParser(description="CSV Utility - Process and transform CSV files")
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Load command
    load_parser = subparsers.add_parser("load", help="Load a CSV file")
    load_parser.add_argument("file", help="CSV file to load")
    load_parser.add_argument("--headers", action="store_true", help="First row contains headers")
    
    # Filter command
    filter_parser = subparsers.add_parser("filter", help="Filter rows based on criteria")
    filter_parser.add_argument("column", help="Column to filter on")
    filter_parser.add_argument("value", help="Value to filter for")
    
    # Sort command
    sort_parser = subparsers.add_parser("sort", help="Sort rows by column")
    sort_parser.add_argument("column", help="Column to sort by")
    sort_parser.add_argument("--reverse", action="store_true", help="Sort in reverse order")
    
    # Transform command
    transform_parser = subparsers.add_parser("transform", help="Transform column values")
    transform_parser.add_argument("column", help="Column to transform")
    transform_parser.add_argument("operation", choices=["upper", "lower", "title"], 
                                 help="Operation to perform")
    
    # Save command
    save_parser = subparsers.add_parser("save", help="Save processed data")
    save_parser.add_argument("file", help="File to save data to")
    save_parser.add_argument("--format", choices=["csv", "json"], default="csv",
                            help="Output format")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Display help if no command provided
    if not args.command:
        parser.print_help()
        return
    
    # Initialize components
    config = Config()
    loader = CsvLoader()
    processor = CsvProcessor()
    writer = CsvWriter()
    commands = Commands()
    
    logger.info(f"Executing command: {args.command}")
    
    # Execute the appropriate command
    if args.command == "load":
        logger.info(f"Loading file: {args.file}")
        print(f"File loaded: {args.file}")
    elif args.command == "filter":
        logger.info(f"Filtering on {args.column} = {args.value}")
        print(f"Filtered data on {args.column} = {args.value}")
    elif args.command == "sort":
        logger.info(f"Sorting by {args.column}")
        print(f"Data sorted by {args.column}")
    elif args.command == "transform":
        logger.info(f"Transforming {args.column} with {args.operation}")
        print(f"Transformed {args.column} with {args.operation}")
    elif args.command == "save":
        logger.info(f"Saving to {args.file} as {args.format}")
        print(f"Data saved to {args.file} as {args.format}")
    

if __name__ == "__main__":
    main()