#!/usr/bin/env python3
"""
Command-line interface for prompt scaffolding system.
"""
import argparse
import json
import os
import subprocess
import sys
from typing import Dict, Any, Optional

from src.main import ScaffoldConfig, TierConfig, PromptTemplate


def load_config(config_path: str) -> ScaffoldConfig:
    """Load configuration from a JSON file."""
    try:
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
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)


def execute_llm_prompt(prompt: str, output_format: str, model: str = "claude-3-sonnet-20240229") -> str:
    """
    Execute a prompt with the Claude CLI.
    
    Args:
        prompt: The prompt to send to Claude
        output_format: The expected output format (text or json)
        model: The model to use (currently not used directly in command)
        
    Returns:
        The response from Claude
    """
    # Check if we're in testing mode (environment variable)
    if os.environ.get("SCAFFOLD_TESTING") == "1":
        # Return a mock response for testing
        return f"Test response for prompt: {prompt[:30]}..."
    
    try:
        # Call claude CLI - just using the basic interface
        cmd = ["claude", prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if output_format == "json":
            try:
                # Ensure the result is valid JSON
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                print("Warning: Could not parse JSON output")
                return result.stdout
        
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error calling Claude: {e}")
        print(f"stderr: {e.stderr}")
        return f"Error: {e}"


def save_output(output: Any, output_path: Optional[str] = None) -> None:
    """Save output to a file or print to stdout."""
    if output_path:
        with open(output_path, 'w') as f:
            if isinstance(output, dict):
                json.dump(output, f, indent=2)
            else:
                f.write(str(output))
        print(f"Output saved to {output_path}")
    else:
        if isinstance(output, dict):
            print(json.dumps(output, indent=2))
        else:
            print(output)


def main():
    parser = argparse.ArgumentParser(description="Prompt scaffolding CLI")
    
    # Config options
    parser.add_argument("--config", "-c", help="Path to config file")
    parser.add_argument("--create-config", action="store_true", help="Create a new config file")
    parser.add_argument("--output", "-o", help="Output file path")
    
    # Tier execution options
    parser.add_argument("--tier", "-t", help="Tier to execute")
    parser.add_argument("--input", "-i", help="Input data for the tier")
    parser.add_argument("--enable-tier", help="Enable a specific tier")
    parser.add_argument("--disable-tier", help="Disable a specific tier")
    
    # System options
    parser.add_argument("--model", default="claude-3-sonnet-20240229", help="Claude model to use")
    
    args = parser.parse_args()
    
    # Create a new config file
    if args.create_config:
        config = ScaffoldConfig(
            project_name=input("Project name: "),
            description=input("Description: "),
            variables={
                "concept": input("Project concept: "),
                "language": input("Programming language: "),
            },
            tiers={
                "initial": TierConfig(
                    enabled=True,
                    prompt_template=PromptTemplate(
                        content="Create a plan for $concept using $language with consideration for system information: $system",
                    ),
                    use_system_info=True
                ),
                "file_generation": TierConfig(
                    enabled=False,
                    prompt_template=PromptTemplate(
                        content="Generate file $file_name based on the plan: $input"
                    ),
                    output_format="text"
                )
            }
        )
        
        # Save config
        config_path = args.config or "scaffold_config.json"
        with open(config_path, "w") as f:
            # Convert to dict for serialization
            config_dict = config.model_dump()
            # Handle nested Pydantic models
            for tier_name, tier in config_dict["tiers"].items():
                config_dict["tiers"][tier_name]["prompt_template"] = tier["prompt_template"]
            
            json.dump(config_dict, f, indent=2)
            
        print(f"Config created at {config_path}")
        return
    
    # Load config
    if not args.config:
        print("No config specified. Use --config to specify a config file or --create-config to create one.")
        return
    
    config = load_config(args.config)
    
    # Enable or disable tiers
    if args.enable_tier:
        if args.enable_tier in config.tiers:
            config.tiers[args.enable_tier].enabled = True
            print(f"Tier '{args.enable_tier}' enabled")
        else:
            print(f"Tier '{args.enable_tier}' not found")
            
    if args.disable_tier:
        if args.disable_tier in config.tiers:
            config.tiers[args.disable_tier].enabled = False
            print(f"Tier '{args.disable_tier}' disabled")
        else:
            print(f"Tier '{args.disable_tier}' not found")
    
    # Execute tier
    if args.tier:
        if args.tier not in config.tiers:
            print(f"Tier '{args.tier}' not found")
            return
            
        input_data = None
        if args.input:
            # Try to load input as JSON, otherwise treat as string
            try:
                with open(args.input, 'r') as f:
                    input_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                input_data = args.input
        
        # Override the internal execute method with our CLI command
        config._execute_prompt = lambda prompt, output_format: execute_llm_prompt(
            prompt, output_format, args.model
        )
        
        # Process the tier
        result = config.process_tier(args.tier, input_data)
        
        # Save or print the output
        save_output(result, args.output)
    

if __name__ == "__main__":
    main()