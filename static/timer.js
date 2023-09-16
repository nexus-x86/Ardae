function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = 0; // Timer stops at 0:00
            // You can add additional actions here when the timer reaches 0
        }
    }, 1000);
}

// Start the timer when the page loads
window.onload = function () {
    var oneMinute = 59, // 60 seconds
        display = document.querySelector('#timer');
    startTimer(oneMinute, display);
};
