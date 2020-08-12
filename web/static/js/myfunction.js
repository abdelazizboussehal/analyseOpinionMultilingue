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




