from flaskr.github_api import check_connection_to_github

def test_check_connection_to_github():
    assert check_connection_to_github()