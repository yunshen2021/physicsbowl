let contestTimeRemaining = 0;
let contestInterval = null;

function initContestTimer(totalSeconds) {
  contestTimeRemaining = totalSeconds;
  updateTimerUI();

  contestInterval = setInterval(() => {
    if (contestTimeRemaining > 0) {
      contestTimeRemaining--;
      updateTimerUI();

      if (contestTimeRemaining === 0) {
        clearInterval(contestInterval);
        alert("Time is up! Auto-submitting your contest exam.");
        submitContestExam(true);
      }
    }
  }, 1000);
}

function updateTimerUI() {
  const elem = document.getElementById("contest-timer");
  if (!elem) return;

  const mins = Math.floor(contestTimeRemaining / 60).toString().padStart(2, '0');
  const secs = (contestTimeRemaining % 60).toString().padStart(2, '0');
  elem.textContent = `${mins}:${secs}`;

  // Warning colors
  if (contestTimeRemaining <= 60) {
    elem.style.color = "#f85149"; // Red
  } else if (contestTimeRemaining <= 300) {
    elem.style.color = "#d29922"; // Yellow
  }
}
