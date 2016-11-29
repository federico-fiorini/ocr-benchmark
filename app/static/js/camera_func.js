$( document ).ready(function() {
    var takePicture = document.querySelector("#cam_pic"),
        showPicture = document.querySelector("#preview-pic");
    if (takePicture && showPicture) {
        // Set events
        takePicture.onchange = function (event) {
            console.log("taking picture");
            // Get a reference to the taken picture or chosen file
            var files = event.target.files,
                file;
            if (files && files.length > 0) {
                file = files[0];
				console.log(file);
                try {
                    // Create ObjectURL
                    var imgURL = window.URL.createObjectURL(file);
					showPicture.style.visibility = "visible";
                    // Set img src to ObjectURL
                    showPicture.src = imgURL;
		
                    console.log(imgURL);

                    // Revoke ObjectURL
                    //URL.revokeObjectURL(imgURL);
                }
                catch (e) {
                    try {
                        // Fallback if createObjectURL is not supported
                        var fileReader = new FileReader();
                        fileReader.onload = function (event) {
                            showPicture.src = event.target.result;
                        };
                        fileReader.readAsDataURL(file);
                    }
                    catch (e) {
                        //
                        var error = document.querySelector("#error");
                        if (error) {
                            error.innerHTML = "Neither createObjectURL or FileReader are supported";
                        }
                    }
                }
            }
        };
    }
});