import openai 
import os
import requests
from PIL import Image
from io import BytesIO

# Ensure you have installed the required libraries:
# pip install openai requests Pillow



# Set up OpenAI API key
os.environ['OPENAI_API_KEY'] = open('key.txt').read().strip()
openai.api_key = os.getenv("OPENAI_API_KEY")



client = openai.OpenAI()


# Get user input
goal = input("Enter your goal for today: ")

# Generate motivational quote
print("\nGenerating motivational quote...")
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=f"Provide an inspiring and motivational quote related to the following goal: {goal}",
    max_tokens=150,
    n=1,
    stop=None,
    temperature=1,
)

quote = response.choices[0].text.strip()
print(f"\nMotivational Quote:\n{quote}")

# Generate image
print("\nGenerating image...")
image_response = client.images.generate(
    prompt=goal,
    n=1,
    size="512x512"
)

image_url = image_response.data[0].url

# Download the image
image_data = requests.get(image_url).content
image = Image.open(BytesIO(image_data))

# Save and display the image
image_filename = "goal_image.png"
image.save(image_filename)
print(f"\nImage saved as '{image_filename}'.")
image.show()
