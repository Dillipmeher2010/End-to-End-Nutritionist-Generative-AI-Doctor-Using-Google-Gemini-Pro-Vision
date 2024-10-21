# Health Management APP
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()  # Load all the environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the Google Gemini response
def get_gemini_response(input_text, image_data, prompt):
    try:
        st.write(f"Input Text: {input_text}")  # Debugging log
        st.write(f"Image Data Length: {len(image_data)}")  # Log the length of image data
        
        # Attempt to use the generate_text method
        response = genai.generate_text(
            model="gemini-pro-vision",  # Ensure this model name is correct
            prompt=prompt,
            examples=[input_text],  # Use input_text as an example
            image_data=image_data  # Pass the image data here
        )
        
        # Debugging: Log the entire response
        st.write("Raw API Response:")
        st.write(response)  # Log the raw response to understand its structure

        # Now try to access the response text
        if hasattr(response, 'text'):
            return response.text  # Modify this based on the actual response structure
        else:
            st.error("Response does not contain 'text'. Full response:")
            st.write(response)  # Display the entire response if 'text' is missing
    except AttributeError as e:
        st.error("AttributeError: Check if the SDK function or model name is correct.")
        st.write(f"Error details: {e}")  # Display the error in the Streamlit app
    except Exception as e:
        st.error("An unexpected error occurred.")
        st.write(f"Error details: {e}")

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
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

# Initialize our Streamlit app
st.set_page_config(page_title="Gemini Health App")
st.header("Gemini Health App")
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

input_prompt = """
You are an expert in nutrition. Analyze the food items in the image and calculate the total calories, 
providing details for each food item with calorie intake in the following format:

1. Item 1 - number of calories
2. Item 2 - number of calories
...
"""

# If the submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_text, image_data, input_prompt)
    st.subheader("The Response is")
    st.write(response)
