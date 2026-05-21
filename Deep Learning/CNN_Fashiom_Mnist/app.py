import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# ------------------------
# Page Config
# ------------------------
st.set_page_config(
    page_title="Fashion MNIST Classifier",
    page_icon="👕",
    layout="centered"
)

# ------------------------
# Load CSS
# ------------------------
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ------------------------
# Load Model
# ------------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("fashion_model.h5")

model = load_model()

# ------------------------
# Class Names
# ------------------------
class_names = [
    'T-shirt/top',
    'Trouser',
    'Pullover',
    'Dress',
    'Coat',
    'Sandal',
    'Shirt',
    'Sneaker',
    'Bag',
    'Ankle boot'
]

# ------------------------
# Header
# ------------------------
st.markdown("<h1 class='title'>Fashion MNIST Classifier</h1>", unsafe_allow_html=True)

st.markdown(
    "<p class='subtitle'>Upload a fashion image and let AI predict the clothing type.</p>",
    unsafe_allow_html=True
)

# ------------------------
# File Upload
# ------------------------
uploaded_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("L")

    st.image(
        image,
        caption="Uploaded Image",
        width=250
    )

    # Resize to 28x28
    image = image.resize((28, 28))

    img_array = np.array(image)

    # Normalize
    img_array = img_array / 255.0

    # Reshape for CNN
    img_array = img_array.reshape(1, 28, 28, 1)

    # Prediction
    prediction = model.predict(img_array)

    predicted_class = np.argmax(prediction)
    confidence = np.max(prediction) * 100

    st.markdown(
        f"""
        <div class="result-box">
            <h2>Prediction</h2>
            <h3>{class_names[predicted_class]}</h3>
            <p>Confidence: {confidence:.2f}%</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Prediction Probabilities")

    for i, prob in enumerate(prediction[0]):
        st.write(f"{class_names[i]} : {prob*100:.2f}%")
        st.progress(float(prob))