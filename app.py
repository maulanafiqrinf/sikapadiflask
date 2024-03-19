import os
import io
import logging
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from PIL import Image

app = Flask(__name__)
app.secret_key = "secret!@8102"

MODEL_ARCHITECTURE = 'model/clean721.json'
MODEL_WEIGHTS = 'model/clean721.h5'

# PREDICTION_CLASSES = {
#     0: ('Tanaman Padimu Terkena', 'klasifikasi-brown.html'),
#     1: ('Tanaman Padimu Terkena', 'klasifikasi-blast.html'),
#     2: ('Tanaman Padimu Terkena', 'klasifikasi-blight.html'),
#     3: ('Tanaman', 'klasifikasi-sehat.html'),
#     4: ('Gambar Tidak Cocok', 'no-klasifikasi.html'),
# }
PREDICTION_CLASSES = {
    0: ('Gambar Tidak Cocok', 'no-klasifikasi.html'),
    1: ('Tanaman Padimu Terkena', 'klasifikasi-blast.html'),
    2: ('Tanaman Padimu Terkena', 'klasifikasi-blight.html'),
    3: ('Tanaman Padimu Terkena', 'klasifikasi-brown.html'),
    4: ('Tanaman', 'klasifikasi-sehat.html'),
}

def load_model_from_file():
    try:
        with open(MODEL_ARCHITECTURE, 'r') as json_file:
            loaded_model_json = json_file.read()
        model = model_from_json(loaded_model_json)
        model.load_weights(MODEL_WEIGHTS)
        return model
    except Exception as e:
        logging.error(f"Error loading model: {str(e)}")
        return None

model = load_model_from_file()

def model_predict(img_path, model):
    try:
        TARGET_IMAGE_SIZE = (224, 224)
        test_image = load_img(img_path, target_size=TARGET_IMAGE_SIZE)
        logging.info("@@ Got Image for prediction")

        test_image = img_to_array(test_image) / 255
        test_image = np.expand_dims(test_image, axis=0)

        result = model.predict(test_image)
        pred_class = np.argmax(result, axis=1)[0]
        pred_prob = result[0][pred_class] * 100

        return PREDICTION_CLASSES[pred_class][0], PREDICTION_CLASSES[pred_class][1], pred_prob
    except Exception as e:
        logging.error(f"Error predicting: {str(e)}")
        return 'Error', 'error.html', 0

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/blog", methods=['GET'])
def blog():
    return render_template('blog.html')

@app.route("/contact", methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route("/klasifikasirgb", methods=['GET', 'POST'])
def klasifikasirgb():
    return render_template('klasifikasirgb.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    file = request.files['image']

    original_image = Image.open(io.BytesIO(file.read()))
    resized_image = original_image.resize((4, 4))

    pixel_values = np.array(resized_image)

    blue_values = pixel_values[:, :, 2]
    green_values = pixel_values[:, :, 1]
    red_values = pixel_values[:, :, 0]

    return render_template('result.html', blue_values=blue_values, green_values=green_values, red_values=red_values)

@app.route("/klasifikasi", methods=['GET', 'POST'])
def klasifikasi():
    return render_template('klasifikasi.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image']
        filename = secure_filename(file.filename)
        logging.info("@@ Input posted =", filename)

        file_path = os.path.join('static', 'user_uploaded', filename)
        file.save(file_path)

        logging.info("@@ Predicting class...")
        pred_class, output_page, pred_prob = model_predict(file_path, model)

        return render_template(output_page, pred_output=pred_class, pred_prob=pred_prob, user_image=file_path)

if __name__ == "__main__":
    app.run(debug=True)