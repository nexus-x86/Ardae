from flask import Flask, render_template, request, jsonify
from lyricsgenius import Genius
import requests
import json
from init_word_db import *
import random
import lyricModule

app = Flask(__name__)

secretFile = json.load(open("secret.json"))
genius = Genius(secretFile["clientAccessToken"], timeout = 15)

currentWord = ""

guessed = []

class Guess():
    def __init__(self, guess_name, song_name, is_correct, song_image):
        self.song_name = song_name
        self.is_correct = is_correct
        self.guess_name = guess_name
        self.song_image = song_image

guesses = []

@app.route('/timer-done', methods=['GET'])
def timerDone():
    global guesses
    print(guessed)
    if len(guesses) == 0:
        print("No guesses")
        return jsonify(error = "No guesses"),
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

    return jsonify(word=currentWord)

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

    guess = Guess(song_name, ourSong.title, is_correct, ourSong.song_art_image_thumbnail_url)

    global guesses
    guesses.append(guess)

    return jsonify(is_correct=is_correct)

@app.route('/')
def index():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)
