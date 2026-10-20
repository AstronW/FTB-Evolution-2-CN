import de.marhali.json5.Json5;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;

/** Parse with the same json5-java 3.0.0 dependency used by installed FTB Library. */
class ValidateJson5 {
    public static void main(String[] args) throws Exception {
        var parser = new Json5();
        int files = 0;
        int keys = 0;
        var seen = new HashSet<String>();
        try (var paths = Files.walk(Path.of(args[0]))) {
            for (var path : paths.filter(p -> p.toString().endsWith(".json5")).toList()) {
                var object = parser.parse(Files.readString(path)).getAsJson5Object();
                for (var key : object.asMap().keySet()) {
                    if (!seen.add(key)) throw new IllegalStateException("Duplicate language key: " + key);
                }
                keys += object.asMap().size();
                files++;
            }
        }
        System.out.println("json5-java 3.0.0: parsed " + files + " files, " + keys + " unique language keys");
    }
}
