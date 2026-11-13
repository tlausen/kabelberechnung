Android-Konvertierung: Der Quellcode ist vollständig enthalten. Die vorbereitete APK liegt als `kabelberechnung.apk` hier im Verzeichnis.

## APK selbst bauen

```bash
ANDROID_HOME=<SDK-Pfad> ./build_apk.sh
```

Voraussetzungen: JDK 17+ und Android SDK (platforms/android-34, build-tools/34.0.0).
Das Skript nutzt aapt2/javac/d8/zipalign/apksigner direkt – kein Gradle nötig.
