import java.nio.file.*;
import java.util.*;
import guideme.libs.mdast.*;
import com.google.gson.*;
import com.google.gson.stream.JsonWriter;
import java.io.StringWriter;
import guideme.libs.mdast.mdx.MdxMdastExtension;
import guideme.libs.mdast.gfm.GfmTableMdastExtension;
import guideme.libs.mdast.gfmstrikethrough.GfmStrikethroughMdastExtension;
import guideme.libs.mdx.MdxSyntax;
import guideme.libs.micromark.extensions.YamlFrontmatterSyntax;
import guideme.libs.micromark.extensions.gfm.GfmTableSyntax;
import guideme.libs.micromark.extensions.gfmstrikethrough.GfmStrikethroughSyntax;
import guideme.internal.shaded.snakeyaml.Yaml;
import guideme.internal.shaded.snakeyaml.LoaderOptions;
import guideme.internal.shaded.snakeyaml.constructor.SafeConstructor;
public class ValidateManuals {
 public static void main(String[] args) throws Exception {
  var options = new MdastOptions()
   .withSyntaxExtension(MdxSyntax.INSTANCE)
   .withSyntaxExtension(YamlFrontmatterSyntax.INSTANCE)
   .withSyntaxExtension(GfmTableSyntax.INSTANCE)
   .withSyntaxExtension(GfmStrikethroughSyntax.INSTANCE)
   .withMdastExtension(MdxMdastExtension.INSTANCE)
   .withMdastExtension(YamlFrontmatterExtension.INSTANCE)
   .withMdastExtension(GfmTableMdastExtension.INSTANCE)
   .withMdastExtension(GfmStrikethroughMdastExtension.INSTANCE);
  int count=0, frontmatters=0;
  var yamlOptions=new LoaderOptions();
  var yaml=new Yaml(new SafeConstructor(yamlOptions));
  for (String arg:args) {
   try(var files=Files.walk(Path.of(arg))) {
    for(var p:files.filter(x->x.toString().endsWith(".md")).sorted().toList()) {
     var text=Files.readString(p).replaceAll("\\r\\n?", "\n");
     Object metadata=null;
     if(text.startsWith("---\n")) {
      int end=text.indexOf("\n---",3);
      if(end<0)throw new IllegalStateException("Unclosed YAML frontmatter: "+p);
      try {metadata=yaml.load(text.substring(4,end));}
      catch(RuntimeException e){throw new IllegalStateException("Invalid YAML frontmatter: "+p,e);}
      frontmatters++;
     }
     var root=MdAst.fromMarkdown(text,options);
     if(root==null)throw new IllegalStateException("No root: "+p);
     StringWriter buffer=new StringWriter();
     root.toJson(new JsonWriter(buffer));
     if(System.getProperty("astOutput")!=null){
      var out=Path.of(System.getProperty("astOutput"),p.toString()+".json");
      Files.createDirectories(out.getParent());Files.writeString(out,buffer.toString());
      Files.writeString(Path.of(out.toString()+".yaml.json"),new Gson().toJson(metadata));
     }
     count++;
    }
   }
  }
  System.out.println("GuideME native Markdown/MDX parser: parsed "+count+" pages successfully.");
  System.out.println("GuideME embedded SnakeYAML: parsed "+frontmatters+" frontmatters successfully.");
 }
}
