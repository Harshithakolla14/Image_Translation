import gradio as gr
import google.generativeai as genai
import base64
from io import BytesIO
from PIL import Image

# Configure Gemini API Key
GOOGLE_API_KEY = "AIzaSyCOsr7gV5hyZoFglhwI1mKnJMHR9XLx72M"
genai.configure(api_key=GOOGLE_API_KEY)

def image_to_poem(image, language):
    """
    Generates a poem in the selected language based on the uploaded image using Gemini 1.5 Pro.
    """
    try:
        # Convert image to Base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        image_b64 = base64.b64encode(img_bytes).decode('utf-8')

        # Create initial description
        prompt = "Describe this image in one sentence."
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content([{"mime_type": "image/png", "data": image_b64}, prompt])
        description = response.text if response else "No description available."

        # Map for language prompts
        lang_prompts = {
            "Tamil": "Based on this image description: {desc}, write a short, beautiful poem in Tamil.",
            "English": "Based on this image description: {desc}, write a short, beautiful poem in English.",
            "Hindi": "Based on this image description: {desc}, write a short, beautiful poem in Hindi.",
            "Telugu": "Based on this image description: {desc}, write a short, beautiful poem in Telugu."
        }

        poem_prompt = lang_prompts.get(language, lang_prompts["English"]).format(desc=description)
        response_poem = model.generate_content(poem_prompt)
        poem = response_poem.text if response_poem else "Poem could not be generated."

        return poem

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Define Gradio Interface
interface = gr.Interface(
    fn=image_to_poem,
    inputs=[
        gr.Image(type="pil", label="📷 Upload an Image"),
        gr.Dropdown(choices=["Tamil", "English", "Hindi", "Telugu"], label="🗣️ Select Language", value="Tamil")
    ],
    outputs=gr.Textbox(label="📝 Generated Poem"),
    title="🎨✨ Multi-Language Poem Generator from Image (Gemini AI)",
    description="Upload an image and choose a language — AI will create a beautiful poem inspired by the image. Try Tamil, English, Hindi, or Telugu!"
)

if __name__ == "__main__":
    interface.launch()
