#!/usr/bin/env python3
"""
Example demonstrating meta-prompt optimization capabilities.
"""
import os
import sys
import json

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import ScaffoldConfig, TierConfig, PromptTemplate
from src.pipeline import PipelineProcessor, add_tier


def create_optimized_config():
    """Create a configuration with meta-prompt optimization."""
    # Start with a basic config
    config = ScaffoldConfig(
        project_name="optimized_api",
        description="REST API with meta-prompt optimization",
        variables={
            "concept": "A REST API for managing a blog with posts and comments",
            "language": "python",
            "framework": "FastAPI",
        },
        tiers={
            "initial": TierConfig(
                enabled=True,
                prompt_template=PromptTemplate(
                    content="""
                    Create a detailed development plan for $concept using $language and $framework.
                    
                    Include:
                    1. Project structure
                    2. Data models
                    3. API endpoints
                    4. Implementation details
                    
                    For each file, specify:
                    - File name
                    - Purpose
                    - Key components/functions
                    """
                ),
                use_system_info=True,
                optimize=True  # Enable optimization
            ),
            "file_generation": TierConfig(
                enabled=True,
                prompt_template=PromptTemplate(
                    content="""
                    Generate the file $file_name based on the following plan:
                    
                    $plan
                    
                    Use $language with $framework.
                    Follow best practices and include proper documentation.
                    """
                ),
                output_format="text",
                optimize=True  # Enable optimization
            )
        }
    )
    
    # Add a meta-optimization tier
    add_tier(
        config=config,
        tier_name="meta_optimization",
        prompt_template="""
        You are an expert software developer specializing in code optimization.
        
        Review the following code for $file_name:
        
        $input
        
        Improve this code with:
        1. More efficient algorithms
        2. Better use of $framework features
        3. Improved error handling
        4. Performance optimizations
        
        Explain your optimization strategy, then provide the optimized code.
        """,
        enabled=True,
        output_format="text",
        optimize=False  # No need to optimize the optimizer
    )
    
    # Custom optimization prompt for the initial tier
    config._optimize_result = lambda result, tier_name: _optimize_with_custom_prompt(
        result, tier_name, config.variables
    )
    
    return config


def _optimize_with_custom_prompt(result, tier_name, variables):
    """
    Custom optimization function that would normally call Claude with a meta-prompt.
    
    In a real implementation, this would call Claude with a specific optimization
    prompt depending on the tier.
    """
    # In a real implementation, we would call Claude here
    print(f"Optimizing result for tier '{tier_name}' with custom meta-prompt")
    
    # For demonstration purposes, just indicate optimization happened
    if isinstance(result, str):
        return f"### OPTIMIZED OUTPUT ###\n{result}"
    elif isinstance(result, dict):
        result["optimized"] = True
        return result
    else:
        return result


def main():
    """Run the meta-prompt optimization example."""
    # Create the optimized config
    config = create_optimized_config()
    
    # Create the pipeline processor
    processor = PipelineProcessor(config)
    
    # Process the pipeline
    print("Processing pipeline with meta-optimization...")
    results = processor.process_pipeline("initial")
    
    # Save the outputs
    output_dir = "./generated/optimized_api"
    os.makedirs(output_dir, exist_ok=True)
    processor.save_outputs(output_dir, create_files=True)
    
    print(f"Project scaffolding with meta-optimization completed. Check {output_dir} for results.")


if __name__ == "__main__":
    main()