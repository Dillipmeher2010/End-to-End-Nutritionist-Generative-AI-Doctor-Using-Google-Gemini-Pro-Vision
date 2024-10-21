from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google Gemini API with the correct key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to call Google Gemini API and get response
def get_gemini_response(prompt, image_data):
    try:
        # Using generate_content method as an alternative to generate_text
        response = genai.generate_content(
            prompt=prompt, 
            images=[image_data]
        )
        return response  # Adjusting based on API structure
    
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None

# Function to handle the uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the uploaded image as bytes
        bytes_data = uploaded_file.read()
        image_parts = {
            "mime_type": uploaded_file.type,  # MIME type of the image
            "data": bytes_data  # Image data
        }
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")

# User inputs
input_text = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Define a prompt to send to the model
input_prompt = """
You are an expert nutritionist. Analyze the food items in the image, calculate the total calories, 
and provide details of each food item with its calorie count in the following format:

1. Item 1 - no of calories
2. Item 2 - no of calories
----
"""

# Submit button to send request
submit = st.button("Tell me the total calories")

if submit and uploaded_file:
    try:
        # Prepare the image for API input
        image_data = input_image_setup(uploaded_file)
        
        # Get the response from Gemini API
        response = get_gemini_response(input_prompt, image_data)
        
        if response:
            st.subheader("The Response is:")
            st.write(response)
        else:
            st.write("No response received.")
    
    except FileNotFoundError as e:
        st.error(f"File error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
