import streamlit as st
from PIL import Image, ImageDraw
import json
import requests
import os


# Function to make API request with image
def predict_image(image_path):
    # Replace these with your actual values
    token = "ovsb2mdu8c1f8tpmahgusrahcl"
    project_id = "60873"
    model = "Object-detection-2ld-DI"
    
    headers = {"X-Auth-token": token, "Content-Type": "application/octet-stream"}
    
    with open(image_path, 'rb') as handle:
        r = requests.post('https://platform.sentisight.ai/api/predict/{}/{}/'.format(project_id,model), headers=headers, data=handle)

    return r.json()

def draw_bounding_boxes(image, predictions):
    draw = ImageDraw.Draw(image)
    
    # Define a mapping from labels to colors
    label_colors = {
        "Sunkvezimis": "red",
        "Lengvoji": "blue",
        "Motociklas": "green",
        # Add more labels and colors as needed
    }

    for prediction in predictions:
        label = prediction.get('label', 'Unknown')  # Get label or default to 'Unknown'
        score = prediction.get('score', 0.0)  # Get score or default to 0.0
        x0, y0 = prediction.get('x0', 0), prediction.get('y0', 0)
        x1, y1 = prediction.get('x1', 0), prediction.get('y1', 0)
        
        # Get color based on label
        color = label_colors.get(label, "yellow")  # Default to green if label not found in mapping

        # Draw bounding box rectangle with label-specific color
        draw.rectangle([x0, y0, x1, y1], outline=color, width=3)
        
        # Add label and score as text near the bounding box
        text = f"{label} ({score:.1f})"
        draw.text((x0, y0 - 20), text, fill=color)

    return image
        
#   [{"label":"Sunkvezimis","score":98.0,"x0":336,"y0":407,"x1":369,"y1":467},{"label":"Lengvoji","score":74.9,"x0":355,"y0":456,"x1":406,"y1":530},{"label":"Lengvoji","score":65.3,"x0":302,"y0":438,"x1":336,"y1":487}]

# Streamlit app
def main():
    st.title("Object Prediction App")
    
    # File uploader for image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Parodo ikelta paveiksleli ir laikinai ji issaugo kad butu galima paduot ji i REST API
        temp_image_path = 'temp_image.jpg'  # e.g., 'temp_image.jpg'

        image = Image.open(uploaded_file)   #atidaro paveiksleli
        image.save(temp_image_path)         #issaugo paveiksleli
        st.image(image, use_column_width=True)  #parodo paveiksleli streamlite

        
        
        # Button to trigger prediction
        if st.button("Predict"):
            # Call predict_image function with uploaded image file
            st.text(temp_image_path)
            result = predict_image(temp_image_path)

            if result is not None:
                st.write("Prediction Result:")
                annotated_image = draw_bounding_boxes(image, result)
                st.image(annotated_image, caption="Annotated Image", use_column_width=True)

            os.remove(temp_image_path)
            
if __name__ == "__main__":
    main()
