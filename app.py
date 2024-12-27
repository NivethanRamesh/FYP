from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load classification model
classification_model_path = 'car_parts_classification_model.h5'
classification_model = load_model(classification_model_path)

# Configure MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/car'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define image dimensions
img_width, img_height = 150, 150

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
    
# Define a model for predictions
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc).astimezone().isoformat())
    component = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(50), nullable=False)

# Define Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc).astimezone().isoformat())

# Create the database and tables (if not exist)
with app.app_context():
    db.create_all()

# Function to save feedback to database
def save_feedback_to_db(name, email, phone, feedback):
    feedback_entry = Feedback(name=name, email=email, phone_number=phone, feedback_text=feedback)
    db.session.add(feedback_entry)
    db.session.commit()

# Function to save prediction to database
def save_to_db(component, condition):
    prediction = Prediction(component=component, condition=condition)
    db.session.add(prediction)
    db.session.commit()
    
    # Check if the part is damaged and count damaged parts
    if condition == 'Damaged':
        damaged_count = Prediction.query.filter_by(condition='Damaged').count()
        return damaged_count
    return 0

    
@app.route('/')
def animation():
    return render_template('animation.html')

@app.route('/start')
def start():
    return render_template('start.html')

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

        # Save prediction to database and get damaged count
        damaged_count = save_to_db(damage_component, condition)

        # Define component functions
        component_functions = {
            'spark-plug': 'Ignites the air-fuel mixture in the engine\'s combustion chamber to start the engine.',
            'BRAKE PAD': 'Provides the friction needed to slow down or stop the vehicle when the brakes are applied.',
            'windshield wiper': 'Cleans the windshield of the vehicle to provide a clear view for the driver.'
        }

        component_function = component_functions.get(damage_component, "Function not available")

        return render_template('result.html', component=damage_component, condition=condition, function=component_function, damaged_count=damaged_count)

    except Exception as e:
        return render_template('result.html', result="Error predicting, please try again.")


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        feedback_text = request.form['feedback']

        # Save feedback to database
        save_feedback_to_db(name, email, phone, feedback_text)

        return redirect(url_for('index'))  

    return render_template('feedback.html')

@app.route('/logs')
def logs():
    # Retrieve all predictions from the database
    predictions = Prediction.query.all()
    return render_template('logs.html', logs=predictions)

@app.route('/purchase')
def purchase():
    part = request.args.get('part')
    return render_template('Purchase.html', part=part)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run(debug=True)


