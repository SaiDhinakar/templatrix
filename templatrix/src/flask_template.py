import os
import subprocess
from textwrap import dedent
import shutil
from pathlib import Path

class FlaskTemplate:
    def __init__(self, dir: str = os.getcwd(), vcs: bool = False, override: bool = False, template: bool = False) -> None:
        """
            Initialize a new Flask project structure.
            Creates a basic Flask project structure with necessary files and directories.
            The structure includes run.py and config.py files with a basic Flask application setup
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
                - run.py (Flask app entry point)
                - config.py (Application configuration)
                - .env.example (Environment configuration example)
                - Folders: app (with routes, models, templates, static subfolders), tests
        """
        self.folders = {
            "app": ["routes", "templates", "static"],
        }
        
        self.dir_path = dir
        self.template = template  # Fixed typo from 'tempalte' to 'template'
        self.override = override

        if self.override and os.path.exists(self.dir_path):
            shutil.rmtree(self.dir_path)

        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        

        # Create run.py with a simple Flask application
        with open(os.path.join(self.dir_path, 'run.py'), 'w') as fp:
            content = dedent("""
            from flask import Flask, render_template
            
            app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
            
            @app.route('/')
            def index():
                return render_template('index.html')
            
            if __name__ == '__main__':
                app.run(host='127.0.0.1', port=5000, debug=True)
            """)
            fp.write(content)
            
        with open(os.path.join(self.dir_path, '.env.example'), 'w') as fp:
            content = dedent("""
            # Environment Configuration
            # Copy this file to .env and modify as needed
            
            # Flask Server Configuration
            HOST=127.0.0.1
            PORT=5000
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
                        content = f"# {os.path.basename(self.dir_path)}\n\nA Flask project template.\n"
                    fp.write(content)
                fp.close()
    
        
    def generate_template(self):
        if self.template:
            # Copy from template_flask directory when template=True
            source_dir = Path(__file__).parent.joinpath("templates", "template_flask") # Source template directory
            for item in os.listdir(source_dir.resolve()):
                source = os.path.join(source_dir, item)
                destination = os.path.join(self.dir_path, item)
                if os.path.isdir(source):
                    shutil.copytree(source, destination, dirs_exist_ok=True)
                else:
                    shutil.copy2(source, destination)
        else:
            # Create a simple, user-friendly structure
            for folder in self.folders:
                folder_path = os.path.join(self.dir_path, folder)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                # Create subdirectories
                if folder == "app":
                    for subfolder in self.folders[folder]:
                        subfolder_path = os.path.join(folder_path, subfolder)
                        if not os.path.exists(subfolder_path):
                            os.makedirs(subfolder_path)
                    
                    # Create a simple __init__.py in app folder
                    with open(os.path.join(folder_path, '__init__.py'), 'w') as fp:
                        pass
                    
                    # Create a simple index.html template
                    templates_path = os.path.join(folder_path, "templates")
                    with open(os.path.join(templates_path, 'index.html'), 'w') as fp:
                        content = dedent("""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Flask App</title>
                            <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
                        </head>
                        <body>
                            <div class="container">
                                <h1>Welcome to Your Flask App!</h1>
                                <p>This is a simple Flask application created with Templatrix.</p>
                            </div>
                        </body>
                        </html>
                        """)
                        fp.write(content)
                    
                    # Create a basic CSS file
                    static_path = os.path.join(folder_path, "static")
                    with open(os.path.join(static_path, 'style.css'), 'w') as fp:
                        content = dedent("""
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f5f5f5;
                        }
                        
                        .container {
                            width: 80%;
                            margin: 100px auto;
                            padding: 20px;
                            background-color: white;
                            border-radius: 5px;
                            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                            text-align: center;
                        }
                        
                        h1 {
                            color: #333;
                        }
                        """)
                        fp.write(content)
                    
                    # Create a simple routes/__init__.py file
                    routes_path = os.path.join(folder_path, "routes")
                    with open(os.path.join(routes_path, '__init__.py'), 'w') as fp:
                        pass
        return
        
                
                
                    
                