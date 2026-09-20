# =====================================================
# INDUSTRIAL MAINTENANCE AI
# LANGUAGE DETECTION SERVICE
# =====================================================

import re


# =====================================================
# ENGLISH VOCABULARY
# =====================================================

ENGLISH_WORDS = {
    # General English
    "what", "are", "the", "is", "how", "why", "when",
    "where", "which", "can", "does", "do", "and", "of",
    "to", "for", "with", "from", "this", "that",
    "these", "those", "it", "its", "function", "functions",
    "purpose", "used", "use", "work", "works",
    "explain", "describe", "tell", "give",

    # Maintenance
    "maintenance", "failure", "cause", "causes",
    "prevent", "preventive", "repair", "fix",
    "problem", "problems", "machine", "machines",
    "equipment", "temperature", "pressure", "vibration",
    "damage", "wear", "inspection", "contamination",
    "alignment", "overheating", "leak", "leakage",
    "lubrication", "safety", "motor", "motors",
    "bearing", "bearings", "pump", "pumps",
    "hydraulic", "hydraulics", "system", "systems",
    "oil", "grease", "failure", "maintenance",
    "procedure", "procedures", "inspection", "service",
    "replace", "replacement", "clean", "cleaning"
}


# =====================================================
# KISWAHILI VOCABULARY
# =====================================================

SWAHILI_WORDS = {
    # Greetings
    "habari", "yako", "mambo", "vipi", "hujambo",
    "shikamoo",

    # Common Swahili
    "ni", "nini", "gani", "kwa", "jinsi", "sababu",
    "ya", "na", "za", "wa", "cha", "vya","wewe", "yeye", "sisi", "nyinyi", "wao",
    "hii", "hicho", "hiyo", "hilo", "hivi","ni", "za", "wa", "cha", "vya", "wewe", "yeye", "sisi", "nyinyi", "wao",
    "hivyo", "hizi", "hizo", "huyo", "hao","nani", "nani", "nini", "gani", "kama", "hivyo", "hizi", "hizo", "huyo", "hao",
    "hake", "hapo", "huko", "hapa",

    # Maintenance
    "kushindwa", "kuharibika", "uharibifu",
    "matengenezo", "mashine", "mitambo",
    "motor", "mota", "pampu", "bearing", "bearings",
    "mafuta", "grisi", "joto", "mtetemo",
    "shinikizo", "usalama", "ukaguzi", "uchunguzi",
    "uchafu", "kuvuja", "kuchakaa",
    "kurekebisha", "kuzuia", "kuepuka",
    "kupunguza", "kuondoa", "kufanya",

    # Common question words
    "ninawezaje", "nawezaje", "unawezaje",
    "tunawezaje", "mnawezaje",
    "nifanye", "nifanyeje",
    "ipi", "vipi", "je",

    # Maintenance terms commonly mixed with English
    "kazi", "kaziya", "sehemu", "sehemuya",
    "inafanya", "inafanyaje", "kazi",
    "inatumika", "kutumika", "hufanya",
    "inaweza", "inawezaje"
}


# =====================================================
# FRENCH VOCABULARY
# =====================================================

FRENCH_WORDS = {
    "bonjour", "salut", "bonsoir",
    "comment", "pourquoi", "quelles", "quelle",
    "quels", "quel", "sont", "les", "des",
    "une", "un", "et", "de", "du", "la",
    "le", "ce", "cela", "ça", "ceci",
    "causes", "défaillance", "maintenance",
    "roulement", "roulements", "moteur", "moteurs",
    "pompe", "pompes", "lubrification",
    "hydraulique", "sécurité", "réparation",
    "inspection", "usure", "vibration",
    "température", "pression", "contamination",
    "alignement", "fuite", "huile", "graisse",
    "éviter", "prévenir", "réparer"
}


# =====================================================
# COMMON MIXED-LANGUAGE / COLLOQUIAL TERMS
# =====================================================

# These are common ways users may type technical
# questions using a mixture of English and Kiswahili.

SWAHILI_TECHNICAL_ALIASES = {
    "mota": "motor",
    "motar": "motor",
    "motore": "motor",
    "pamp": "pump",
    "beering": "bearing",
    "bering": "bearing",
    "lubrication": "lubrication",
    "maintanance": "maintenance",
    "maintainance": "maintenance",
    "hydroliki": "hydraulic",
    "haidroliki": "hydraulic",
    "presha": "pressure",
    "pressure": "pressure",
    "temperature": "temperature",
    "vibration": "vibration"
}


# =====================================================
# NORMALIZE TEXT
# =====================================================

def normalize_text(text: str) -> str:
    """
    Normalizes text before language detection.
    """

    text = text.lower().strip()

    text = re.sub(
        r"[^\w\sàâçéèêëîïôûùüÿœæ'-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# =====================================================
# EXACT GREETINGS
# =====================================================

def detect_greeting(text: str):
    swahili_greetings = {
        "habari",
        "habari yako",
        "mambo",
        "mambo vipi",
        "hujambo",
        "shikamoo"
    }

    french_greetings = {
        "bonjour",
        "salut",
        "bonsoir"
    }

    english_greetings = {
        "hi",
        "hello",
        "hey",
        "how are you",
        "good morning",
        "good afternoon",
        "good evening"
    }

    if text in swahili_greetings:
        return "sw"

    if text in french_greetings:
        return "fr"

    if text in english_greetings:
        return "en"

    return None


# =====================================================
# DETECT LANGUAGE
# =====================================================

def detect_language(text: str) -> str:
    """
    Detects English, Kiswahili, French,
    including mixed English + Kiswahili questions.

    Returns:
        en = English
        sw = Kiswahili
        fr = French
    """

    text = normalize_text(text)

    if not text:
        return "en"

    # -------------------------------------------------
    # GREETINGS
    # -------------------------------------------------

    greeting = detect_greeting(text)

    if greeting:
        return greeting

    # -------------------------------------------------
    # SPECIAL KISWAHILI FOLLOW-UP PHRASES
    # -------------------------------------------------

    swahili_phrases = {
        "ninawezaje",
        "nawezaje",
        "unawezaje",
        "tunawezaje",
        "mnawezaje",
        "nifanye nini",
        "nifanyeje",
        "ninawezaje kuzuia",
        "nawezaje kuzuia",
        "ninawezaje kurekebisha",
        "nawezaje kurekebisha",
        "kwa nini hilo",
        "kwa nini hiyo",
        "kwa nini hii",
        "sababu yake",
        "hilo lina",
        "hiyo ina",
        "hii ina",
        "inawezaje",
        "kuzuia hilo",
        "kurekebisha hilo"
    }

    for phrase in swahili_phrases:
        if phrase in text:
            return "sw"

    # -------------------------------------------------
    # SPECIAL FRENCH PHRASES
    # -------------------------------------------------

    french_phrases = {
        "comment puis-je",
        "comment puis je",
        "que dois-je faire",
        "que dois je faire",
        "comment éviter cela",
        "comment éviter ça",
        "pourquoi cela",
        "pourquoi ça"
    }

    for phrase in french_phrases:
        if phrase in text:
            return "fr"

    # -------------------------------------------------
    # WORD SCORING
    # -------------------------------------------------

    words = set(text.split())

    english_score = len(
        words.intersection(ENGLISH_WORDS)
    )

    swahili_score = len(
        words.intersection(SWAHILI_WORDS)
    )

    french_score = len(
        words.intersection(FRENCH_WORDS)
    )

    # -------------------------------------------------
    # TECHNICAL ALIAS DETECTION
    # -------------------------------------------------

    for word in words:
        if word in SWAHILI_TECHNICAL_ALIASES:
            swahili_score += 2

    # -------------------------------------------------
    # SWAHILI PATTERN DETECTION
    # -------------------------------------------------

    swahili_patterns = [
        "nina",
        "naweza",
        "nawez",
        "unawez",
        "tunawez",
        "mnawez",
        "ku",
        "kwa",
        "hilo",
        "hiyo",
        "hii",
        "hizi",
        "hizo",
        "kuzuia",
        "kurekebisha",
        "kuepuka",
        "nifanye",
        "mota",
        "presha",
        "haidro"
    ]

    for pattern in swahili_patterns:
        if pattern in text:
            swahili_score += 1

    # -------------------------------------------------
    # FRENCH PATTERN DETECTION
    # -------------------------------------------------

    french_patterns = [
        "comment",
        "pourquoi",
        "quell",
        "quelle",
        "quels",
        "défa",
        "répar",
        "éviter",
        "prévenir"
    ]

    for pattern in french_patterns:
        if pattern in text:
            french_score += 1

    # -------------------------------------------------
    # ENGLISH PATTERN DETECTION
    # -------------------------------------------------

    english_patterns = [
        "what ",
        "how ",
        "why ",
        "where ",
        "when ",
        "which ",
        "can i",
        "how can",
        "how do",
        "what causes",
        "how to",
        "function",
        "functions",
        "purpose of",
        "used for",
        "what is"
    ]

    for pattern in english_patterns:
        if pattern in text:
            english_score += 1

    # -------------------------------------------------
    # MIXED ENGLISH + KISWAHILI RULE
    # -------------------------------------------------

    # If the user mixes English and Kiswahili,
    # do NOT reject the question.
    #
    # English technical words such as:
    # function, causes, maintenance, failure, motor
    # can appear together with:
    # mota, nini, gani, ya, kwa, ni, etc.

    mixed_swahili_indicators = {
        "mota",
        "presha",
        "joto",
        "hilo",
        "hiyo",
        "hii",
        "nini",
        "gani",
        "ya",
        "kwa",
        "ni",
        "na",
        "kuzuia",
        "kurekebisha",
        "kufanya",
        "inafanya",
        "inatumika"
    }

    mixed_english_indicators = {
        "function",
        "functions",
        "purpose",
        "maintenance",
        "failure",
        "cause",
        "causes",
        "motor",
        "bearing",
        "pump",
        "hydraulic",
        "lubrication",
        "safety",
        "repair",
        "inspection",
        "pressure",
        "temperature",
        "vibration"
    }

    has_swahili_indicator = bool(
        words.intersection(
            mixed_swahili_indicators
        )
    )

    has_english_indicator = bool(
        words.intersection(
            mixed_english_indicators
        )
    )

    if (
        has_swahili_indicator
        and has_english_indicator
    ):
        # For mixed English + Kiswahili,
        # Kiswahili is preferred as response language.
        return "sw"

    # -------------------------------------------------
    # SPECIAL KISWAHILI FOLLOW-UP RULE
    # -------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "ninawezaje",
            "nawezaje",
            "kuzuia hilo",
            "kurekebisha hilo",
            "nifanye nini",
            "kwa nini hilo",
            "kwa nini hiyo",
            "hilo lina",
            "hiyo ina"
        ]
    ):
        return "sw"

    # -------------------------------------------------
    # SPECIAL FRENCH FOLLOW-UP RULE
    # -------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "comment éviter",
            "pourquoi cela",
            "pourquoi ça",
            "que dois je faire"
        ]
    ):
        return "fr"

    # -------------------------------------------------
    # FINAL SCORE
    # -------------------------------------------------

    scores = {
        "en": english_score,
        "sw": swahili_score,
        "fr": french_score
    }

    detected_language = max(
        scores,
        key=scores.get
    )

    if scores[detected_language] == 0:
        return "en"

    return detected_language