
function initORC(){
    
    
    // Simulate orc by delay
	/*
    setTimeout(function(){  
        
        window.location = "result";        
    }, 2000);
    */
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
					console.log("Ready to submit");
					document.getElementById('ocr_result').value = ocr_result;
					document.getElementById('ocrForm').submit();
				}
		})
	}
}