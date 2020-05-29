let testData = {
    labels: ['Extraversion', 'Consciousness', 'Agreeableness', 'Neuroticism', 'Openness'],
    datasets: [
    {
        label: 'Results',
        fill: true,
        backgroundColor: "rgba(96,184,150,0.2)",
        borderColor: "rgba(96,184,150,1)",
        pointBorderColor: "rgba(50,50,50,1)",
        pointBackgroundColor: "rgba(96,184,150,0.2)",
        labels: ['Extraversion', 'Consciousness', 'Agreeableness', 'Neuroticism', 'Openness'],
        //data: [{{ data.EXT }}, {{ data.CON }}, {{ data.AGR }}, {{ data.NEU }}, {{ data.OPN }}]
    }]
};
let testOptions = {
    responsive: true,
    legend: {
        position: 'top',
    },
    title: {
        display: true,
        text: 'Test results'
    },
    scale: {
        angleLines: {
            display: false
        },
        ticks: {
            suggestedMin: 0,
            suggestedMax: 100
        }
    }
};

window.onload = function() {
  new Chart(document.getElementById("chart"), {
    type: 'radar',
    data: testData,
    options: testOptions
    });
}