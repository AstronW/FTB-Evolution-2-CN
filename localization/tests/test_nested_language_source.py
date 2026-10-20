import hashlib,io,json,pathlib,sys,tempfile,unittest,zipfile
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from ordinary_translation import language_source

def archive(member,payload):
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w') as z:z.writestr(member,payload)
    return buffer.getvalue()

class NestedLanguageSource(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.outer=pathlib.Path(self.tmp.name)/'distribution.jar'
        self.lang='assets/example/lang/en_us.json';self.payload=b'{"option.tooltip":"Current nested option"}'
        self.member='META-INF/jarjar/actual-mod.jar';self.inner=archive(self.lang,self.payload)
        self.outer.write_bytes(archive(self.member,self.inner))
        self.manifest={'jar':str(self.outer),'nested_jar':self.member,'jar_sha256':hashlib.sha256(self.outer.read_bytes()).hexdigest(),'nested_jar_sha256':hashlib.sha256(self.inner).hexdigest(),'language_path':self.lang}
    def test_reads_language_from_embedded_mod_not_outer_distribution(self):
        self.assertEqual(self.payload,language_source(self.manifest))
    def test_rejects_unreviewed_distribution_change(self):
        self.outer.write_bytes(archive(self.member,archive(self.lang,b'{}')))
        with self.assertRaisesRegex(AssertionError,'Outer JAR changed'):language_source(self.manifest)
    def test_rejects_unreviewed_inner_change_even_when_parent_rebound(self):
        self.manifest['nested_jar_sha256']='0'*64
        with self.assertRaisesRegex(AssertionError,'Nested JAR changed'):language_source(self.manifest)
    def test_reads_two_level_dependency_and_checks_intermediate_identity(self):
        member='META-INF/jarjar/library.jar'
        middle=archive(member,self.inner)
        self.outer.write_bytes(archive(self.member,middle))
        manifest={'jar':str(self.outer),'jar_sha256':hashlib.sha256(self.outer.read_bytes()).hexdigest(),
                  'language_path':self.lang,'nested_jars':[
                      {'path':self.member,'sha256':hashlib.sha256(middle).hexdigest()},
                      {'path':member,'sha256':hashlib.sha256(self.inner).hexdigest()}]}
        self.assertEqual(self.payload,language_source(manifest))
        manifest['nested_jars'][0]['sha256']='0'*64
        with self.assertRaisesRegex(AssertionError,'Nested JAR changed'):language_source(manifest)

if __name__=='__main__':unittest.main()
