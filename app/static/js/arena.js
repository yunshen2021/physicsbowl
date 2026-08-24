let selectedOption = null;
let secondsElapsed = 0;
let timerInterval = null;

document.addEventListener("DOMContentLoaded", () => {
  // Start per-problem stopwatch
  startStopwatch();

  // Render KaTeX math
  renderAllMath();

  // Setup options selection
  setupOptionClicks();

  // Setup keyboard shortcuts (1-5 or A-E to select, Enter to submit)
  setupKeyboardShortcuts();

  // Load existing notes
  setupNotes();
});

function renderAllMath() {
  if (window.renderMathInElement) {
    window.renderMathInElement(document.body, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false }
      ],
      throwOnError: false
    });
  }
}

function startStopwatch() {
  const timerElem = document.getElementById("stopwatch-display");
  if (!timerElem) return;
  
  timerInterval = setInterval(() => {
    secondsElapsed++;
    const mins = Math.floor(secondsElapsed / 60).toString().padStart(2, '0');
    const secs = (secondsElapsed % 60).toString().padStart(2, '0');
    timerElem.textContent = `${mins}:${secs}`;
  }, 1000);
}

function setupOptionClicks() {
  const cards = document.querySelectorAll(".option-card");
  cards.forEach(card => {
    card.addEventListener("click", () => {
      selectOption(card.getAttribute("data-option"));
    });
  });
}

function selectOption(opt) {
  selectedOption = opt;
  document.querySelectorAll(".option-card").forEach(card => {
    if (card.getAttribute("data-option") === opt) {
      card.classList.add("selected");
    } else {
      card.classList.remove("selected");
    }
  });

  const submitBtn = document.getElementById("btn-submit-answer");
  if (submitBtn) {
    submitBtn.removeAttribute("disabled");
  }
}

function setupKeyboardShortcuts() {
  document.addEventListener("keydown", (e) => {
    // If typing in textarea, don't trigger shortcuts
    if (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT") return;

    const key = e.key.toUpperCase();
    const map = { "1": "A", "2": "B", "3": "C", "4": "D", "5": "E", "A": "A", "B": "B", "C": "C", "D": "D", "E": "E" };
    if (map[key]) {
      selectOption(map[key]);
    } else if (e.key === "Enter" && selectedOption) {
      submitAnswer();
    }
  });
}

async function submitAnswer() {
  if (!selectedOption) return;

  const submitBtn = document.getElementById("btn-submit-answer");
  if (submitBtn) submitBtn.disabled = true;

  try {
    const res = await fetch(`/api/problems/${window.PROBLEM_ID}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        selected_option: selectedOption,
        time_spent_seconds: secondsElapsed
      })
    });

    const data = await res.json();
    displayVerdict(data);
  } catch (err) {
    console.error("Submission error:", err);
    alert("Failed to submit answer. Check connection.");
    if (submitBtn) submitBtn.disabled = false;
  }
}

function displayVerdict(data) {
  const acceptedBox = document.getElementById("verdict-accepted");
  const wrongBox = document.getElementById("verdict-wrong");
  const solutionPanel = document.getElementById("solution-view");

  // Style the option cards
  document.querySelectorAll(".option-card").forEach(card => {
    const opt = card.getAttribute("data-option");
    if (opt === data.correct_answer) {
      card.classList.add("correct");
    } else if (opt === data.selected_option && !data.is_correct) {
      card.classList.add("incorrect");
    }
  });

  if (data.is_correct) {
    if (acceptedBox) acceptedBox.style.display = "block";
    if (wrongBox) wrongBox.style.display = "none";
    triggerConfetti();
  } else {
    if (acceptedBox) acceptedBox.style.display = "none";
    if (wrongBox) {
      wrongBox.style.display = "block";
      const txt = document.getElementById("wrong-explanation-text");
      if (txt) txt.textContent = `You selected (${data.selected_option}). The correct answer is (${data.correct_answer}).`;
    }
  }

  // Show and render solution
  if (solutionPanel) {
    solutionPanel.style.display = "block";
    renderAllMath();
  }
}

function triggerConfetti() {
  if (window.confetti) {
    window.confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 }
    });
  }
}

function switchLeftTab(tabId) {
  document.querySelectorAll(".panel-tab").forEach(tab => {
    if (tab.getAttribute("data-tab") === tabId) {
      tab.classList.add("active");
    } else {
      tab.classList.remove("active");
    }
  });

  document.querySelectorAll(".tab-pane").forEach(pane => {
    if (pane.id === `tab-${tabId}`) {
      pane.style.display = "block";
    } else {
      pane.style.display = "none";
    }
  });

  renderAllMath();
}

async function toggleBookmark(problemId) {
  const btn = document.getElementById("btn-bookmark");
  try {
    const res = await fetch(`/api/problems/${problemId}/bookmark`, { method: "POST" });
    const data = await res.json();
    if (btn) {
      if (data.bookmarked) {
        btn.innerHTML = "★ Bookmarked";
        btn.style.color = "#ffa116";
      } else {
        btn.innerHTML = "☆ Bookmark";
        btn.style.color = "var(--text-secondary)";
      }
    }
  } catch (err) {
    console.error("Bookmark error:", err);
  }
}

function setupNotes() {
  const noteArea = document.getElementById("notes-textarea");
  if (!noteArea) return;

  let timeout = null;
  noteArea.addEventListener("input", () => {
    clearTimeout(timeout);
    timeout = setTimeout(async () => {
      try {
        await fetch(`/api/problems/${window.PROBLEM_ID}/note`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: noteArea.value })
        });
      } catch (err) {
        console.error("Failed to save note:", err);
      }
    }, 800);
  });
}

function toggleFormulaDrawer() {
  const drawer = document.getElementById("formula-drawer");
  const overlay = document.getElementById("drawer-overlay");
  if (!drawer) return;

  if (drawer.classList.contains("open")) {
    drawer.classList.remove("open");
    if (overlay) overlay.classList.remove("open");
  } else {
    drawer.classList.add("open");
    if (overlay) overlay.classList.add("open");
    renderAllMath();
  }
}
