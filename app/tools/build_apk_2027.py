# -*- coding: utf-8 -*-
"""Builds a signed APK for ALI MU'IZ ENGLISH 2027 (v1.12.11) without Gradle.

Uses the Android SDK build-tools directly: aapt2 -> javac -> d8 -> zipalign ->
apksigner, with the existing app/release.jks key (same key as the earlier apps).

    py app/tools/build_apk_2027.py
"""
import io, os, re, sys, glob, shutil, subprocess, zipfile

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
APP = os.path.join(ROOT, 'app')
AND = os.path.join(APP, 'android_english2027')
WEB_INDEX = os.path.join(APP, 'english2027', 'index.html')
DIST = os.path.join(APP, 'dist')
TMP = os.path.join(os.environ.get('TEMP', r'C:\Windows\Temp'), 'e2027build')
KEYSTORE = os.path.join(APP, 'release.jks')

PKG = 'com.alshallah.english2027'
MIN_SDK = 24
TARGET_SDK = 34
VERSION_CODE = 16
VERSION_NAME = '1.12.11'
OUT_NAME = 'انكليزي-السادس-الاعدادي-2027-v1.12.11.apk'
# كلمة مرور مفتاح التوقيع تُقرأ من البيئة فقط — لا تُكتب في المستودع
KS_PASS = os.environ.get('E2027_KS_PASS', '')
KS_ALIAS = os.environ.get('E2027_KS_ALIAS', 'grammar')

SDK_CANDIDATES = [
    os.environ.get('ANDROID_HOME'),
    os.environ.get('ANDROID_SDK_ROOT'),
    os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Android', 'Sdk'),
    r'C:\Android\Sdk',
]
JAVA_CANDIDATES = [
    r'C:\Program Files\Android\Android Studio\jbr',
    os.path.join(os.environ.get('JAVA_HOME', '') or '', ''),
]


def die(msg):
    print('ERROR:', msg)
    sys.exit(1)


def find_sdk():
    for c in SDK_CANDIDATES:
        if c and os.path.isdir(c) and os.path.isdir(os.path.join(c, 'build-tools')):
            return c
    die('Android SDK not found')


def find_java():
    # 1) project-local JDK (downloaded into .tools/jdk)
    hits = glob.glob(os.path.join(os.environ.get('TEMP', ''), 'jdk*', 'bin', 'javac.exe'))
    hits += glob.glob(os.path.join(ROOT, '.tools', 'jdk', '**', 'bin', 'javac.exe'), recursive=True)
    hits += glob.glob(os.path.join(ROOT, '.tools', 'jdk-*', 'bin', 'javac.exe'))
    for c in JAVA_CANDIDATES:
        if c and os.path.isfile(os.path.join(c, 'bin', 'javac.exe')):
            hits.append(os.path.join(c, 'bin', 'javac.exe'))
    if not hits:
        die('JDK (javac) not found — download Temurin 17 into .tools/jdk')
    return os.path.dirname(os.path.dirname(hits[0]))


def newest_dir(parent, prefix):
    cands = [d for d in os.listdir(parent) if d.startswith(prefix)]
    if not cands:
        die('missing ' + prefix + ' in ' + parent)
    cands.sort(key=lambda d: [int(x) if x.isdigit() else 0 for x in re.split(r'[.\-]', d)])
    return os.path.join(parent, cands[-1])


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.decode('utf-8', 'replace')
    if p.returncode != 0:
        print(out)
        die('failed: ' + ' '.join(str(c) for c in cmd))
    return out


def main():
    if not os.path.isfile(WEB_INDEX):
        die('missing ' + WEB_INDEX)
    sdk = find_sdk()
    java = find_java()
    bt = newest_dir(os.path.join(sdk, 'build-tools'), '')
    plat = newest_dir(os.path.join(sdk, 'platforms'), 'android-')
    android_jar = os.path.join(plat, 'android.jar')
    aapt2 = os.path.join(bt, 'aapt2.exe')
    zipalign = os.path.join(bt, 'zipalign.exe')
    d8_jar = os.path.join(bt, 'lib', 'd8.jar')
    apksigner_jar = os.path.join(bt, 'lib', 'apksigner.jar')
    java_exe = os.path.join(java, 'bin', 'java.exe')
    javac = os.path.join(java, 'bin', 'javac.exe')
    keytool = os.path.join(java, 'bin', 'keytool.exe')

    print('SDK     :', sdk)
    print('Build   :', bt)
    print('Platform:', plat)
    print('JDK     :', java)

    for d in (TMP, DIST):
        if os.path.isdir(d):
            shutil.rmtree(d)
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(DIST, exist_ok=True)

    # 1) assets: the single-file app only (the v1.12.2 backup must not ship)
    assets = os.path.join(TMP, 'assets')
    os.makedirs(assets, exist_ok=True)
    shutil.copyfile(WEB_INDEX, os.path.join(assets, 'index.html'))
    print('asset   : index.html %.0f KB' % (os.path.getsize(WEB_INDEX) / 1024))

    # 2) project copy to an ASCII path (Java tools reject the Arabic workspace path)
    proj = os.path.join(TMP, 'project')
    shutil.copytree(AND, proj)
    res_dir = os.path.join(proj, 'res')
    manifest = os.path.join(proj, 'AndroidManifest.xml')
    java_dir = os.path.join(proj, 'java')

    # 3) compile resources
    res_zip = os.path.join(TMP, 'res.zip')
    run([aapt2, 'compile', '--dir', res_dir, '-o', res_zip])
    print('[1/6] resources compiled')

    # 4) link manifest + resources + assets
    base_apk = os.path.join(TMP, 'base.ap_')
    gen_dir = os.path.join(TMP, 'gen')
    os.makedirs(gen_dir, exist_ok=True)
    run([aapt2, 'link', '-o', base_apk, '-I', android_jar, '--manifest', manifest,
         '-R', res_zip, '-A', assets, '--java', gen_dir,
         '--min-sdk-version', str(MIN_SDK), '--target-sdk-version', str(TARGET_SDK),
         '--version-code', str(VERSION_CODE), '--version-name', VERSION_NAME,
         '--auto-add-overlay'])
    print('[2/6] linked')

    # 5) compile java
    classes = os.path.join(TMP, 'classes')
    os.makedirs(classes, exist_ok=True)
    srcs = [os.path.join(java_dir, 'com', 'alshallah', 'english2027', 'MainActivity.java')]
    srcs += glob.glob(os.path.join(gen_dir, '**', 'R.java'), recursive=True)
    run([javac, '-encoding', 'UTF-8', '--release', '11', '-nowarn',
         '-classpath', android_jar, '-d', classes] + srcs)
    print('[3/6] javac ok (%d files)' % len(srcs))

    # 6) dex
    dex_dir = os.path.join(TMP, 'dex')
    os.makedirs(dex_dir, exist_ok=True)
    class_files = glob.glob(os.path.join(classes, '**', '*.class'), recursive=True)
    argfile = os.path.join(TMP, 'classes.txt')
    io.open(argfile, 'w', encoding='utf-8').write('\n'.join(class_files))
    run([java_exe, '-cp', d8_jar, 'com.android.tools.r8.D8', '--release',
         '--min-api', str(MIN_SDK), '--lib', android_jar, '--output', dex_dir, '@' + argfile])
    print('[4/6] dex ok (%d classes)' % len(class_files))

    # 7) package + align
    unsigned = os.path.join(TMP, 'app-unsigned.apk')
    shutil.copyfile(base_apk, unsigned)
    with zipfile.ZipFile(unsigned, 'a', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(dex_dir, 'classes.dex'), 'classes.dex')
    aligned = os.path.join(TMP, 'app-aligned.apk')
    run([zipalign, '-p', '-f', '4', unsigned, aligned])
    print('[5/6] packaged + aligned')

    # 8) sign with the existing release key (do not create a new one)
    if not os.path.isfile(KEYSTORE):
        die('release.jks not found — refusing to create a new key')
    if not KS_PASS:
        die('set E2027_KS_PASS to the release.jks password, e.g. E2027_KS_PASS=... py app/tools/build_apk_2027.py')
    ks_tmp = os.path.join(TMP, 'release.jks')
    shutil.copyfile(KEYSTORE, ks_tmp)
    signed = os.path.join(TMP, 'app-signed.apk')
    run([java_exe, '-jar', apksigner_jar, 'sign',
         '--ks', ks_tmp, '--ks-pass', 'pass:' + KS_PASS, '--key-pass', 'pass:' + KS_PASS,
         '--v1-signing-enabled', 'true', '--v2-signing-enabled', 'true',
         '--v3-signing-enabled', 'true', '--min-sdk-version', str(MIN_SDK),
         '--out', signed, aligned])
    verify = run([java_exe, '-jar', apksigner_jar, 'verify', '--print-certs', signed])
    print('[6/6] signed + verified')
    for line in verify.splitlines():
        if 'SHA-256' in line or 'Signer' in line:
            print('      ', line.strip())

    final_apk = os.path.join(DIST, OUT_NAME)
    shutil.copyfile(signed, final_apk)
    root_copy = os.path.join(ROOT, OUT_NAME)
    shutil.copyfile(signed, root_copy)

    badging = run([aapt2, 'dump', 'badging', final_apk])
    for line in badging.splitlines():
        if line.startswith('package:') or line.startswith('application-label') or line.startswith('sdkVersion'):
            print('      ', line.strip())

    print('\nAPK :', final_apk)
    print('COPY:', root_copy)
    print('SIZE: %.0f KB (%.2f MB)' % (os.path.getsize(final_apk) / 1024.0,
                                       os.path.getsize(final_apk) / 1048576.0))


if __name__ == '__main__':
    main()
