from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the Google Gemini response
def get_gemini_response(input_text, image_data, prompt):
    try:
        st.write(f"Input Text: {input_text}")  # Debugging log
        st.write(f"Image Data: {image_data}")  # Debugging log
        st.write(f"Prompt: {prompt}")  # Debugging log
        
        # Attempt to use the generate_text method
        response = genai.generate_text(
            model="gemini-pro-vision",  # Make sure this model name is correct
            prompt=prompt,
            examples=[input_text, image_data],  # Check if this format is correct
        )
        st.write(f"Response: {response}")  # Debugging log
        return response['text']  # Modify this based on the actual response structure
    except AttributeError as e:
        st.error("AttributeError: Check if the SDK function or model name is correct.")
        st.write(f"Error details: {e}")  # Display the error in the Streamlit app
    except Exception as e:
        st.error("An unexpected error occurred.")
        st.write(f"Error details: {e}")

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
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_prompt)
        st.subheader("The Response is")
        st.write(response)
    except Exception as e:
        st.error("An error occurred while processing the request.")
        st.write(f"Error details: {e}")
