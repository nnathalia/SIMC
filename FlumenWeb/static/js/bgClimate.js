document.addEventListener("DOMContentLoaded", function () {
  const temperaturaElement = document.getElementById("temperatura");
  const bgClimate = document.getElementById("bgClimate");

  if (temperaturaElement) {
    const temperaturaText = temperaturaElement.innerText.trim().replace("°C", "");
    const temperatura = parseInt(temperaturaText);
    console.log("Temperatura lida:", temperatura);
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
