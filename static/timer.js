function displayResults(data) {
    const resultsDiv = document.createElement("div");
    resultsDiv.innerHTML = `
        <h3>Results</h3>
        <p>Correct Songs: ${data.correct_count}</p>
        <ul>${data.correct_songs.map(song => `<li>${song.song_name}</li>`).join('')}</ul>
        <p>Incorrect Songs: ${data.incorrect_count}</p>
        <ul>${data.incorrect_songs.map(song => `<li>${song.song_name}</li>`).join('')}</ul>
    `;

    // Append results to the body (or another container div)
    document.body.appendChild(resultsDiv);
}

let displayedResults = false;


function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(async function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = 0; // Timer stops at 0:00
            // You can add additional actions here when the timer reaches 0
            const response = await fetch(`/timer-done?game_id=${gameId}`);
            const data = await response.json();

            // Display results on the website
            if (!displayedResults) {
                displayedResults = true;
                displayResults(data);
            }
        }
    }, 1000);
}

// Start the timer when the page loads
function startTimerOnLoad() {
    var oneMinute = 59, // 60 seconds
        display = document.querySelector('#timer');
    startTimer(oneMinute, display);
}
window.addEventListener('load', startTimerOnLoad);

