"""Run translation checks from this independent project directory."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {'info', 'check'}:
        raise SystemExit('Usage: python project.py info|check')
    if sys.argv[1] == 'info':
        print((ROOT / 'project.json').read_text())
        return
    commands = [
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'localization/tests'],
        [sys.executable, 'localization/quest_translation.py', 'check'],
        [sys.executable, 'localization/verify_quests.py'],
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
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        rows.append({'command':command, 'returncode':result.returncode, 'stdout':result.stdout, 'stderr':result.stderr})
        print(('PASS ' if result.returncode == 0 else 'FAIL ') + ' '.join(command[1:]))
    report = {'status':'passed' if all(r['returncode'] == 0 for r in rows) else 'failed',
              'baseline':'1.3.2', 'target_1_4_0_adaptation_complete':False,
              'component_baselines':json.loads((ROOT / 'project.json').read_text()).get('component_baselines',{}),
              'unfinished_excluded':unfinished, 'checks':rows, 'in_game_tested':False}
    (ROOT / 'localization/reports/project-migration-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    if report['status'] != 'passed':
        for row in rows:
            if row['returncode']:
                print(row['stdout'] + row['stderr'])
        raise SystemExit(1)
    print('All completed translation checks passed. Unfinished drafts: ' + ', '.join(unfinished))

if __name__ == '__main__':
    main()
