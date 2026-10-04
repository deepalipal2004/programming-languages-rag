import os
import requests
from dotenv import load_dotenv


load_dotenv()

NUGEN_API_KEY = os.getenv("NUGEN_API_KEY")
NUGEN_MODEL_ID = os.getenv("NUGEN_MODEL_ID")
NUGEN_ENDPOINT = os.getenv("NUGEN_ENDPOINT")


def generate_answer(prompt):
    """
    Sends a prompt to the Nugen model
    and returns the generated answer.
    """

    headers = {
        "Authorization": f"Bearer {NUGEN_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": NUGEN_MODEL_ID,
        "prompt": prompt,
        "max_tokens": 400,
        "temperature": 0.2,
        "stream": False
    }

    response = requests.post(
        NUGEN_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=60
    )

    print("Status code:", response.status_code)

    response.raise_for_status()

    data = response.json()

    print("Response received.")

    if "choices" in data:
        return data["choices"][0]["text"]

    if "response" in data:
        return data["response"]

    if "text" in data:
        return data["text"]

    return str(data)


if __name__ == "__main__":

    test_prompt = "Explain ASP.NET in one simple sentence."

    answer = generate_answer(test_prompt)

    print("\nNugen response:\n")
    print(answer)