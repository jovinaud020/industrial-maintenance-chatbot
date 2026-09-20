from backend.services.language_service import detect_language


questions = [

    "What are the common causes of bearing failure?",

    "Ni mambo gani yanaweza kusababisha bearing kushindwa kufanya kazi?",

    "Quelles sont les causes courantes de défaillance d'un roulement ?"
]


for question in questions:

    language = detect_language(
        question
    )

    print()
    print("Question:")
    print(question)

    print(
        f"Detected language: {language}"
    )