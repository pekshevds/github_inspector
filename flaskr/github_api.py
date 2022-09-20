import requests
import os
from datetime import datetime, timedelta, date
from flask import render_template
from collections import namedtuple


GITHUB_URL = "https://api.github.com"
TOKEN_FOR_ACCESS_TO_GITHUB = os.environ.get('GIT_HUB_TOKEN', '')
LANGUAGE_OF_REPO = os.environ.get('LANGUAGE_OF_GIT_HUB_REPO', 'Python')


def get_headers_for_connect_to_guthub() -> dict:
    """ 
    returns headers for autorization on github.com
    """
    return {
        'Authorization': f"Bearer {TOKEN_FOR_ACCESS_TO_GITHUB}"
    }


def check_connection_to_github() -> bool:
    """testing connection to github ()"""
    result = requests.get(url=f"{GITHUB_URL}/user", headers=get_headers_for_connect_to_guthub())
    return result.ok


def get_commit_info(username: str, repo_name: str) -> dict:
    """returns commits list"""
    result = requests.get(url=f"{GITHUB_URL}/repos/{username}/{repo_name}/commits", headers=get_headers_for_connect_to_guthub())
    if result.ok:
        return result.json()
    return []


def get_forked_repos_number(repos: list) -> int:
    """returns the number of forked repositories"""
    return len([repo for repo in repos if repo['fork']])


def get_target_projects_urls(repos: list) -> list:
    """return repositories unmarked fork in python"""
    return [repo['html_url'] for repo in repos if not repo['fork'] and repo['language'] == LANGUAGE_OF_REPO]


def get_total_avg_errors(repos: list) -> int:
    """returns the average number of errors"""
    if len(repos):
        return len([repo for repo in repos if repo['has_issues']])/len(repos)
    return 0


def get_projects_with_docs(repos: list) -> int:
    """returns the number of projects with docs"""
    return len([repo for repo in repos if repo['has_wiki']])


def get_commits_or_projects_number(repos: list, commits: bool = True) -> int:
    """returns the number of commits or projects in the public repos in the 30 last days"""
    one_day = timedelta(days=1)
    today = date.today()
    thirty_days_ago = today - (one_day * 30)
    number_counter = 0
    
    for repo in repos:
        if repo['private']:
            continue
            
        username, repo_name = repo['full_name'].split('/')
        repo_commit_info = get_commit_info(username, repo_name)
            
        for commit_info in repo_commit_info:
            
            commit_date_str = commit_info['commit']['author']['date'].replace('T', ' ').replace('Z', '')
            commit_date = datetime.strptime(commit_date_str, "%Y-%m-%d %H:%M:%S").date()
                
            if commit_date <= thirty_days_ago:
                
                number_counter += 1
                if commits:
                    break
        
    return number_counter


def get_commits_number(repos: list) -> int:
    """returns the number of commits in the public repos in the 30 last days"""
    return get_commits_or_projects_number(repos)


def get_projects_number(repos: list) -> int:    
    """returns the number of the public repos with commits in the 30 last days"""
    return get_commits_or_projects_number(repos, False)


def get_repos_info(username: str) -> dict:
    """collects info about user projects on github"""
    
    result = requests.get(url=f"{GITHUB_URL}/users/{username}/repos", headers=get_headers_for_connect_to_guthub())
    if not result.ok:
        return {}

    repos = result.json()

    repos_info = {}        
    repos_info['total_repos_number'] = len(repos)
    repos_info['forked_repos_number'] = get_forked_repos_number(repos)
    repos_info['target_projects_urls'] = get_target_projects_urls(repos),
    repos_info['commits_number'] = get_commits_number(repos)
    repos_info['projects_number'] = get_projects_number(repos)
    repos_info['total_avg_errors'] = get_total_avg_errors(repos)
    repos_info['used_technologies'] = 0
    repos_info['projects_with_tests'] = 0
    repos_info['projects_with_docs'] =  get_projects_with_docs(repos)
            
    return repos_info    


def get_repos_info_json(username: str) -> dict:
    """returns content in json format"""
    return get_repos_info(username)


def get_repos_info_html(username: str) -> str:
    """returns content in html format"""
    repos_info = get_repos_info(username)
    return render_template('repos_info.html', repos_info=repos_info)