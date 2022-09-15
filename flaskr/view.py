from datetime import datetime, timedelta, date
from flask import render_template
import requests
from .config import TOKEN


def get_headers() -> dict:
    """ 
    returns headers for autorization
    """
    return {
        'Authorization': f"Bearer {TOKEN}"
    }


def check_connection_with_github() -> bool:
    """
    testing connection to github ()
    """
    result = requests.get(url='https://api.github.com/user', headers=get_headers())
    return result.status_code >= 399


def get_commit_info(username: str, repo_name: str) -> dict:
    """
    returns commits list
    """
    result = requests.get(url=f"https://api.github.com/repos/{username}/{repo_name}/commits", headers=get_headers())
    if result.status_code <= 399:
        return result.json()
    return []


def get_forked_repos_number(repos: list) -> int:
    """
    returns the number of forked repositories
    """
    return len([repo for repo in repos if repo['fork']])


def get_target_projects_urls(repos: list) -> list:
    """
    return repositories unmarked fork in python
    """
    return [repo['html_url'] for repo in repos if not repo['fork'] and repo['language'] == 'Python']


def get_total_avg_errors(repos: list) -> int:
    """
    returns the average number of errors 
    """
    if len(repos):
        return len([1 for repo in repos if repo['has_issues']])/len(repos)
    return 0


def get_projects_with_docs(repos: list) -> int:
    """
    returns the number of projects with docs
    """
    return len([repo for repo in repos if repo['has_wiki']])


def get_commits_number(repos: list) -> int:    
    """
    returns the number of commits in the public repos in the 30 last days
    """
    one_day = timedelta(days=1)
    today = date.today()
    thirty_days_ago = today - (one_day * 30)
    commit_counter = 0
    
    for repo in repos:
        if not repo['private']:
            
            username, repo_name = repo['full_name'].split('/')
            repo_commit_info = get_commit_info(username, repo_name)
            
            for commit_info in repo_commit_info:
            
                commit_date_str = commit_info['commit']['author']['date'].replace('T', ' ').replace('Z', '')
                commit_date = datetime.strptime(commit_date_str, "%Y-%m-%d %H:%M:%S").date()
                
                if commit_date <= thirty_days_ago:
                    commit_counter += 1
    return commit_counter


def get_projects_number(repos: list) -> int:    
    """
    returns the number of the public repos with commits in the 30 last days
    """
    one_day = timedelta(days=1)
    today = date.today()
    thirty_days_ago = today - (one_day * 30)
    project_counter = 0

    for repo in repos:
        if not repo['private']:
            
            username, repo_name = repo['full_name'].split('/')
            repo_commit_info = get_commit_info(username, repo_name)
            
            for commit_info in repo_commit_info:
                
                commit_date_str = commit_info['commit']['author']['date'].replace('T', ' ').replace('Z', '')
                commit_date = datetime.strptime(commit_date_str, "%Y-%m-%d %H:%M:%S").date()
            
                if commit_date <= thirty_days_ago:                    
                    project_counter += 1
                    break
    return project_counter


def get_repos_info(username: str) -> dict:

    result = requests.get(url=f"https://api.github.com/users/{username}/repos", headers=get_headers())
    if result.status_code <= 399:
        repos = result.json()
        
        repos_info = {}
        repos_info['total_repos_number'] = len(repos)
        repos_info['forked_repos_number'] = get_forked_repos_number(repos)
        repos_info['target_projects_urls'] = get_target_projects_urls(repos)
        repos_info['commits_number'] = get_commits_number(repos)
        repos_info['projects_number'] = get_projects_number(repos)
        repos_info['total_avg_errors'] = get_total_avg_errors(repos)
        repos_info['used_technologies'] = 'undefined'
        repos_info['projects_with_tests'] = 'undefined'
        repos_info['projects_with_docs'] = get_projects_with_docs(repos)

        return repos_info

    return {}    


def get_repos_info_json(username: str) -> dict:
    return get_repos_info(username)


def get_repos_info_html(username: str) -> dict:
    repos_info = get_repos_info(username)
    return render_template('repos_info.html', repos_info=repos_info)


def inspect(username: str, format:str='html') -> str:
    """
    """
    if format == 'html':
        return get_repos_info_html(username)
    return get_repos_info_json(username)
