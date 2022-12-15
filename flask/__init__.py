import FlaskApp.db

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
from flask import Response, send_file

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_call():
    return "Hello World!"


@app.route('/api/games', methods=['GET'])
def get_games_by_uid():
    return "Hey!! I'm the fact you got!!!"


@app.route('/api/games/new', methods=['GET'])
def get_new_games():
    return "Hey!! I'm the fact you got!!!"


@app.route('/api/game/add', methods=['POST'])
def add_game(name):
    return "I got your name " + name


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


# @app.route('/insert', methods=['post'])
# def insert():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         gender = request.form['optradio']
#         comment = request.form['comment']
#         db.insert_details(name, email, comment, gender)
#         details = db.get_details()
#         print(details)
#         for detail in details:
#             var = detail
#         return render_template('index.html', var=var)


# this commands the script to run in the given port
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
