# -*- coding: utf-8 -*-
"""يبني APK لتطبيق «ملزمة القواعد» 4.0 (Poppins + تمارين قابلة للحل)."""
import io, os, re, shutil, subprocess, sys, zipfile, glob

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
APP = os.path.join(ROOT, 'app')
AND = os.path.join(APP, 'android_malzmah')
WEB = os.path.join(APP, 'web4')
DIST = os.path.join(APP, 'dist')
TMP = os.path.join(os.environ.get('TEMP', r'C:\Windows\Temp'), 'g6build_malzmah')
BUILD = TMP

MIN_SDK = 24
TARGET_SDK = 34
VERSION_CODE = 5
VERSION_NAME = '4.1'
KS_PASS = 'grammar6'
KS_ALIAS = 'grammar'

SDK_CANDIDATES = [os.environ.get('ANDROID_HOME'), os.environ.get('ANDROID_SDK_ROOT'),
                   os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Android', 'Sdk'),
                   r'C:\Android\Sdk']
JAVA_CANDIDATES = [r'C:\Program Files\Android\Android Studio\jbr',
                   os.path.join(os.environ.get('JAVA_HOME', '')),
                   os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Android Studio', 'jbr')]


def die(m):
    print('ERROR:', m)
    sys.exit(1)


def find_sdk():
    for c in SDK_CANDIDATES:
        if c and os.path.isdir(os.path.join(c, 'build-tools')):
            return c
    die('Android SDK not found')


def find_java():
    for c in JAVA_CANDIDATES:
        if c and os.path.isfile(os.path.join(c, 'bin', 'javac.exe')):
            return c
    die('JDK not found')


def newest_dir(parent, prefix):
    c = [d for d in os.listdir(parent) if d.startswith(prefix)]
    c.sort(key=lambda d: [int(x) if x.isdigit() else 0 for x in re.split(r'[.\-]', d)])
    return os.path.join(parent, c[-1])


def run(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.decode('utf-8', 'replace')
    if p.returncode != 0:
        print(out)
        die('failed: ' + ' '.join(str(c) for c in cmd))
    return out


def main():
    sdk, java = find_sdk(), find_java()
    bt = newest_dir(os.path.join(sdk, 'build-tools'), '')
    plat = newest_dir(os.path.join(sdk, 'platforms'), 'android-')
    android_jar = os.path.join(plat, 'android.jar')
    aapt2 = os.path.join(bt, 'aapt2.exe')
    zipalign = os.path.join(bt, 'zipalign.exe')
    d8_jar = os.path.join(bt, 'lib', 'd8.jar')
    apksigner_jar = os.path.join(bt, 'lib', 'apksigner.jar')
    keytool = os.path.join(java, 'bin', 'keytool.exe')
    java_exe = os.path.join(java, 'bin', 'java.exe')
    javac = os.path.join(java, 'bin', 'javac.exe')

    if os.path.isdir(BUILD):
        shutil.rmtree(BUILD)
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(DIST, exist_ok=True)

    assets = os.path.join(BUILD, 'assets')
    shutil.copytree(WEB, assets)
    for junk in ('data/content.json', 'icon.html', 'data/exam.js'):
        p = os.path.join(assets, junk)
        if os.path.exists(p):
            os.remove(p)
    print('web assets:', sum(len(f) for _, _, f in os.walk(assets)), 'files')

    PROJ = os.path.join(BUILD, 'project')
    shutil.copytree(AND, PROJ)
    res_dir = os.path.join(PROJ, 'res')
    manifest = os.path.join(PROJ, 'AndroidManifest.xml')
    java_dir = os.path.join(PROJ, 'java')

    # إصدار البيان
    s = io.open(manifest, encoding='utf-8').read()
    s = re.sub(r'android:versionCode="\d+"', 'android:versionCode="%d"' % VERSION_CODE, s)
    s = re.sub(r'android:versionName="[^"]*"', 'android:versionName="%s"' % VERSION_NAME, s)
    io.open(manifest, 'w', encoding='utf-8').write(s)

    res_zip = os.path.join(BUILD, 'res.zip')
    run([aapt2, 'compile', '--dir', res_dir, '-o', res_zip])
    print('[1/6] resources compiled')

    base_apk = os.path.join(BUILD, 'base.ap_')
    gen_dir = os.path.join(BUILD, 'gen')
    os.makedirs(gen_dir, exist_ok=True)
    run([aapt2, 'link', '-o', base_apk, '-I', android_jar,
         '--manifest', manifest, '-R', res_zip, '-A', assets, '--java', gen_dir,
         '--min-sdk-version', str(MIN_SDK), '--target-sdk-version', str(TARGET_SDK),
         '--version-code', str(VERSION_CODE), '--version-name', VERSION_NAME,
         '--auto-add-overlay'])
    print('[2/6] resources linked')

    classes = os.path.join(BUILD, 'classes')
    os.makedirs(classes, exist_ok=True)
    srcs = glob.glob(os.path.join(java_dir, 'com', 'sixth', 'grammar', 'malzmah', '*.java'))
    srcs += glob.glob(os.path.join(gen_dir, '**', 'R.java'), recursive=True)
    run([javac, '-encoding', 'UTF-8', '--release', '11', '-nowarn',
         '-classpath', android_jar, '-d', classes] + srcs)
    print('[3/6] java compiled (%d files)' % len(srcs))

    dex_dir = os.path.join(BUILD, 'dex')
    os.makedirs(dex_dir, exist_ok=True)
    class_files = glob.glob(os.path.join(classes, '**', '*.class'), recursive=True)
    argfile = os.path.join(BUILD, 'classes.txt')
    io.open(argfile, 'w', encoding='utf-8').write('\n'.join(class_files))
    run([java_exe, '-cp', d8_jar, 'com.android.tools.r8.D8', '--release',
         '--min-api', str(MIN_SDK), '--lib', android_jar, '--output', dex_dir, '@' + argfile])
    print('[4/6] dex created (%d classes)' % len(class_files))

    unsigned = os.path.join(BUILD, 'app-unsigned.apk')
    shutil.copyfile(base_apk, unsigned)
    with zipfile.ZipFile(unsigned, 'a', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(dex_dir, 'classes.dex'), 'classes.dex')
    aligned = os.path.join(BUILD, 'app-aligned.apk')
    run([zipalign, '-p', '-f', '4', unsigned, aligned])
    print('[5/6] packaged')

    ks_home = os.path.join(APP, 'release.jks')
    ks_tmp = os.path.join(BUILD, 'release.jks')
    if os.path.exists(ks_home):
        shutil.copyfile(ks_home, ks_tmp)
    if not os.path.exists(ks_tmp):
        run([keytool, '-genkeypair', '-v', '-keystore', ks_tmp, '-storepass', KS_PASS,
             '-keypass', KS_PASS, '-alias', KS_ALIAS, '-keyalg', 'RSA', '-keysize', '2048',
             '-validity', '10950',
             '-dname', 'CN=Grammar6, OU=School, O=Grammar, L=Amman, S=Amman, C=JO'])
        shutil.copyfile(ks_tmp, ks_home)

    signed_tmp = os.path.join(BUILD, 'app-signed.apk')
    run([java_exe, '-jar', apksigner_jar, 'sign', '--ks', ks_tmp,
         '--ks-pass', 'pass:' + KS_PASS, '--key-pass', 'pass:' + KS_PASS,
         '--v1-signing-enabled', 'true', '--v2-signing-enabled', 'true',
         '--v3-signing-enabled', 'true', '--min-sdk-version', str(MIN_SDK),
         '--out', signed_tmp, aligned])
    run([java_exe, '-jar', apksigner_jar, 'verify', signed_tmp])

    final_apk = os.path.join(DIST, 'ملزمة-القواعد-%s.apk' % VERSION_NAME)
    shutil.copyfile(signed_tmp, final_apk)
    shutil.copyfile(signed_tmp, os.path.join(ROOT, 'ملزمة-القواعد-%s.apk' % VERSION_NAME))
    print('[6/6] signed and verified')
    print('\nAPK: %s\nsize: %.0f KB' % (final_apk, os.path.getsize(final_apk) / 1024.0))


if __name__ == '__main__':
    main()
