//On load
var xhr = new XMLHttpRequest();
var allItems = this.getAllItems();
var itemEditButtons = [];
var itemDeleteButtons = [];
var allMeals = this.getAllMeals();
var mealEditButtons = [];
var mealDeleteButtons = [];
var allListItems = this.getAllListItems();

// Load page
this.tableLoader(allItems, "mainItemTable");

this.tableLoader(allMeals, "mainMealTable");

this.listLoader();

document.getElementById('addNewItemButton').addEventListener("click", () =>{
	modalHandler("addItemModal");
})

document.getElementById('addNewMealButton').addEventListener("click", () =>{
	addMealModal();
})

document.getElementById('resetList').addEventListener("click", () =>{
	this.xhr.open("DELETE", 'http://localhost:8000/list',false);
	this.xhr.send(null);
	location.reload();
})

//Functions
function getAllItems(){
	this.xhr.open("GET", 'http://localhost:8000/items',false);
	this.xhr.send(null);
	var items = JSON.parse(this.xhr.responseText);
	
	return items;
}

function getAllMeals(){
	this.xhr.open("GET", 'http://localhost:8000/meals',false);
	this.xhr.send(null);
	var meals = JSON.parse(this.xhr.responseText);
	
	return meals;
}

function getAllListItems(){
	this.xhr.open("GET", 'http://localhost:8000/list',false);
	this.xhr.send(null);
	var list = JSON.parse(this.xhr.responseText);
	
	return list;
}

function tableLoader(data,tableId){
	var table = document.getElementById(tableId);
	for(var i = 0; i < data.length; i++){
		var newRow = table.insertRow(i+1)
		var name = newRow.insertCell(0);
		var description = newRow.insertCell(1);
		var addToList = newRow.insertCell(2);
		var action = newRow.insertCell(3);
		name.innerHTML = data[i].name;
		description.innerHTML = data[i].description;
		if(tableId == "mainItemTable"){
			addToList.innerHTML = '<button type="button" onclick="addItemToList(this.id.substr(19))" class="addItemToListButton" id="itemAddToListButton'+data[i].id+'">Add To List</button>';
			action.innerHTML = '<button type="button" onclick="editItemModal(this.id.substr(14))" class="itemEditButton" id="itemEditButton'+data[i].id+
			'">Edit</button>  <button type="button" onclick="deleteItem(this.id.substr(16))" class="itemDeleteButton" id="itemDeleteButton'+data[i].id+
			'">Delete</button>';
		}
		else if(tableId == "mainMealTable"){
			addToList.innerHTML = '<button type="button" onclick="addMealItemsToList(this.id.substr(23))" class="addMealItemToListButton" id="mealItemAddToListButton'+data[i].id+'">Add To List</button>';
			action.innerHTML = '<button type="button" class="mealEditButton" id="mealEditButton'+data[i].id+
			'">Edit</button> <button type="button" onclick="deleteMeal(this.id.substr(16))" class="mealDeleteButton" id="mealDeleteButton'+data[i].id+'">Delete</button>';
		}
	}
}

function listLoader(){
	var list = document.getElementById("currentItemsList");
	for(var i = 0; i < allListItems.length; i++){
		var newElement = new Option(allListItems[i].name);
		list.add(newElement);
	}
}

function showId(elementId){
	alert(elementId.substr(16));
}

function addItemToList(itemId){
	xhr.open("POST", 'http://localhost:8000/list/items?item_id='+itemId, false);
	xhr.send(null);
	location.reload();
}

function addMealItemsToList(mealId){
	xhr.open("POST", 'http://localhost:8000/list/?meal_id='+mealId, false);
	xhr.send(null);
	location.reload();
}

function editItemModal(itemId){
	xhr.open("GET", 'http://localhost:8000/items/'+itemId, false);
	xhr.send(null);
	var item = JSON.parse(xhr.responseText);
	var itemName = document.getElementById("editItemName");
	itemName.value = item.name;
	var itemDesc = document.getElementById("editItemDescription");
	itemDesc.value = item.description;
	var submit = document.getElementById("editItemSubmit");
	modalHandler("editItemModal");

	
	submit.addEventListener("click", () =>{
		xhr.open("POST", 'http://localhost:8000/items/'+itemId+'?name='+itemName.value+'&description='+itemDesc.value, false);
		xhr.send(null);
		location.reload();
	})
	
}

function addMealModal(){
	xhr.open("GET", 'http://localhost:8000/items', false);
	xhr.send(null);
	var availItems = JSON.parse(xhr.responseText);
	var availItemsList = document.getElementById("addMealAvailItems");
	var selectItems = [];
	var selectItemsList = document.getElementById("addMealSelectItems");
	
	for(var i = 0; i < availItems.length; i++){
		var newElement = new Option(availItems[i].name);
		availItemsList.add(newElement);
	}
	
	modalHandler("addMealModal");
	
	//On load: show all available items on the left. Create two temporary arrays: available items and added items
	//If the user adds an item to the meal, remove from the available items and move to the added items
	//Once the user submits the meal, save the added items in the meal_item table
}

function deleteItem(itemId){
	xhr.open("DELETE", 'http://localhost:8000/items/'+itemId, false);
	xhr.send(null);
	location.reload();
}

function deleteMeal(mealId){
	xhr.open("DELETE", 'http://localhost:8000/meals/'+mealId+'/items', false);
	xhr.open("DELETE", 'http://localhost:8000/meals/'+mealId, false);
	xhr.send(null);
	location.reload();
}

function modalHandler(modalId){
	var modal = document.getElementById(modalId);
	
	// Get the <span> element that closes the modal
	var span = document.getElementsByClassName("close")[0];
	
	// When the user clicks the button, open the modal 
	modal.style.display = "block";
	
	// When the user clicks on <span> (x), close the modal
	span.onclick = function() {
	  modal.style.display = "none";
	}
	
	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	  if (event.target == modal) {
	    modal.style.display = "none";
	  }
	}
}
