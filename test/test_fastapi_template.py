from templatrix.src.fastapi_template import FastapiTemplate
if __name__ == '__main__':
    # Generate FastAPI template with proper Python library structure
    # sample_db is always True by default now
    Ft = FastapiTemplate(dir='./output', vcs=False, override=True, template=True)
    Ft.generate_template()
    
    # Example with override to regenerate existing files
    # Ft.generate_template(override=True)
    
    # Example with blank template (only folder structure)
    # Ft.generate_template(blank=True)