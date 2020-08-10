// include html
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


function addpopretext() {
    var element = document.getElementById("cadretexte");
    element.hidden=false;
    var element1 = document.getElementById("cadretwitter");
    element1.hidden=true;

}

function addtweetr() {
    var element = document.getElementById("cadretexte");
    element.hidden=true;
    var element1 = document.getElementById("cadretwitter");
    element1.hidden=false;
}

function addfichiertext() {
    var element = document.getElementById("maincontainer");
    element.innerHTML = "<p class=\"card-text\">cette option nous permettre de choisir un fichier depuis desktop</p>\n" +
        "                    <div class=\"custom-file\">\n" +
        "                        <div class=\"row \">\n" +
        "                            <input id='\"file\"' type=\"file\" class=\"custom-file-input\" id=\"customFile\">\n" +
        "                            <label class=\"custom-file-label \" for=\"customFile\">choisir fichier</label>\n" +
        "                        </div>\n" +
        "                    </div>";

}


