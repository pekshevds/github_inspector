from flask import Flask, request
from flaskr.view import inspect


app = Flask(__name__)


@app.route('/inspect', methods=['GET'])
def route_api() -> str:
    
    username = request.args.get('username', '')    
    format = request.args.get('format', '')
    
    return inspect(username, format=format)


if __name__ == "__main__":
    app.run()
