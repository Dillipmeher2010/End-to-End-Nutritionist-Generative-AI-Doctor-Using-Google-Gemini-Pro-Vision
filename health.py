from dotenv import load_dotenv
load_dotenv()  # load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import base64

# Configure API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(user_input: str, image_data: str, prompt: str):
    try:
        # Initialize the model and generate content
        response = genai.generate_content(
            model='gemini-1.5-flash',
            contents=[{"content": user_input}, {"content": prompt}],
            image_data=image_data  # Assuming image data is in base64
        )
        return response.text  # Ensure this returns a string
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Image encoding function for API compatibility
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        encoded_image = base64.b64encode(bytes_data).decode("utf-8")
        return encoded_image  # Returning base64-encoded image as a string
    else:
        st.error("Please upload an image file.")
        return None

# Streamlit app setup
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image_data = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    image_data = input_image_setup(uploaded_file)  # Correctly obtaining base64 image data

# Prompt for the nutrition analysis
input_prompt = """
You are an expert nutritionist. Analyze the food items from the image 
and calculate the total calories. Provide the details of each food item with 
caloric intake in the following format:

1. Item 1 - number of calories - Nutritious (Yes/No) - Health benefits
2. Item 2 - number of calories - Nutritious (Yes/No) - Health benefits
...
Total calories: [total calories]

Additionally, provide the recommended daily intake for an average adult and specify 
if these food items contribute positively to a healthy diet. Are they suitable for a balanced diet?
"""

submit = st.button("Tell me the total calories")

# Execute if submit button is clicked
if submit and image_data:
    response = get_gemini_response("Analyze image", image_data, input_prompt)
    
    # Debugging response
    if response is None:
        st.error("Failed to get a valid response.")
    else:
        st.subheader("The Response is")
        st.write(response)
