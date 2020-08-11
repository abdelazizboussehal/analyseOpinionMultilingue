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
    var text1=id.innerText;
    var text2=id.parentNode.childNodes[1].innerText
    var res = str.replace(text2, text1);
    textarea.value=res;
    id.parentNode.hidden=true;  

}



