from google import genai
from google.genai import types
from API_KEY import API_KEY

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a cat. Your name is Neko."),
    contents="Hello there"
)

print(response.text)