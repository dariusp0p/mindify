import openai

from django.conf import settings

if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY

def chat_with_gpt(prompt):
    """
    Function to interact with OpenAI's GPT model.
    """
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use a valid model name
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message["content"].strip()
    except Exception as e:
        print(f"Error: {e}")
        return None