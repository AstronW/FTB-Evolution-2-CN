"""Validate feedback Markdown and YAML using this instance's native GuideME."""
import json,subprocess
from feedback_fixes import BASE,GAME,OUTPUT,ROOT
libraries=GAME.parents[1]/'bin/libraries'
cp=[str(next((GAME/'mods').glob('guideme-*.jar')))]+[str(next(libraries.rglob(name))) for name in ['gson-2.13.2.jar','slf4j-api-2.0.17.jar','guava-33.5.0-jre.jar']]
result=subprocess.run(['java','--class-path',':'.join(cp),str(ROOT/'localization/ValidateManuals.java'),str(OUTPUT)],text=True,capture_output=True)
(BASE/'native-parser-check.txt').write_text(result.stdout+result.stderr)
print(result.stdout)
assert result.returncode==0,result.stderr
expected=len(list(OUTPUT.rglob('*.md')))
assert f'parsed {expected} pages successfully' in result.stdout,expected
