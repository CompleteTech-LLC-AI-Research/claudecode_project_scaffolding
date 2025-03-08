#!/usr/bin/env python3
"""
Tests for the pipeline module.
"""
import pytest
import sys
import os
import tempfile
import json
from typing import Dict, Any

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import ScaffoldConfig, TierConfig, PromptTemplate
from src.pipeline import PipelineProcessor, add_tier, create_pipeline_config


class TestPipelineProcessor:
    """Tests for the PipelineProcessor class."""
    
    @pytest.fixture
    def sample_config(self) -> ScaffoldConfig:
        """Create a sample scaffold config for testing."""
        config = ScaffoldConfig(
            project_name="test_project",
            description="Test project description",
            variables={"concept": "test concept", "language": "python"},
            tiers={
                "initial": TierConfig(
                    prompt_template=PromptTemplate(
                        content="Create a plan for $concept using $language"
                    )
                ),
                "file_generation": TierConfig(
                    enabled=False,
                    prompt_template=PromptTemplate(
                        content="Generate file $file_name based on: $plan"
                    )
                )
            }
        )
        
        # Mock the execute_prompt method to return a fixed result
        config._execute_prompt = lambda prompt, format: (
            "File1: test_file1.py\nFile2: test_file2.py" 
            if "Create a plan" in prompt 
            else f"Content for {prompt.split('$file_name')[1].split(' ')[0]}"
        )
        
        return config
    
    def test_process_pipeline_basic(self, sample_config):
        """Test basic pipeline processing."""
        processor = PipelineProcessor(sample_config)
        
        result = processor.process_pipeline("initial")
        
        # Check that we have results for the initial tier
        assert "tier_results" in result
        assert "initial" in result["tier_results"]
        assert "File1: test_file1.py" in result["tier_results"]["initial"]
        
        # File generation should not have run because it's disabled
        assert "file_outputs" in result
        assert not result["file_outputs"]
        
    def test_process_pipeline_with_file_generation(self, sample_config):
        """Test pipeline processing with file generation enabled."""
        # Enable file generation
        sample_config.tiers["file_generation"].enabled = True
        
        processor = PipelineProcessor(sample_config)
        result = processor.process_pipeline("initial")
        
        # Check that we have file outputs
        assert "file_outputs" in result
        assert len(result["file_outputs"]) == 2
        assert "test_file1.py" in result["file_outputs"]
        assert "test_file2.py" in result["file_outputs"]
        
    def test_save_outputs(self, sample_config):
        """Test saving pipeline outputs."""
        # Enable file generation
        sample_config.tiers["file_generation"].enabled = True
        
        processor = PipelineProcessor(sample_config)
        result = processor.process_pipeline("initial")
        
        # Save outputs to a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            processor.save_outputs(temp_dir, create_files=True)
            
            # Check that the tier results file exists
            tier_results_path = os.path.join(temp_dir, "tier_results.json")
            assert os.path.exists(tier_results_path)
            
            # Check that the file outputs directory and files exist
            files_dir = os.path.join(temp_dir, "files")
            assert os.path.exists(files_dir)
            
            # Check that the individual files were created
            assert os.path.exists(os.path.join(files_dir, "test_file1.py"))
            assert os.path.exists(os.path.join(files_dir, "test_file2.py"))
            
            # Check that the file_outputs.json file exists
            file_outputs_path = os.path.join(temp_dir, "file_outputs.json")
            assert os.path.exists(file_outputs_path)


class TestPipelineHelpers:
    """Tests for the pipeline helper functions."""
    
    def test_add_tier(self):
        """Test adding a new tier to a config."""
        config = ScaffoldConfig(
            project_name="test_project",
            description="Test project description",
            variables={},
            tiers={}
        )
        
        # Add a new tier
        config = add_tier(
            config=config,
            tier_name="new_tier",
            prompt_template="Test prompt $var",
            enabled=True,
            output_format="json",
            use_system_info=True,
            optimize=True
        )
        
        # Check that the tier was added correctly
        assert "new_tier" in config.tiers
        assert config.tiers["new_tier"].enabled is True
        assert config.tiers["new_tier"].output_format == "json"
        assert config.tiers["new_tier"].use_system_info is True
        assert config.tiers["new_tier"].optimize is True
        assert config.tiers["new_tier"].prompt_template.content == "Test prompt $var"
    
    def test_create_pipeline_config(self):
        """Test creating a standard pipeline configuration."""
        config = create_pipeline_config(
            project_name="test_project",
            concept="Test concept",
            language="python",
            description="Test description",
            additional_vars={"framework": "FastAPI"}
        )
        
        # Check basic config properties
        assert config.project_name == "test_project"
        assert config.description == "Test description"
        assert config.variables["concept"] == "Test concept"
        assert config.variables["language"] == "python"
        assert config.variables["framework"] == "FastAPI"
        
        # Check that the default tiers are created
        assert "initial" in config.tiers
        assert "file_generation" in config.tiers
        assert "optimization" in config.tiers
        
        # Check tier properties
        assert config.tiers["initial"].enabled is True
        assert config.tiers["initial"].use_system_info is True
        assert config.tiers["initial"].optimize is True
        
        assert config.tiers["file_generation"].enabled is False
        assert "$file_name" in config.tiers["file_generation"].prompt_template.content
        
        assert config.tiers["optimization"].enabled is False
        assert "$file_name" in config.tiers["optimization"].prompt_template.content