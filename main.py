from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from lyricsgenius import Genius
import requests
import json
from init_word_db import *
import random
import lyricModule

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
db = SQLAlchemy(app)

secretFile = json.load(open("secret.json"))
genius = Genius(secretFile["clientAccessToken"], timeout = 15)

currentWord = ""

guessed = []

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    guesses = db.relationship('Guess', backref='game', lazy=True)

class Guess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(300), nullable=False)
    is_correct = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/timer-done', methods=['GET'])
def timerDone():
    game_id = request.args.get('game_id')
    if not game_id:
        return jsonify(error = "Game ID is required!"),400
    guesses = Guess.query.filter_by(game_id=game_id).all()
    if not guesses:
        return jsonify(error = "No guesses for the provided game ID"),
    correct_guesses = [guess for guess in guesses if guess.is_correct]
    incorrect_guesses = [guess for guess in guesses if not guess.is_correct ]

    response = {
        "correct_count": len(correct_guesses),
        "incorrect_count": len(incorrect_guesses),
        "correct_songs": [{"song_name": guess.song_name} for guess in correct_guesses],
        "incorrect_songs": [{"song_name": guess.song_name} for guess in incorrect_guesses]
    }

    return jsonify(response)

@app.route('/get-word', methods=['GET'])
def get_word():
    # put the dictionary api here, this is just dummy code for me
    words = word_list(150)
    global currentWord
    currentWord = random.choice(words)

    game = Game(word=currentWord)
    db.session.add(game)
    db.session.commit()
    return jsonify(word=currentWord, game_id=game.id)

def fetch_song(song_name, retries=2):  # 2 retries by default
    for i in range(retries):
        try:
            song = genius.search_song(song_name)
            if song != None:
                if song.id in guessed:
                    print("Your can't guess the same thing more then once!")
                    return "nuh uh"
                guessed.append(song.id)
                print("Added " + str(song.id) + " to gussed songs.")
            return song
        except requests.exceptions.ReadTimeout:
            print(f"Request timeout. Retry attempt {i+1}...")

    print(f"Failed to fetch song after {retries} attempts.")
    return None

@app.route('/validate-song', methods=['POST'])
def validate_song():
    song_name = request.json.get('song_name')
    game_id = request.json.get('game_id')
    
    ourSong = fetch_song(song_name)

    is_correct = 0 # 3 means already guessed
    if type(ourSong) == str:
        is_correct = 3
    else:
        if ourSong:
            if lyricModule.songContains(ourSong.id, currentWord):
                is_correct = 1
            else:
                is_correct = 0
            #print(ourSong.lyrics)
        else:
            print("Song fetch failed")
            is_correct = 0 


    guess = Guess(song_name=song_name, is_correct=is_correct, game_id=game_id)
    
    db.session.add(guess)
    db.session.commit()
    return jsonify(is_correct=is_correct)

@app.route('/reset', methods = ['GET'])
def reset():
    global guessed
    guessed = []
    print("Guesses reset")
    return 'testresponse', 204  # HTTP status code 204 (No Content)

@app.route('/')
def index():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)