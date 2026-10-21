import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from catalog.engine.detector import detect_language

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

if __name__ == "__main__":
    unittest.main()
