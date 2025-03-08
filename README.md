# 🚀 Claude Generator: AI-Powered Code Generation & Project Scaffolding

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Claude AI](https://img.shields.io/badge/Powered%20by-Claude%20AI-blueviolet)
![Project Generation](https://img.shields.io/badge/Code-Generator-brightgreen)

> **Generate complete, production-ready code projects in minutes with AI | The ultimate Claude prompt engineering toolkit**

A revolutionary AI code generation system that leverages Claude's advanced capabilities to produce entire codebases from simple concept descriptions. From automated project planning to intelligent file generation, test creation, and code optimization - deliver production-ready applications in a fraction of the time using cutting-edge prompt engineering techniques.

## ✨ Why Choose Claude Generator for AI Code Development?

- **Accelerate Development by 10x** - Generate complete projects (files, folders, tests) in minutes not days
- **Slash AI Development Costs** - Full-stack demo application with source code generated for only $4.01
- **Full-Stack Code Generation** - Generate frontend, backend, database, and API code simultaneously
- **Language & Framework Flexibility** - Python, JavaScript, TypeScript, React, Node.js, FastAPI and more
- **AI-Generated Tests** - Comprehensive test suites with high coverage automatically created
- **Perfect for MVP Development** - Rapidly prototype and validate ideas with production-quality code

## 🛠️ Advanced AI Code Generation Features

- **ChatGPT Alternative** - Superior code generation using Claude's capabilities
- **AI Code Assistant** - Generate entire projects or specific code components on demand
- **Prompt Engineering Framework** - Create, chain, optimize and reuse powerful prompts
- **Multi-Tier Generation Pipeline** - Progressive refinement through specialized AI stages
- **Pydantic Validation** - Robust validation ensuring generated code meets requirements
- **Context-Aware Templates** - Dynamic variable substitution for highly relevant code
- **Cross-Platform Development** - Generate code for any environment or platform
- **Extensible Architecture** - Easily customize the generation pipeline for any use case

## 🔍 How AI Code Generation Works

```
Concept Description → AI Architecture Planning → Intelligent File Generation → Auto Test Creation → AI Code Optimization
```

1. **Define Your Project Concept** - Simply describe what you want to build in natural language
2. **AI-Powered Architecture Design** - Claude automatically creates detailed project structure and architecture
3. **Full-Stack Code Generation** - Generate complete files with proper imports, dependencies, and documentation
4. **Automated Test Suite Creation** - AI writes comprehensive tests ensuring functionality and reliability
5. **Intelligent Code Optimization** - Claude analyzes and enhances performance, security and code quality

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-generator.git
cd claude-generator

# Install requirements
pip install -r requirements.txt

# Install package (development mode)
pip install -e .
```

## 📝 Quick Start

```bash
# Create a new project config
scaffold --create-config --config my_project.json

# Generate project plan
scaffold --config my_project.json --tier initial --output plan.txt

# Generate files based on the plan
scaffold --config my_project.json --enable-tier file_generation --tier file_generation --input plan.txt
```

## 💼 AI Code Generation Success Story

Our demo project showcases the power of Claude Generator for real-world applications:

- **Complete End-to-End AI Development**: Entire application with frontend, backend, API and database generated in one run
- **Production-Ready Code Quality**: High-quality, well-structured code that works immediately out-of-the-box
- **Unbeatable Cost-Efficiency**: Full-stack application with complete source code generated for only $4.01 in AI costs
- **10x Development Speed**: What would take days or weeks of manual coding accomplished in minutes
- **Advanced Prompt Engineering**: Demonstrates sophisticated prompt chaining, context management and scaffolding techniques
- **Better Than Human-Written Code**: Consistent patterns, comprehensive error handling, and thorough documentation

## 📦 Advanced Configuration

The system uses JSON configuration files with the following structure:

```json
{
  "project_name": "my_project",
  "description": "A sample project",
  "variables": {
    "concept": "Web application for task management",
    "language": "python"
  },
  "tiers": {
    "initial": {
      "enabled": true,
      "prompt_template": {
        "content": "Create a plan for $concept using $language with consideration for $system",
        "variables": {}
      },
      "use_system_info": true,
      "output_format": "text"
    },
    "file_generation": {
      "enabled": false,
      "prompt_template": {
        "content": "Generate file $file_name based on the plan: $input",
        "variables": {}
      },
      "output_format": "text"
    }
  }
}
```

## 📄 License

MIT License

## Notes from the Author

- My complete chat log with Claude is included with this project for reference.
- I originally developed this tool for personal use, but after seeing its impressive first-run demo, I decided it was worth sharing.
- I'm considering integrating additional tools such as dSpy / TextGrad to enhance its functionality further.
- Unfortunately, since the tool was built using Claude-generated code via prompt piping, it's currently limited in usefulness to those with access to the research preview.
- I'm also evaluating the possibility of transitioning to the OpenAI API, which aligns well with many model providers, or potentially Ollama, to allow easier portability and adaptation.
- Potentialy a Frontend for easy input possibly or a tester agent which will verify the code works at the end and fixes it if necessary, however pydantic may already be solving this issue as this was a 1 - shot prompt.
