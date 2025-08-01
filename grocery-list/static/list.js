//On load
var xhr = new XMLHttpRequest();

document.getElementById('resetButton').addEventListener("click", reset);

//Functions
function getAllItems(){
	this.xhr.open("GET", 'http://localhost:8000/items',false);
	this.xhr.send(null);
	var items = JSON.parse(this.xhr.responseText);
	
	return items;
}

function reset(){
	var url = 'http://localhost:8000/list'
	xhr.open("DELETE", url, false);
	xhr.send(null);
}