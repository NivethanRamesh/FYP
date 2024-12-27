from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load the models
damage_model_path = r'C:\Users\nivet\OneDrive - Asia Pacific University\Desktop\Year3(Semester2)\FYP\Finalized\FINAL PROJECT_Nivethan_TP062192\plug_check_model.h5'  # Update with your damage model path
classification_model_path = 'car_parts_classification_model.h5'  # Update with your classification model path
damage_model = load_model(damage_model_path)
classification_model = load_model(classification_model_path)

# Define image dimensions (should match the dimensions used during training)
img_width, img_height = 150, 150

# Function to predict component and its condition
def predict(image_path):
    try:
        # Load and preprocess the image
        img = image.load_img(image_path, target_size=(img_width, img_height))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize pixel values

        # Predict component type
        class_predictions = classification_model.predict(img_array)
        class_idx = np.argmax(class_predictions[0])
        class_names = ['BRAKE PAD', 'spark-plug', 'windshield wiper']  # Updated class names
        component_name = class_names[class_idx]

        # Predict damage condition if component is spark-plug
        if component_name == 'spark-plug':
            damage_img = cv2.imread(image_path)
            damage_img = cv2.resize(damage_img, (224, 224)) / 255.0
            damage_img = np.expand_dims(damage_img, axis=0)
            damage_prediction = damage_model.predict(damage_img)
            condition = 'Damaged' if damage_prediction < 0.5 else 'Undamaged'
        else:
            condition = 'Not applicable'

        return component_name, condition

    except Exception as e:
        print(f"Error predicting: {str(e)}")
        return "Error predicting component", "Error predicting condition"

app = Flask(__name__)

# Route to render animation page for 10 seconds and then redirect to index
@app.route('/')
def animation():
    return render_template('animation.html')

# Route to render index.html which has the upload form
@app.route('/index')
def index():
    return render_template('index.html')

# Route to handle file upload and redirect to loading page
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(os.getcwd(), filename)  # Get full path where file was uploaded
            file.save(filepath)
            return redirect(url_for('loading', filepath=filepath))  # Redirect to loading page with filepath

    return redirect(url_for('index'))

# Route to render loading.html and start the prediction process
@app.route('/loading')
def loading():
    filepath = request.args.get('filepath')
    if filepath is None:
        return render_template('result.html', result="Error: Filepath is None")
    return render_template('loading.html', filepath=filepath)

# Route to render result.html and show prediction result
@app.route('/result')
def result():
    filepath = request.args.get('filepath')
    if filepath is None:
        return render_template('result.html', result="Error: Filepath is None")

    if not os.path.exists(filepath):
        return render_template('result.html', result="File does not exist")

    try:
        component, condition = predict(filepath)
        return render_template('result.html', component=component, condition=condition)
    except Exception as e:
        return render_template('result.html', result="Error predicting, please try again.")

# Route to render purchase.html for selecting replacement options
@app.route('/purchase')
def purchase():
    part = request.args.get('part')
    return render_template('purchase.html', part=part)

# Disable caching for all routes
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run(debug=True)
