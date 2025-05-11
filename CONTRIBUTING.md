# Contributing to ProxmoxMCP

Thank you for your interest in contributing to ProxmoxMCP! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Contribution Workflow](#contribution-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue and Pull Request Process](#issue-and-pull-request-process)
- [Security Vulnerabilities](#security-vulnerabilities)
- [Community](#community)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and considerate of others when contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a new branch for your changes
5. Make your changes
6. Submit a pull request

## Development Environment

### Prerequisites

- Python 3.8 or higher
- Docker (for containerized development)
- Proxmox VE instance (for testing)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ProxmoxMCP.git
   cd ProxmoxMCP
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Configure your Proxmox connection:
   ```bash
   cp proxmox-config/config.example.json proxmox-config/config.json
   # Edit config.json with your Proxmox credentials
   ```

## Contribution Workflow

1. Check the [issues](https://github.com/yourusername/ProxmoxMCP/issues) for tasks to work on or create a new issue for your proposed change
2. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Add tests for your changes
5. Run the tests to ensure they pass:
   ```bash
   pytest
   ```
6. Update documentation as needed
7. Commit your changes with a descriptive commit message:
   ```bash
   git commit -m "Add feature: your feature description"
   ```
8. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
9. Create a pull request against the `main` branch of the original repository

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all functions, classes, and modules
- Keep functions focused on a single responsibility
- Use meaningful variable and function names
- Add comments for complex logic

### Code Formatting

We use the following tools for code formatting and linting:
- [Black](https://black.readthedocs.io/) for code formatting
- [isort](https://pycqa.github.io/isort/) for import sorting
- [flake8](https://flake8.pycqa.org/) for linting

You can run these tools with:
```bash
black src tests
isort src tests
flake8 src tests
```

## Testing

- Write unit tests for all new functionality
- Ensure all tests pass before submitting a pull request
- Aim for high test coverage of your code
- Include both positive and negative test cases

To run tests:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=src
```

## Documentation

- Update documentation for any changes to functionality
- Document all public APIs
- Include examples where appropriate
- Keep the README up to date
- Add docstrings to all functions, classes, and modules

## Issue and Pull Request Process

### Issues

- Use the appropriate issue template
- Provide clear and detailed information
- Include steps to reproduce for bugs
- Label issues appropriately

### Pull Requests

- Reference the related issue in your pull request
- Provide a clear description of the changes
- Update documentation as needed
- Ensure all tests pass
- Request review from maintainers

## Security Vulnerabilities

If you discover a security vulnerability, please do NOT open an issue. Instead, email [security@example.com](mailto:security@example.com) with details. We take security issues seriously and will address them promptly.

## Community

- Join our [discussions](https://github.com/yourusername/ProxmoxMCP/discussions) for questions and community support
- Follow the project on GitHub to stay updated
- Share your success stories and use cases

Thank you for contributing to ProxmoxMCP!