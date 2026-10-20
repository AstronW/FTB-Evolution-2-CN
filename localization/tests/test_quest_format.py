import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import quest_translation as q


class QuestFormatTests(unittest.TestCase):
    def test_reported_title_rejected_at_build_seam(self):
        source = "&fWelcome to &eIron's Gems \\&\\ Jewelry&r!"
        broken = "&f欢迎使用&eIron's Gems & Jewelry&r!"
        with self.assertRaisesRegex(ValueError, 'invalid quest format'):
            q.translate({'title': source}, {'0': broken}, {})
        fixed = broken.replace(' & ', ' \\&\\ ')
        self.assertEqual(q.translate({'title': source}, {'0': fixed}, {})[0]['title'], fixed)

    def test_reset_before_punctuation_and_other_valid_codes(self):
        q.assert_quest_format({'text': ['&f欢迎&e模组&r!', '&z彩虹&r正文', '&#aAbBcC颜色', r'名称 \& 饰品']})

    def test_bad_codes_rejected(self):
        for text in ('名称 & 饰品', '结尾&', '&x错误', '&#12345', '&#gggggg'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                q.assert_quest_format({'description': [text]})

    def test_json_component_literal_ampersands_are_valid(self):
        q.assert_quest_format({'title': json.dumps(['名称', {'text': ' & 饰品'}])})

    def test_generated_quest_corpus(self):
        for path in q.TARGET.rglob('*.json5'):
            with self.subTest(path=path):
                q.assert_quest_format(q.load_source(path))


if __name__ == '__main__':
    unittest.main()
