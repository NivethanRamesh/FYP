from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2

app = Flask(__name__)

# Define image dimensions
img_width, img_height = 150, 150

# Load classification model
classification_model_path = 'car_parts_classification_model.h5'
classification_model = load_model(classification_model_path)

# Define function to predict damage condition
def predict_damage(image_path, component_name):
    try:
        if component_name == 'spark-plug':
            damage_model_path = 'PlugCheck.h5'
        elif component_name == 'BRAKE PAD':
            damage_model_path = 'BreakPadCheck.h5'
        elif component_name == 'windshield wiper':
            damage_model_path = 'WinderShieldWiperCheck.h5'
        else:
            return "Not applicable", "Not applicable"

        # Load damage check model
        damage_model = load_model(damage_model_path)

        # Load and preprocess the image
        img = image.load_img(image_path, target_size=(img_width, img_height))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize pixel values

        # Predict damage condition
        damage_prediction = damage_model.predict(img_array)
        condition = 'Damaged' if damage_prediction < 0.5 else 'Undamaged'

        return component_name, condition

    except Exception as e:
        print(f"Error predicting damage: {str(e)}")
        return "Error predicting damage", "Error predicting damage"

# Routes definitions :

@app.route('/')
def animation():
    return render_template('animation.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(os.getcwd(), filename)
            file.save(filepath)
            return redirect(url_for('loading', filepath=filepath))
    return redirect(url_for('index'))

@app.route('/loading')
def loading():
    filepath = request.args.get('filepath')
    if filepath is None:
        return render_template('result.html', result="Error: Filepath is None")
    return render_template('loading.html', filepath=filepath)

@app.route('/result')
def result():
    filepath = request.args.get('filepath')
    if filepath is None:
        return render_template('result.html', result="Error: Filepath is None")

    if not os.path.exists(filepath):
        return render_template('result.html', result="File does not exist")

    try:
        # Predict component type
        img = image.load_img(filepath, target_size=(img_width, img_height))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        class_predictions = classification_model.predict(img_array)
        class_idx = np.argmax(class_predictions[0])
        class_names = ['BRAKE PAD', 'spark-plug', 'windshield wiper']
        component_name = class_names[class_idx]

        # Predict damage condition
        damage_component, condition = predict_damage(filepath, component_name)

        return render_template('result.html', component=damage_component, condition=condition)

    except Exception as e:
        return render_template('result.html', result="Error predicting, please try again.")

@app.route('/purchase')
def purchase():
    part = request.args.get('part')
    return render_template('purchase.html', part=part)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run(debug=True)
