const generateButton = document.getElementById('generate_button');
generateButton.onclick = function() {
	var source = new EventSource("/progress");
	source.onmessage = function(event) {
		$('.progress-bar').css('width', event.data+'%').attr('aria-valuenow', event.data);
		$('.progress-bar-label').text(event.data+'%');

		if (event.data == 100) {
			source.close();
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