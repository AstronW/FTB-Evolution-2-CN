import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import quest_translation as q

class ProtectedTextTests(unittest.TestCase):
    def test_changes_are_rejected(self):
        for source, target in [
            ('earth>10 !earth *metallic', 'earth<10 earth metallic'),
            ('Value %1$08.2f %% %n %<s', '数值 %1$08.3f %% %n %<s'),
            ('$(l:guide/page)Link$(/l) ${player} {0}', '$(l:guide/other)链接$(/l) ${name} {1}'),
            ('&zText&r', '文字&r'),
            ('#forge:ingots/*', '#forge:ingots/iron'),
            ('Use {}', '使用'),
            ('[Foci](entry://anima:codex/components/soul_focus)', '法器'),
            ('$(l:shapes/zone)zones.', '$(l:shapes/zone)区域$().'),
        ]:
            with self.subTest(source=source):
                with self.assertRaises(ValueError):
                    q.translate({'text': source}, {'0': target}, {})

    def test_valid_localization_forms(self):
        for source,target in [
            ('Applied %s from %s', '已应用%1$s来自%2$s'),
            ('35% of damage, 25%, 35% and 15%', '35%伤害,25%,35%和15%'),
            ('**Important:** tools &amp; armor', '**重要:**工具&amp;护甲'),
            ('&ey 60&r', '&ey=60&r'),
            ('&cBad Omen&r;', '&c不祥之兆&r.'),
        ]:
            self.assertEqual(q.signature(source,quest=True),q.signature(target,quest=True))

    def test_prose_and_tokens(self):
        source = 'Find earth>10, !earth and *metallic; %s $(br) ${player} {0} &zHi&r'
        target = '查找 earth>10, !earth 和 *metallic; %s $(br) ${player} {0} &z你好&r'
        self.assertFalse(q.translate({'text': source}, {'0': target}, {})[1])

if __name__ == '__main__':
    unittest.main()
