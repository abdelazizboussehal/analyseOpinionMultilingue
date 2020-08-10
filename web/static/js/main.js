
function getjson(subdomaine){

	// 1. Create a new XMLHttpRequest object
let xhr = new XMLHttpRequest();
var url="http://127.0.0.1:5000/"+subdomaine;
// 2. Configure it: GET-request for the URL /article/.../load
xhr.open('GET', url);

// 3. Send the request over the network
xhr.send();

// 4. This will be called after the response is received
xhr.onload = function() {
  if (xhr.status != 200) { // analyze HTTP status of the response
    alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
  } else { // show the result
	var jsons=JSON.parse(xhr.responseText);
    alert(jsons.username); // response is the server
  }
};

}

function includeHTML(id,URL) {
	var elmnt, file, xhttp;
	/* Loop through a collection of all HTML elements: */
	  elmnt = document.getElementById(id);
	  /*search for elements with a certain atrribute:*/
	  file = URL;
	  if (file) {
		/* Make an HTTP request using the attribute value as the file name: */
		xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
		  if (this.readyState == 4) {
			if (this.status == 200) {
				alert("Page not found.22");
				elmnt.innerHTML = this.responseText;}
			if (this.status == 404) {alert("Page not found.");}

		  }
		}
		xhttp.open("GET", file, true);
		xhttp.send();
		/* Exit the function: */
		return;
	  }

  }

  function addhtml(){
	  includeHTML("next",'/templates/aziz.html');
  }