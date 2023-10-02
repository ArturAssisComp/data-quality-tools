from invoke import task
import os
import platform

@task
def clean(c, docs='false', venv='false'):
    """Clean up build artifacts and temporary files."""
    if platform.system() == "Windows":
        c.run("if exist dist rmdir /S /Q dist")
        c.run("if exist build rmdir /S /Q build")
        c.run("if exist .pytest_cache rmdir /S /Q .pytest_cache")
        c.run("if exist src\\data_quality_tools.egg-info rmdir /S /Q src\\data_quality_tools.egg-info")
        c.run("FOR /D /R . %G IN (__pycache__) DO if exist %G rmdir /S /Q %G")
        c.run("FOR /R %G IN (*.pyc) DO if exist %G del /F /Q %G")
        if docs=='true':
            c.run("if exist docs\\_build rmdir /S /Q docs\\_build")
        if venv=='true':
            c.run("if exist venv rmdir /S /Q venv")
    else:
        c.run("rm -rf dist build .pytest_cache src/data_quality_tools.egg-info")
        c.run("find . -type d -name '__pycache__' -exec rm -rf {} +")
        c.run("find . -name '*.pyc' -delete")
        if docs=='true':
            c.run("rm -rf docs/_build")
        if venv=='true':
            c.run("rm -rf venv")


@task
def test(c, target=None):
    """
    Run tests for the project.

    ## Parameters
        target (str): The specific test or test directory to run. (default: None, runs all tests)

    ## Examples
    invoke test --target=tests/test_module.py
    """
    if target:
        c.run(f"pytest {target}")
    else:
        c.run("pytest")

@task
def setupVenv(c):
    """Create and setup, installing the requirements, a virtual environment."""
    if not os.path.isdir("venv"):
        c.run("virtualenv venv")
        print("Virtual environment created.")
        if platform.system() == "Windows":
            c.run(".\\venv\\Scripts\\pip install -r requirements.txt")
        else:
            c.run("venv/bin/pip install -r requirements.txt")
        print("Dependencies installed.")
    else:
        print("Virtual environment already exists.")


@task
def installDev(c):
    """Install the package in development mode."""
    c.run("pip install -e .")

@task
def install(c):
    """Install the package."""
    c.run("pip install .")

@task
def uninstall(c):
    c.run("pip uninstall data_quality_tools")