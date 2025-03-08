#!/usr/bin/env python3
"""
Tests for the main module.
"""
import pytest
import sys
import os
from typing import Dict, Any

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import ScaffoldConfig, TierConfig, PromptTemplate, SystemInfo


class TestPromptTemplate:
    """Tests for the PromptTemplate class."""
    
    def test_render_basic(self):
        """Test basic template rendering."""
        template = PromptTemplate(
            content="Hello, $name!",
            variables={"name": "World"}
        )
        
        result = template.render()
        assert result == "Hello, World!"
        
    def test_render_with_context(self):
        """Test rendering with additional context."""
        template = PromptTemplate(
            content="$greeting, $name! Welcome to $place.",
            variables={"greeting": "Hello"}
        )
        
        result = template.render({"name": "User", "place": "Python"})
        assert result == "Hello, User! Welcome to Python."
        
    def test_render_missing_variable(self):
        """Test rendering with missing variables."""
        template = PromptTemplate(
            content="Hello, $name! Your score is $score."
        )
        
        result = template.render({"name": "User"})
        # Missing variables should remain as placeholders
        assert result == "Hello, User! Your score is $score."
        
    def test_context_overrides_variables(self):
        """Test that context overrides template variables."""
        template = PromptTemplate(
            content="$greeting, $name!",
            variables={"greeting": "Hello", "name": "World"}
        )
        
        result = template.render({"greeting": "Hi"})
        assert result == "Hi, World!"


class TestTierConfig:
    """Tests for the TierConfig class."""
    
    def test_tier_config_defaults(self):
        """Test TierConfig default values."""
        template = PromptTemplate(content="Test prompt")
        tier = TierConfig(prompt_template=template)
        
        assert tier.enabled is True
        assert tier.output_format == "text"
        assert tier.use_system_info is False
        assert tier.optimize is False
        
    def test_tier_config_custom_values(self):
        """Test TierConfig with custom values."""
        template = PromptTemplate(content="Test prompt")
        tier = TierConfig(
            enabled=False,
            prompt_template=template,
            output_format="json",
            use_system_info=True,
            optimize=True
        )
        
        assert tier.enabled is False
        assert tier.output_format == "json"
        assert tier.use_system_info is True
        assert tier.optimize is True


class TestScaffoldConfig:
    """Tests for the ScaffoldConfig class."""
    
    @pytest.fixture
    def sample_config(self) -> ScaffoldConfig:
        """Create a sample scaffold config for testing."""
        return ScaffoldConfig(
            project_name="test_project",
            description="Test project description",
            variables={"key": "value"},
            tiers={
                "test_tier": TierConfig(
                    prompt_template=PromptTemplate(content="Test $key")
                )
            }
        )
        
    def test_process_tier_not_found(self, sample_config):
        """Test processing a non-existent tier."""
        with pytest.raises(ValueError, match="Tier 'nonexistent' not found"):
            sample_config.process_tier("nonexistent")
            
    def test_process_tier_disabled(self, sample_config):
        """Test processing a disabled tier."""
        sample_config.tiers["test_tier"].enabled = False
        
        # Should return input data when tier is disabled
        input_data = "test_input"
        result = sample_config.process_tier("test_tier", input_data)
        assert result == input_data
        
    def test_process_tier_basic(self, sample_config):
        """Test basic tier processing."""
        # Mock the execute_prompt method to return a fixed result
        original_execute = sample_config._execute_prompt
        sample_config._execute_prompt = lambda prompt, format: f"Result from {prompt}"
        
        result = sample_config.process_tier("test_tier")
        assert "Result from Test value" in result
        
        # Restore original method
        sample_config._execute_prompt = original_execute
        
    def test_process_tier_with_system_info(self, sample_config):
        """Test tier processing with system info."""
        sample_config.tiers["test_tier"].use_system_info = True
        sample_config.tiers["test_tier"].prompt_template = PromptTemplate(
            content="Test with system: $system"
        )
        
        # Mock the execute_prompt method
        original_execute = sample_config._execute_prompt
        sample_config._execute_prompt = lambda prompt, format: prompt
        
        # Reset system_info to ensure consistent test results
        sample_config.system_info.platform = "TestOS"
        sample_config.system_info.python_version = "3.X.Y"
        sample_config.system_info.packages = {"test-package": "1.0.0"}
        
        result = sample_config.process_tier("test_tier")
        assert "TestOS" in result
        
        # Restore original method
        sample_config._execute_prompt = original_execute
        
    def test_process_tier_with_optimization(self, sample_config):
        """Test tier processing with optimization."""
        sample_config.tiers["test_tier"].optimize = True
        
        # Mock the methods
        original_execute = sample_config._execute_prompt
        original_optimize = sample_config._optimize_result
        
        sample_config._execute_prompt = lambda prompt, format: "Test result"
        sample_config._optimize_result = lambda result, tier: f"Optimized: {result}"
        
        result = sample_config.process_tier("test_tier")
        assert result == "Optimized: Test result"
        
        # Restore original methods
        sample_config._execute_prompt = original_execute
        sample_config._optimize_result = original_optimize