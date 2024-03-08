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
	$("#generate_button").prop("disabled", true);
	$("#generate_button").text('Generating...');
	var source = new EventSource("/update_progress/" + task_id);
	source.onmessage = function(event) {
		$('.progress-bar').css('width', event.data+'%').attr('aria-valuenow', event.data);
		$('.progress-bar-label').text(event.data+'%');

		if (event.data == 100) {
			source.close();
			var result_url = "/get_result/" + task_id;
			downloadFile(result_url, 'name.zip');
			$("#generate_button").prop("disabled", false);
			$("#generate_button").text('Generate!');
			//$('.progress-bar').css('width', '0%').attr('aria-valuenow', '0');
			//$('.progress-bar-label').text('0%');
		}
	}
};
