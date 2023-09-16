let word;
let gameId;

async function loadWordAndGameId() {
    const response = await fetch('/get-word');
    const data = await response.json();
    word = data.word;
    gameId = data.game_id;
    document.getElementById('word').innerText = word;
}
window.addEventListener('load', loadWordAndGameId);



async function validateSong() {
    const songName = document.getElementById('songName').value;
    const response = await fetch('/validate-song', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ song_name: songName, game_id: gameId })
    });
    const data = await response.json();
    if(data.is_correct) {
        alert("Correct!");
    } else {
        alert("Wrong!");
    }
}
