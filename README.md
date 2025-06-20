# Templatrix

[![PyPI version](https://img.shields.io/pypi/v/templatrix.svg)](https://pypi.org/project/templatrix/)
[![Python Version](https://img.shields.io/pypi/pyversions/templatrix.svg)](https://pypi.org/project/templatrix/)
[![License](https://img.shields.io/github/license/SaiDhinakar/templatrix)](https://github.com/SaiDhinakar/templatrix/blob/main/LICENSE)

A powerful Python package for quickly generating structured web application templates for FastAPI and Flask frameworks.

## Overview

Templatrix provides an intuitive command-line interface for scaffolding new web application projects with best practices already implemented. It offers two template options for each supported framework:

1. **Basic Structure** - A minimal, clean project structure with essential files and directories
2. **Complete Template** - A comprehensive application template with example models, routes, authentication, and more

## Installation

```bash
pip install templatrix
```

## Requirements

- Python 3.12 or higher
- Dependencies will be installed automatically:
  - FastAPI
  - Flask
  - uvicorn
  - python-dotenv
  - pytest
  - httpx

## Usage

### Basic Command Structure

```bash
templatrix [framework] [options]
```

### Available Frameworks

- `fastapi` - Generate a FastAPI project structure
- `flask` - Generate a Flask project structure

### Options

- `--path PATH` - Specify a custom project directory (defaults to current directory)
- `--override` - Override existing directory if it exists
- `--template` - Use a fully featured template with example code
- `--vcs` - Initialize git repository with appropriate .gitignore

### Examples

```bash
# Create a basic FastAPI project in the current directory
templatrix fastapi

# Create a complete Flask template in a custom directory
templatrix flask --path ./my-flask-app --template

# Create a FastAPI project with git initialization
templatrix fastapi --vcs

# Create a Flask project overriding any existing directory
templatrix flask --override
```

## Project Structures

### FastAPI Structure

#### Basic Structure

```
project-directory/
├── .env.example
├── main.py
├── db/
│   └── __init__.py
├── models/
│   └── __init__.py
├── routes/
│   └── __init__.py
├── tests/
│   └── __init__.py
└── utils/
    └── __init__.py
```

#### Template Structure

The template option includes a complete application structure with:

- User model and database setup
- Authentication routes
- Health check endpoints
- Configuration utilities
- Database utilities
- Example tests

### Flask Structure

#### Basic Structure

```
project-directory/
├── .env.example
├── run.py
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   └── __init__.py
│   ├── static/
│   │   └── style.css
│   └── templates/
│       └── index.html
```

#### Template Structure

The template option includes a complete application structure with:

- User model and database setup
- Authentication system
- Multiple route examples
- Static assets (CSS/JS)
- HTML templates
- Example tests

## Development

### Setting up a development environment

1. Clone the repository:
```bash
git clone https://github.com/SaiDhinakar/templatrix.git
cd templatrix
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- **SaiDhinakar** - [GitHub Profile](https://github.com/SaiDhinakar)

## Acknowledgments

- FastAPI - https://fastapi.tiangolo.com/
- Flask - https://flask.palletsprojects.com/
