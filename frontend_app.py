import streamlit as st
import requests
from PIL import Image
from io import BytesIO

API_URL = "http://127.0.0.1:8000/predict/"

def upload_image():
    """Upload image via Streamlit interface and predict category"""
    st.title("Product Category Classifier")

    # Upload image
    uploaded_file = st.file_uploader("Upload an image of the product with white background", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Open image for display
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Convert image to bytes
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

        response = requests.post(API_URL, files={"file": img_byte_arr})

        if response.status_code == 200:
            prediction = response.json()
            st.write(f"Predicted Category ID: {prediction['predicted_id']}")
            st.write(f"Category Name: {prediction['category_name']}")
        else:
            st.error("Error in prediction: Unable to get response from the backend.")


if __name__ == "__main__":
    upload_image()
