import FlaskApp.db

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
from flask import Response, send_file

app = Flask(__name__)

# Created and Implemented Flask Code (Done By - Yue Xing)
@app.route('/', methods=['GET'])
def handle_call():
    return "Hello World!"


@app.route('/api/game/add', methods=['POST'])
def add_game():
    if request.method == 'POST':
        uid = request.form["uid"]
        target = request.form["target"]
        score = request.form["score"]
        miss = request.form["miss"]

        db.add_game(uid, target, score, miss)

        return {
            "status": "Game added."
        }


@app.route('/api/game', methods=['POST'])
def get_game_by_uid():
    if request.method == 'POST':
        uid = request.form["uid"]

        return db.get_game_by_uid(uid)


@app.route('/api/game/all', methods=['GET'])
def get_all_games():
    return db.get_all_games()


@app.route('/api/user/add', methods=['POST'])
def add_user_details():
    if request.method == 'POST':
        uid = request.form["uid"]
        dob = request.form["dob"]
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        gender = request.form["gender"]
        country = request.form["country"]

        db.add_user_details(uid, dob, firstName, lastName, gender, country)

        return {
            "status": "User details added."
        }

@app.route('/api/user', methods=['POST'])
def get_user_details():
    if request.method == 'POST':
        uid = request.form["uid"]

        return db.get_user_details(uid)


# this commands the script to run in the given port
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
