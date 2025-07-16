from flask import Flask, render_template, request, jsonify
import numpy as np, cv2, base64
from keras.models import load_model

app = Flask(__name__)
model = load_model('model/nationality_model.h5')
classes = ['Asia', 'Afrika', 'Eropa', 'Amerika', 'Timur Tengah']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        img_data = data['image'].split(',')[1]
        img_bytes = base64.b64decode(img_data)
        img_np = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Gagal membaca gambar'}), 400

        img = cv2.resize(img, (224, 224))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)

        pred = model.predict(img)[0]
        label = classes[np.argmax(pred)]
        confidence = float(np.max(pred))

        return jsonify({'label': label, 'confidence': confidence})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
