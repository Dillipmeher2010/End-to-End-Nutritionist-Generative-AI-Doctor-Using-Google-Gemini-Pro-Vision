### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,image[0],prompt])
    return response.text

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
    
##initialize our streamlit app

st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the total calories")

input_prompt="""
You are a nutrition expert analyzing food items from an image. Your task is to identify each food item, estimate its calorie count, and provide a detailed breakdown of calories. Follow these steps carefully:

 **Food Item Identification and Calorie Calculation:**
   - Identify each visible food item in the image.
   - Calculate the approximate calories for each item, providing values in the following format:
     
     1. [Food Item 1] - [Approximate Calories]
     2. [Food Item 2] - [Approximate Calories]
     ...
   
 **Total Calorie Count:**
   - Sum the individual calorie counts to calculate the **total calories** for the entire meal or food spread shown in the image.
   
**Health Assessment:**
   - For each item, assess if it is generally healthy or unhealthy based on nutritional content (e.g., high in sugars, fats, or refined carbs).
   - Clearly indicate any items that should be limited or avoided due to high levels of unhealthy ingredients.
   
**Daily Caloric Needs and Nutritional Tips:**
   - Based on general dietary guidelines, provide a recommendation for daily caloric intake, considering factors such as age, gender, and activity level.
   - Share one or two **health tips** for a balanced diet, including advice for incorporating more nutrient-dense foods and maintaining a healthy lifestyle.
"""


## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)


