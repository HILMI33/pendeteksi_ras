import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Define constants
IMG_SIZE = 224
NUM_CLASSES = 5
EPOCHS = 5
BATCH_SIZE = 32
NUM_SAMPLES = 500  # Number of dummy samples

# Generate dummy image data (random noise)
x_train = np.random.rand(NUM_SAMPLES, IMG_SIZE, IMG_SIZE, 3).astype('float32')
# Generate dummy labels (one-hot encoded)
y_train = tf.keras.utils.to_categorical(np.random.randint(NUM_CLASSES, size=NUM_SAMPLES), NUM_CLASSES)

# Build a simple CNN model
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(NUM_CLASSES, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model on dummy data
model.fit(x_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE)

# Save the model
model.save('model/nationality_model.h5')
print("Dummy model training complete and saved to 'model/nationality_model.h5'")
