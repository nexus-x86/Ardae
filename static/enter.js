var input = document.getElementById("songName");

// Add an event listener for the "keydown" event
input.addEventListener("keydown", function(event) {
    // Check if the key pressed is Enter (key code 13)
    if (event.key === 'Enter') {
        const songInput = document.getElementById('songName');
        // Call your function here or perform any desired action
        if(songInput.value != ""){
            validateSong();
        }
        songInput.value = "";
    }
});
