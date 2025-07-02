async function fetchData() {
  const url = document.getElementById("chart").getAttribute("data-url");
  const response = await fetch(url);
  const data = await response.json();
  return data;
}

async function renderChart() {
  const ctx = document.getElementById('chart').getContext('2d');
  const rawData = await fetchData();

  // Criar um array de cores dinâmico
  const backgroundColors = rawData.datasets[0].data.map(temp => {
    if (temp <= 10) {
      return "#1E90FF"; 
    } else if (temp <= 25) {
      return "#00008B"; 
    } else if (temp <= 35) {
      return "#FF8C00"; 
    } else {
      return "#FF4500"; 
    }
  });

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: rawData.labels,
      datasets: [{
        label: "Temperatura (°C)",
        data: rawData.datasets[0].data,
        backgroundColor: backgroundColors,
        borderColor: "#fff",
        borderWidth: 1,
        borderRadius: 10,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            label: function(tooltipItem) {
              return ` ${tooltipItem.raw}°C`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", renderChart);
