
var currentView = "dashboard";
function changeView(newView){
    $("#" + currentView).addClass('hidden');
    $("#" + newView).removeClass('hidden');
    currentView = newView;
}

function doOcr(id){
    changeView("ocr");
    var form_data = new FormData($('#'+id)[0]);
    
    switch($('#mode option:selected').text()){
        case "Local":
            localOcr(form_data);
            break;
        case "Remote":
            sendMultiFiles(form_data);
            break;
        case "Benchmark":
            console.error("not implemented");
            break;
        default:
            console.error("not implemented")
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
                            $('#result_text').html(ocr_result);
                            console.log("Ok");
                            changeView("result")
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
            $('#result_text').html(results.text);
            console.log("Ok", results);
            changeView("result")
        },
        error: function(error) {
            console.log(error)
        }
    });
}