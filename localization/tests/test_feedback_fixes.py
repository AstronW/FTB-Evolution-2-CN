import json,pathlib,re,sys,unittest,zipfile
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import feedback_fixes as fixes
import release_pack
from audit_guideme_recipes import visible_source

class FeedbackFixes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs,_,_=release_pack.assemble_resourcepack([])
        cls.manifest=fixes.read(fixes.BASE/'manifest.json')
    def test_quest_names_follow_current_approved_names(self):
        changes=fixes.read(fixes.BASE/'quest-name-changes.json')
        for row in changes:
            value=fixes.read(fixes.ROOT/row['file'])[row['key']]
            text=re.sub(r'[&§][0-9a-fklmnor]','',value,flags=re.I)
            self.assertIn(row['zh'],text)
            self.assertNotRegex(text,r'(?<![A-Za-z0-9_:/.])'+re.escape(row['en'])+r'(?![A-Za-z0-9_:/.])')
    def test_oracle_metadata_preserves_keys_icons_and_order(self):
        for rel,names in fixes.read(fixes.BASE/'metadata-translations.json').items():
            book,rest=rel.split('/',1)
            jar=next((fixes.GAME/'mods').glob('kindredspirits-*.jar' if book=='kindredspirits' else 'oracle_index-*.jar'))
            with zipfile.ZipFile(jar) as z:original=json.loads(z.read('assets/oracle_index/books/'+rel))
            member='assets/oracle_index/books/'+book+'/translated/zh_cn/'+rest.removeprefix('docs/')
            translated=json.loads(self.outputs[member][0])
            self.assertEqual(list(original),list(translated))
            for key in original:
                self.assertEqual(names[key],translated[key]['name'])
                self.assertEqual({k:v for k,v in original[key].items() if k!='name'},{k:v for k,v in translated[key].items() if k!='name'})
    def test_patchouli_literal_keys_are_shipped(self):
        for ns,entries in fixes.read(fixes.BASE/'landing-translations.json').items():
            merged=json.loads(self.outputs[f'assets/{ns}/lang/zh_cn.json'][0])
            for key,zh in entries.items():self.assertEqual(zh,merged[key])
    def test_all_source_bound_overlay_files_are_shipped(self):
        for member,path in fixes.resource_overrides():
            if not member.endswith('/lang/zh_cn.json'):self.assertEqual(path.read_bytes(),self.outputs[member][0])
    def test_unified_recipe_queries_and_component_corrections(self):
        for row in self.manifest['recipe_reference_changes']:
            text=self.outputs[row['page']][0].decode()
            self.assertIn(f'id="{row["new"]}"',text)
            self.assertNotIn(f'<{row["tag"]} id="{row["old"]}"',text)
        for row in self.manifest['component_corrections']:
            text=self.outputs[row['page']][0].decode()
            self.assertIn(row['new'],text)
            self.assertNotIn(row['old'],text)
            self.assertNotIn('fallbackText=""',row['new'])
    def test_commented_and_example_recipe_tags_are_not_live(self):
        text='[//]: # (<RecipeFor id="absent" />)\n```mdx\n<Recipe id="example" />\n```\n<Recipe id="live" />\n'
        masked=visible_source(text)
        self.assertNotIn('absent',masked);self.assertNotIn('example',masked);self.assertIn('live',masked)
        self.assertEqual(text.count('\n'),masked.count('\n'))
    def test_no_nodeworks_code_patch_is_shipped(self):
        self.assertFalse((fixes.BASE/'mod-manifest.json').exists())
        extras=release_pack.extra_instance_files()
        self.assertFalse(any(name.startswith('mods/') for name in extras))

if __name__=='__main__':unittest.main()
