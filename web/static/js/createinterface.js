function addpopretext() {
    var element = document.getElementById("cadretexte");
    element.hidden = false;
    var element1 = document.getElementById("cadretwitter");
    element1.hidden = true;
    var element2 = document.getElementById("cadretfile");
    element2.hidden = true;

}

function addtweetr() {
    var element = document.getElementById("cadretexte");
    element.hidden = true;
    var element1 = document.getElementById("cadretwitter");
    element1.hidden = false;
    var element2 = document.getElementById("cadretfile");
    element2.hidden = true;
}

function addfichiertext() {
    var element = document.getElementById("cadretexte");
    element.hidden = true;
    var element1 = document.getElementById("cadretwitter");
    element1.hidden = true;
    var element1 = document.getElementById("cadretfile");
    element1.hidden = false;

}


