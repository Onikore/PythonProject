function getValues(className, textMode) {
    var res = [];
    var z = document.getElementsByClassName(className);
    for (let i = 0; i < z.length; i++) {
        var temp = z[i].innerText;
        textMode
            ? res.push(temp)
            : res.push(parseFloat(temp));
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
            labels: getValues('key', true),
            datasets: [{
                data: getValues('value', false),
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