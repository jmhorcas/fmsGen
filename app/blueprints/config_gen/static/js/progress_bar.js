// const generateButton = document.getElementById('generate_button');
// generateButton.onclick = function() {
// 	var source = new EventSource("/get_result");
// 	source.onmessage = function(event) {
// 		$('.progress-bar').css('width', event.data+'%').attr('aria-valuenow', event.data);
// 		$('.progress-bar-label').text(event.data+'%');

// 		if (event.data == 100) {
// 			source.close();
// 		}
// 	}
// };

function downloadFile(url, fileName) {
	fetch(url, { method: "get", mode: "no-cors", referrerPolicy: "no-referrer" })
	  .then((res) => res.blob())
	  .then((res) => {
		const aElement = document.createElement("a");
		aElement.setAttribute("download", fileName);
		const href = URL.createObjectURL(res);
		aElement.href = href;
		aElement.setAttribute("target", "_blank");
		aElement.click();
		URL.revokeObjectURL(href);
	  });
  }

function update_progress_bar(task_id) {
	console.log("update progress bar: " + task_id);
	var source = new EventSource("/update_progress/" + task_id);
	source.onmessage = function(event) {
		$('.progress-bar').css('width', event.data+'%').attr('aria-valuenow', event.data);
		$('.progress-bar-label').text(event.data+'%');

		if (event.data == 100) {
			source.close();
			var result_url = "/get_result/" + task_id
			downloadFile(result_url, 'name.zip');
			// fetch(result_url).then(function(resp) {
			// 	return resp.blob();
			// }).then(function(blob) {
			// 	download(blob);
			// });
		}
	}
};


// var source = new EventSource("/get_result");
// 	source.onmessage = function(event) {
// 		$('.progress-bar').css('width', event.data+'%').attr('aria-valuenow', event.data);
// 		$('.progress-bar-label').text(event.data+'%');

// 		if (event.data == 100) {
// 			source.close();
// 		}
// 	}

// var eventSource = new EventSource("/progress");
// eventSource.addEventListener = ('progress_bar', function(event) {
// 	$('.progress-bar').css('width', event.data+'%').attr('aria-valuenow', event.data);
// 	$('.progress-bar-label').text(event.data+'%');

// 	if (event.data == 100) {
// 		eventSource.close();
// 	}
// });

// var source = new EventSource("{{ url_for('config_gen.get_result') }}");
// source.addEventListener('greeting', function(event) {
// 	var data = JSON.parse(event.data);
// 	alert("The server says " + data.message);
// }, false);
// source.addEventListener('error', function(event) {
// 	alert("Failed to connect to event stream. Is Redis running?");
// }, false);