from backend.services.groq_service import ask_groq


questions = [
    "What is preventive maintenance?",
    "Preventive maintenance ni nini?",
    "Qu'est-ce que la maintenance préventive ?"
]


for question in questions:

    print("\nQUESTION:")
    print(question)

    result = ask_groq(
        f"""
Identify the language of this question and respond with
ONLY the detected language.

Question:
{question}
"""
    )

    print("LANGUAGE:")
    print(result)