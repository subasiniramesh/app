%%streamlit_runner

import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# Load the models
first_model_path = '/content/drive/MyDrive/test/INCC AND RESNET.2ALL_dataaugment_final_model.h5'
first_model = load_model(first_model_path)

microcalcification_model_path = '/content/drive/MyDrive/test/SEPMICROinceptionresnetv2_1.h5'
microcalcification_model = load_model(microcalcification_model_path)

mass_model_path = '/content/drive/MyDrive/test/sepmassXception_1.h5'
mass_model = load_model(mass_model_path)

def classify_image(img):
    # Preprocess the image
    img = img.resize((224, 224))  # Resize the image to match the model's input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    # Initial classification using the first model
    initial_prediction = first_model.predict(img_array)
    initial_class = np.argmax(initial_prediction)
    classes = {0: 'mass', 1: 'microcalcification', 2: 'normal'}
    initial_class_label = classes[initial_class]

    # If the initial classification is 'normal,' return the result
    if initial_class_label == 'normal':
        return initial_class_label

    # Otherwise, proceed to the second model for microcalcification classification
    if initial_class_label == 'microcalcification':
        microcalcification_prediction = microcalcification_model.predict(img_array)
        microcalcification_class = np.argmax(microcalcification_prediction)
        benign_malignant = {0: 'benign', 1: 'malignant'}
        microcalcification_class_label = benign_malignant[microcalcification_class]

        # Combine the initial classification and microcalcification prediction for the final result
        final_result = f"{initial_class_label} {microcalcification_class_label}"
        return final_result

    # Otherwise, proceed to the third model for mass classification
    if initial_class_label == 'mass':
        mass_prediction = mass_model.predict(img_array)
        mass_class = np.argmax(mass_prediction)
        benign_malignant = {0: 'benign', 1: 'malignant'}
        mass_class_label = benign_malignant[mass_class]

        # Combine the initial classification and mass prediction for the final result
        final_result = f"{initial_class_label} {mass_class_label}"
        return final_result

# Streamlit app
st.title('Breast Cancer Image Classifier')

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Perform classification on the uploaded image
    result = classify_image(image)
    st.write(f"Prediction: {result}")
