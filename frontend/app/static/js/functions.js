
function initORC(){
    
    
    // Simulate orc by delay
	/*
    setTimeout(function(){  
        
        window.location = "result";        
    }, 2000);
    */
	var ocr_result;
	Tesseract.recognize(cam_pic)
		.then(function(result){
			console.log(result);
			ocr_result = result['text'];
			document.getElementById('ocr_result').value = ocr_result;
			document.getElementById('ocrForm').submit();
	})
}