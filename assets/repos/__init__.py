import re

from .github_handler import github_handler

HANDLERS = [github_handler]

def get_repo_for_repo_url(repo_url):
    for handler in HANDLERS:
        if re.match(handler.repo_regex, repo_url):
            return handler
