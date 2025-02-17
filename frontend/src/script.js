const item_names = [
  "Banana",
  "Bomb",
  "redShroom",
  "goldShroom",
  "redShell",
  "blueShell",
  "lightning",
  "bulletBill",
];
const powerUpImages = document.querySelectorAll(".slideshow img");

let countDownDuration = 5000; // Total countdown time in miliseconds
let countDownStart = 0;
let timerVisible = false;

function drawArc(state) {
  console.log("drawArc", state.canvas.width, state.canvas.height);
  state.ctx.clearRect(0, 0, state.canvas.width, state.canvas.height); // Clear the canvas
  state.ctx.beginPath();
  const percentage = state.durationTime == 0 ? 0 : state.elapsedTime / state.durationTime;
  console.log("percentage", percentage);
  state.ctx.arc(
    state.canvas.width / 2,
    state.canvas.height / 2,
    170,
    1.5 * Math.PI,
    1.5 * Math.PI + 2 * Math.PI * percentage,
    true
  );
  state.ctx.lineWidth = 8;
  state.ctx.strokeStyle = "blue";
  state.ctx.stroke();
  state.ctx.closePath();
  console.log(1.5 * Math.PI, 1.5 * Math.PI + 2 * Math.PI * percentage);
}

function hidePowerUp(state) {
  state.powerUpImages.forEach((img) => img.classList.remove("active"));
}

function updateTimer(state) {
  let elapsed = new Date().getTime() - state.countDownStart;
  if (elapsed < state.countDownDuration && state.timerVisible) {
    drawArc(elapsed, state.countDownDuration);
    requestAnimationFrame(() => updateTimer(state.countDownStart)); // Call the next frame with a parameter
  } else {
    hideTimer(); // Ensure the arc is fully drawn at the end
    hidePowerUp();
    console.log("Countdown finished!");
  }
}

function showTimer(state) {
  console.log("show timer");
  drawArc(state);
  state.timerVisible = true;
}

function hideTimer(state) {
  console.log("hide timer");
  drawArc(1, 1);
  state.timerVisible = false;
}

// Show powerup
let index = 0;

function changeImage(state) {
  state.powerUpImages.forEach((img) => img.classList.remove("active"));
  index = (index + 1) % state.powerUpImages.length;
  state.powerUpImages[index].classList.add("active");
}

function showItem(state, item) {
  console.log("show item");
  let startTime = new Date().getTime();
  let intervalId = setInterval(function () {
    changeImage(state);
    if (new Date().getTime() - startTime >= 1000) {
      clearInterval(intervalId);
      state.powerUpImages.forEach((img) => img.classList.remove("active"));
      state.powerUpImages[item].classList.add("active");
    }
  }, 100);
  console.log(powerUpImages[item]);
}

const trapImages = document.querySelectorAll(".warning img");
const warningPopup = document.querySelectorAll(".warning");
let imageShowing = false;

function blinkImage(state, item) {
  if (state.imageShowing) {
    state.trapImages[item].classList.remove("active");
  } else {
    state.trapImages[item].classList.add("active");
  }
  state.imageShowing = !state.imageShowing;
}

//Show warning
function showWarning(state, item) {
  hidePowerUp();
  hideTimer();
  console.log("incoming item");
  let startTime = new Date().getTime();
  let intervalId = setInterval(function () {
    document.getElementById("warningDiv").style.backgroundColor = "red";
    blinkImage(item);
    if (new Date().getTime() - startTime >= 5000) {
      clearInterval(intervalId);
      trapImages[item].classList.remove("active");
      document.getElementById("warningDiv").style.backgroundColor = "transparent";
    }
  }, 100);
}

export { showTimer, showItem, showWarning, hidePowerUp, hideTimer, updateTimer };
