document.getElementById('captureEmotionButton').addEventListener('click', function() {
    fetch('/detect_emotion', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'Emotion captured') {
                window.location.href = '/recommend';
            }
        });
});
