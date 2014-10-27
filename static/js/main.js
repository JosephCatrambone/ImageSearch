var httpRequest;

function getElement(id){ return document.getElementById(id); }

function makeRequest(url, postMethod, toSend, onSuccess, onError) {
	if (window.XMLHttpRequest) {
		httpRequest = new XMLHttpRequest();
	} else if (window.ActiveXObject) {
		try {
			httpRequest = new ActiveXObject("Msxml2.XMLHTTP");
		}
		catch (e) {
			try {
				httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
			}
			catch (e) {}
		}
	}

	if (!httpRequest) {
		alert('Unable to instance httpRequest object.');
		return false;
	}

	httpRequest.onreadystatechange = function() {
		if (httpRequest.readyState === 4) {
			if (httpRequest.status === 200) {
				if(onSuccess) { onSuccess(httpRequest.responseText) };
			} else {
				if(onError) { onError() };
			}
		}
	};
	httpRequest.open(postMethod, url);
	if(toSend != null) {
		httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		httpRequest.send("json=" + encodeURIComponent(JSON.stringify(toSend)));
	} else {
		httpRequest.send();
	}
	return true;
}

function submitImage() {
	if(this.files && this.files[0]) {
		var fileReader = new FileReader();
		fileReader.onload = function(e) {
			var fileData = e.target.result;
			makeRequest(
				"/submit_image",
				"POST",
				{"image_data":window.btoa(fileData), "algorithm":algorithm},
				function(data) {},
				function(data) {}
			);
		};
		//fileReader.readAsDataURL(this.files[0]);
		fileReader.readAsBinaryString(this.files[0]);
	}
}

function getImage(responseText) {
	var json = JSON.parse(responseText);
	var imageData = json['image_data'];
	getElement("picture").src = "data:image/png;base64," + imageData;
}

$(document).ready(function() {
	//getElement("pictureInput").addEventListener("change", submitImage, false);
	$("#pictureInput").on()
	$("#submitButton").on('click', submitImage);
	//makeRequest('get_image', 'GET', null, getImage);
});
