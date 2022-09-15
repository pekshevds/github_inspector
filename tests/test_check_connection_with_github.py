from flaskr.view import check_connection_with_github

def test_check_connection_with_github():
    assert check_connection_with_github()