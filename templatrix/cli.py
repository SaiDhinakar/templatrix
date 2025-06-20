import argparse
import os
from .src.fastapi_template import FastapiTemplate
from .src.flask_template import FlaskTemplate
from rich import print


def main():
    """
    Main CLI entry point for Templatrix.
    
    This function parses command-line arguments and generates project templates
    based on the specified framework and options. It supports generating FastAPI
    and Flask web application templates with various configuration options.
    
    Command-line Interface:
        templatrix [framework] [options]
        
    Arguments:
        framework: Either 'fastapi' or 'flask', specifies the web framework to use
        
    Options:
        --path PATH     Custom project directory (defaults to current directory)
        --override      Override existing directory if it exists
        --template      Use a fully featured template with example code
        --vcs           Initialize git repository with appropriate .gitignore
    
    Examples:
        templatrix fastapiI
        templatrix flask --path ./my-flask-app --template
        templatrix fastapi --vcs
        templatrix flask --override
    """
    parser = argparse.ArgumentParser(description="Templatrix - Web Framework Project Generator")

    # Positional argument: framework type (fastapi or flask)
    parser.add_argument(
        'framework',
        choices=['fastapi', 'flask'],
        help='Choose the web framework to use'
    )

    # Optional arguments
    parser.add_argument('--path', type=str, help="Optional project setup path")
    parser.add_argument('--override', action='store_true', help="Override the existing directory")
    parser.add_argument('--template', action='store_true', help="Use template")
    parser.add_argument('--vcs', action='store_true', help="Enable version control")

    args = parser.parse_args()

    # Build kwargs dynamically
    kwargs = {}
    if args.path is not None:
        kwargs['dir'] = args.path  # Changed from 'path' to 'dir' to match FastapiTemplate constructor
    if args.override:
        kwargs['override'] = True
    if args.template:
        kwargs['template'] = True
    if args.vcs:
        kwargs['vcs'] = True

    # Use framework value as needed
    framework = args.framework
    
    if framework == "fastapi":
        fastapi_template = FastapiTemplate(**kwargs)
        fastapi_template.generate_template()
        print(f"\n[green]✅ {framework.capitalize()} project structure created successfully[/green]")
        print("To run the FastAPI app, use one of the following commands:")
        print("  [bold]uvicorn run:app --reload[/bold]")
        print("  [bold]fastapi run[/bold]")
        print("  [bold]python run.py[/bold]")
    elif framework == "flask":
        flask_template = FlaskTemplate(**kwargs)
        flask_template.generate_template()
        print(f"\n[green]✅ {framework.capitalize()} project structure created successfully[/green]")
        print("To run the Flask app, use one of the following commands:")
        print("  [bold]flask run[/bold]")
        print("  [bold]python run.py[/bold]")
    