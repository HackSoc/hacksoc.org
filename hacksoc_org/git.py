""" Handles all things git (there aren't many of them) """
from pygit2 import discover_repository, Repository
import os

PATH = discover_repository(os.path.dirname(__file__))
REPO = Repository(PATH)
# https://www.pygit2.org/repository.html
