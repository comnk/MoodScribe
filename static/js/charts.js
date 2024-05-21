console.log(sentimentData);

document.addEventListener("DOMContentLoaded", function() {
    const ctx = document.getElementById('moodTrendChart').getContext('2d');
    const data = sentimentData;

    const labels = data.map(entry => entry.date);
    const sentimentScores = data.map(entry => entry.sentiment);
    
    let positiveCount = 0;
    let neutralCount = 0;
    let negativeCount = 0;

    sentimentData.forEach(entry => {
        if (entry.sentiment > 0) {
            positiveCount++;
        } else if (entry.sentiment === 0) {
            neutralCount++;
        } else {
            negativeCount++;
        }
    });

    const totalCount = sentimentData.length;
    const positivePercentage = (positiveCount / totalCount) * 100;
    const neutralPercentage = (neutralCount / totalCount) * 100;
    const negativePercentage = (negativeCount / totalCount) * 100;
    
    const sentimentCtx = document.getElementById('sentimentPieChart').getContext('2d');

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Mood Sentiment Over Time',
                data: sentimentScores,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Sentiment Score'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    enabled: true
                }
            }
        }
    });

    const sentimentChart = new Chart(sentimentCtx, {
        type: 'pie',
        data: {
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [{
                label: 'Sentiment Distribution',
                data: [positivePercentage, neutralPercentage, negativePercentage],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(255, 99, 132, 0.5)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Sentiment Distribution'
                }
            }
        }
    });
});

