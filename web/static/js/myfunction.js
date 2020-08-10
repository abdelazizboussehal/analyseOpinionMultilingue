function testhttp() {
    const Http = new XMLHttpRequest();
    const url = 'http://127.0.0.1:5000/test';
    Http.open("GET", url, false);
    Http.send();

    Http.onreadystatechange = (e) => {
        console.log(Http.responseText);
    }
}

function includeHTML(id, filename) {
    console.log("aziz");
    var elmnt, file, xhttp;

    elmnt = document.getElementById(id);
    /*search for elements with a certain atrribute:*/
    file = filename;
    if (file) {
        /* Make an HTTP request using the attribute value as the file name: */
        xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    elmnt.innerHTML = this.responseText;
                }
                if (this.status == 404) {
                    elmnt.innerHTML = "Page not found.";
                }

            }
        }
        xhttp.open("GET", file, true);
        xhttp.send();
        /* Exit the function: */
        return;
    }

}

function submitform() {
    document.getElementById("usrform").submit();
}

//multi step animation
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches
function next(id_current, id_next) {
    current_fs = $('#' + id_current);
    next_fs = $('#' + id_next);
    //activate next step on progressbar using the index of next_fs
    $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

    //show the next fieldset
    next_fs.show();
    //hide the current fieldset with style
    current_fs.hide();

}

function previous(id_current, id_prev) {

    if (animating) return false;
    animating = true;

    current_fs = $('#' + id_current);
    previous_fs = $('#' + id_prev);

    //de-activate current step on progressbar
    $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

    //show the previous fieldset
    previous_fs.show();
    current_fs.hide();
}

function next_pretraitment() {
    // pre-fill FormData from the form
    let formData = new FormData();
    var x = document.getElementById("myTextarea").value;
    // add one more field
    formData.append("input", x);

    // send it out
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/json/correction");
    xhr.send(formData);

    xhr.onload = function () {
        if (xhr.status != 200) { // analyze HTTP status of the response
            alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
        } else { // show the result
            next("fld1", "fld2");
            var jsons = JSON.parse(xhr.responseText);
            console.log(JSON.stringify(jsons));
            var language = jsons.language;
            var texte = jsons.content;
            var words = jsons.list_word;
            var sugestion = jsons.list_suggestion;
            var htmlcorrection = '<div class="card shadow mb-4 card border-left-primary shadow h-100 py-2 mx-2 my-2">\n' +
                '        <div class="d-flex flex-row justify-content-center card-header py-3">\n' +
                '            <h6 class="m-0 font-weight-bold text-primary">Texte</h6>\n' +
                '        </div>\n' +
                '        <h5 class="m-0 font-weight-bold text-primary mx-2">langue est :' + language;
            htmlcorrection = htmlcorrection + '</h5>\n' +
                '        <div class="d-flex flex-row justify-content-center card-body">\n' +
                '            <textarea class="form-control" id="Textareacorrection" rows="3">' +
                texte + '</textarea>\n' +
                '        </div>';
            for (var i = 0; i < words[0].length; i++) {
                htmlcorrection = htmlcorrection + '<div class="d-flex flex-row justify-content-star align-items-center ml-4">' +
                    '<p>' + words[0][i] + '</p>';
                for (var j = 0; j < sugestion[0][i].length; j++) {
                    htmlcorrection = htmlcorrection + '<a onclick="correct_suggestion(this)" href="#" class="btn btn-danger btn-icon-split px-2 my-2 mx-2">\n' +
                        '                <span class="text">' + sugestion[0][i][j] + '</span>\n' +
                        '            </a>\n' +
                        '            ';
                }
                htmlcorrection = htmlcorrection + '</div>\n' +
                    '        ';

            }
            htmlcorrection = htmlcorrection + '<hr class="mx-4">\n' +
                '        <div class="d-flex flex-row justify-content-center card-body justify-content-around">\n' +
                '\n' +
                '            <a href="#" onclick="prev_correction()" class="btn btn-danger btn-icon-split">\n' +
                '                <span class="icon text-white-50">\n' +
                '                        <i class="fas fa-arrow-circle-left"></i>\n' +
                '                </span>\n' +
                '                <span class="text">precedent</span>\n' +
                '            </a>\n' +
                '            <a href="#" onclick="next_correction()" class="btn btn-primary btn-icon-split">\n' +
                '                <span class="icon text-white-50">\n' +
                '                    <i class="fas fa-chevron-circle-right"></i>\n' +
                '                </span>\n' +
                '                <span class="text">suivant</span>\n' +
                '            </a>\n' +
                '\n' +
                '        </div>\n' +
                '\n' +
                '    </div>\n';

            document.getElementById("maincontainer2").innerHTML = htmlcorrection;
            console.log(words)

        }
    };
}

function prev_correction() {
    previous("fld2", "fld1");
}

function correct_suggestion() {
    var x=$(this).attr('id');
    debugger;
}

function next_correction() {
    // pre-fill FormData from the form
    let formData = new FormData();
    var x = document.getElementById("Textareacorrection").value;
    // add one more field
    formData.append("input", x);

    // send it out
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/json/Segmentation");
    xhr.send(formData);

    xhr.onload = function () {
        if (xhr.status != 200) { // analyze HTTP status of the response
            alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
        } else { // show the result
            var jsons = JSON.parse(xhr.responseText);
            console.log(JSON.stringify(jsons));
            var formsub=document.getElementById("maincontainer3");
            var phrases=jsons.sentences;
            console.log("hhhhhhhhhhh+"+phrases[0]);
            var subjective=jsons.subjective_state;
            var htmlform='<div class="card shadow mb-4 card border-left-primary shadow h-100 py-2 mx-2 my-2">\n' +
                '        <div class="d-flex flex-row justify-content-center card-header py-3">\n' +
                '            <h6 class="m-0 font-weight-bold text-primary">Liste des phrases</h6>\n' +
                '        </div>\n' +
                '\n' +
                '        <form class="d-flex flex-row align-items-center mx-4 my-4">';
            for(var i=0; i <phrases.length;i++){
                htmlform=htmlform+'<form class="d-flex flex-row align-items-center mx-4 my-4">'+
                '<label id="input" name="input'+i+'" value="1"> '+phrases[i]+'</label>'+
                '<input type="hidden" name="r_id'+i+'" value="'+phrases[i]+'" />'+
                    '<div class="mx-4">\n' +
                    '                <div class="form-check">\n' +
                    '                    <label class="form-check-label">\n' +
                    '                <input type="radio" class="form-check-input" name="optradio" checked>porteurse</label>\n' +
                    '                </div>\n' +
                    '                <div class="form-check">\n' +
                    '                    <label class="form-check-label">\n' +
                    '                <input type="radio" class="form-check-input" name="optradio">non porteurse</label>\n' +
                    '                </div>\n' +
                    '            </div>\n' +
                    '            <hr class="mx-4">';
            }
            htmlform=htmlform+' </form>\n' +
                '\n' +
                '\n' +
                '\n' +
                '        <div class="d-flex flex-row justify-content-center card-body justify-content-around">\n' +
                '\n' +
                '            <a href="#" onclick="" class="btn btn-danger btn-icon-split">\n' +
                '                <span class="icon text-white-50">\n' +
                '                        <i class="fas fa-arrow-circle-left"></i>\n' +
                '                </span>\n' +
                '                <span class="text">precedent</span>\n' +
                '            </a>\n' +
                '            <a href="#" onclick="submitform()" class="btn btn-primary btn-icon-split">\n' +
                '                <span class="icon text-white-50">\n' +
                '                    <i class="fas fa-chevron-circle-right"></i>\n' +
                '                </span>\n' +
                '                <span class="text">suivant</span>\n' +
                '            </a>\n' +
                '\n' +
                '        </div>\n' +
                '\n' +
                '    </div>\n' +
                '\n';
            formsub.innerHTML=htmlform;
            next("fld2", "fld3");
        }
    }
}



