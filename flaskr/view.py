import requests
from .config import TOKEN


def get_headers() -> dict:

    return {
        'Authorization': f"Bearer {TOKEN}"
    }


def check_connection_with_github() -> bool:

    result = requests.get(url='https://api.github.com/user', headers=get_headers())
    return result.status_code >= 399


def get_comnit_info(username: str, repo_name: str) -> dict:
    result = requests.get(url=f"https://api.github.com/repos/{username}/{repo_name}/commits", headers=get_headers())
    if result.status_code <= 399:
        return result.json()
    return {}


def get_repos_info(username: str) -> dict:

    result = requests.get(url=f"https://api.github.com/users/{username}/repos", headers=get_headers())
    if result.status_code <= 399:
        repos = result.json()
        
        repos_info = {}
        repos_info['total_repos_number'] = len(repos)
        repos_info['forked_repos_number'] = len([1 for repo in repos if repo['fork']])
        repos_info['target_projects_urls'] = [repo['html_url'] for repo in repos if not repo['fork'] and repo['language'] == 'Python']
        repos_info['commits_number'] = 1
        repos_info['projects_number'] = 1
        repos_info['total_avg_errors'] = len([1 for repo in repos if repo['has_issues']])/len(repos)
        repos_info['used_technologies'] = 1
        repos_info['projects_with_tests'] = 1
        repos_info['projects_with_docs'] = len([1 for repo in repos if repo['has_wiki']])

        return repos_info

    return {}
    


def inspect(username: str, format:str='html') -> str:
    """
    """
    
    return get_repos_info(username)
