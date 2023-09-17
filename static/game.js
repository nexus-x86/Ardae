let word;
let gameId;
let displayedResults = false;

async function loadWordAndGameId() {
    const response = await fetch('/get-word');
    const data = await response.json();
    word = data.word;
    gameId = data.game_id;
    document.getElementById('word').innerText = word;

    window.gameId = gameId; // Set the global gameId variable
}

async function validateSong() {
    const songName = document.getElementById('songName').value;
    const response = await fetch('/validate-song', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ song_name: songName, game_id: gameId })
    });
    const data = await response.json();
    if(data.is_correct == 1) {
        alert("Correct!");
    } else if (data.is_correct == 0) {
        alert("Wrong!");
    }
    else{
        alert("Already guessed");
    }
}

function displayResults(data) {
    const resultsDiv = document.createElement("div");
    resultsDiv.id='res';
    resultsDiv.innerHTML = `
        <h3>Results</h3>
        <p>Correct Songs: ${data.correct_count}</p>
        <ul>${data.correct_songs.map(song => `<li>${song.song_name}</li>`).join('')}</ul>
        <p>Incorrect Songs: ${data.incorrect_count}</p>
        <ul>${data.incorrect_songs.map(song => `<li>${song.song_name}</li>`).join('')}</ul>
    `;

    document.body.appendChild(resultsDiv);
}

async function startGame() {
    loadWordAndGameId(); // Fetch the word and gameId.
    document.getElementById('word').style.display = 'block'; // Show the word.
    startTimerOnLoad(); // Start the timer.

    document.getElementById('startButton').style.display = 'none'; // Hide start button.
    document.getElementById('restartButton').style.display = 'block'; // Show restart button.

    const response = await fetch('/reset')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        console.log('Reset successful');
        // You can add further handling if needed
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function restartGame() {
    stopTimer(); // Stop the current timer.
    // clear the previous results
    const resultsDiv = document.getElementById("res");
    if (resultsDiv) {
        resultsDiv.innerHTML = '';
    }
    startGame(); // Re-initialize the game.
}

window.addEventListener('load', () => {
    document.getElementById('word').style.display = 'none'; // Hide the word initially.
    document.getElementById('restartButton').style.display = 'none'; // Hide the restart button initially.
    document.getElementById('startButton').addEventListener('click', startGame);
    document.getElementById('restartButton').addEventListener('click', restartGame);
});
