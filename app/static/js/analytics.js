function initTopicRadarChart(topicData) {
  const ctx = document.getElementById("topicRadarChart");
  if (!ctx || !window.Chart) return;

  const labels = Object.keys(topicData);
  const dataValues = labels.map(l => {
    const item = topicData[l];
    return item.total > 0 ? Math.round((item.solved / item.total) * 100) : 0;
  });

  new Chart(ctx, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Topic Mastery %',
        data: dataValues,
        backgroundColor: 'rgba(88, 166, 255, 0.25)',
        borderColor: '#58a6ff',
        pointBackgroundColor: '#58a6ff',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#58a6ff'
      }]
    },
    options: {
      scales: {
        r: {
          angleLines: { color: '#30363d' },
          grid: { color: '#21262d' },
          pointLabels: { color: '#8b949e', font: { size: 11 } },
          suggestedMin: 0,
          suggestedMax: 100,
          ticks: { backdropColor: 'transparent', color: '#6e7681', stepSize: 25 }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}
