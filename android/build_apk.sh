#!/usr/bin/env bash
# Baut die APK ohne Gradle: aapt2 + javac + d8 + zipalign + apksigner.
# Benötigt: JDK (java/keytool auf PATH), ANDROID_HOME mit platforms/android-34
# und build-tools/34.0.0.
set -euo pipefail

cd "$(dirname "$0")"

: "${ANDROID_HOME:?ANDROID_HOME muss gesetzt sein (SDK mit platforms/android-34 und build-tools/34.0.0)}"
BT="$ANDROID_HOME/build-tools/34.0.0"
PLATFORM="$ANDROID_HOME/platforms/android-34/android.jar"
SRC=app/src/main/java
OUT=build
PKG=de.tlausen.kabelapp
KEYSTORE="$OUT/debug.keystore"
APK_UNSIGNED="$OUT/kabelberechnung-unsigned.apk"
APK_ALIGNED="$OUT/kabelberechnung-aligned.apk"
APK="kabelberechnung.apk"

rm -rf "$OUT"
mkdir -p "$OUT/classes"

echo "== aapt2: Ressourcen linken"
"$BT/aapt2" link -o "$APK_UNSIGNED" \
    --manifest app/AndroidManifest.xml \
    -I "$PLATFORM" \
    --auto-add-overlay

echo "== javac"
javac -source 8 -target 8 -nowarn \
    -classpath "$PLATFORM" \
    -d "$OUT/classes" \
    $(find "$SRC" -name '*.java')

echo "== d8: Dex erstellen"
"$BT/d8" --release --lib "$PLATFORM" \
    --output "$OUT" \
    $(find "$OUT/classes" -name '*.class')

echo "== classes.dex einpacken"
cd "$OUT"
cp kabelberechnung-unsigned.apk base.apk
zip -qj base.apk classes.dex
cd ..

echo "== zipalign"
"$BT/zipalign" -f 4 "$OUT/base.apk" "$APK_ALIGNED"

echo "== Debug-Keystore + Signatur"
if [ ! -f "$KEYSTORE" ]; then
    keytool -genkeypair -keystore "$KEYSTORE" -storepass android -keypass android \
        -alias androiddebugkey -keyalg RSA -keysize 2048 -validity 10000 \
        -dname "CN=Android Debug,O=Android,C=DE" >/dev/null 2>&1
fi
"$BT/apksigner" sign --ks "$KEYSTORE" --ks-pass pass:android --key-pass pass:android \
    --out "$APK" "$APK_ALIGNED"
"$BT/apksigner" verify "$APK"

echo "Fertig: $(cd "$(dirname "$APK")" && pwd)/$(basename "$APK")"
