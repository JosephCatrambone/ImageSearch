var httpRequest;

function submitImage(algorithm, imageFile) {
	var fileReader = new FileReader();
	fileReader.onload = function(e) {
		var fileData = e.target.result;
		$.ajax({
			url: "/search/" + algorithm,
			type: "POST",
			dataType: "json",
			data: window.btoa(fileData),
			success: function(data) {
				alert("HURR!");
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

$(document).ready(function() {
	//getElement("pictureInput").addEventListener("change", submitImage, false);
	$("#searchButton").on('click', submitImage);
	$("#defaultSearchButton")
	$("#exactSearchButton")
	//makeRequest('get_image', 'GET', null, getImage);
});
