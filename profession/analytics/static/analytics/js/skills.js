function getValues(key, textMode, year) {
    var res = [];
    var z = document.getElementsByClassName('year');
    for (let i = 0; i < z.length; i++) {
        var temp = z[i].cells[key].innerHTML;
        if (z[i].dataset.year === year) {
            textMode
                ? res.push(temp)
                : res.push(parseFloat(temp));
        }
    }
    return res;
}
function chartUpdater(year) {
    feather.replace({'aria-hidden': 'true'})
    var ctx = document.getElementById('myChart')
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: getValues(0, true, year),
            datasets: [{
                data: getValues(1, false, year),
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
}

function tableUpdater(event, firstRun) {
    let selectedYear = (firstRun)
        ? '2015'
        : event.target.value;
    let elems = document.getElementsByClassName('year');
    for (let i = 0; i < elems.length; i++) {
        let elem = elems[i];
        if (elem.dataset.year === selectedYear) {
            elem.style.display = 'table-row';
        } else {
            elem.style.display = 'none';
        }
    }
}

let selector = document.querySelector('select');

tableUpdater(null, true);
chartUpdater('2015');
selector.addEventListener('change', function (event) {
    chartUpdater(event.target.value);
    tableUpdater(event);
});



