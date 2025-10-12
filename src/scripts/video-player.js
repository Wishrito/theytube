const video = document.getElementById("video");
const playPauseBtn = document.getElementById("play-pause");
const playIcon = document.getElementById("play-icon");
const pauseIcon = document.getElementById("pause-icon");
const timeDisplay = document.getElementById("time-display");
const progressBar = document.getElementById("progress");
const progressContainer = document.getElementById("progress-bar-container");
const muteBtn = document.getElementById("mute");
const volumeSlider = document.getElementById("volume");
const fullscreenBtn = document.getElementById("fullscreen");
const videoContainer = document.querySelector(".video-container");

// Lecture / pause
playPauseBtn.addEventListener("click", () => {
    if (video.paused) {
        video.play();
        playIcon.style.display = "none";
        pauseIcon.style.display = "block";
    } else {
        video.pause();
        playIcon.style.display = "block";
        pauseIcon.style.display = "none";
    }
});

// Temps
video.addEventListener("timeupdate", () => {
    const current = video.currentTime;
    const duration = video.duration || 0;

    const percent = (current / duration) * 100;
    progressBar.style.width = `${percent}%`;

    const format = (t) => String(Math.floor(t / 60)).padStart(2, "0") + ":" + String(Math.floor(t % 60)).padStart(2, "0");
    timeDisplay.textContent = `${format(current)} / ${format(duration)}`;
});

// Barre de progression cliquable
progressContainer.addEventListener("click", (e) => {
    const rect = progressContainer.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    video.currentTime = percent * video.duration;
});

// Volume
volumeSlider.addEventListener("input", () => {
    video.volume = volumeSlider.value;
    muteBtn.textContent = video.volume === 0 ? "🔇" : "🔊";
});

muteBtn.addEventListener("click", () => {
    video.muted = !video.muted;
    muteBtn.textContent = video.muted ? "🔇" : "🔊";
});

// Plein écran
fullscreenBtn.addEventListener("click", () => {
    if (!document.fullscreenElement) {
        videoContainer.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
});
