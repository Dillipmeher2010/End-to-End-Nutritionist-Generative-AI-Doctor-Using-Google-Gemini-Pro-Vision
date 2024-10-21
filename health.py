from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()  # This will load your API key from .env

# Configure the Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the Google Gemini response
def get_gemini_response(input_text, image_data, prompt):
    response = genai.generate_text(
        model="gemini-pro-vision",  # Correct model name
        prompt=prompt,
        examples=[input_text, image_data],
    )
    return response['text']  # Modify according to the actual SDK response format

# Function to handle image uploads
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Health App")
st.header("Gemini Health App")

# Take user input for prompt
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

# Default prompt for AI model
input_prompt = """
    You are an expert nutritionist. Analyze the food items in the image,
    calculate the total calories, and provide details about each food item
    and its calorie content. Use the format:

    1. Item 1 - no of calories
    2. Item 2 - no of calories
    ----
    ----
"""

# When submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_text, image_data, input_prompt)
    st.subheader("The Response is")
    st.write(response)
