# llm.py

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv(override=True)
#print(os.environ.get("OPENAI_API_KEY"))

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are 'Jet Voice' a smart voice assistant running on Jetson Nano board"},
        {"role": "user",   "content": "Tell me about yourself."}
    ]
)

print(response.choices[0].message.content)

