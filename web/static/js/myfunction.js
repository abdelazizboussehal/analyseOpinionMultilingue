function testhttp() {
    const Http = new XMLHttpRequest();
    const url = 'http://127.0.0.1:5000/test';
    Http.open("GET", url, false);
    Http.send();

    Http.onreadystatechange = (e) => {
        console.log(Http.responseText);
    }
}


function submitform() {
    document.getElementById("usrform").submit();
}

function correction(id) {
    var textarea = document.getElementById("exampleFormControlTextarea1");
    var str = textarea.value;
    var text1 = id.innerText;
    var text2 = id.parentNode.childNodes[1].innerText
    var res = str.replace(text2, text1);
    textarea.value = res;
    id.parentNode.hidden = true;
    var nbr_error = document.getElementById("nbr_errors");
    nbr_error.innerText = parseInt(nbr_error.innerText) - 1;


}

function uploadfile() {
    var input = document.getElementById('filetext');
    var fullPath = document.getElementById('upload').value;
    if (fullPath) {
        var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
        var filename = fullPath.substring(startIndex);
        if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
            filename = filename.substring(1);
        }
        input.innerText = filename;
        document.getElementById('button_file').hidden = false;
    }
}

function starprogress() {
    document.getElementById("countdown").hidden = false;
    $("#countdown").progressBarTimer({
        autoStart: true,
        timeLimit: 10, //total number of seconds
        warningThreshold: 5, //seconds remaining triggering switch to warning color
        autoStart: true, // start the countdown automatically //invoked once the timer expires
        baseStyle: '', //bootstrap progress bar style at the beginning of the timer
        warningStyle: 'bg-danger', //bootstrap progress bar style in the warning phase
        smooth: false, // should the timer be smooth or stepping
        completeStyle: 'bg-success', //bootstrap progress bar style at completion of timer
        onFinish: function () {

        }
    });
}

function statistic() {
// Set new default font family and font color to mimic Bootstrap's default styling
    Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#858796';
    console.log(document.getElementById("nbr_aux").value + "+++" +
        document.getElementById("nbr_proprn").value);

// Pie Chart Example
    var ctx = document.getElementById("mon_model");
    var myPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["verbe", "adjective", "nouns", "auxiliaire", "propre nom", "autre"],
            datasets: [{
                data: [document.getElementById("nbr_verb").value,
                    document.getElementById("nbr_adj").value,
                    document.getElementById("nbr_nom").value,
                    document.getElementById("nbr_aux").value,
                    document.getElementById("nbr_proprn").value,
                    document.getElementById("nbr_autre").value],
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#23cc2d', '#36b9cc', '#23cc2d'],
                hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#cc37c7', '#2c9faf', '#cc37c7'],
                hoverBorderColor: "rgba(234, 236, 244, 1)",
            }],
        },
        options: {
            maintainAspectRatio: false,
            tooltips: {
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10,
            },
            legend: {
                display: false
            },
            cutoutPercentage: 80,
        },
    });
}

function save_graphe() {
    var canvas = document.getElementById('mon_model');
    var context = canvas.getContext('2d');
    var button = document.getElementById("save_button");

    // only jpeg is supported by jsPDF
    var imgData = canvas.toDataURL();
    button.href = imgData;
    button.download = "graphe.png";
}

function save_graphe_column() {
    var canvas = document.getElementById('myBarChart');
    var context = canvas.getContext('2d');
    var button = document.getElementById("save_button1");

    // only jpeg is supported by jsPDF
    var imgData = canvas.toDataURL();
    button.href = imgData;
    button.download = "graphe_column.png";
}

function save_table() {
    $("#dataTable").tableHTMLExport({
        // csv, txt, json, pdf
        type: 'csv',
        // file name
        filename: 'csv.pdf'
    });
}

function reprocess_correction() {
    document.getElementById("form_correction").submit();
}


function reprocess_subjectivity() {
    document.getElementById("form_subjectivity").submit();
}


function number_format(number, decimals, dec_point, thousands_sep) {
    // *     example: number_format(1234.56, 2, ',', ' ');
    // *     return: '1 234,56'
    number = (number + '').replace(',', '').replace(' ', '');
    var n = !isFinite(+number) ? 0 : +number,
        prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
        sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
        dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
        s = '',
        toFixedFix = function (n, prec) {
            var k = Math.pow(10, prec);
            return '' + Math.round(n * k) / k;
        };
    // Fix for IE parseFloat(0.55).toFixed(0) = 0;
    s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
    if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
    }
    if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
    }
    return s.join(dec);
}

function statistic2() {
    // Set new default font family and font color to mimic Bootstrap's default styling
    Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#858796';
    console.log(document.getElementById("nbr_aux").value + "+++" +
        document.getElementById("nbr_proprn").value);

// Bar Chart Example
    var ctx = document.getElementById("myBarChart");
    var myBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["Noms", "Verbes", "Adjectifs", "Auxiliaire", "Propre nom", "Autres"],
            datasets: [{
                label: "Revenue",
                backgroundColor: "#4e73df",
                hoverBackgroundColor: "#2e59d9",
                borderColor: "#4e73df",
                data: [document.getElementById("nbr_verb").value,
                    document.getElementById("nbr_adj").value,
                    document.getElementById("nbr_nom").value,
                    document.getElementById("nbr_aux").value,
                    document.getElementById("nbr_proprn").value,
                    document.getElementById("nbr_autre").value],
            }],
        },
        options: {
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0
                }
            },
            scales: {
                xAxes: [{
                    time: {
                        unit: 'month'
                    },
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 6
                    },
                    maxBarThickness: 25,
                }],
                yAxes: [{
                    ticks: {
                        min: 0,
                        max: document.getElementById("total").value,
                        maxTicksLimit: 5,
                        padding: 10,
                        // Include a dollar sign in the ticks
                        callback: function (value, index, values) {
                            return number_format(value);
                        }
                    },
                    gridLines: {
                        color: "rgb(234, 236, 244)",
                        zeroLineColor: "rgb(234, 236, 244)",
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    }
                }],
            },
            legend: {
                display: false
            },
            tooltips: {
                titleMarginBottom: 10,
                titleFontColor: '#6e707e',
                titleFontSize: 14,
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10,
                callbacks: {
                    label: function (tooltipItem, chart) {
                        var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                        return number_format(tooltipItem.yLabel);
                    }
                }
            },
        }
    });

}

function visualizer_dep(bt) {
    var content = bt.previousSibling.previousSibling.previousSibling.previousSibling.value;
    document.getElementById("div_vis_dep").innerHTML = content;
    $('#list_vis_dep').modal('show');
}

function visualizer_ent(bt) {
    var content = bt.previousSibling.previousSibling.previousSibling.previousSibling.value;
    document.getElementById("div_vis_dep").innerHTML = content;
    $('#list_vis_dep').modal('show');
}



