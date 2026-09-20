from groq import Groq

from backend.config import GROQ_API_KEY, GROQ_MODEL


client = Groq(
    api_key=GROQ_API_KEY
)


def ask_groq(prompt: str) -> str:

    response = client.chat.completions.create(
        model=GROQ_MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an Industrial Maintenance "
                    "Knowledge Assistant. "
                    "The system supports English, Kiswahili, "
                    "and French."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,

        max_completion_tokens=1000
    )

    return response.choices[0].message.content