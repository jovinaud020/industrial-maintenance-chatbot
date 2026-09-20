import re


# ============================================================
# INDUSTRIAL MAINTENANCE KEYWORDS
# ============================================================

MAINTENANCE_KEYWORDS = {

    # --------------------------------------------------------
    # Bearings
    # --------------------------------------------------------

    "bearing",
    "bearings",
    "roulement",
    "roulements",

    # --------------------------------------------------------
    # Lubrication
    # --------------------------------------------------------

    "lubrication",
    "lubricant",
    "lubricants",
    "grease",
    "oil",
    "mafuta",
    "grisi",
    "lubrification",
    "lubrifiant",

    # --------------------------------------------------------
    # Motors
    # --------------------------------------------------------

    "motor",
    "motors",
    "moteur",
    "moteurs",
    "electric motor",

    # --------------------------------------------------------
    # Pumps
    # --------------------------------------------------------

    "pump",
    "pumps",
    "pompe",
    "pompes",

    # --------------------------------------------------------
    # Hydraulics
    # --------------------------------------------------------

    "hydraulic",
    "hydraulics",
    "hydraulic system",
    "hydraulique",
    "hydrauliques",
    "shinikizo",

    # --------------------------------------------------------
    # Maintenance
    # --------------------------------------------------------

    "maintenance",
    "matengenezo",
    "entretien",

    # --------------------------------------------------------
    # Failure / Damage
    # --------------------------------------------------------

    "failure",
    "failures",
    "fault",
    "damage",
    "wear",
    "failure mode",
    "failed",
    "kushindwa",
    "kuharibika",
    "uharibifu",
    "uchakavu",
    "défaillance",
    "dommage",
    "usure",

    # --------------------------------------------------------
    # Operating conditions
    # --------------------------------------------------------

    "temperature",
    "temperatures",
    "vibration",
    "vibrations",
    "pressure",
    "contamination",
    "alignment",
    "misalignment",
    "overload",
    "temperature",
    "joto",
    "mtetemo",
    "shinikizo",
    "uchafu",
    "alignment",
    "misalignment",

    # --------------------------------------------------------
    # Safety
    # --------------------------------------------------------

    "safety",
    "safe",
    "hazard",
    "hazards",
    "risk",
    "protection",
    "usalama",
    "hatari",
    "protection",
    "sécurité",
    "danger",
    "risque",
}


# ============================================================
# KEYWORD EXTRACTION
# ============================================================

def extract_keywords(text: str):

    text_lower = text.lower()

    found_keywords = set()

    # --------------------------------------------------------
    # Check multi-word keywords first
    # --------------------------------------------------------

    for keyword in MAINTENANCE_KEYWORDS:

        if " " in keyword:

            if keyword in text_lower:

                found_keywords.add(
                    keyword
                )

    # --------------------------------------------------------
    # Check single-word keywords
    # --------------------------------------------------------

    words = re.findall(
        r"\b[\wÀ-ÿ]+\b",
        text_lower
    )

    for word in words:

        if word in MAINTENANCE_KEYWORDS:

            found_keywords.add(
                word
            )

    return sorted(
        found_keywords
    )