# Contributing to AI Resume & Job Matcher

Thank you for your interest in contributing to the AI Resume & Job Matcher project! This document provides guidelines and information for contributors.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Contributing Guidelines](#contributing-guidelines)
5. [Pull Request Process](#pull-request-process)
6. [Issue Reporting](#issue-reporting)
7. [Feature Requests](#feature-requests)
8. [Documentation](#documentation)
9. [Testing](#testing)
10. [Code Style](#code-style)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. Please:

- Be respectful and inclusive
- Use welcoming and inclusive language
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- OpenAI API key (for testing)
- Basic knowledge of Python, FastAPI, and AI/ML concepts

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/resume-job-matcher.git
   cd resume-job-matcher
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-owner/resume-job-matcher.git
   ```

## Development Setup

### Environment Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

3. **Install development tools**:
   ```bash
   pip install pytest pytest-cov black flake8 mypy pre-commit
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

### Pre-commit Hooks

Set up pre-commit hooks for code quality:

```bash
pre-commit install
```

This will run:
- Code formatting (black)
- Linting (flake8)
- Type checking (mypy)
- Security checks (bandit)

## Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

1. **Bug Fixes**: Fix existing issues
2. **Feature Additions**: Add new functionality
3. **Documentation**: Improve or add documentation
4. **Tests**: Add or improve test coverage
5. **Performance**: Optimize existing code
6. **Security**: Improve security measures

### Contribution Process

1. **Check existing issues** and pull requests
2. **Create an issue** for significant changes
3. **Fork and create a branch** for your changes
4. **Make your changes** following the guidelines
5. **Test your changes** thoroughly
6. **Submit a pull request** with a clear description

### Branch Naming

Use descriptive branch names:
- `fix/issue-123-description`
- `feature/new-endpoint`
- `docs/update-readme`
- `test/add-coverage`

## Pull Request Process

### Before Submitting

1. **Update your fork**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** and commit:
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

4. **Run tests**:
   ```bash
   pytest
   python samples/test_api.py
   ```

5. **Check code quality**:
   ```bash
   black --check .
   flake8 .
   mypy .
   ```

### Pull Request Template

When submitting a pull request, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test improvement
- [ ] Performance optimization
- [ ] Security improvement

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Related Issues
Closes #123
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** in different environments
4. **Documentation** review
5. **Approval** and merge

## Issue Reporting

### Bug Reports

When reporting bugs, include:

1. **Clear title** describing the issue
2. **Detailed description** of the problem
3. **Steps to reproduce** the issue
4. **Expected behavior** vs actual behavior
5. **Environment information**:
   - Python version
   - Operating system
   - Dependencies versions
6. **Error messages** and logs
7. **Minimal example** if possible

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.9.7]
- Package version: [e.g. 1.0.0]

**Additional context**
Any other context about the problem.
```

## Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional context**
Any other context or screenshots about the feature request.
```

### Feature Request Guidelines

1. **Check existing issues** for similar requests
2. **Provide clear use cases** and examples
3. **Consider implementation complexity**
4. **Think about backward compatibility**
5. **Consider performance implications**

## Documentation

### Documentation Standards

1. **Clear and concise** writing
2. **Code examples** for all features
3. **Up-to-date** with code changes
4. **Consistent** formatting and style
5. **Comprehensive** coverage of functionality

### Documentation Types

1. **API Documentation**: Endpoint descriptions and examples
2. **User Guides**: Installation and usage instructions
3. **Developer Guides**: Contributing and development setup
4. **Architecture Docs**: System design and components
5. **Troubleshooting**: Common issues and solutions

### Documentation Updates

When making code changes:
1. **Update relevant documentation**
2. **Add examples** for new features
3. **Update API documentation** for endpoint changes
4. **Review existing documentation** for accuracy

## Testing

### Test Requirements

1. **Unit tests** for new functionality
2. **Integration tests** for API endpoints
3. **Edge case testing** for error conditions
4. **Performance testing** for critical paths
5. **Security testing** for input validation

### Test Structure

```
tests/
├── test_api.py          # API endpoint tests
├── test_models.py       # Pydantic model tests
├── test_pipeline.py     # Pipeline logic tests
├── test_parsers.py      # Parser tests
├── test_matcher.py      # Matching algorithm tests
├── test_ats_validator.py # ATS validation tests
└── fixtures/            # Test data and fixtures
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v

# Run tests in parallel
pytest -n auto
```

### Test Guidelines

1. **Test names** should be descriptive
2. **One assertion** per test when possible
3. **Mock external dependencies** (OpenAI API)
4. **Use fixtures** for common test data
5. **Test error conditions** and edge cases

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

1. **Line length**: 100 characters (not 79)
2. **Import order**: Standard library, third-party, local imports
3. **Docstrings**: Google style for functions and classes
4. **Type hints**: Required for all functions and methods

### Code Formatting

We use **Black** for code formatting:

```bash
# Format code
black .

# Check formatting
black --check .
```

### Linting

We use **Flake8** for linting:

```bash
# Run linter
flake8 .

# Configuration in setup.cfg or .flake8
```

### Type Checking

We use **MyPy** for type checking:

```bash
# Run type checker
mypy .

# Configuration in mypy.ini or pyproject.toml
```

### Example Code Style

```python
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ExampleModel(BaseModel):
    """Example model with proper documentation.
    
    Args:
        name: The name of the item
        value: The value of the item
        tags: Optional list of tags
    """
    name: str = Field(..., description="The name of the item")
    value: int = Field(..., ge=0, description="The value of the item")
    tags: Optional[List[str]] = Field(default=None, description="Optional tags")

def example_function(
    items: List[ExampleModel],
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """Process a list of items with optional limit.
    
    Args:
        items: List of items to process
        limit: Optional limit on number of items
        
    Returns:
        Dictionary with processed results
        
    Raises:
        ValueError: If limit is negative
    """
    if limit is not None and limit < 0:
        raise ValueError("Limit must be non-negative")
    
    # Process items...
    return {"processed": len(items), "limit": limit}
```

## Release Process

### Version Numbering

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. **Update version** in all relevant files
2. **Update CHANGELOG.md** with new features and fixes
3. **Run full test suite** and ensure all tests pass
4. **Update documentation** if needed
5. **Create release notes** with highlights
6. **Tag the release** in Git
7. **Create GitHub release** with release notes

## Community

### Getting Help

1. **Check documentation** first
2. **Search existing issues** for similar problems
3. **Ask questions** in GitHub Discussions
4. **Join community** discussions

### Recognition

Contributors are recognized in:
- **CONTRIBUTORS.md** file
- **Release notes** for significant contributions
- **GitHub contributors** page

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Contact

For questions about contributing:
- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For general questions and discussions
- **Email**: For sensitive or private matters

Thank you for contributing to the AI Resume & Job Matcher project!
