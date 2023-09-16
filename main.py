from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from lyricsgenius import Genius
import requests
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
db = SQLAlchemy(app)

secretFile = json.load(open("secret.json"))
genius = Genius(secretFile["clientAccessToken"])

currentWord = ""

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    guesses = db.relationship('Guess', backref='game', lazy=True)

class Guess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(300), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/get-word', methods=['GET'])
def get_word():
    # put the dictionary api here, this is just dummy code for me
    import random
    words = ['love', 'world', 'life', 'night', 'music'] 
    global currentWord
    currentWord = random.choice(words)

    game = Game(word=currentWord)
    db.session.add(game)
    db.session.commit()
    return jsonify(word=currentWord, game_id=game.id)

@app.route('/validate-song', methods=['POST'])
def validate_song():
    song_name = request.json.get('song_name')
    game_id = request.json.get('game_id')
    # dummy code for now, replace with actual music lyrics database/API check.
    # going to fuzzy search genius for the song
    ourSong = genius.search_song(song_name)
    is_correct = False
    if ourSong:
        if currentWord in ourSong.lyrics: # this .lyrics needs to be pruned
            is_correct = True
        else:
            is_correct = False
    else:
        return "-1" # song not found


    guess = Guess(song_name=song_name, is_correct=is_correct, game_id=game_id)
    
    db.session.add(guess)
    db.session.commit()
    return jsonify(is_correct=is_correct)

@app.route('/')
def index():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)
