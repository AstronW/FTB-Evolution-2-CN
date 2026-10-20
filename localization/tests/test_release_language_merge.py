import json
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import release_pack as release

class ReleaseLanguageMerge(unittest.TestCase):
    def test_manual_language_keys_survive_consolidation(self):
        outputs, _, _ = release.assemble_resourcepack([])
        for path in release.MANUALS_PACK.glob('assets/*/lang/zh_cn.json'):
            member = path.relative_to(release.MANUALS_PACK).as_posix()
            merged = json.loads(outputs[member][0])
            for key, value in json.loads(path.read_text()).items():
                self.assertTrue(key in merged, (member, key))
                self.assertEqual(value, merged[key], (member, key))

if __name__ == '__main__':
    unittest.main()
