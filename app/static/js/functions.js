
var currentView = "dashboard";
function changeView(newView){
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

function remoteDone(text){  
    console.log("Remote Done");
    if(benchmark){
        benchmarkStop("remote");
        var result = "Times:\n local " + benchmarkTimes.local + "ms\n  remote " + benchmarkTimes.remote+ "ms"; 
        $('#benchmark_result_text').html(result);
        changeView("benchmark");
    } else {
        showText(text);
    }
}

    
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
    Tesseract.recognize(cam_pic[count])
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
        async: false,
        success: function(results) {
            remoteDone(results.text)
        },
        error: function(error) {
            console.log(error)
        }
    });
}

function saveResult() {
    var blob = new Blob([$('#result_text').html()], {type: "text/plain;charset=utf-8"});
    saveAs(blob, "result.txt");
}
