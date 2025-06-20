import os
import subprocess
from textwrap import dedent
import shutil
from pathlib import Path

class FastapiTemplate:
    def __init__(self, dir: str = os.getcwd(), vcs: bool = False, override: bool = False, template: bool = False) -> None:
        """
            Initialize a new FastAPI project structure.
            Creates a basic FastAPI project structure with necessary files and directories.
            The structure includes a main.py file with a basic FastAPI application setup
            and an environment configuration example file.
            Parameters
            ----------
            dir : str, optional
                Directory path where the project will be created, by default current working directory
            vcs : bool, optional
                Initialize version control system (Git) in the project directory, by default False
            override : bool, optional
                Whether to override the directory if it already exists, by default False
            template : bool, optional
                Whether to create a template project, by default False
            Notes
            -----
            - If `override` is True and the directory exists, it will be removed
            - If `vcs` is True, a Git repository will be initialized and basic VCS files
              (.gitignore, README.md) will be created
            - Creates the following structure:
                - main.py (FastAPI app entry point)
                - .env.example (Environment configuration example)
                - Folders: db, models, routes, tests, utils
        """
        self.folders = ('db', 'models', 'routes', 'tests', 'utils')
        
        self.dir_path = dir
        self.template = template
        self.override = override

        if self.override and os.path.exists(self.dir_path):
            shutil.rmtree(self.dir_path)

        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        

        with open(os.path.join(self.dir_path, 'main.py'), 'w') as fp:
            content = dedent("""
            from fastapi import FastAPI
            import os
            from dotenv import load_dotenv
            
            load_dotenv()
            
            app = FastAPI(title="Templatrix | FastAPI Template")
            
            @app.get('/')
            def index():
                return "Hello World"
            
            if __name__ == '__main__':
                import uvicorn
                uvicorn.run('main:app', host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "8000")))
            """)
            fp.write(content)
            
        with open(os.path.join(self.dir_path, '.env.example'), 'w') as fp:
            content = dedent("""
            # Environment Configuration
            # Copy this file to .env and modify as needed
            
            # Server Configuration
            HOST=127.0.0.1
            PORT=8000
            DEBUG=true
            
            """)
            fp.write(content) 
            
        if vcs:
            subprocess.run(['git', 'init'], cwd=self.dir_path)
            vcs_files = ['.gitignore', 'README.md'] 
            for file in vcs_files:
                with open(os.path.join(self.dir_path, file), 'w') as fp:
                    if file == '.gitignore':
                        content = "__pycache__/\n*.pyc\n.env\n.venv/\nvenv/\n.pytest_cache/\n.coverage\n"
                    else:
                        content = f"# {os.path.basename(self.dir_path)}\n\nA FastAPI project template.\n"
                    fp.write(content)
                fp.close()
    
        
    def generate_template(self):
        if self.template:
            source_dir = Path(__file__).parent.joinpath("templates", "template_fastapi") # Source template directory
            for item in os.listdir(source_dir.resolve()):
                source = os.path.join(source_dir, item)
                destination = os.path.join(self.dir_path, item)
                if os.path.isdir(source):
                    shutil.copytree(source, destination, dirs_exist_ok=True)
                else:
                    shutil.copy2(source, destination)
        else:
            for folder in self.folders:
                folder_path = os.path.join(self.dir_path, folder)
                os.mkdir(folder_path)
                with open(os.path.join(folder_path,'__init__.py'), 'w') as fp:
                    pass
                fp.close()
                
        return
        
                
                
                    
                