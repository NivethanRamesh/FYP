'''
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam

# Define the path to your dataset directory
dataset_directory = 'Plug_Data'

train_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_directory,
    labels='inferred',           
    label_mode='int',            
    batch_size=32,               
    image_size=(150, 150),      
    shuffle=True,                
    validation_split=0.15,        
    subset='training',           
    seed=123                     
)

# Create the validation dataset
validation_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_directory,
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(150, 150),
    shuffle=True,
    validation_split=0.15,
    subset='validation',
    seed=123
)

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal_and_vertical"),  
    tf.keras.layers.RandomRotation(0.2),                    
    tf.keras.layers.RandomZoom(0.35),                      
    tf.keras.layers.RandomContrast(0.5),                   
    tf.keras.layers.RandomBrightness(0.25)                   
])

# Normalize pixel values to [0, 1]
normalization_layer = tf.keras.layers.Rescaling(1./255)

train_dataset = train_dataset.map(lambda x, y: (normalization_layer(x), y))

validation_dataset = validation_dataset.map(lambda x, y: (normalization_layer(x), y))


# Define the model
model = Sequential([
 
    # Input layer
    model.add(layers.InputLayer(input_shape=(150, 150, 3), name="input_layer"))

    # First Convolutional Layer
    Conv2D(
        filters=16,
        kernel_size=(3, 3),
        strides=(1, 1),
        padding='valid',
        activation='relu',
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        input_shape=(256, 256, 3),
        name='conv2d_1'
    ),
    MaxPooling2D(
        pool_size=(2, 2),
        strides=(2, 2),
        padding='valid',
        name='max_pooling2d_1'
    ),

    # Second Convolutional Layer
    Conv2D(
        filters=32,
        kernel_size=(3, 3),
        strides=(1, 1),
        padding='valid',
        activation='relu',
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        name='conv2d_2'
    ),
    MaxPooling2D(
        pool_size=(2, 2),
        strides=(2, 2),
        padding='valid',
        name='max_pooling2d_2'
    ),

    # Third Convolutional Layer
    Conv2D(
        filters=16,
        kernel_size=(3, 3),
        strides=(1, 1),
        padding='valid',
        activation='relu',
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        name='conv2d_3'
    ),
    MaxPooling2D(
        pool_size=(2, 2),
        strides=(2, 2),
        padding='valid',
        name='max_pooling2d_3'
    ),

    # Flatten Layer
    Flatten(name='flatten'),

    # First Dense Layer
    Dense(
        units=256,
        activation='relu',
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        name='dense_1'
    ),

    # Output Dense Layer
    Dense(
        units=1,
        activation='sigmoid',
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        name='output_layer'
    )
])

# Define the Adam optimizer with specific parameters
adam = Adam(
    learning_rate=0.001,
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-07,
    amsgrad=False
)

# Compile the model with the specified loss function parameters
model.compile(
    optimizer=adam,
    loss=tf.keras.losses.BinaryCrossentropy(
        from_logits=False,
        label_smoothing=0.0,
        reduction=tf.keras.losses.Reduction.SUM_OVER_BATCH_SIZE
    ),
    metrics=['accuracy']
)

# Summary of the model
model.summary()

# Training the model 
history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=10, 
    batch_size=32, 
    validation_split=0.15
)

'''