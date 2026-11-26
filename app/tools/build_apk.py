# -*- coding: utf-8 -*-
"""يبني ملف APK لتطبيق انكليزي السادس الاعدادي باستخدام أدوات Android SDK مباشرة (بدون Gradle)."""
import io, os, sys, re, shutil, subprocess, zipfile, glob, time

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
APP = os.path.join(ROOT, 'app')
AND = os.path.join(APP, 'android')
WEB = os.path.join(APP, 'web')
DIST = os.path.join(APP, 'dist')

# أدوات Android لا تتعامل مع المسارات غير الإنجليزية (العربية) — نستخدم مجلدًا مؤقتًا
TMP = os.path.join(os.environ.get('TEMP', r'C:\Windows\Temp'), 'g6build')
BUILD = TMP
KEYSTORE = os.path.join(APP, 'release.jks')

MIN_SDK = 24
TARGET_SDK = 34
VERSION_CODE = 6
VERSION_NAME = '1.5'
KS_PASS = 'grammar6'
KS_ALIAS = 'grammar'

SDK_CANDIDATES = [
    os.environ.get('ANDROID_HOME'),
    os.environ.get('ANDROID_SDK_ROOT'),
    os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Android', 'Sdk'),
    r'C:\Android\Sdk',
]
JAVA_CANDIDATES = [
    r'C:\Program Files\Android\Android Studio\jbr',
    os.path.join(os.environ.get('JAVA_HOME', '')),
    os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Android Studio', 'jbr'),
]


def die(msg):
    print('ERROR:', msg)
    sys.exit(1)


def find_sdk():
    for c in SDK_CANDIDATES:
        if c and os.path.isdir(c) and os.path.isdir(os.path.join(c, 'build-tools')):
            return c
    die('لم يتم العثور على Android SDK')


def find_java():
    for c in JAVA_CANDIDATES:
        if c and os.path.isfile(os.path.join(c, 'bin', 'javac.exe')):
            return c
    die('لم يتم العثور على JDK (javac)')


def newest_dir(parent, prefix):
    cands = [d for d in os.listdir(parent) if d.startswith(prefix)]
    if not cands:
        die('لا يوجد ' + prefix + ' في ' + parent)
    cands.sort(key=lambda d: [int(x) if x.isdigit() else 0 for x in re.split(r'[.\-]', d)])
    return os.path.join(parent, cands[-1])


def run(cmd, cwd=None, env=None):
    p = subprocess.run(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.decode('utf-8', 'replace')
    if p.returncode != 0:
        print(out)
        die('فشل الأمر: ' + ' '.join(str(c) for c in cmd))
    return out


def main():
    sdk = find_sdk()
    java = find_java()
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

    print('SDK   :', sdk)
    print('Build :', bt)
    print('Platform:', plat)
    print('JDK   :', java)

    # ---------- تنظيف ----------
    for d in (BUILD, DIST):
        if os.path.isdir(d):
            shutil.rmtree(d)
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(DIST, exist_ok=True)

    # ---------- نسخ الأصول ----------
    assets = os.path.join(BUILD, 'assets')
    shutil.copytree(WEB, assets)
    # ملفات غير لازمة في الحزمة
    for junk in ('data/exercises.json', 'data/app.json'):
        p = os.path.join(assets, junk)
        if os.path.exists(p):
            os.remove(p)
    print('أصول الويب:', sum(len(f) for _, _, f in os.walk(assets)), 'ملف')

    # ---------- 0) نسخ مشروع أندرويد لمسار إنجليزي ----------
    PROJ = os.path.join(BUILD, 'project')
    shutil.copytree(AND, PROJ)
    res_dir = os.path.join(PROJ, 'res')
    manifest = os.path.join(PROJ, 'AndroidManifest.xml')
    java_dir = os.path.join(PROJ, 'java')

    # ---------- 1) ترجمة الموارد ----------
    res_zip = os.path.join(BUILD, 'res.zip')
    run([aapt2, 'compile', '--dir', res_dir, '-o', res_zip])
    print('[1/6] تم ترجمة الموارد')

    # ---------- 2) ربط الموارد ----------
    base_apk = os.path.join(BUILD, 'base.ap_')
    gen_dir = os.path.join(BUILD, 'gen')
    os.makedirs(gen_dir, exist_ok=True)
    run([aapt2, 'link',
         '-o', base_apk,
         '-I', android_jar,
         '--manifest', manifest,
         '-R', res_zip,
         '-A', assets,
         '--java', gen_dir,
         '--min-sdk-version', str(MIN_SDK),
         '--target-sdk-version', str(TARGET_SDK),
         '--version-code', str(VERSION_CODE),
         '--version-name', VERSION_NAME,
         '--auto-add-overlay'])
    print('[2/6] تم ربط الموارد والأصول')

    # ---------- 3) ترجمة جافا ----------
    classes = os.path.join(BUILD, 'classes')
    os.makedirs(classes, exist_ok=True)
    srcs = [os.path.join(java_dir, 'com', 'sixth', 'grammar', 'MainActivity.java')]
    srcs += glob.glob(os.path.join(gen_dir, '**', 'R.java'), recursive=True)
    run([javac, '-encoding', 'UTF-8', '--release', '11',
         '-nowarn', '-classpath', android_jar,
         '-d', classes] + srcs)
    print('[3/6] تم ترجمة الشيفرة (', len(srcs), 'ملف )')

    # ---------- 4) تحويل إلى dex ----------
    dex_dir = os.path.join(BUILD, 'dex')
    os.makedirs(dex_dir, exist_ok=True)
    class_files = glob.glob(os.path.join(classes, '**', '*.class'), recursive=True)
    argfile = os.path.join(BUILD, 'classes.txt')
    io.open(argfile, 'w', encoding='utf-8').write('\n'.join(class_files))
    run([java_exe, '-cp', d8_jar, 'com.android.tools.r8.D8',
         '--release', '--min-api', str(MIN_SDK), '--lib', android_jar,
         '--output', dex_dir, '@' + argfile])
    print('[4/6] تم إنشاء classes.dex من', len(class_files), 'صنف')

    # ---------- 5) تجميع الحزمة ----------
    unsigned = os.path.join(BUILD, 'app-unsigned.apk')
    shutil.copyfile(base_apk, unsigned)
    with zipfile.ZipFile(unsigned, 'a', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(dex_dir, 'classes.dex'), 'classes.dex')
    aligned = os.path.join(BUILD, 'app-aligned.apk')
    run([zipalign, '-p', '-f', '4', unsigned, aligned])
    print('[5/6] تم تجميع الحزمة ومحاذاتها')

    # ---------- 6) التوقيع ----------
    ks_home = os.path.join(APP, 'release.jks')
    ks_tmp = os.path.join(BUILD, 'release.jks')
    if os.path.exists(ks_home):
        shutil.copyfile(ks_home, ks_tmp)
    if not os.path.exists(ks_tmp):
        run([keytool, '-genkeypair', '-v',
             '-keystore', ks_tmp, '-storepass', KS_PASS, '-keypass', KS_PASS,
             '-alias', KS_ALIAS, '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10950',
             '-dname', 'CN=Grammar6, OU=School, O=Grammar, L=Amman, S=Amman, C=JO'])
        shutil.copyfile(ks_tmp, ks_home)
        print('تم إنشاء مفتاح التوقيع')

    # أدوات Java لا تتفاعل مع المسار عربية، نعمل التوقيع إلى مسار باسط إنجليزي
    signed_tmp = os.path.join(BUILD, 'app-signed.apk')
    run([java_exe, '-jar', apksigner_jar, 'sign',
         '--ks', ks_tmp, '--ks-pass', 'pass:' + KS_PASS, '--key-pass', 'pass:' + KS_PASS,
         '--v1-signing-enabled', 'true', '--v2-signing-enabled', 'true',
         '--v3-signing-enabled', 'true', '--min-sdk-version', str(MIN_SDK),
         '--out', signed_tmp, aligned])
    run([java_exe, '-jar', apksigner_jar, 'verify', '--print-certs', signed_tmp])

    final_apk = os.path.join(DIST, 'انكليزي-السادس-الاعدادي-%s.apk' % VERSION_NAME)
    shutil.copyfile(signed_tmp, final_apk)
    print('[6/6] تم التوقيع والتحقق')

    size = os.path.getsize(final_apk) / 1024.0
    print('\nتم إنشاء التطبيق:\n  %s\n  الحجم: %.0f KB' % (final_apk, size))


if __name__ == '__main__':
    main()
