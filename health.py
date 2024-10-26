# health.py
### Health Management APP
from dotenv import load_dotenv
load_dotenv()  # load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(user_input, image_data, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Pass the input and prompt as plain text, with the image encoded if required
        response = model.generate_content([user_input, prompt])
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the image to base64 encoding to meet API expectations
        bytes_data = uploaded_file.getvalue()
        encoded_image = base64.b64encode(bytes_data).decode("utf-8")
        return encoded_image
    else:
        raise FileNotFoundError("No file uploaded")
    
## Initialize Streamlit app
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

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

## If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response("Analyze image", image_data, input_prompt)  # Adjusted argument usage
    if response:
        st.subheader("The Response is")
        st.write(response)
