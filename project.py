"""Run translation checks from this independent project directory."""
from pathlib import Path
import json
import subprocess
import sys
import traceback

ROOT = Path(__file__).resolve().parent

def execute_check(command):
    """Keep ordinary batches independent while sharing the read-only JAR index."""
    if len(command) == 3 and command[1] == 'localization/ordinary_translation.py':
        sys.path.insert(0, str(ROOT / 'localization'))
        import ordinary_translation
        try:
            report = ordinary_translation.process(ROOT / 'localization/ordinary' / command[2], False)
            return subprocess.CompletedProcess(command, 0, json.dumps(report, ensure_ascii=False) + '\n', '')
        except Exception:
            return subprocess.CompletedProcess(command, 1, '', traceback.format_exc())
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {'info', 'check'}:
        raise SystemExit('Usage: python project.py info|check')
    if sys.argv[1] == 'info':
        print((ROOT / 'project.json').read_text())
        return
    config = json.loads((ROOT / 'project.json').read_text())
    instance_path = Path(config['target_instance']) / 'instance.json'
    if instance_path.is_file():
        actual = json.loads(instance_path.read_text())['version']
        if actual != config['target_pack_version']:
            report = {'status': 'needs_source_review', 'configured_baseline': config['target_pack_version'],
                      'actual_pack_version': actual, 'checks': [], 'in_game_tested': False,
                      'reason': 'Pack version changed; audit and reconcile source inputs before checking translations.'}
            output = ROOT / f'localization/reports/project-verification-{actual}.json'
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
            print(f"Instance updated: {config['target_pack_version']} -> {actual}. "
                  'Run python localization/assess_pack_update.py and review the source deltas first. '
                  'Translation checks were not run against stale inputs.')
            raise SystemExit(2)
    commands = [
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'localization/tests'],
        [sys.executable, 'localization/glossary.py', 'check'],
        [sys.executable, 'localization/audit_item_names.py'],
        [sys.executable, 'localization/quest_translation.py', 'check'],
        [sys.executable, 'localization/verify_quests.py'],
        [sys.executable, 'localization/feedback_fixes.py', 'check'],
        [sys.executable, 'localization/verify_feedback_native.py'],
        [sys.executable, 'localization/audit_guideme_recipes.py'],
        [sys.executable, 'localization/manual_translation.py', 'check'],
        [sys.executable, 'localization/verify_manuals.py'],
        [sys.executable, 'localization/custom_translation.py', '--check'],
        [sys.executable, 'localization/custom_batches.py'],
        ['node', 'localization/custom/verify_runtime.cjs'],
        ['node', 'localization/client_fixes/verify_runtime.cjs'],
        [sys.executable, 'localization/client_fixes/verify_sources.py'],
        [sys.executable, 'localization/verify_ordinary_rebind.py'],
    ]
    unfinished = []
    for folder in sorted((ROOT / 'localization/ordinary').glob('batch-*')):
        if (folder / 'verification.json').exists():
            commands.append([sys.executable, 'localization/ordinary_translation.py', folder.name])
        else:
            unfinished.append(folder.name)
    commands.append([sys.executable, 'localization/verify_manuals_native.py'])
    commands.append([sys.executable, 'localization/manual_extra_translation.py', 'check'])
    commands.append([sys.executable, 'localization/verify_manual_extra.py'])
    commands.append([sys.executable, 'localization/patchouli_translation.py', 'check'])
    commands.append([sys.executable, 'localization/group_labels.py', 'check'])
    if (ROOT / 'localization/cfpa_review/build-manifest.json').exists():
        commands.extend([
            [sys.executable, 'localization/cfpa_review_build.py', 'check'],
            [sys.executable, 'localization/cfpa_review/manuals/validate_native.py'],
            [sys.executable, 'localization/verify_cfpa_review.py'],
        ])
    rows = []
    for command in commands:
        result = execute_check(command)
        rows.append({'command':command, 'returncode':result.returncode, 'stdout':result.stdout, 'stderr':result.stderr})
        print(('PASS ' if result.returncode == 0 else 'FAIL ') + ' '.join(command[1:]))
    config = json.loads((ROOT / 'project.json').read_text())
    version = config['target_pack_version']
    report = {'status':'passed' if all(r['returncode'] == 0 for r in rows) else 'failed',
              'target_pack_version':version,
              'component_baselines':config.get('component_baselines',{}),
              'unfinished_excluded':unfinished, 'checks':rows, 'in_game_tested':False}
    (ROOT / f'localization/reports/project-verification-{version}.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    if report['status'] != 'passed':
        for row in rows:
            if row['returncode']:
                print(row['stdout'] + row['stderr'])
        raise SystemExit(1)
    print('All completed translation checks passed. Unfinished drafts: ' + ', '.join(unfinished))

if __name__ == '__main__':
    main()
