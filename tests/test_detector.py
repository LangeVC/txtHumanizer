#!/usr/bin/env python3
"""
Unit tests for txt-humanizer Detector Engine
"""
import sys
import os

# Add parent path to import detector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from catalog.engine.detector import detect_language


def test_german_standard():
    text = "Künstliche Intelligenz ist ein zentrales Werkzeug für die Analyse von großen Datenmengen in Unternehmen."
    res = detect_language(text)
    assert res["language"] == "de", f"Expected de, got {res['language']}"
    assert res["variety"] == "de-DE", f"Expected de-DE, got {res['variety']}"
    assert res["elapsed_ms"] < 50.0, f"Too slow: {res['elapsed_ms']}ms"


def test_swiss_german():
    text = "Wir parkieren das Velo beim Spital und besprechen das naechste Traktandum ohne Verzug."
    res = detect_language(text)
    assert res["language"] == "de"
    assert res["variety"] == "de-CH", f"Expected de-CH, got {res['variety']}"
    assert "parkieren" in res["variety_details"]["evidence"]


def test_austrian_german():
    text = "Im Jänner essen wir gerne frischen Topfen und Paradeiser auf der Stiege."
    res = detect_language(text)
    assert res["language"] == "de"
    assert res["variety"] == "de-AT", f"Expected de-AT, got {res['variety']}"
    assert "jänner" in res["variety_details"]["evidence"]


def test_bavarian_dialect_signal():
    text = "Dahoam is dahoam und i schaugn ma des bisserl spaeter o, servus!"
    res = detect_language(text)
    assert res["language"] == "de"
    dialects = [s["name"] for s in res["human_signals"] if s["type"] == "dialect"]
    assert "bairisch" in dialects, f"Expected bairisch signal, got {dialects}"


def test_english_us():
    text = "The organization will analyze the color palette and center the text accordingly."
    res = detect_language(text)
    assert res["language"] == "en", f"Expected en, got {res['language']}"
    assert res["variety"] == "en-US", f"Expected en-US, got {res['variety']}"


def test_english_gb():
    text = "The committee will organise the programme to analyse the colour of the theatre."
    res = detect_language(text)
    assert res["language"] == "en"
    assert res["variety"] == "en-GB", f"Expected en-GB, got {res['variety']}"


def test_english_hybrid_style_bleed():
    text = "We will organise the colour scheme and center the text for maximum visual impact."
    res = detect_language(text)
    assert res["language"] == "en"
    assert res["variety"] == "en-hybrid", f"Expected en-hybrid, got {res['variety']}"
    assert "warning" in res["variety_details"]


def test_runtime_performance():
    sample = "This is a standard text designed to benchmark the detector engine latency across a hundred repetitions."
    res = detect_language(sample)
    assert res["elapsed_ms"] < 20.0, f"Detector exceeded 20ms: {res['elapsed_ms']}ms"


if __name__ == "__main__":
    tests = [
        test_german_standard,
        test_swiss_german,
        test_austrian_german,
        test_bavarian_dialect_signal,
        test_english_us,
        test_english_gb,
        test_english_hybrid_style_bleed,
        test_runtime_performance
    ]
    for t in tests:
        t()
        print(f"[PASS] {t.__name__}")
    print("\nALL DETECTOR TESTS PASSED SUCCESSFULLY!")
