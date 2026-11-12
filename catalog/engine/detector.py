#!/usr/bin/env python3
"""
txt-humanizer Deterministic Language & Variety Detector
Zero external dependencies. Runtime < 20ms.
Supports: DE, EN, FR, ES, IT, PT, VI.
"""
import re
import time
import unicodedata
from functools import lru_cache
from typing import Dict, Any, Iterable, List

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

STOPWORDS_FR = {
    "le", "la", "les", "de", "des", "du", "un", "une", "et", "est", "en", "que",
    "qui", "dans", "pour", "pas", "sur", "ce", "il", "sont", "avec", "nous", "vous", "au", "par"
}

STOPWORDS_ES = {
    "el", "la", "los", "las", "de", "del", "un", "una", "unos", "unas", "y", "en",
    "es", "por", "para", "con", "que", "su", "al", "como", "más", "pero", "este", "esta", "son"
}

STOPWORDS_IT = {
    "il", "lo", "la", "i", "gli", "le", "di", "del", "della", "dei", "un", "uno",
    "una", "e", "è", "in", "per", "con", "su", "che", "non", "si", "sono", "questo", "come"
}

STOPWORDS_PT = {
    "o", "a", "os", "as", "de", "do", "da", "dos", "das", "um", "uma", "uns", "umas",
    "e", "é", "em", "no", "na", "nos", "nas", "por", "para", "com", "que", "não", "se", "como"
}

STOPWORDS_VI = {
    "và", "của", "là", "có", "được", "trong", "một", "cho", "người", "với", "các",
    "những", "này", "đã", "để", "không", "khi", "tại", "từ", "nhiều", "về", "như", "thì"
}

# Regional lexical anchors & variety dictionaries
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

# French variety indicators
QUEBECOIS = {"magasiner", "courriel", "char", "divan", "chicane", "stationnement", "breuvage", "fin de semaine"}
DIALECT_MARKERS_FR = {
    "verlan": ["meuf", "keuf", "zarbi", "ouf", "reuch", "chelou", "relou"],
    "argot": ["bouquin", "fringues", "boulot", "môme", "gosse", "thune", "kiffer"]
}

# Spanish variety indicators
ARGENTINE = {"pileta", "remera", "laburo", "colectivo", "frutilla", "che", "pibe", "morfi", "guita", "tenés", "podés"}
MEXICAN = {"platicar", "computadora", "chamarra", "alberca", "chido", "chamba", "neta", "güey", "orale"}
DIALECT_MARKERS_ES = {
    "lunfardo": ["che", "pibe", "morfi", "guita", "mina", "quilombo", "chabón"],
    "mexicano": ["chido", "chamba", "neta", "güey", "padre", "orale"]
}

# Italian dialect markers
DIALECT_MARKERS_IT = {
    "romanesco": ["daje", "annamo", "stamo", "ao", "namo", "piagne", "famo"],
    "napoletano": ["uè", "guagliò", "comm'a", "chillu", "chillo", "maronn'"]
}

# Portuguese variety indicators
PT_BR_INDICATORS = {"celular", "ônibus", "trem", "equipe", "esporte", "tela", "oxente", "vixe", "mermão"}
PT_PT_INDICATORS = {"telemóvel", "autocarro", "comboio", "equipa", "desporto", "ecrã"}
DIALECT_MARKERS_PT = {
    "nordestino": ["oxente", "vixe", "arretado", "mainha", "painho"],
    "carioca": ["mermão", "ko", "parça", "sinistro"]
}

# Vietnamese variety & dialect indicators
VI_CENTRAL_INDICATORS = {"mô", "tê", "răng", "rứa", "chi", "nỏ", "nhút", "chộ", "đọi", "trốc", "cấy"}
VI_SOUTH_INDICATORS = {"ly", "máy lạnh", "heo", "bắp", "xe hơi", "bự", "xài", "quẹo", "nghen", "hen", "hổng", "mần", "xỉn", "xạo"}
DIALECT_MARKERS_VI = {
    "nghe_tinh": ["mô", "tê", "răng", "rứa", "nỏ", "nhút", "chộ"],
    "nam_bo": ["nghen", "hen", "nè", "hổng", "mần", "xỉn", "xạo", "rảnh", "hết sảy"]
}


def normalize_text(text: str) -> str:
    """Normalize input text to Unicode NFC form."""
    return unicodedata.normalize("NFC", text)


@lru_cache(maxsize=512)
def compile_phrase_pattern(phrase: str) -> re.Pattern:
    """Compile a case-insensitive regex with Unicode word boundaries for a word or phrase."""
    tokens = normalize_text(phrase).strip().split()
    if not tokens:
        return re.compile(r"(?!)")
    body = r"\s+".join(re.escape(token) for token in tokens)
    return re.compile(rf"(?<!\w){body}(?!\w)", re.IGNORECASE | re.UNICODE)


def find_phrase_matches(text: str, phrase: str) -> List[re.Match]:
    """Return all boundary-aware matches of `phrase` in NFC-normalized `text`."""
    if not text or not phrase or not phrase.strip():
        return []
    return list(compile_phrase_pattern(phrase).finditer(normalize_text(text)))


def _matched_markers(text: str, markers: Iterable[str]) -> List[str]:
    """Return markers from `markers` that match NFC-normalized `text` at word boundaries."""
    normalized = normalize_text(text)
    return [marker for marker in markers if compile_phrase_pattern(marker).search(normalized)]


def _collect_dialect_signals(
    text: str,
    marker_groups: Dict[str, List[str]],
    signal_type: str = "dialect",
) -> List[Dict[str, Any]]:
    """Collect matched dialect or colloquial marker signals for a language."""
    signals: List[Dict[str, Any]] = []
    for dial_name, markers in marker_groups.items():
        found_markers = _matched_markers(text, markers)
        if found_markers:
            signals.append({"type": signal_type, "name": dial_name, "evidence": found_markers})
    return signals


def tokenize_words(text: str) -> List[str]:
    normalized = normalize_text(text)
    return [w.lower() for w in re.findall(r"\b[\w\-]+\b", normalized, re.UNICODE)]


def detect_language(text: str) -> Dict[str, Any]:
    t0 = time.perf_counter()
    text = normalize_text(text)
    words = tokenize_words(text)
    total_words = len(words)
    if total_words == 0:
        return {"language": "unknown", "confidence": "none", "elapsed_ms": 0.0}

    # Stopword counting
    scores = {
        "de": sum(1 for w in words if w in STOPWORDS_DE),
        "en": sum(1 for w in words if w in STOPWORDS_EN),
        "fr": sum(1 for w in words if w in STOPWORDS_FR),
        "es": sum(1 for w in words if w in STOPWORDS_ES),
        "it": sum(1 for w in words if w in STOPWORDS_IT),
        "pt": sum(1 for w in words if w in STOPWORDS_PT),
        "vi": sum(1 for w in words if w in STOPWORDS_VI)
    }

    # Add character / diacritic hints
    if any(c in text for c in "äöüßÄÖÜ"):
        scores["de"] += 3
    if any(c in text for c in "àâéèêëîïôùûçœæ"):
        scores["fr"] += 2
    if any(c in text for c in "ñáéíóú¿¡"):
        scores["es"] += 2
    if any(c in text for c in "ãõêôáéíóúç"):
        scores["pt"] += 2
    if any(c in text for c in "àèéìíîòóùú"):
        scores["it"] += 1
    if any(c in text for c in "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"):
        scores["vi"] += 5

    # Check dialect hints
    dialect_score_groups = (
        ("de", DIALECT_MARKERS_DE, 3),
        ("fr", DIALECT_MARKERS_FR, 3),
        ("es", DIALECT_MARKERS_ES, 3),
        ("it", DIALECT_MARKERS_IT, 3),
        ("pt", DIALECT_MARKERS_PT, 3),
        ("vi", DIALECT_MARKERS_VI, 4),
    )
    for lang_code, marker_groups, weight in dialect_score_groups:
        for markers in marker_groups.values():
            if _matched_markers(text, markers):
                scores[lang_code] += weight

    primary_lang = max(scores, key=scores.get)
    max_score = scores[primary_lang]
    conf = "high" if max_score >= 3 else ("medium" if max_score >= 1 else "low")

    variety = "standard"
    variety_details = {}
    human_signals = []

    # Variety detection for German
    if primary_lang == "de":
        has_eszett = "ß" in text
        helv_found = [w for w in words if w in HELVETISMS]
        aust_found = [w for w in words if w in AUSTRICISMS]
        human_signals.extend(_collect_dialect_signals(text, DIALECT_MARKERS_DE))

        if not has_eszett and (helv_found or "«" in text or "»" in text):
            variety = "de-CH"
            variety_details = {"name": "Schweizer Hochdeutsch", "evidence": helv_found}
        elif aust_found or "heuer" in words:
            variety = "de-AT"
            variety_details = {"name": "Österreichisches Deutsch", "evidence": aust_found}
        else:
            variety = "de-DE"
            variety_details = {"name": "Bundesdeutsch"}

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
            variety_details = {"name": "British English", "evidence": gb_found}
        else:
            variety = "en-US"
            variety_details = {"name": "American English", "evidence": us_found}

    # Variety detection for French
    elif primary_lang == "fr":
        qc_found = _matched_markers(text, sorted(QUEBECOIS))
        human_signals.extend(_collect_dialect_signals(text, DIALECT_MARKERS_FR, signal_type="colloquial_marker"))

        if qc_found:
            variety = "fr-CA"
            variety_details = {"name": "Français canadien / québécois", "evidence": qc_found}
        else:
            variety = "fr-FR"
            variety_details = {"name": "Français métropolitain"}

    # Variety detection for Spanish
    elif primary_lang == "es":
        ar_found = [w for w in words if w in ARGENTINE]
        mx_found = [w for w in words if w in MEXICAN]
        human_signals.extend(_collect_dialect_signals(text, DIALECT_MARKERS_ES))

        if ar_found:
            variety = "es-AR"
            variety_details = {"name": "Español rioplatense", "evidence": ar_found}
        elif mx_found:
            variety = "es-MX"
            variety_details = {"name": "Español mexicano", "evidence": mx_found}
        else:
            variety = "es-ES"
            variety_details = {"name": "Español peninsular"}

    # Variety detection for Italian
    elif primary_lang == "it":
        variety = "it-IT"
        variety_details = {"name": "Italiano standard"}
        human_signals.extend(_collect_dialect_signals(text, DIALECT_MARKERS_IT))

    # Variety detection for Portuguese
    elif primary_lang == "pt":
        br_found = [w for w in words if w in PT_BR_INDICATORS]
        pt_found = [w for w in words if w in PT_PT_INDICATORS]
        human_signals.extend(_collect_dialect_signals(text, DIALECT_MARKERS_PT))

        if br_found:
            variety = "pt-BR"
            variety_details = {"name": "Português brasileiro", "evidence": br_found}
        elif pt_found:
            variety = "pt-PT"
            variety_details = {"name": "Português europeu", "evidence": pt_found}
        else:
            variety = "pt-BR"
            variety_details = {"name": "Português padrão"}

    # Variety detection for Vietnamese
    elif primary_lang == "vi":
        central_found = _matched_markers(text, sorted(VI_CENTRAL_INDICATORS))
        south_found = _matched_markers(text, sorted(VI_SOUTH_INDICATORS))
        human_signals.extend(_collect_dialect_signals(text, DIALECT_MARKERS_VI))

        if central_found:
            variety = "vi-Central"
            variety_details = {"name": "Tiếng Việt miền Trung (Nghệ Tĩnh / Huế)", "evidence": central_found}
        elif south_found:
            variety = "vi-South"
            variety_details = {"name": "Tiếng Việt miền Nam (Sài Gòn / Mekong)", "evidence": south_found}
        else:
            variety = "vi-North"
            variety_details = {"name": "Tiếng Việt miền Bắc (Hà Nội chuẩn)"}

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
