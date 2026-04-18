# import requests
# from backend.config import GROQ_API_KEY

# def call_llm(prompt):
#     url = "https://api.groq.com/openai/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "model": "qwen/qwen3-32b",
#         "messages": [
#             {"role": "system", "content": "You are a smart sales assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     }

#     response = requests.post(url, headers=headers, json=payload)
#     result = response.json()

#     return result["choices"][0]["message"]["content"]
from groq import Groq
from backend.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def call_llm(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert B2B sales closer and deal intelligence assistant. "
                        "Use past interactions when relevant. "
                        "Respond in a short, persuasive, professional way. "
                        "Keep the response under 3 lines. "
                        "Do not reveal reasoning. "
                        "Do not output <think> tags or internal analysis."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        content = completion.choices[0].message.content
        return content.strip() if content else "I understand the concern. Let’s align on the best next step."

    except Exception as e:
        print("LLM ERROR:", repr(e))
        return f"LLM Error: {str(e)}"