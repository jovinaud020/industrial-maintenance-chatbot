from backend.rag.keyword_extractor import extract_keywords


questions = [

    "What causes bearing failure because of vibration and poor lubrication?",

    "Ni mambo gani yanaweza kusababisha bearing kushindwa kufanya kazi kutokana na mtetemo, joto na lubrication?",

    "Quelles sont les causes de défaillance d'un roulement liées à la lubrification et aux vibrations ?"
]


for question in questions:

    keywords = extract_keywords(
        question
    )

    print()
    print("=" * 70)

    print("Question:")
    print(question)

    print()

    print("Keywords:")

    for keyword in keywords:

        print(
            f"  • {keyword}"
        )