import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Define image size and batch size
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 5

# Define classes
classes = ['Asia', 'Afrika', 'Eropa', 'Amerika', 'Timur Tengah']

# Assuming you have a dataset directory structured as:
# dataset/
#    Asia/
#    Afrika/
#    Eropa/
#    Amerika/
#    Timur Tengah/
# Each folder contains images of that class

dataset_dir = 'dataset'  # Change this to your dataset path

if not os.path.exists(dataset_dir):
    raise FileNotFoundError(f"Dataset directory '{dataset_dir}' not found. Please provide your dataset.")

# Data augmentation and preprocessing
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# Build a simple CNN model
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(len(classes), activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator
)

# Save the model in HDF5 format
model.save('model/nationality_model.h5')
print("Model training complete and saved to 'model/nationality_model.h5'")
