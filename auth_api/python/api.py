from flask import Flask
from flask import jsonify
from flask import request

from database import Database
from methods import Token, Restricted


app = Flask(__name__)

database = Database()

token = Token()
restricted = Restricted()


# Just a health check
@app.route("/")
def url_root():
    return "OK"


# Just a health check
@app.route("/_health")
def url_health():
    return "OK HEALTH"


# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=["POST"])
def url_login():
    try:
        username = request.form["username"]
        password = request.form["password"]

        userData = database.get_user(username, password)
        
        if userData is not None:
            userData = token.generate_token(userData)

        res = {
            "data": userData
        }
        return jsonify(res)
    except:
        return jsonify({"data": None})


# e.g. http://127.0.0.1:8000/protected
@app.route("/protected")
def url_protected():
    try:
        auth_token = request.headers.get('Authorization')
        headerToken = auth_token.split(' ')

        if len(headerToken) == 0 or restricted.access_data(headerToken[1]) is None:
            return "ACCESS DENIED"

        res = {
            "data": "You are under protected data"
        }
        return jsonify(res)
    except:
        return "ACCESS DENIED"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)