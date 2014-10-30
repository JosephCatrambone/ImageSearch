var httpRequest;

function submitImage(algorithm, imageFile) {
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
					displayResults(data['results']);
				}
			}
		});
	};
	fileReader.readAsBinaryString(imageFile);
}

//
// Dom interface methods
//
function clickHandler(algorithm) {
	if(!algorithm) { algorithm = ""; }
	var imageInput = $("#pictureInput");
	if(imageInput && imageInput[0] && imageInput[0].files[0]) {
		submitImage(algorithm, imageInput[0].files[0]);
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
		var temp = template.clone();
		temp.find("[name='image']").attr('src', imagePrefix + data[index][2])
		temp.find("[name='url']").attr('href', data[index][1]);
		temp.find("[name='created']").html("First seen: " + data[index][3]);
		temp.find("[name='info']").attr('src', "");
		$("#results").append(temp);
	}
}

$(document).ready(function() {
	//getElement("pictureInput").addEventListener("change", submitImage, false);
	$("#searchButton").on('click', function(e){clickHandler("default");});
	$("#defaultSearchButton").on('click', function(e){clickHandler("default");});
	$("#exactSearchButton").on('click', function(){clickHandler("exact");});
	//makeRequest('get_image', 'GET', null, getImage);
});
