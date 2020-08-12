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
            document.getElementById("usrform1").submit();
        }
    });
}

function statistic() {
// Set new default font family and font color to mimic Bootstrap's default styling
    Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
    var ctx = document.getElementById("myPieChart");
    var myPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["verbe", "adjective", "nouns"],
            datasets: [{
                data: [document.getElementById("nbr_verb").value,
                    document.getElementById("nbr_adj").value,
                    document.getElementById("nbr_nom").value],
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
                hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
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
    document.getElementById("statistique_cadre").hidden = false;

}




