// Historical Trend Scorer Chart Manager (Chart.js)
let trendChartInstance = null;

function initTrendChart() {
  const ctx = document.getElementById('trendChart').getContext('2d');

  trendChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Check-in 1', 'Check-in 2', 'Check-in 3', 'Check-in 4', 'Check-in 5'],
      datasets: [
        {
          label: '3-Way Congruence %',
          data: [85, 90, 45, 78, 92],
          borderColor: '#00f2fe',
          backgroundColor: 'rgba(0, 242, 254, 0.1)',
          fill: true,
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 4,
          pointBackgroundColor: '#00f2fe'
        },
        {
          label: 'Sentiment Score',
          data: [70, 80, 40, 65, 85],
          borderColor: '#7c3aed',
          backgroundColor: 'transparent',
          borderDash: [5, 5],
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: '#94a3b8',
            font: { family: 'Outfit', size: 12 }
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748b' }
        },
        y: {
          min: 0,
          max: 100,
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748b' }
        }
      }
    }
  });
}

function updateTrendChart(historyData) {
  if (!trendChartInstance || !historyData || historyData.length === 0) return;

  const labels = historyData.map((item, idx) => {
    const timeStr = new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    return `#${idx + 1} (${timeStr})`;
  });

  const congruenceData = historyData.map(item => item.congruence_score);
  const sentimentData = historyData.map(item => Math.round((item.sentiment_score + 1) * 50)); // Normalize [-1, 1] -> [0, 100]

  trendChartInstance.data.labels = labels;
  trendChartInstance.data.datasets[0].data = congruenceData;
  trendChartInstance.data.datasets[1].data = sentimentData;
  trendChartInstance.update();
}

window.addEventListener('DOMContentLoaded', initTrendChart);
