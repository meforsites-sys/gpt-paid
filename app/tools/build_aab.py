# -*- coding: utf-8 -*-
"""يبني حزمة النشر Android App Bundle (.aab) لتطبيق انكليزي السادس الاعدادي دون Gradle.
السلسلة: aapt2 (proto-format) → d8 → bundletool build-bundle → jarsigner → bundletool validate.
"""
import io, os, sys, re, shutil, subprocess, zipfile, glob

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
APP = os.path.join(ROOT, 'app')
AND = os.path.join(APP, 'android')
WEB = os.path.join(APP, 'web')
DIST = os.path.join(APP, 'dist')
BTLIB = os.path.join(APP, 'tools', 'lib', 'bundletool-all.jar')

# أدوات Java لا تتعامل مع المسارات العربية — نعمل في مجلد مؤقت إنجليزي
TMP = os.path.join(os.environ.get('TEMP', r'C:\Windows\Temp'), 'g6aab')
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
    os.environ.get('JAVA_HOME', ''),
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
    die('لم يتم العثور على JDK')


def newest_dir(parent, prefix):
    cands = [d for d in os.listdir(parent) if d.startswith(prefix)]
    if not cands:
        die('لا يوجد ' + prefix + ' في ' + parent)
    cands.sort(key=lambda d: [int(x) if x.isdigit() else 0 for x in re.split(r'[.\-]', d)])
    return os.path.join(parent, cands[-1])


def run(cmd, env=None):
    p = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.decode('utf-8', 'replace')
    if p.returncode != 0:
        print(out[-4000:])
        die('فشل الأمر: ' + ' '.join(str(c) for c in cmd[:6]) + ' ...')
    return out


def main():
    if not os.path.isfile(BTLIB):
        die('bundletool غير موجود: ' + BTLIB)
    sdk = find_sdk()
    java = find_java()
    bt = newest_dir(os.path.join(sdk, 'build-tools'), '')
    plat = newest_dir(os.path.join(sdk, 'platforms'), 'android-')
    android_jar = os.path.join(plat, 'android.jar')
    aapt2 = os.path.join(bt, 'aapt2.exe')
    d8_jar = os.path.join(bt, 'lib', 'd8.jar')
    jarsigner = os.path.join(java, 'bin', 'jarsigner.exe')
    java_exe = os.path.join(java, 'bin', 'java.exe')
    javac = os.path.join(java, 'bin', 'javac.exe')
    print('SDK   :', sdk)
    print('Build :', bt)
    print('bundletool:', BTLIB)

    # ---------- تنظيف ----------
    if os.path.isdir(TMP):
        shutil.rmtree(TMP)
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(DIST, exist_ok=True)
    # أدوات Java ترفض المسار العربي — نسخ bundletool إلى المسار المؤقت
    btjar = os.path.join(TMP, 'bundletool.jar')
    shutil.copyfile(BTLIB, btjar)

    # ---------- أصول الويب (نفس اختيارات build_apk) ----------
    assets = os.path.join(TMP, 'assets')
    shutil.copytree(WEB, assets)
    for junk in ('data/exercises.json', 'data/app.json'):
        p = os.path.join(assets, junk)
        if os.path.exists(p):
            os.remove(p)

    # ---------- مشروع أندرويد بمسار إنجليزي ----------
    PROJ = os.path.join(TMP, 'project')
    shutil.copytree(AND, PROJ)
    res_dir = os.path.join(PROJ, 'res')
    manifest = os.path.join(PROJ, 'AndroidManifest.xml')
    java_dir = os.path.join(PROJ, 'java')

    # ---------- 1) ترجمة الموارد ----------
    res_zip = os.path.join(TMP, 'res.zip')
    run([aapt2, 'compile', '--dir', res_dir, '-o', res_zip])
    print('[1/6] تم ترجمة الموارد')

    # ---------- 2) ربط بصيغة proto (سطح وسيط AAB) ----------
    base_apk = os.path.join(TMP, 'proto.zip')
    gen_dir = os.path.join(TMP, 'gen')
    os.makedirs(gen_dir, exist_ok=True)
    run([aapt2, 'link',
         '--proto-format',
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
    print('[2/6] تم الربط بصيغة proto')

    # ---------- 3) ترجمة جافا إلى dex ----------
    classes = os.path.join(TMP, 'classes')
    os.makedirs(classes, exist_ok=True)
    srcs = [os.path.join(java_dir, 'com', 'sixth', 'grammar', 'MainActivity.java')]
    srcs += glob.glob(os.path.join(gen_dir, '**', 'R.java'), recursive=True)
    run([javac, '-encoding', 'UTF-8', '--release', '11',
         '-nowarn', '-classpath', android_jar,
         '-d', classes] + srcs)
    dex_dir = os.path.join(TMP, 'dex')
    os.makedirs(dex_dir, exist_ok=True)
    class_files = glob.glob(os.path.join(classes, '**', '*.class'), recursive=True)
    argfile = os.path.join(TMP, 'classes.txt')
    io.open(argfile, 'w', encoding='utf-8').write('\n'.join(class_files))
    run([java_exe, '-cp', d8_jar, 'com.android.tools.r8.D8',
         '--release', '--min-api', str(MIN_SDK), '--lib', android_jar,
         '--output', dex_dir, '@' + argfile])
    print('[3/6] تم إنشاء classes.dex من', len(class_files), 'صنف')

    # ---------- 4) تجميع وحدة base ----------
    with zipfile.ZipFile(base_apk) as z:
        names = z.namelist()
        z.extractall(os.path.join(TMP, 'proto_out'))
    base_dir = os.path.join(TMP, 'base')
    os.makedirs(os.path.join(base_dir, 'manifest'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'dex'), exist_ok=True)
    shutil.move(os.path.join(TMP, 'proto_out', 'AndroidManifest.xml'),
                os.path.join(base_dir, 'manifest', 'AndroidManifest.xml'))
    if os.path.exists(os.path.join(TMP, 'proto_out', 'resources.pb')):
        shutil.move(os.path.join(TMP, 'proto_out', 'resources.pb'),
                    os.path.join(base_dir, 'resources.pb'))
    else:
        die('aapt2 لم ينتج resources.pb')
    # الأصول: من ناتج الربط أو من مجلد الويب مباشرة
    a_src = os.path.join(TMP, 'proto_out', 'assets')
    if not os.path.isdir(a_src):
        a_src = assets
    shutil.copytree(a_src, os.path.join(base_dir, 'assets'))
    # ملفات الموارد الفعلية (أيقونات وصور) يشير إليها resources.pb
    if os.path.isdir(os.path.join(TMP, 'proto_out', 'res')):
        shutil.copytree(os.path.join(TMP, 'proto_out', 'res'), os.path.join(base_dir, 'res'))
    shutil.copyfile(os.path.join(dex_dir, 'classes.dex'),
                    os.path.join(base_dir, 'dex', 'classes.dex'))
    # حذف مخلفات الاستخراج غير المستخدمة
    shutil.rmtree(os.path.join(TMP, 'proto_out'), ignore_errors=True)
    print('وحدة base:', sum(len(f) for _, _, f in os.walk(base_dir)), 'ملف')

    base_zip = os.path.join(TMP, 'base.zip')
    with zipfile.ZipFile(base_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(base_dir):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, base_dir).replace('\\', '/')
                z.write(full, rel)
    print('[4/6] تم تجميع وحدة base')

    # ---------- 5) بناء الحزمة bundle ----------
    aab = os.path.join(TMP, 'app-unsigned.aab')
    run([java_exe, '-jar', btjar, 'build-bundle',
         '--modules', base_zip,
         '--output', aab])
    print('[5/6] تم بناء الحزمة (%.0f KB)' % (os.path.getsize(aab) / 1024.0))

    # ---------- 6) توقيع (v1 JAR — شرط رفع AAB إلى المتجر) ----------
    ks_tmp = os.path.join(TMP, 'release.jks')
    shutil.copyfile(KEYSTORE, ks_tmp)
    signed = os.path.join(TMP, 'app-signed.aab')
    run([jarsigner,
         '-keystore', ks_tmp,
         '-storepass', KS_PASS,
         '-keypass', KS_PASS,
         '-sigalg', 'SHA256withRSA',
         '-digestalg', 'SHA-256',
         aab, KS_ALIAS])
    # jarsigner يوقّع في المكان نفسه؛ نعيد تسميته إن لم ينشئ ملفًا جديدًا
    if not os.path.exists(signed):
        signed = aab

    # ---------- التحقق بـ bundletool ----------
    out = run([java_exe, '-jar', btjar, 'validate', '--bundle', signed])
    low = out.lower()
    if 'error' in low or 'invalid' in low or 'exception' in low:
        print(out[-2000:])
        die('فشل التحقق من الحزمة')
    print('bundletool validate: سليمة (exit 0 + لا أخطاء)')

    final = os.path.join(DIST, 'انكليزي-السادس-الاعدادي-%s.aab' % VERSION_NAME)
    shutil.copyfile(signed, final)
    print('[6/6] تم التوقيع والتحقق')
    print('\nتم إنشاء حزمة النشر:\n  %s\n  الحجم: %.0f KB' % (final, os.path.getsize(final) / 1024.0))


if __name__ == '__main__':
    main()
