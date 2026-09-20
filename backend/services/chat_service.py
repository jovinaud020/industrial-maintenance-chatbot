# =====================================================
# INDUSTRIAL MAINTENANCE AI
# CHAT SERVICE
# =====================================================

from backend.rag.retriever import retrieve_documents
from backend.rag.keyword_extractor import extract_keywords
from backend.services.language_service import detect_language
from backend.services.groq_service import ask_groq


# =====================================================
# BASIC RESPONSES
# =====================================================

def get_basic_response(question: str, language: str):
    """
    Handles greetings and simple assistant-related questions.
    """

    normalized = question.lower().strip()

    # -------------------------------------------------
    # ENGLISH
    # -------------------------------------------------

    if language == "en":

        if normalized in {
            "hi",
            "hello",
            "hellow",
            "hi there",
            "hey there",
            "hello there",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        }:
            return {
                "answer": (
                    "Hello! I am the Industrial Maintenance "
                    "Knowledge Assistant. How can I help you "
                    "with industrial maintenance?"
                ),
                "keywords": []
            }

        if normalized in {
            "who are you",
            "what are you",
            "what is your name"
        }:
            return {
                "answer": (
                    "I am an Industrial Maintenance Knowledge "
                    "Assistant."
                ),
                "keywords": []
            }

        if normalized in {
            "what can you do",
            "what do you do",
            "how can you help me"
        }:
            return {
                "answer": (
                    "I can help you with industrial maintenance "
                    "topics such as bearings, motors, pumps, "
                    "lubrication, hydraulics, safety, failures, "
                    "inspection, and preventive maintenance."
                ),
                "keywords": []
            }

        if normalized in {
            "what languages do you support",
            "which languages do you support",
            "what language do you speak"
        }:
            return {
                "answer": (
                    "I support English, Kiswahili, and French."
                ),
                "keywords": []
            }

    # -------------------------------------------------
    # KISWAHILI
    # -------------------------------------------------

    if language == "sw":

        if normalized in {
            "habari",
            "habari yako",
            "mambo",
            "mambo vipi",
            "hujambo",
            "shikamoo"
        }:
            return {
                "answer": (
                    "Habari! Mimi ni Industrial Maintenance "
                    "Knowledge Assistant. Naweza kukusaidia "
                    "kuhusu matengenezo ya mitambo ya viwandani."
                ),
                "keywords": []
            }

        if normalized in {
            "wewe ni nani",
            "nani wewe",
            "wewe nani",
            "wewe ni mtu nani",
            "nani ni wewe",
            "wewe ni mtu gani",
            "unaitwa nani",
            "nani wewe",
            "nani yu",
            "wewe ni nini"
        }:
            return {
                "answer": (
                    "Mimi ni Industrial Maintenance Knowledge "
                    "Assistant."
                ),
                "keywords": []
            }

        if normalized in {
            "unaweza kufanya nini",
            "unaweza kunisaidia nini",
            "unaweza kunisaidiaje"
        }:
            return {
                "answer": (
                    "Naweza kukusaidia kuhusu matengenezo ya "
                    "viwandani kama bearings, motors, pumps, "
                    "lubrication, hydraulics, usalama, "
                    "uchunguzi wa hitilafu na preventive maintenance."
                ),
                "keywords": []
            }

        if normalized in {
            "unaunga mkono lugha gani",
            "unazungumza lugha gani",
            "lugha gani unaunga mkono"
        }:
            return {
                "answer": (
                    "Ninaunga mkono English, Kiswahili, na French."
                ),
                "keywords": []
            }

    # -------------------------------------------------
    # FRENCH
    # -------------------------------------------------

    if language == "fr":

        if normalized in {
            "bonjour",
            "salut",
            "bonsoir"
        }:
            return {
                "answer": (
                    "Bonjour ! Je suis l'Industrial Maintenance "
                    "Knowledge Assistant. Comment puis-je vous "
                    "aider concernant la maintenance industrielle ?"
                ),
                "keywords": []
            }

        if normalized in {
            "qui es tu",
            "qui êtes vous",
            "comment tu t'appelles"
        }:
            return {
                "answer": (
                    "Je suis l'Industrial Maintenance Knowledge "
                    "Assistant."
                ),
                "keywords": []
            }

        if normalized in {
            "que peux tu faire",
            "que pouvez vous faire",
            "comment peux tu m'aider"
        }:
            return {
                "answer": (
                    "Je peux vous aider sur les sujets de "
                    "maintenance industrielle tels que les "
                    "roulements, moteurs, pompes, lubrification, "
                    "hydraulique, sécurité et maintenance préventive."
                ),
                "keywords": []
            }

        if normalized in {
            "quelles langues supportez vous",
            "quelles langues parlez vous",
            "quelles langues supportes tu"
        }:
            return {
                "answer": (
                    "Je prends en charge l'anglais, le kiswahili "
                    "et le français."
                ),
                "keywords": []
            }

    return None


# =====================================================
# MAINTENANCE TOPIC DETECTION
# =====================================================

def is_maintenance_question(question: str) -> bool:
    """
    Checks whether the question contains an industrial
    maintenance-related term.
    """

    maintenance_terms = {

        # -------------------------------------------------
        # ENGLISH
        # -------------------------------------------------

        "bearing",
        "bearings",
        "motor",
        "motors",
        "pump",
        "pumps",
        "lubrication",
        "lubricant",
        "lubricants",
        "grease",
        "oil",
        "hydraulic",
        "hydraulics",
        "maintenance",
        "maintain",
        "repair",
        "inspection",
        "failure",
        "fault",
        "faults",
        "damage",
        "wear",
        "vibration",
        "temperature",
        "pressure",
        "contamination",
        "alignment",
        "shaft",
        "seal",
        "seals",
        "machine",
        "machines",
        "equipment",
        "safety",
        "preventive",
        "predictive",
        "breakdown",
        "overheating",
        "leak",
        "leakage",
        "valve",
        "filter",
        "filters",

        # -------------------------------------------------
        # KISWAHILI
        # -------------------------------------------------

        "matengenezo",
        "mashine",
        "mitambo",
        "motor",
        "motors",
        "pampu",
        "bearing",
        "bearings",
        "mafuta",
        "grisi",
        "majimaji",
        "hydraulic",
        "shinikizo",
        "mtetemo",
        "joto",
        "kuharibika",
        "uharibifu",
        "usalama",
        "uchunguzi",
        "ukaguzi",
        "uchafu",
        "kuvuja",
        "kuchakaa",
        "kushindwa",

        # -------------------------------------------------
        # FRENCH
        # -------------------------------------------------

        "roulement",
        "roulements",
        "moteur",
        "moteurs",
        "pompe",
        "pompes",
        "lubrification",
        "lubrifiant",
        "graisse",
        "huile",
        "hydraulique",
        "maintenance",
        "réparation",
        "inspection",
        "défaillance",
        "panne",
        "dommage",
        "usure",
        "vibration",
        "température",
        "pression",
        "contamination",
        "alignement",
        "arbre",
        "joint",
        "sécurité",
        "fuite",
        "vanne",
        "filtre"
    }

    question_lower = question.lower()

    return any(
        term in question_lower
        for term in maintenance_terms
    )


# =====================================================
# FOLLOW-UP DETECTION
# =====================================================

def is_follow_up_question(question: str) -> bool:
    """
    Detects questions that refer to previous conversation.

    Examples:
        How can I prevent it?
        Why does it happen?
        What about this?
        Ninawezaje kuzuia hilo?
        Kwa nini hiyo inatokea?
        Comment éviter cela ?
    """

    question_lower = question.lower().strip()

    follow_up_phrases = [

        # -------------------------------------------------
        # ENGLISH
        # -------------------------------------------------

        "it",
        "this",
        "that",
        "they",
        "them",
        "these",
        "those",
        "its",
        "their",

        "how can i",
        "how do i",
        "what about",
        "why does it",
        "why is it",
        "why are they",
        "what causes it",
        "how can it",
        "how do you",
        "what should i do",
        "what should be done",
        "how can this",
        "how does this",
        "why does this",
        "what about this",
        "what about that",

        # -------------------------------------------------
        # KISWAHILI
        # -------------------------------------------------

        "hii",
        "hicho",
        "hiyo",
        "hivyo",
        "hizi",
        "hizo",
        "hilo",
        "hilo lina",
        "hilo inat",
        "hilo ni",
        "hilo?",
        "hiyo?",
        "hii?",
        "hicho?",
        "hizi?",
        "hizo?",

        "nawezaje",
        "ninawezaje",
        "nifanye nini",
        "sababu yake",
        "inawezaje",
        "kwa nini hii",
        "kwa nini hiyo",
        "kwa nini hilo",
        "inawezaje kuzuiwa",
        "nawezaje kuzuia",
        "ninawezaje kuzuia",
        "ninawezaje kurekebisha",

        # -------------------------------------------------
        # FRENCH
        # -------------------------------------------------

        "cela",
        "ça",
        "ceci",
        "celui",
        "celle",
        "comment puis",
        "que dois je faire",
        "que faire",
        "comment le",
        "comment la",
        "pourquoi cela",
        "pourquoi ça",
        "comment éviter cela",
        "comment éviter ça"
    ]

    for phrase in follow_up_phrases:
        if phrase in question_lower:
            return True

    return False


# =====================================================
# HISTORY MAINTENANCE CONTEXT
# =====================================================

def history_has_maintenance_context(history) -> bool:
    """
    Checks whether previous conversation contains an
    industrial maintenance topic.
    """

    if not history:
        return False

    for message in history:

        content = message.get("content", "")

        if not content:
            continue

        if is_maintenance_question(content):
            return True

    return False


# =====================================================
# GET PREVIOUS USER LANGUAGE
# =====================================================

def get_previous_user_language(history):
    """
    Gets the language of the most recent user message.

    This is important for follow-up questions.

    Example:

        User:
        Ni sababu gani za kawaida za kuharibika kwa bearing?

        Assistant:
        [Kiswahili answer]

        User:
        Ninawezaje kuzuia hilo?

    The second question should remain Kiswahili.
    """

    if not history:
        return None

    # Search from newest message backwards
    for message in reversed(history):

        if message.get("role") != "user":
            continue

        content = message.get("content", "").strip()

        if not content:
            continue

        return detect_language(content)

    return None


# =====================================================
# DETERMINE CONVERSATION LANGUAGE
# =====================================================

def determine_language(question: str, history) -> str:
    """
    Determines the language for the current response.

    Normal question:
        Detect language from current question.

    Follow-up question:
        Keep the language of the previous user message.

    This allows conversations such as:

        Kiswahili -> Kiswahili follow-up
        English -> English follow-up
        French -> French follow-up
    """

    current_language = detect_language(question)

    follow_up = is_follow_up_question(question)

    if follow_up and history:

        previous_language = get_previous_user_language(
            history
        )

        if previous_language:
            return previous_language

    return current_language


# =====================================================
# BUILD RAG CONTEXT
# =====================================================

def build_context(documents):
    """
    Builds internal RAG context.

    Sources are NOT displayed to the user.
    """

    if not documents:
        return "No relevant information was retrieved."

    context_parts = []

    for index, document in enumerate(documents, start=1):

        text = document.get("text", "")

        if not text:
            continue

        context_parts.append(
            f"Document {index}:\n{text}"
        )

    if not context_parts:
        return "No relevant information was retrieved."

    return "\n\n".join(context_parts)


# =====================================================
# BUILD CONVERSATION HISTORY
# =====================================================

def build_history(history):
    """
    Converts previous conversation into prompt context.

    Previous messages are used only for understanding
    conversation references.

    They are NOT technical knowledge sources.
    """

    if not history:
        return ""

    history_parts = []

    for message in history[-10:]:

        role = message.get("role", "")
        content = message.get("content", "")

        if role not in {
            "user",
            "assistant"
        }:
            continue

        if not content:
            continue

        if role == "user":
            history_parts.append(
                f"User: {content}"
            )

        elif role == "assistant":
            history_parts.append(
                f"Assistant: {content}"
            )

    if not history_parts:
        return ""

    return "\n".join(history_parts)


# =====================================================
# BUILD PROMPT
# =====================================================
def build_prompt(
    question: str,
    context: str,
    language: str,
    history=None
):
    """
    Creates a strict RAG prompt focused on accurate,
    practical industrial-maintenance answers.
    """

    if history is None:
        history = []

    conversation = build_history(history)

    language_name = {
        "en": "English",
        "sw": "Kiswahili",
        "fr": "French"
    }.get(
        language,
        "English"
    )

    if conversation:

        conversation_section = f"""
Previous conversation:

{conversation}

Use the previous conversation ONLY to understand
what the user is referring to.

For example:
- "it"
- "this"
- "that"
- "hilo"
- "hiyo"
- "hii"
- "cela"
- "ça"

Do not use previous conversation as technical evidence.

The retrieved industrial-maintenance information below
is the technical evidence for your answer.
"""

    else:

        conversation_section = """
There is no previous conversation.
Answer the current question using the retrieved
industrial-maintenance information below.
"""

    prompt = f"""
You are an Industrial Maintenance Knowledge Assistant.

You provide technical assistance about industrial
maintenance.

The user's current response language is:

{language_name}

=====================================================
CORE RULE
=====================================================

Answer the user's question using the retrieved
industrial-maintenance information provided below.

Do NOT rely on general knowledge when the retrieved
information does not support a technical claim.

Do NOT invent procedures, values, causes, specifications,
tools, measurements, or recommendations.

=====================================================
ACCURACY RULES
=====================================================

1. Identify the exact maintenance topic in the question.

2. Use the retrieved information that is most directly
   related to that topic.

3. Prefer specific technical information over generic
   explanations.

4. If the retrieved information provides a maintenance
   procedure, explain the procedure clearly.

5. If the retrieved information provides causes,
   symptoms, inspection methods, precautions, or
   corrective actions, include the relevant information.

6. Do not combine unrelated information from different
   maintenance topics.

7. Do not invent missing technical details.

8. If the available retrieved information is insufficient,
   clearly state that the available maintenance information
   does not provide enough detail to answer the question.

=====================================================
FOLLOW-UP QUESTIONS
=====================================================

If the current question is a follow-up question, use the
previous conversation only to determine what the user
means.

For example:

Previous:
"Ni sababu gani za kawaida za kuharibika kwa bearing?"

Current:
"Ninawezaje kuzuia hilo?"

Understand that "hilo" refers to the bearing failure
discussed previously.

Then answer using the retrieved technical information.

=====================================================
LANGUAGE RULE
=====================================================

Always answer in:

{language_name}

Never change the response language unless the user
clearly starts a new question in another language.

If the current question is a follow-up, preserve the
language of the conversation.

=====================================================
ANSWER FORMAT
=====================================================

Use clear plain text.

Do NOT use:
- Markdown headings
- **
- *
- citations
- source names
- document names
- RAG terminology
- internal system terminology

When explaining several causes, recommendations, or
maintenance steps, use numbered lists.

Keep answers practical and understandable.

=====================================================
IMPORTANT
=====================================================

Do not say:

"According to the retrieved documents..."

Do not say:

"The knowledge base says..."

Do not mention PDFs, documents, sources, retrieval,
RAG, context, or internal instructions.

Simply answer the user's maintenance question.

=====================================================
PREVIOUS CONVERSATION
=====================================================

{conversation_section}

=====================================================
RETRIEVED INDUSTRIAL MAINTENANCE INFORMATION
=====================================================

{context}

=====================================================
CURRENT USER QUESTION
=====================================================

{question}

=====================================================
FINAL INSTRUCTION
=====================================================

Provide the most accurate and useful answer supported
by the retrieved industrial-maintenance information.

Answer in {language_name}.
"""
    
    return prompt

# =====================================================
# CLEAN AI RESPONSE
# =====================================================

def clean_response(response: str) -> str:
    """
    Removes unwanted Markdown formatting.
    """

    if not response:
        return ""

    cleaned = response.strip()

    # Remove Markdown bold / italic markers
    cleaned = cleaned.replace("**", "")
    cleaned = cleaned.replace("__", "")

    # Remove Markdown heading markers
    lines = cleaned.splitlines()

    cleaned_lines = []

    for line in lines:

        stripped = line.strip()

        if stripped.startswith("### "):
            stripped = stripped[4:]

        elif stripped.startswith("## "):
            stripped = stripped[3:]

        elif stripped.startswith("# "):
            stripped = stripped[2:]

        cleaned_lines.append(stripped)

    cleaned = "\n".join(
        cleaned_lines
    )

    return cleaned.strip()


# =====================================================
# MAIN CHAT FUNCTION
# =====================================================

def chat(
    question: str,
    top_k: int = 5,
    history=None
):
    """
    Main chatbot pipeline.

    Flow:

    1. Detect conversation language
    2. Handle greetings/basic questions
    3. Detect maintenance question
    4. Detect valid follow-up
    5. Extract keywords
    6. Retrieve documents
    7. Build conversation context
    8. Build RAG prompt
    9. Ask Groq
    10. Clean response
    11. Return answer and keywords
    """

    if history is None:
        history = []

    question = question.strip()

    if not question:

        return {
            "answer": "Please enter a question.",
            "keywords": []
        }

    # -------------------------------------------------
    # STEP 1: DETERMINE LANGUAGE
    # -------------------------------------------------

    language = determine_language(
        question,
        history
    )

    # -------------------------------------------------
    # STEP 2: BASIC RESPONSE
    # -------------------------------------------------

    basic_response = get_basic_response(
        question,
        language
    )

    if basic_response:
        return basic_response

    # -------------------------------------------------
    # STEP 3: FOLLOW-UP DETECTION
    # -------------------------------------------------

    follow_up = is_follow_up_question(
        question
    )

    # -------------------------------------------------
    # STEP 4: MAINTENANCE QUESTION DETECTION
    # -------------------------------------------------

    maintenance_question = is_maintenance_question(
        question
    )

    # -------------------------------------------------
    # STEP 5: ALLOW VALID FOLLOW-UP QUESTIONS
    # -------------------------------------------------

    if not maintenance_question:

        if not (
            follow_up
            and history_has_maintenance_context(history)
        ):

            refusal_messages = {

                "en": (
                    "I can only answer questions related "
                    "to industrial maintenance."
                ),

                "sw": (
                    "Naweza kujibu maswali yanayohusiana "
                    "tu na matengenezo ya mitambo ya viwandani."
                ),

                "fr": (
                    "Je peux répondre uniquement aux questions "
                    "liées à la maintenance industrielle."
                )
            }

            return {
                "answer": refusal_messages.get(
                    language,
                    refusal_messages["en"]
                ),
                "keywords": []
            }

    # -------------------------------------------------
    # STEP 6: KEYWORD EXTRACTION
    # -------------------------------------------------

    try:

        keywords = extract_keywords(
            question
        )

    except Exception:

        keywords = []

    # -------------------------------------------------
    # STEP 7: RETRIEVE DOCUMENTS
    # -------------------------------------------------

    documents = retrieve_documents(
        question,
        top_k=top_k
    )

    # -------------------------------------------------
    # STEP 8: BUILD RAG CONTEXT
    # -------------------------------------------------

    context = build_context(
        documents
    )

    # -------------------------------------------------
    # STEP 9: BUILD PROMPT
    # -------------------------------------------------

    prompt = build_prompt(
        question=question,
        context=context,
        language=language,
        history=history
    )

    # -------------------------------------------------
    # STEP 10: ASK GROQ
    # -------------------------------------------------

    response = ask_groq(
        prompt
    )

    # -------------------------------------------------
    # STEP 11: CLEAN RESPONSE
    # -------------------------------------------------

    answer = clean_response(
        response
    )

    # -------------------------------------------------
    # STEP 12: RETURN RESULT
    # -------------------------------------------------

    return {
        "answer": answer,
        "keywords": keywords
    }