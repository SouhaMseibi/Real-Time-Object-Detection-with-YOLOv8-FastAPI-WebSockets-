function displayFileName() {
    let input = document.getElementById('file-upload');
    let fileName = document.getElementById('file-name');
    fileName.textContent = input.files[0].name;
}

document.getElementById("upload-form").onsubmit = async function(e) {
    e.preventDefault();
    let formData = new FormData();
    let fileInput = document.getElementById("file-upload");
    formData.append("file", fileInput.files[0]);

    let response = await fetch("/predict/", {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        let imageBlob = await response.blob();
        let imageUrl = URL.createObjectURL(imageBlob);
        document.getElementById("output-img").src = imageUrl;
        document.getElementById("output-img").style.display = "block";
    } else {
        alert("Error processing the image.");
    }
};

async function takeSnapshot() {
    let response = await fetch("/snapshot");
    if (response.ok) {
        let imageBlob = await response.blob();
        let imageUrl = URL.createObjectURL(imageBlob);
        document.getElementById("snapshot-img").src = imageUrl;
        document.getElementById("snapshot-img").style.display = "block";
    } else {
        alert("Error capturing snapshot.");
    }
}

let ws;  
function startStream() {
    let imgElement = document.getElementById("video-stream");
    imgElement.style.display = "block";

    if (ws) {
        ws.close();
    }

    ws = new WebSocket("ws://" + window.location.host + "/video");
    ws.binaryType = "blob";  

    ws.onmessage = function(event) {
        let imageBlob = event.data;
        let imageUrl = URL.createObjectURL(imageBlob);
        imgElement.src = imageUrl;
    };

    ws.onerror = function(error) {
        console.error("WebSocket error:", error);
    };

    ws.onclose = function() {
        console.log("WebSocket connection closed.");
    };
}

function stopStream() {
    if (ws) {
        ws.close();
        console.log("Stream stopped.");
    }
}
