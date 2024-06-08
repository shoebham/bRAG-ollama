# __init__.py - at the top level of the project
# read-only tomllib is now part of python core, so we do not need to install it
import tomllib

# we get the version from pyproject.toml and put it into a variable
with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
    version = data["project"]["version"]