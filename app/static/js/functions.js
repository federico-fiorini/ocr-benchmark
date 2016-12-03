
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
    benchmarkTimes[name] = (t1 - benchmarkT0);  
    benchmark = false; 
}


var form_data;
function doOcr(id){
    changeView("ocr");
    form_data = new FormData($('#'+id)[0]);
    
    mode = $('#mode option:selected').text();
    switch(mode){
        case "Local":
            localOcr(form_data);
            break;
        case "Remote":
            sendMultiFiles(form_data);
            break;
        case "Benchmark":
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
        var result = "Times: local " + Math.round(benchmarkTimes.local) + "ms,  remote " + Math.round(benchmarkTimes.remote)+ "ms"; 
        $('#benchmark_result_text').html(result);
        changeView("benchmark");
    } else {
        showText(text);
    }
}

    
var cam_pic = [];
function localOcr(form_data) { 

    console.log("Processing files", form_data);
    
    cam_pic = [form_data.get("files")];

    var ocr_result = "";
    console.log(cam_pic);
    var count = 0;
    for(var i = 0; i < cam_pic.length; i++){
        Tesseract.recognize(cam_pic[i])
            .then(function(result){
                    count++;
                    console.log(result);
                    ocr_result += result['text'];
                    if(count == (cam_pic.length)) {
                            //console.log("Ready to submit");
                            //document.getElementById('ocr_result').value = ocr_result;
                            //document.getElementById('ocrForm').submit();
                            localDone(ocr_result);
                    }
        })
    }
}

var ajaxURL;
function sendMultiFiles(form_data) { 

    console.log("Sending files", form_data);
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