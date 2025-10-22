function bgClimate(temperatura) {
  const bg = document.getElementById("bgClimate");
  if (!bg || isNaN(temperatura)) return;

  let gradient;
  if (temperatura <= 25) {
    gradient = "linear-gradient(#1E90FF, #00008B)"; // frio
  } else if (temperatura <= 35) {
    gradient = "linear-gradient(#FFD700, #FF8C00)"; // quente moderado
  } else {
    gradient = "linear-gradient(#FF4500, #FFD700)"; // muito quente
  }

  bg.style.transition = "background 1s ease";
  bg.style.background = gradient;
}
