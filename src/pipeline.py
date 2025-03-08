#!/usr/bin/env python3
"""
Multi-tier pipeline processing for prompt scaffolding system.
"""
import json
import os
from typing import Dict, List, Any, Optional, Tuple

from src.main import ScaffoldConfig, TierConfig, PromptTemplate


class PipelineProcessor:
    """Processor for multi-tier pipelines."""
    
    def __init__(self, config: ScaffoldConfig):
        """Initialize with a scaffold config."""
        self.config = config
        self._tier_results = {}  # Store results for each tier
        self._file_outputs = {}  # Store generated file content
        
    def process_pipeline(self, start_tier: str, input_data: Any = None) -> Dict[str, Any]:
        """
        Process a multi-tier pipeline starting from a specific tier.
        
        Args:
            start_tier: The name of the tier to start with
            input_data: Optional input data to provide to the first tier
            
        Returns:
            Dictionary of results for each tier
        """
        if start_tier not in self.config.tiers:
            raise ValueError(f"Starting tier '{start_tier}' not found")
            
        # Process the starting tier
        result = self.config.process_tier(start_tier, input_data)
        self._tier_results[start_tier] = result
        
        # Determine next tiers based on configuration
        # For now, we'll just implement a simple flow from initial -> file_generation
        if start_tier == "initial" and "file_generation" in self.config.tiers:
            if self.config.tiers["file_generation"].enabled:
                # Parse the initial result to get file names
                # This is a simplified implementation - in a real system,
                # we might have a more structured way to get this information
                file_names = self._extract_file_names(result)
                
                # Process each file
                for file_name in file_names:
                    # Add file name to context
                    file_context = {"file_name": file_name, "plan": result}
                    
                    # Process the file generation tier
                    file_result = self.config.process_tier("file_generation", file_context)
                    
                    # Store the result
                    self._file_outputs[file_name] = file_result
        
        # Combine all results
        all_results = {
            "tier_results": self._tier_results,
            "file_outputs": self._file_outputs
        }
        
        return all_results
    
    def _extract_file_names(self, plan_result: str) -> List[str]:
        """
        Extract file names from a plan result.
        
        This is a simplified implementation that looks for file names in the plan.
        In a real implementation, this would need to be more robust.
        
        Args:
            plan_result: The output from the initial planning tier
            
        Returns:
            List of file names extracted from the plan
        """
        # Simple heuristic to extract file names - this would need to be more robust
        # in a real implementation
        file_names = []
        
        # Try to parse as JSON first
        if isinstance(plan_result, dict) and "files" in plan_result:
            # If the result is already structured, use that
            for file in plan_result["files"]:
                if isinstance(file, dict) and "name" in file:
                    file_names.append(file["name"])
                elif isinstance(file, str):
                    file_names.append(file)
            return file_names
        
        # Otherwise, try to parse from text
        if isinstance(plan_result, str):
            lines = plan_result.split("\n")
            for line in lines:
                if ":" in line and ("file" in line.lower() or "." in line):
                    # Simple heuristic to find file names
                    parts = line.split(":")
                    name = parts[-1].strip()
                    # Check if it looks like a file name
                    if "." in name and "/" not in name:
                        file_names.append(name)
                        
        return file_names
    
    def save_outputs(self, output_dir: str, create_files: bool = False) -> None:
        """
        Save the outputs of the pipeline.
        
        Args:
            output_dir: The directory to save outputs to
            create_files: Whether to create actual files for file outputs
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Save tier results
        with open(os.path.join(output_dir, "tier_results.json"), "w") as f:
            json.dump(self._tier_results, f, indent=2)
            
        # Save file outputs
        files_dir = os.path.join(output_dir, "files")
        if self._file_outputs:
            os.makedirs(files_dir, exist_ok=True)
            
            # Save as a single JSON file
            with open(os.path.join(output_dir, "file_outputs.json"), "w") as f:
                json.dump(self._file_outputs, f, indent=2)
                
            # Optionally create actual files
            if create_files:
                for file_name, content in self._file_outputs.items():
                    file_path = os.path.join(files_dir, file_name)
                    with open(file_path, "w") as f:
                        if isinstance(content, dict):
                            json.dump(content, f, indent=2)
                        else:
                            f.write(str(content))
                            
        print(f"Pipeline outputs saved to {output_dir}")


def add_tier(config: ScaffoldConfig, tier_name: str, prompt_template: str, 
             enabled: bool = True, output_format: str = "text", 
             use_system_info: bool = False, optimize: bool = False) -> ScaffoldConfig:
    """
    Add a new tier to an existing config.
    
    Args:
        config: The existing scaffold config
        tier_name: Name for the new tier
        prompt_template: The prompt template text
        enabled: Whether the tier is enabled
        output_format: Output format (text or json)
        use_system_info: Whether to include system info
        optimize: Whether to apply optimization
        
    Returns:
        Updated scaffold config
    """
    config.tiers[tier_name] = TierConfig(
        enabled=enabled,
        prompt_template=PromptTemplate(content=prompt_template),
        output_format=output_format,
        use_system_info=use_system_info,
        optimize=optimize
    )
    
    return config


def create_pipeline_config(
    project_name: str,
    concept: str,
    language: str = "python",
    description: str = "",
    additional_vars: Dict[str, Any] = None
) -> ScaffoldConfig:
    """
    Create a standard pipeline configuration with default tiers.
    
    Args:
        project_name: Name of the project
        concept: Core concept for the project
        language: Programming language
        description: Project description
        additional_vars: Additional variables for the config
        
    Returns:
        A scaffold config with default tiers
    """
    variables = {
        "concept": concept,
        "language": language,
    }
    
    if additional_vars:
        variables.update(additional_vars)
        
    config = ScaffoldConfig(
        project_name=project_name,
        description=description,
        variables=variables,
        tiers={
            "initial": TierConfig(
                enabled=True,
                prompt_template=PromptTemplate(
                    content="""
                    Create a detailed development plan for $concept using $language.
                    
                    Consider the following when creating the plan:
                    1. System info: $system
                    2. Best practices for $language
                    3. Project structure
                    
                    For each file, include:
                    - File name
                    - Purpose
                    - Key components/functions
                    
                    Output the plan as a structured document with clear sections.
                    """
                ),
                use_system_info=True,
                optimize=True
            ),
            "file_generation": TierConfig(
                enabled=False,
                prompt_template=PromptTemplate(
                    content="""
                    Generate the file $file_name based on the following plan:
                    
                    $plan
                    
                    Follow best practices for $language and ensure the code is:
                    1. Well-documented
                    2. Properly structured
                    3. Following idiomatic patterns for $language
                    
                    Output only the file content, ready to be saved.
                    """
                ),
                output_format="text"
            ),
            "optimization": TierConfig(
                enabled=False,
                prompt_template=PromptTemplate(
                    content="""
                    Review and optimize the following code for $file_name:
                    
                    $input
                    
                    Consider:
                    1. Performance improvements
                    2. Code cleanliness
                    3. Best practices for $language
                    4. Error handling
                    
                    Output the improved code without additional comments.
                    """
                ),
                output_format="text"
            )
        }
    )
    
    return config