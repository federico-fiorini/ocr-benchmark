var hist_data;

function show_history() {
	$.getJSON("history", function(data, status){
		data = JSON.stringify(data);
        //console.log("Data: " + data + "\nStatus: " + status);
		data = JSON.parse(data);
		//console.log(data);
		/*
		<a href="#" class="list-group-item active">
				  <h4 class="list-group-item-heading">First List Group Item Heading</h4>
				  <p class="list-group-item-text">List Group Item Text</p>
				</a>
		*/
		data = data['history'];
		hist_data = data;
		var hst_list_str = "";
		$(".history").empty();
		$.each(data, function(key, value) {
			hst_list_str += "<span onclick='show_history_item(" + key + ")' class='list-group-item'>" +
								"<div class='row'>" +
									"<div class='col-xs-4'><img style='display:block; margin: auto;' width='100' height='120' src='data:image/jpg;base64,"+ value['thumbnail'] +"' /></div>" +
									"<div class='col-xs-8'>"+ "<div class='hist_text'>" + value['text'] + "</div>" +"</div>" +				
								"</div>" +
							"</span>";
		});
		$(".history").append(hst_list_str);
	  
    });
}

function show_history_item(idx) {
	changeView('history_element');
	$("#history_element").find(".well").empty();
	$("#history_element").find(".well").append(hist_data[idx]['text']);
	$("#history_element").find(".label").empty();
	timestamp = hist_data[idx]['timestamp'].replace("T", " ");
	$("#history_element").find(".label").append(timestamp);
	var src_files_str = "";
	$.each(hist_data[idx]['source-files'], function(index, value) {
		src_files_str += "<div class='col-xs-3'><button class='btn btn-primary btn-block' onclick=show_history_img(" + idx + "," + index + ") role='button'>Img " + (index+1).toString() + "</button></div>";
	});
	$("#history_element").find(".images").empty();
	$("#history_element").find(".images").append(src_files_str);
	
}

function show_history_img(idx, index) {
	url = hist_data[idx]['source-files'][index];
	console.log(url);
	$.get(url, function(data, status){
		img_src = "data:image/jpg;base64," + data; 
		$('#imagepreview').attr('src', img_src); // here asign the image to the modal when the user click the enlarge link
		$('#imagemodal').modal('show'); // imagemodal is the id attribute assigned to the bootstrap modal, then i use the show function
	});
}

function saveHistResult() {
    var blob = new Blob([$('#history_element').find(".well").html()], {type: "text/plain;charset=utf-8"});
    saveAs(blob, "result.txt");
}

$( document ).ready(show_history());