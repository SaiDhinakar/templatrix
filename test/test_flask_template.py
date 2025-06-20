from templatrix.src.flask_template import FlaskTemplate
if __name__ == '__main__':
    # Generate Flask template with proper Python library structure
    # sample_db is always True by default now
    Ft = FlaskTemplate(dir='./output', vcs=True, override=True)
    Ft.generate_template()
    
    # Example with override to regenerate existing files
    # Ft.generate_template(override=True)
    
    # Example with blank template (only folder structure)
    # Ft.generate_template(blank=True)