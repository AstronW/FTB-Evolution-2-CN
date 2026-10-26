import hashlib
import io
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import zipfile
from source_archive import read_resource


class SourceArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.mods = Path(self.temp.name)
        self.member = 'assets/example/lang/en_us.json'
        self.raw = b'{"title":"Example"}'
        self.sha = hashlib.sha256(self.raw).hexdigest()

    def write(self, name, value, nested=False):
        path = self.mods / name
        with zipfile.ZipFile(path, 'w') as archive:
            if nested:
                buffer = io.BytesIO()
                with zipfile.ZipFile(buffer, 'w') as inner:
                    inner.writestr(self.member, value)
                archive.writestr('META-INF/jarjar/example-v2.jar', buffer.getvalue())
            else:
                archive.writestr(self.member, value)
            archive.writestr('unrelated.txt', name)
        return path

    def test_renamed_jar_and_unrelated_changes_keep_reviewed_resource(self):
        old = self.mods / 'example-v1.jar'
        self.write('example-v2.jar', self.raw)
        raw, evidence = read_resource(self.member, old, self.sha, self.mods)
        self.assertEqual(raw, self.raw)
        self.assertTrue(evidence['jar'].endswith('example-v2.jar'))
        self.assertEqual(evidence['resource_sha256'], self.sha)

    def test_nested_version_rename_preserves_outer_and_inner_evidence(self):
        self.write('example-v2.jar', self.raw, nested=True)
        raw, evidence = read_resource(self.member, expected_sha256=self.sha, mods=self.mods)
        self.assertEqual(raw, self.raw)
        self.assertEqual(len(evidence['nested_jars']), 1)
        self.assertEqual(len(evidence['jar_sha256']), 64)

    def test_changed_english_requires_review(self):
        self.write('example-v2.jar', b'{"title":"New meaning"}')
        with self.assertRaisesRegex(ValueError, 'source content changed'):
            read_resource(self.member, expected_sha256=self.sha, mods=self.mods)

    def test_missing_and_duplicate_provider_are_not_silently_accepted(self):
        with self.assertRaisesRegex(ValueError, 'found 0'):
            read_resource(self.member, mods=self.mods)
        self.write('example-v1.jar', self.raw)
        self.write('example-v2.jar', self.raw)
        with self.assertRaisesRegex(ValueError, 'found 2'):
            read_resource(self.member, mods=self.mods)

    def test_mod_identity_disambiguates_same_resource_from_other_mod(self):
        wanted = self.write('example-v2.jar', self.raw)
        other = self.write('integration.jar', b'{"title":"Other mod override"}')
        for path, mod_id in [(wanted, 'example'), (other, 'integration')]:
            with zipfile.ZipFile(path, 'a') as archive:
                archive.writestr('META-INF/neoforge.mods.toml',
                                 '[[mods]]\nmodId = "' + mod_id + '"\n')
        raw, evidence = read_resource(self.member, self.mods / 'example-v1.jar',
                                      self.sha, self.mods, mod_id='example')
        self.assertEqual(raw, self.raw)
        self.assertEqual(evidence['mod_ids'], ['example'])

    def test_stale_archive_outside_current_mods_cannot_mask_missing_source(self):
        stale = self.write('example-v1.jar', self.raw)
        outside = self.mods.parent / (self.mods.name + '-stale.jar')
        stale.rename(outside)
        self.addCleanup(outside.unlink)
        with self.assertRaisesRegex(ValueError, 'found 0'):
            read_resource(self.member, outside, self.sha, self.mods)

    def test_preferred_old_version_cannot_hide_duplicate_mod_identity(self):
        old = self.write('example-v1.jar', self.raw)
        new = self.write('example-v2.jar', b'{"title":"Changed English"}')
        for path in [old, new]:
            with zipfile.ZipFile(path, 'a') as archive:
                archive.writestr('META-INF/neoforge.mods.toml', '[[mods]]\nmodId = "example"\n')
        with self.assertRaisesRegex(ValueError, 'found 2'):
            read_resource(self.member, old, self.sha, self.mods, mod_id='example')

    def test_unrelated_outer_update_keeps_nested_resource_binding(self):
        path = self.write('wrapper-v1.jar', self.raw, nested=True)
        with zipfile.ZipFile(path, 'a') as archive:
            archive.writestr('META-INF/neoforge.mods.toml', '[[mods]]\nmodId = "wrapper"\n')
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        with zipfile.ZipFile(path, 'a') as archive:
            archive.writestr('unrelated.class', b'new code')
        raw, evidence = read_resource(self.member, path, self.sha, self.mods, mod_id='wrapper')
        self.assertEqual(raw, self.raw)
        self.assertNotEqual(before, evidence['jar_sha256'])
        self.assertEqual(len(evidence['nested_jars']), 1)
