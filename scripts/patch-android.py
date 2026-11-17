"""Dijalankan oleh workflow setelah `npx cap add android`:
   - menimpa ikon/splash dengan logo Corvus
   - menambah versi, tanda tangan rilis, dan warna status bar."""
import os, re, shutil, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = os.path.join(root, 'android', 'app')
res = os.path.join(app, 'src', 'main', 'res')

# 1. hapus splash.png bawaan (diganti splash.xml) lalu salin res kita
for dp, dn, fn in os.walk(res):
    for f in fn:
        if re.match(r'splash\.(png|jpg|webp)$', f): os.remove(os.path.join(dp, f))
shutil.copytree(os.path.join(root, 'res'), res, dirs_exist_ok=True)

# 2. build.gradle: versi + tanda tangan
bg = os.path.join(app, 'build.gradle'); s = open(bg).read()
ver = open(os.path.join(root, 'VERSION')).read().strip()
mj, mn, pt = [int(x) for x in ver.split('.')]
code = str(mj * 10000 + mn * 100 + pt)
s = re.sub(r'versionCode \d+', 'versionCode ' + code, s, count=1)
s = re.sub(r'versionName "[^"]*"', 'versionName "' + ver + '"', s, count=1)
s += '''
android {
    signingConfigs {
        corvusRelease {
            storeFile file(System.getenv("KS_PATH"))
            storePassword System.getenv("KS_PASS")
            keyAlias System.getenv("KS_ALIAS")
            keyPassword System.getenv("KS_PASS")
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.corvusRelease
        }
    }
}
'''
open(bg, 'w').write(s)

# 3. warna status bar / navigation bar
st = os.path.join(res, 'values', 'styles.xml'); t = open(st).read()
extra = '        <item name="android:statusBarColor">#3B1480</item>\n        <item name="android:navigationBarColor">#FFFFFF</item>\n        <item name="android:windowLightNavigationBar">true</item>\n'
t = t.replace('<style name="AppTheme.NoActionBar" parent="Theme.AppCompat.DayNight.NoActionBar">', '<style name="AppTheme.NoActionBar" parent="Theme.AppCompat.DayNight.NoActionBar">\n' + extra, 1)
open(st, 'w').write(t)
# 4. nomor versi di user agent agar aplikasi tahu versinya (untuk pemberitahuan pembaruan)
import json
cp = os.path.join(root, 'capacitor.config.json'); cfg = json.load(open(cp))
cfg.setdefault('android', {})['appendUserAgent'] = 'CorvusApp/' + ver
json.dump(cfg, open(cp, 'w'), indent=2)
print('patch ok; versi', ver, 'versionCode', code)
