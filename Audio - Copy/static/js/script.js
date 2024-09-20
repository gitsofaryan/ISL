document.getElementById('charButton').onclick = function() {
    convertText('character');
};

document.getElementById('gestureButton').onclick = function() {
    convertText('gesture');
};

async function convertText(level) {
    const inputText = document.getElementById('inputText').value;

    if (!inputText.trim()) {
        alert("Please enter some text.");
        return;
    }

    const response = await fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: inputText, level: level })
    });

    const data = await response.json();

    if (response.ok) {
        const videoContainer = document.getElementById('videoContainer');
        videoContainer.innerHTML = '';  // Clear previous videos

        const videoElement = document.createElement('video');
        videoElement.src = data.video_path;
        videoElement.controls = true;
        videoElement.autoplay = true;
        videoContainer.appendChild(videoElement);
    } else {
        alert(data.error || 'Something went wrong');
    }
}
