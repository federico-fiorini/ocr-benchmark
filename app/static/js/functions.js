
var currentView = "dashboard";
function changeView(newView){
	if(newView == "dashboard") {
		show_history();
	}
	if(newView == "camera"){
		$(".cam_pic_class").click();
	}
	
    $("#" + currentView).addClass('hidden');
    $("#" + newView).removeClass('hidden');
    currentView = newView;
}


var benchmark = false;
var benchmarkTimes = {};
var benchmarkT0;
function benchmarkStart(){
    benchmark = true; 
    benchmarkT0 = performance.now();
}
function benchmarkStop(name){ 
    var t1 = performance.now();
    if(!benchmarkTimes[name]) benchmarkTimes[name] = [];
    benchmarkTimes[name].push(t1 - benchmarkT0);  
    console.log(benchmarkTimes[name]);
    benchmark = false; 
}


var form_data;
function doOcr(id){
    form_data = new FormData($('#'+id)[0]);
    if(form_data.getAll("files").length == 0)
        return;
    else    
        changeView("ocr");    
    
    mode = $('#mode option:selected').text();
    switch(mode){
        case "Local":
            localOcr(form_data);
            break;
        case "Remote":
            sendMultiFiles(form_data);
            break;
        case "Benchmark":
            benchmarkTimes = {};
            // start with local
            benchmarkStart();
            localOcr(form_data);
            break;
        default:
            console.error("not implemented");
    }
}



function showText(text){
    $('#result_text').html(text);
    changeView("result");    
}

function localDone(text){
    console.log("Local Done");

    if(benchmark){
        benchmarkStop("local");
        // continue with remote
        benchmarkStart();
        sendMultiFiles(form_data);        
    } else {
        showText(text);
    }
}

function remoteDone(text, remoteTimes){  
    remoteTimes = remoteTimes || [NaN];
    console.log("Remote Done");
    if(benchmark){
        benchmarkStop("remote");
         
        bytesTransferred = analyze_form_files();
        showBenchmark(benchmarkTimes.local, remoteTimes, bytesTransferred);
    } else {
        showText(text);
    }
}

 
function analyze_form_files(){
  var bytesTransferred = [];
  var files = form_data.getAll("files");
  for(var i = 0; i < files.length; i++){ 
    console.log(files[i]);
    bytesTransferred.push(files[i].size);
  }
  console.log(bytesTransferred);
  return bytesTransferred;
}


function showText(text){
    $('#result_text').html(text);
    changeView("result");    
}


function round(a){
  return Math.round(a * 100) / 100;
}

function getStatistics(values){
  var min = Math.min.apply(null, values);
  var min_i= values.indexOf(min);
  var max = Math.max.apply(null, values);
  var max_i= values.indexOf(max);
  var sum = values.reduce(function(a, b) { return a + b; }, 0);
  var avg = sum / values.length;
  var sqDiffs = values.map(function(value){return (value - avg) * (value - avg);});
  var sqSum = sqDiffs.reduce(function(a, b) { return a + b; }, 0);
  var sDev = Math.sqrt(sqSum / values.length);
  return[round(min) +" ("+min_i+")", round(max) +" ("+max_i+")", round(avg) +" ("+round(sDev)+")"];
  
}


function showBenchmark(localTimes, remoteTimes, bytesTransferred){  
  
  var result = [
    ["", ["min (index)","max (index)","average (deviation)"]],
    ["Local times (ms) " , getStatistics(localTimes)],
    ["Remote times (ms) " , getStatistics(remoteTimes)],
    ["Remote bytes" , getStatistics(bytesTransferred)],
  ]; 
  
    var d = document;

    var fragment = d.createDocumentFragment();

    var tr = d.createElement("tr");
    var td = d.createElement("td");
    td.innerHTML = "--- ";
    tr.appendChild(td);
    fragment.appendChild(tr);
    
    var tr = d.createElement("tr");
    var td = d.createElement("td");
    td.innerHTML = "Result for " + localTimes.length + " file(s)";
    tr.appendChild(td);
    fragment.appendChild(tr);
    
    for (i = 0; i < result.length; i++) {
        var tr = d.createElement("tr");

        var td = d.createElement("td");
        td.style.width = '30%';
        td.innerHTML = result[i][0];
        tr.appendChild(td);
        for (j = 0; j < result[i][1].length; j++) {    
            var td = d.createElement("td");
        td.style.width = '20%';
            td.innerHTML = result[i][1][j];
            tr.appendChild(td);
        }

        //does not trigger reflow
        fragment.appendChild(tr);
    }

    var table = d.createElement("table");
    table.appendChild(fragment);
    $('#benchmark_result').append(table);
    
    changeView("benchmark");
}



var img = new Image();   
var cam_pic = [];
var count = 0;
var ocr_result = ""; 
function localOcr(form_data, nextPicture) {
    nextPicture = nextPicture || false;

    if (!nextPicture) {
        count = 0;
        ocr_result = ""; 
        cam_pic = form_data.getAll("files");
    }

    console.log("Processing file ", cam_pic[count]);
    var c = document.createElement("canvas");
	c.setAttribute("id", "my-image");
	var reader  = new FileReader();
	reader.readAsDataURL(cam_pic[count]);
	reader.onload = function () {
		img.src = reader.result;
		Caman(c, img.src, function () {
			this.sharpen(100);
			this.contrast(50);
			this.gamma(4);
			this.greyscale();
			this.render(function() {
				img.src = c.toDataURL("image/png", 1);
				Tesseract.recognize(img.src)
					.then(function(result){
							count++;
							console.log(result);
							ocr_result += result['text'];
							if(count == (cam_pic.length)) {
							    //console.log("Ready to submit");
							    //document.getElementById('ocr_result').value = ocr_result;
							    //document.getElementById('ocrForm').submit();
							    localDone(ocr_result);
							    return;
							} 
							if (benchmark){
							    benchmarkStop("local"); 
							    benchmarkStart();
							}
							localOcr(form_data, true);
					})
			})
		})
	 };
}

var ajaxURL;
function sendMultiFiles(form_data) { 
 
    console.log("Sending files", form_data.getAll("files"));
    $.ajax({
        type: "POST",
        url: ajaxURL,
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        async: true,
        success: function(results) {
            remoteDone(results.text, results.times)
        },
        error: function(error) {
            console.log(error);
            remoteDone("# Failed: " + error.statusText + " #"); 
        }
    });
}

function saveResult() {
    var blob = new Blob([$('#result_text').html()], {type: "text/plain;charset=utf-8"});
    saveAs(blob, "result.txt");
}
