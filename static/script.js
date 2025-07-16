const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const result = document.getElementById('result');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => video.srcObject = stream)
    .catch(err => console.error('Gagal mengakses kamera:', err));

function capture() {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg');

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            result.textContent = "Gagal memproses gambar: " + data.error;
        } else {
            result.textContent = `Keturunan: ${data.label} (Confidence: ${(data.confidence * 100).toFixed(2)}%)`;
        }
    })
    .catch(error => {
        result.textContent = "Error: " + error;
    });
}
