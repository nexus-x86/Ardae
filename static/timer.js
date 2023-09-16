let timerInterval;

function stopTimer() {
    clearInterval(timerInterval);
}

function startTimer(duration, display) {
    stopTimer(); // Ensure any existing timer is stopped.
    
    var timer = duration, minutes, seconds;
    timerInterval = setInterval(async function() {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = 0;
            stopTimer();

            const response = await fetch(`/timer-done?game_id=${gameId}`);
            const data = await response.json();

            if (!displayedResults) {
                displayedResults = true;
                displayResults(data);
            }

            document.getElementById('restartButton').style.display = 'block'; // Show the restart button.
        }
    }, 1000);
}

// Start the timer when the start button is pressed
function startTimerOnLoad() {
    var oneMinute = 59, // 60 seconds
        display = document.querySelector('#timer');
    startTimer(oneMinute, display);
}
