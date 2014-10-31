var MAX_DISTANCE = 200;

function submitImage(algorithm, imageFile, onSuccess, onFailure) {
	var fileReader = new FileReader();
	fileReader.onload = function(e) {
		var fileData = e.target.result;
		$.ajax({
			url: "/search",
			type: "POST",
			dataType: "json",
			data: {
				imageData: window.btoa(fileData),
				algorithm: algorithm
			},
			success: function(data) {
				if(data['success']) {
					onSuccess(data['results']);
				} else {
					onFailure(data);
				}
			},
			failure: onFailure
		});
	};
	fileReader.readAsBinaryString(imageFile);
}

//
// Dom interface methods
//
function clickHandler(algorithm) {
	clearResults();
	if(!algorithm) { algorithm = ""; }
	var imageInput = $("#pictureInput");
	if(imageInput && imageInput[0] && imageInput[0].files[0]) {
		submitImage(
			algorithm, 
			imageInput[0].files[0],
			function(results) { displayResults(results); },
			function(err) { /* Show some error. */ }
		);
	}
}

function getImage(responseText) {
	var json = JSON.parse(responseText);
	var imageData = json['image_data'];
	getElement("picture").src = "data:image/png;base64," + imageData;
}

function clearResults() {
	$("#results").empty();
}

function displayResults(data) {
	var imagePrefix = "/images/"; // Make sure this matches with settings.MEDIA_ROOT
	var template = $("#resultTemplate").contents();
	for(var index=0; index < data.length; index++) {
		// From database.py schema:
		// images.id, images.url, images.filename, images.created, distance 
		var id = data[index][0];
		var url = data[index][1];
		var filename = data[index][2];
		var created = data[index][3];
		var distance = data[index][4];
		if(distance < MAX_DISTANCE) {
			var temp = template.clone();
			temp.find("[name='image']").attr('src', imagePrefix + filename)
			temp.find("[name='url']").attr('href', url);
			temp.find("[name='url']").text(url);
			temp.find("[name='created']").html(created);
			//temp.find("[name='info']").attr('src', "");
			$("#results").append(temp);
		}
	}
}

$(document).ready(function() {
	//getElement("pictureInput").addEventListener("change", submitImage, false);
	$("#searchButton").on('click', function(e){clickHandler("default");});
	$("#defaultSearchButton").on('click', function(e){clickHandler("default");});
	$("#exactSearchButton").on('click', function(){clickHandler("exact");});
	//makeRequest('get_image', 'GET', null, getImage);
});
