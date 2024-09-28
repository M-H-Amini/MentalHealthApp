import openai 
import os
import requests
from PIL import Image
from io import BytesIO



def generate_quote_image_4goal(goal):
    os.environ['OPENAI_API_KEY'] = open('key.txt').read().strip()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()
  
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Provide an inspiring and motivational quote related to the following goal: {goal}",
        max_tokens=200, n=1, stop=None, temperature=1,
    )
    quote = response.choices[0].text.strip()


    # Generate image
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=f"Provide an inspiring and motivational animated image related to the following goal: {goal}. Create the image in a nice workspace with good vibes and nice colors.",
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = image_response.data[0].url

    # Download the image
    image_data = requests.get(image_url).content
    image = Image.open(BytesIO(image_data))
    # Save and display the image
    image_filename = "goal_image.png"
    image.save(image_filename)

    return quote, image_filename



if __name__ == "__main__":
    goal = "being kind and feeling good about myself"
    quote, image_name = generate_quote_image_4goal(goal)
    print(quote)
    print(image_name)


