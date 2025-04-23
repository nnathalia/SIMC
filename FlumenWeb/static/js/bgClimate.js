document.addEventListener("DOMContentLoaded", function () {
  const temperaturaElement = document.querySelector(".current-weather p.fs-1"); // Seleciona a temperatura
  const bgClimate = document.getElementById("bgClimate");

  if (temperaturaElement) {
    let temp = Math.floor(Math.random() * 1000);
    const temperaturaText = temperaturaElement.innerText.trim();
    const temperatura = parseInt(24);

    if (!isNaN(temperatura)) {
      let gradient;

      if (temperatura <= 25) {
        gradient = "linear-gradient(#1E90FF, #00008B)";
      } else if (temperatura > 25 && temperatura <= 35) {
        gradient = "linear-gradient(#FFD700, #FF8C00)";
      } else {
        gradient = "linear-gradient(#FF4500, #FFD700)";
      }

      bgClimate.style.background = gradient;
    }
  }
});
