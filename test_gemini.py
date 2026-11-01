import streamlit as st
from google import genai

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Reply with exactly: HealthAI Gemini connection successful."
    )
    print(response.text)

except Exception as e:
    print(f"Test failed: {type(e).__name__}: {e}") 