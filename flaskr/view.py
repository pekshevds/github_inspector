from flaskr.github_api import get_repos_info_html, get_repos_info_json


def inspect(username: str, format:str='html') -> str:    
    if format == 'html':
        return get_repos_info_html(username)
    return get_repos_info_json(username)
