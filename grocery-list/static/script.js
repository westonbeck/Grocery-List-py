//On load
var allItems = this.getAllItems();
var allMeals = this.getAllMeals();
this.tableLoader(allItems, "mainItemTable");

document.getElementById("countChecked").addEventListener("click", countChecked);

/*var itemTable = document.getElementById("mainItemTable");

itemTable.onclick = function test(event){
	alert(event.target.id);
}*/

//Functions
function getAllItems(){
	var xhr = new XMLHttpRequest();
	xhr.open("GET", 'http://localhost:8000/items',false);
	xhr.send(null);
	var items = JSON.parse(xhr.responseText);
	
	return items;
}

function getAllMeals(){
	var xhr = new XMLHttpRequest();
	xhr.open("GET", 'http://localhost:8000/meals',false);
	xhr.send(null);
	var meals = JSON.parse(xhr.responseText);
	
	return meals;
}

function tableLoader(data,selectId){
	var table = document.getElementById(selectId);
	for(var i = 0; i < data.length; i++){
		var newRow = table.insertRow(i+1)
		var itemName = newRow.insertCell(0);
		var itemDescription = newRow.insertCell(1);
		var addToList = newRow.insertCell(2);
		var action = newRow.insertCell(3);
		itemName.innerHTML = data[i].name;
		itemDescription.innerHTML = data[i].description;
		addToList.innerHTML = '<input type="checkbox" id="checkbox'+i+'">';
		action.innerHTML = '<button type="button" id="edit'+(i)+'">Edit</button> <button type="button" id="delete'+(i)+'">Delete</button>';
	}
}

function countChecked(){
	var table = document.getElementById("mainItemTable");
	var count = 0;
	var prefix = 'checkbox';
	for(var n = 1; n < table.rows.length; n++){
		var checkbox = document.getElementById(prefix+(n-1));
		console.log(checkbox.innerHTML);
		if(checkbox.checked == true){
			count++;
		}
	}
	alert(count);
}