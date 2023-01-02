function getValues(className) {
    var res = [];
    var z = document.getElementsByClassName(className);
    for (let i = 0; i < z.length; i++) {
        res.push(parseFloat(z[i].innerText));
    }
    return res;
}

(function () {
    'use strict'
    feather.replace({'aria-hidden': 'true'})
    var ctx = document.getElementById('myChart')
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: getValues('key'),
            datasets: [{
                data: getValues('value'),
                lineTension: 0,
                backgroundColor: 'transparent',
                borderColor: '#007bff',
                borderWidth: 4,
                pointBackgroundColor: '#007bff'
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }]
            },
            legend: {
                display: false
            }
        }
    })
})()

