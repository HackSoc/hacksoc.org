""" Handles all things git (there aren't many of them) """
from pygit2 import discover_repository, Repository
import os

path = discover_repository(os.path.dirname(__file__))
repo = Repository(path)
# https://www.pygit2.org/repository.html
