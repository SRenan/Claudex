# Contributing to AOE2 Record APM Analyzer

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

1. **Clear title**: Briefly describe the issue
2. **Description**: Detailed explanation of the problem
3. **Steps to reproduce**: How to recreate the issue
4. **Expected behavior**: What should happen
5. **Actual behavior**: What actually happens
6. **Environment**: OS, Python version, mgz version
7. **Sample file**: If possible, share a problematic `.aoe2record` file (if it doesn't contain sensitive information)

### Suggesting Features

Feature requests are welcome! Please create an issue with:

1. **Use case**: Why is this feature needed?
2. **Description**: What should the feature do?
3. **Alternatives**: Have you considered any alternatives?

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**: Follow conventional commit format
6. **Push to your fork**
7. **Create a pull request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/aoe2-apm-analyzer.git
cd aoe2-apm-analyzer

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Add comments for complex logic

### Example:

```python
def calculate_apm(actions: int, duration_minutes: float) -> float:
    """
    Calculate Actions Per Minute.

    Args:
        actions: Total number of actions
        duration_minutes: Game duration in minutes

    Returns:
        APM as a float, rounded to 2 decimal places
    """
    if duration_minutes == 0:
        return 0.0
    return round(actions / duration_minutes, 2)
```

## Testing

Before submitting a pull request:

1. Test with various `.aoe2record` files
2. Test edge cases (corrupted files, empty files, very large files)
3. Test both CLI and Python API usage
4. Ensure backward compatibility

## Areas for Contribution

Here are some areas where contributions would be particularly valuable:

### Features

- **EAPM Calculation**: Implement Effective APM (filtering out redundant actions)
- **Time-based APM**: Calculate APM for specific time intervals (early game, mid game, late game)
- **Visualization**: Add graphs and charts for APM over time
- **Web Interface**: Create a simple web UI for non-technical users
- **Comparison Tool**: Compare APM across multiple games
- **Database Integration**: Store and query historical APM data

### Improvements

- **Performance**: Optimize parsing for large files
- **Error Handling**: Better error messages and recovery
- **Documentation**: Improve docs, add tutorials, create videos
- **Testing**: Add unit tests and integration tests
- **Platform Support**: Better support for different platforms

### Bug Fixes

- Fix any reported issues
- Handle edge cases better
- Improve compatibility with different game versions

## Code Review Process

1. All PRs will be reviewed by maintainers
2. Feedback will be provided constructively
3. Changes may be requested before merging
4. Once approved, the PR will be merged

## Commit Message Guidelines

Use conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(analyzer): Add EAPM calculation support

Implement Effective Actions Per Minute calculation by filtering
out redundant actions like repeated selections.

Closes #42
```

## Communication

- Be respectful and constructive
- Ask questions if something is unclear
- Provide context in discussions
- Be patient with review process

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in the README and release notes.

Thank you for contributing to the AOE2 Record APM Analyzer!
