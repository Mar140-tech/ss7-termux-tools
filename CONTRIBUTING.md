# Contributing to SS7 Termux Tools 🤝

Thank you for your interest in contributing!

## Code of Conduct

Be respectful and professional.

## How to Contribute

### 1. Report Bugs 🐛

**Before creating a bug report, check the issue list.**

Include:
- Title: Clear and descriptive
- Description: Expected vs actual behavior
- Steps to reproduce
- Environment: OS, Termux version, Python version
- Logs: Error messages

### 2. Suggest Features 💡

Include:
- Feature description
- Motivation: Why is this useful?
- Implementation ideas
- Example usage

### 3. Submit Pull Requests 🔧

**Before starting work:**
1. Check existing PRs
2. Open an issue first
3. Get approval

**PR Process:**
1. Fork the repository
2. Create feature branch: `git checkout -b feature/description`
3. Make changes
4. Test thoroughly
5. Commit: `git commit -m "feat: Add new feature"`
6. Push: `git push origin feature/description`
7. Open Pull Request
8. Address feedback
9. Merge after approval

## Development Setup

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ss7-termux-tools.git
cd ss7-termux-tools
```

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8
```

### Run Tests

```bash
pytest tests/
pytest tests/ --cov=src/
```

### Check Code Quality

```bash
# Format code
black src/

# Check style
flake8 src/
```

## Code Style

### Python Style Guide

We follow PEP 8:
- Line length: 100 characters max
- Indentation: 4 spaces
- Quotes: Double quotes
- Docstrings: Google style

### Example

```python
def scan_network(cidr: str, timeout: int = 5) -> List[ScanResult]:
    """
    Scan a network for SS7 services.
    
    Args:
        cidr: Network in CIDR notation
        timeout: Connection timeout in seconds
    
    Returns:
        List of ScanResult objects
    
    Raises:
        ValueError: If CIDR is invalid
    """
    if not validate_cidr(cidr):
        raise ValueError(f"Invalid CIDR: {cidr}")
    
    results = []
    # Implementation
    return results
```

### Naming Conventions

- **Classes:** PascalCase (e.g., `SS7Scanner`)
- **Functions:** snake_case (e.g., `scan_network`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `DEFAULT_TIMEOUT`)
- **Private:** Leading underscore (e.g., `_internal_method`)

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code formatting
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Build/CI

### Examples

```
feat(scanner): Add multi-threaded scanning

Implement concurrent port scanning for better performance.

Closes #42
```

## Testing

### Writing Tests

```python
import pytest
from src.tools.scanner import SS7Scanner

def test_scanner_initialization():
    """Test scanner initialization"""
    scanner = SS7Scanner()
    assert scanner.timeout == 5
    assert scanner.retries == 3

def test_scan_invalid_cidr():
    """Test invalid CIDR rejection"""
    scanner = SS7Scanner()
    with pytest.raises(ValueError):
        scanner.scan_network("invalid.cidr")
```

### Run Tests

```bash
pytest
pytest -v
pytest --cov=src/
```

## Documentation

### Docstring Template

```python
def function(param1: str, param2: int = 5) -> bool:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description
        param2: Description (default: 5)
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When invalid
        IOError: On file errors
    
    Example:
        >>> result = function("test", 10)
        >>> print(result)
        True
    """
    pass
```

## Review Process

### What Reviewers Look For

1. Functionality: Does it work?
2. Code Quality: Clean and maintainable?
3. Tests: Included and passing?
4. Documentation: Updated?
5. Style: Follows conventions?
6. Performance: Any concerns?
7. Security: Safe?

### Feedback Guidelines

- Be respectful and constructive
- Focus on code, not person
- Suggest improvements

### Addressing Feedback

1. Read comments carefully
2. Make requested changes
3. Commit with clear message
4. Reply to comments
5. Request re-review if needed

## Resources

- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Guides](https://guides.github.com/)
- [Termux Docs](https://termux.com/)

## Questions?

- Open an issue
- Check documentation
- Be patient and respectful

---

**Thank you for contributing! 🙏**
