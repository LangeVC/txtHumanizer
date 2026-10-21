#!/usr/bin/env python3
"""
txt-humanizer Deterministic Language & Variety Detector
Zero external dependencies. Runtime < 20ms.
"""
import re
import time
from typing import Dict, Any, List

# Core stopwords for primary language detection
STOPWORDS_DE = {
    "und", "der", "die", "das", "in", "ist", "von", "mit", "den", "auf", "für",
    "eine", "einer", "einem", "einen", "nicht", "sich", "dem", "dass", "auch",
    "es", "an", "als", "zu", "nach", "wie", "im", "aus", "bei", "um", "aber"
}

STOPWORDS_EN = {
    "the", "and", "is", "in", "it", "you", "that", "he", "was", "for", "on", "are",
    "as", "with", "his", "they", "at", "be", "this", "have", "from", "or", "one",
    "had", "by", "word", "but", "not", "what", "all", "were", "we", "when", "your"
}

# Regional lexical anchors
HELVETISMS = {
    "parkieren", "grillieren", "velo", "billett", "natel", "trottoir", "spital",
    "traktandum", "traktanden", "estrich", "postcheck", "matur"
}

AUSTRICISMS = {
    "jänner", "feber", "topfen", "stiege", "paradeiser", "erdapfel", "obers",
    "kukuruz", "marille", "karfiol", "beiried", "spitalreif", "matura", "semmel",
    "kren", "fisolen", "heuer"
}

DIALECT_MARKERS_DE = {
    "bairisch": ["ned", "nedda", "dahoam", "schaugn", "bisserl", "servus", "griasdi", "ois"],
    "alemannisch": ["luaga", "schdimmd", "mädle", "schee"],
    "ripuarisch": ["nit", "wat", "dat", "joot", "verzälle", "fastelovend", "alaaf"],
    "niederdeutsch": ["moin", "snacken", "lütt", "tüddelkram"]
}

US_INDICATORS = {
    "color", "flavor", "honor", "labor", "neighbor", "organize", "realize", "analyze",
    "center", "theater", "traveled", "canceled"
}

GB_INDICATORS = {
    "colour", "flavour", "honour", "labour", "neighbour", "organise", "realise", "analyse",
    "centre", "theatre", "travelled", "cancelled"
}


def tokenize_words(text: str) -> List[str]:
    return [w.lower() for w in re.findall(r"\b[\w\-]+\b", text, re.UNICODE)]


def detect_language(text: str) -> Dict[str, Any]:
    t0 = time.perf_counter()
    words = tokenize_words(text)
    total_words = len(words)
    if total_words == 0:
        return {"language": "unknown", "confidence": "none", "elapsed_ms": 0.0}

    de_hits = sum(1 for w in words if w in STOPWORDS_DE)
    en_hits = sum(1 for w in words if w in STOPWORDS_EN)

    # Check for dialect markers before resolving primary language tie
    has_de_dialect = any(
        any(re.search(r"\b" + re.escape(m) + r"\b", text, re.I) for m in markers)
        for markers in DIALECT_MARKERS_DE.values()
    )
    if has_de_dialect:
        de_hits += 5

    # Primary language resolution
    if de_hits > en_hits:
        primary_lang = "de"
        conf = "high" if de_hits >= 3 else "medium"
    elif en_hits > de_hits:
        primary_lang = "en"
        conf = "high" if en_hits >= 3 else "medium"
    else:
        # Check specific character clues
        if any(c in text for c in "äöüßÄÖÜ"):
            primary_lang = "de"
            conf = "medium"
        else:
            primary_lang = "en"
            conf = "low"

    variety = "standard"
    variety_details = {}
    human_signals = []

    # Variety detection for German
    if primary_lang == "de":
        has_eszett = "ß" in text
        helv_found = [w for w in words if w in HELVETISMS]
        aust_found = [w for w in words if w in AUSTRICISMS]

        # Dialect scanning
        for dial_name, markers in DIALECT_MARKERS_DE.items():
            found_markers = [m for m in markers if re.search(r"\b" + re.escape(m) + r"\b", text, re.I)]
            if found_markers:
                human_signals.append({
                    "type": "dialect",
                    "name": dial_name,
                    "evidence": found_markers,
                    "confidence": "high" if len(found_markers) >= 2 else "medium"
                })

        if not has_eszett and (helv_found or "«" in text or "»" in text):
            variety = "de-CH"
            variety_details = {
                "name": "Schweizer Hochdeutsch",
                "evidence": helv_found,
                "uses_eszett": False
            }
        elif aust_found or "heuer" in words:
            variety = "de-AT"
            variety_details = {
                "name": "Österreichisches Deutsch",
                "evidence": aust_found,
                "uses_eszett": has_eszett
            }
        else:
            variety = "de-DE"
            variety_details = {
                "name": "Bundesdeutsch",
                "uses_eszett": has_eszett
            }

    # Variety detection for English
    elif primary_lang == "en":
        us_found = [w for w in words if w in US_INDICATORS]
        gb_found = [w for w in words if w in GB_INDICATORS]

        if us_found and gb_found:
            variety = "en-hybrid"
            variety_details = {
                "name": "Hybrid Style Bleed",
                "us_evidence": us_found,
                "gb_evidence": gb_found,
                "warning": "Inconsistent mix of American and British conventions (strong AI tell)"
            }
        elif gb_found:
            variety = "en-GB"
            variety_details = {
                "name": "British English",
                "evidence": gb_found
            }
        elif us_found:
            variety = "en-US"
            variety_details = {
                "name": "American English",
                "evidence": us_found
            }
        else:
            variety = "en-US" # Default international English baseline
            variety_details = {
                "name": "Standard English (Baseline)",
                "evidence": []
            }

    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    return {
        "language": primary_lang,
        "variety": variety,
        "variety_details": variety_details,
        "confidence": conf,
        "human_signals": human_signals,
        "elapsed_ms": round(elapsed_ms, 2)
    }


if __name__ == "__main__":
    import sys
    sample = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Wir parkieren das Velo beim Spital und essen dann ein feines Zmorge."
    res = detect_language(sample)
    print(res)
