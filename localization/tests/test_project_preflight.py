import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


class ProjectPreflightTests(unittest.TestCase):
    def test_version_change_reports_once_without_running_stale_batch_checks(self):
        project_path = Path(__file__).resolve().parents[2] / 'project.py'
        spec = importlib.util.spec_from_file_location('project_preflight_test', project_path)
        project = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(project)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            game = root / 'game'
            game.mkdir()
            (game / 'instance.json').write_text(json.dumps({'version': '1.6.0'}))
            (root / 'project.json').write_text(json.dumps({'target_pack_version': '1.5.1', 'target_instance': str(game)}))
            with patch.object(project, 'ROOT', root), patch.object(project.sys, 'argv', ['project.py', 'check']), patch.object(project.subprocess, 'run') as run:
                with self.assertRaises(SystemExit) as error:
                    project.main()
                self.assertEqual(error.exception.code, 2)
                run.assert_not_called()
            report = json.loads((root / 'localization/reports/project-verification-1.6.0.json').read_text())
            self.assertEqual(report['status'], 'needs_source_review')
            self.assertEqual(report['checks'], [])

    def test_batch_failures_are_reported_independently_in_shared_process(self):
        from types import SimpleNamespace
        project_path = Path(__file__).resolve().parents[2] / 'project.py'
        spec = importlib.util.spec_from_file_location('project_batch_test', project_path)
        project = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(project)
        calls = []
        def process(folder, build):
            calls.append((folder.name, build))
            if folder.name == 'batch-bad':
                raise ValueError('English source changed')
            return {'status': 'passed'}
        with patch.dict(project.sys.modules, {'ordinary_translation': SimpleNamespace(process=process)}):
            bad = project.execute_check(['python', 'localization/ordinary_translation.py', 'batch-bad'])
            good = project.execute_check(['python', 'localization/ordinary_translation.py', 'batch-good'])
        self.assertEqual(bad.returncode, 1)
        self.assertIn('English source changed', bad.stderr)
        self.assertEqual(good.returncode, 0)
        self.assertEqual(calls, [('batch-bad', False), ('batch-good', False)])
