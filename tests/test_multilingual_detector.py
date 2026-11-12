import unittest
import unicodedata
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from catalog.engine.detector import (
    compile_phrase_pattern,
    detect_language,
    find_phrase_matches,
    normalize_text,
    tokenize_words,
)

class TestMultilingualDetector(unittest.TestCase):
    def test_french_metropolitan(self):
        text = "Il est important de souligner que nous analysons les données avec soin."
        res = detect_language(text)
        self.assertEqual(res["language"], "fr")
        self.assertEqual(res["variety"], "fr-FR")

    def test_french_canadian(self):
        text = "En fin de semaine, nous allons magasiner avec le char."
        res = detect_language(text)
        self.assertEqual(res["language"], "fr")
        self.assertEqual(res["variety"], "fr-CA")

    def test_spanish_peninsular(self):
        text = "Es fundamental destacar que el informe presentado contiene los datos."
        res = detect_language(text)
        self.assertEqual(res["language"], "es")
        self.assertEqual(res["variety"], "es-ES")

    def test_spanish_argentine_lunfardo(self):
        text = "Che, mirá qué quilombo con la guita para el laburo."
        res = detect_language(text)
        self.assertEqual(res["language"], "es")
        self.assertEqual(res["variety"], "es-AR")
        self.assertTrue(any(s["name"] == "lunfardo" for s in res["human_signals"]))

    def test_italian_standard_and_romanesco(self):
        text = "Daje, annamo a vedere il progetto che è fondamentale per noi."
        res = detect_language(text)
        self.assertEqual(res["language"], "it")
        self.assertTrue(any(s["name"] == "romanesco" for s in res["human_signals"]))

    def test_portuguese_brazil(self):
        text = "Peguei o celular no ônibus e mandei uma mensagem para a equipe."
        res = detect_language(text)
        self.assertEqual(res["language"], "pt")
        self.assertEqual(res["variety"], "pt-BR")

    def test_portuguese_portugal(self):
        text = "Utilizei o telemóvel no autocarro antes de apanhar o comboio."
        res = detect_language(text)
        self.assertEqual(res["language"], "pt")
        self.assertEqual(res["variety"], "pt-PT")

    def test_vietnamese_northern(self):
        text = "Đáng chú ý là báo cáo này phân tích các dữ liệu một cách cẩn thận."
        res = detect_language(text)
        self.assertEqual(res["language"], "vi")
        self.assertEqual(res["variety"], "vi-North")

    def test_vietnamese_central_dialect(self):
        text = "Mô, tê, răng, rứa chi nỏ có việc gì khó khăn hết."
        res = detect_language(text)
        self.assertEqual(res["language"], "vi")
        self.assertEqual(res["variety"], "vi-Central")
        self.assertTrue(any(s["name"] == "nghe_tinh" for s in res["human_signals"]))

    def test_vietnamese_southern_dialect(self):
        text = "Hổng sao đâu nghen, xài máy lạnh này đã đời lắm nè."
        res = detect_language(text)
        self.assertEqual(res["language"], "vi")
        self.assertEqual(res["variety"], "vi-South")
        self.assertTrue(any(s["name"] == "nam_bo" for s in res["human_signals"]))

    def test_vietnamese_nfd_normalization(self):
        nfc_text = "Hổng sao đâu nghen, xài máy lạnh này đã đời lắm nè."
        nfd_text = unicodedata.normalize("NFD", nfc_text)
        self.assertNotEqual(nfc_text, nfd_text)
        self.assertEqual(normalize_text(nfd_text), unicodedata.normalize("NFC", nfc_text))
        self.assertEqual(tokenize_words(nfd_text), tokenize_words(nfc_text))

        res = detect_language(nfd_text)
        self.assertEqual(res["language"], "vi")
        self.assertEqual(res["variety"], "vi-South")
        self.assertTrue(any(s["name"] == "nam_bo" for s in res["human_signals"]))
        self.assertIn("máy lạnh", res["variety_details"]["evidence"])

    def test_vietnamese_syllable_boundary_safety(self):
        text = "Sinh viên học môn học này và mài giũa tên tuổi của mình, không phải nghend."
        res = detect_language(text)
        self.assertEqual(res["language"], "vi")
        self.assertEqual(res["variety"], "vi-North")
        self.assertEqual(res["human_signals"], [])

        self.assertEqual(find_phrase_matches("môn học", "mô"), [])
        self.assertEqual(find_phrase_matches("mài giũa", "mà"), [])
        self.assertEqual(find_phrase_matches("tên tuổi", "tê"), [])
        self.assertEqual(find_phrase_matches("nghend", "nghen"), [])
        self.assertEqual(len(find_phrase_matches("Mô đó?", "mô")), 1)

    def test_multiword_compound_indicators(self):
        vi_text = "Hôm nay gia đình tôi đi xe   hơi có máy lạnh rất mát."
        vi_res = detect_language(vi_text)
        self.assertEqual(vi_res["language"], "vi")
        self.assertEqual(vi_res["variety"], "vi-South")
        self.assertIn("xe hơi", vi_res["variety_details"]["evidence"])
        self.assertIn("máy lạnh", vi_res["variety_details"]["evidence"])

        nfd_compound = unicodedata.normalize("NFD", "xe hơi và máy   lạnh")
        self.assertEqual(len(find_phrase_matches(nfd_compound, "xe hơi")), 1)
        self.assertEqual(len(find_phrase_matches(nfd_compound, "máy lạnh")), 1)
        self.assertTrue(
            compile_phrase_pattern("đóng vai trò quan trọng").search(
                "Yếu tố này đóng  vai   trò quan trọng trong báo cáo."
            )
        )

        fr_text = "En fin de semaine, nous allons visiter le musée avec les amis."
        fr_res = detect_language(fr_text)
        self.assertEqual(fr_res["language"], "fr")
        self.assertEqual(fr_res["variety"], "fr-CA")
        self.assertIn("fin de semaine", fr_res["variety_details"]["evidence"])

if __name__ == "__main__":
    unittest.main()
