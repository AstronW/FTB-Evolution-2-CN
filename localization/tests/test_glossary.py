import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import glossary as g


def entry(**fields):
    base = {'id': 'mod.term', 'en': 'Term', 'zh': '术语', 'namespaces': ['mod'],
            'source': 'test', 'status': 'approved'}
    base.update(fields)
    return base


class GlossaryTests(unittest.TestCase):
    def test_repository_glossary_is_valid(self):
        self.assertEqual(g.validate_schema(g.load_glossary()), [])

    def test_same_english_may_differ_across_namespaces(self):
        data = {'entries': [entry(id='a.spirit', en='Spirit Attuned', zh='魔灵同调', namespaces=['a']),
                            entry(id='b.spirit', en='Spirit Attuned', zh='灵魂调谐', namespaces=['b'])]}
        self.assertEqual(g.validate_schema(data), [])

    def test_conflict_inside_one_namespace_is_rejected(self):
        data = {'entries': [entry(id='a.one', zh='甲'), entry(id='a.two', zh='乙')]}
        self.assertTrue(any('conflicts' in error for error in g.validate_schema(data)))

    def test_bad_records_are_rejected(self):
        for bad in [entry(status='done'), entry(zh='术语，'), entry(id='Bad Id'),
                    entry(avoid=['术语']), entry(extra=1), entry(keep_english=True)]:
            with self.subTest(bad=bad):
                self.assertTrue(g.validate_schema({'entries': [bad]}))

    def test_avoid_ignores_canonical_and_allowed_uses(self):
        term = entry(zh='魔像', avoid=['傀儡'], allow=['铁傀儡'])
        self.assertEqual(g.find_avoided(term, '村民与铁傀儡'), [])
        self.assertEqual(g.find_avoided(term, '工坊傀儡'), ['傀儡'])

    def test_scope_matches_namespaces_and_quest_chapters(self):
        term = entry(namespaces=['integrated*'], quest_chapters=['integrated_dynamics'])
        self.assertTrue(g.in_scope(term, 'integratedterminals'))
        self.assertTrue(g.in_scope(term, 'quest:integrated_dynamics'))
        self.assertFalse(g.in_scope(term, 'quest:oritech'))
        self.assertFalse(g.in_scope(term, 'oritech'))
        self.assertTrue(g.in_scope(entry(namespaces=['*']), 'quest:oritech'))

    def test_key_namespace(self):
        self.assertEqual(g.key_namespace('item.auroral.shimmersteel_ingot'), 'auroral')
        self.assertEqual(g.key_namespace('replication.matteropedia'), 'replication')


if __name__ == '__main__':
    unittest.main()
