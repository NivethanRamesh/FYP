from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing import image

# Define image dimensions
img_width, img_height = 150, 150

# Directory containing test images
test_data_dir = 'test'

test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=(img_width, img_height),
    batch_size=32,
    class_mode='binary')

# Load the saved model
model = load_model('BreakPadCheck.h5')

# Evaluate on test set
test_loss, test_acc = model.evaluate(test_generator)
print(f'Test accuracy: {test_acc}')

# Example prediction
img_path = 'UNDBreakPad.png'
img = image.load_img(img_path, target_size=(img_width, img_height))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

predictions = model.predict(img_array)
class_idx = int(predictions[0][0])
class_names = ['Damage', 'Undamage']
print(f'Prediction: {class_names[class_idx]}')
print(f'Probability: {predictions[0][0]}')
