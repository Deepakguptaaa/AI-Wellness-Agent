from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6KaYZlKTzce5uogjhZTiZJl1zFy1utWYkTfCqIZ2FpTtw"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello"
)

print(response.text)