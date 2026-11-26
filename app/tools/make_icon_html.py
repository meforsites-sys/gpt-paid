# -*- coding: utf-8 -*-
"""يبني ملف HTML يحتوي شعار التطبيق (SVG) لتصديره صور PNG."""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'app', 'web3', 'icon.html')

NAVY = '#1B2A55'
NAVY_D = '#111C3A'
GOLD = '#B8860B'
GOLD_L = '#D9A520'

SVG = '''<svg xmlns="http://www.w3.org/2000/svg" id="logo" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D9A520"/>
      <stop offset="55%" stop-color="#B8860B"/>
      <stop offset="100%" stop-color="#8C6508"/>
    </linearGradient>
    <linearGradient id="gold2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#E8C15A"/>
      <stop offset="100%" stop-color="#A8750A"/>
    </linearGradient>
    <clipPath id="circ"><circle cx="500" cy="500" r="490"/></clipPath>
  </defs>

  <rect width="1000" height="1000" fill="#ffffff"/>

  <g clip-path="url(#circ)">
    <!-- القوس -->
    <path d="M 120 560 A 380 380 0 0 1 880 560" fill="none" stroke="__NAVY__" stroke-width="16" stroke-linecap="round"/>

    <!-- الريشة -->
    <g transform="translate(628,300) rotate(18)">
      <path d="M0,150 C -14,80 -6,20 34,-40 C 58,-76 96,-104 120,-124 C 116,-70 104,-16 74,26 C 46,66 18,110 0,150 Z"
            fill="__NAVY__"/>
      <path d="M2,148 C 22,92 50,42 84,-14 C 96,-32 108,-52 118,-70" fill="none" stroke="#F4E3B2" stroke-width="7" stroke-linecap="round"/>
      <path d="M22,104 C 40,92 54,80 66,64 M40,74 C 58,62 72,50 84,34 M62,42 C 78,32 92,22 102,8"
            fill="none" stroke="#F4E3B2" stroke-width="5" stroke-linecap="round"/>
    </g>

    <!-- حرف A -->
    <text x="352" y="700" text-anchor="middle" font-family="Amiri" font-weight="700"
          font-size="430" fill="__NAVY__">A</text>
    <!-- حرف M -->
    <text x="628" y="700" text-anchor="middle" font-family="Amiri" font-weight="700"
          font-size="430" fill="url(#gold)">M</text>

    <!-- الموجة الذهبية -->
    <path d="M 214 556 C 300 470 372 452 452 470 C 520 486 566 470 604 430
             C 566 486 520 522 452 508 C 376 492 300 520 214 596 Z" fill="url(#gold2)"/>

    <!-- الاسم -->
    <text x="500" y="838" text-anchor="middle" font-family="Tajawal" font-weight="700"
          font-size="118" fill="__NAVY__" direction="rtl">على معز الله</text>

    <!-- الفاصل -->
    <g>
      <rect x="228" y="884" width="266" height="7" fill="url(#gold2)"/>
      <rect x="506" y="884" width="266" height="7" fill="url(#gold2)"/>
      <path d="M500,860 L524,888 L500,916 L476,888 Z" fill="url(#gold2)"/>
    </g>
  </g>
</svg>'''

HTML = '''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@font-face{font-family:'Tajawal';src:url('fonts/Tajawal-Bold.ttf') format('truetype');font-weight:700}
@font-face{font-family:'Tajawal';src:url('fonts/Tajawal-Regular.ttf') format('truetype');font-weight:400}
@font-face{font-family:'Amiri';src:url('fonts/Amiri-Bold.ttf') format('truetype');font-weight:700}
html,body{margin:0;padding:0;background:#fff}
#box{width:1000px;height:1000px}
svg{display:block}
</style></head>
<body><div id="box">__SVG__</div>
<script>
// تصدير الشعار بصور PNG بمقاسات مختلفة
window.exportIcons = function (sizes, transparent) {
  var svg = document.getElementById('logo');
  var out = {};
  var clone = svg.cloneNode(true);
  if (transparent) {
    var rects = clone.querySelectorAll('rect');
    for (var i = 0; i < rects.length; i++) {
      if (rects[i].getAttribute('width') === '1000') { rects[i].parentNode.removeChild(rects[i]); }
    }
  }
  var xml = new XMLSerializer().serializeToString(clone);
  var url = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(xml)));
  return new Promise(function (resolve) {
    var img = new Image();
    img.onload = function () {
      sizes.forEach(function (s) {
        var c = document.createElement('canvas');
        c.width = s; c.height = s;
        var ctx = c.getContext('2d');
        if (!transparent) {
          ctx.fillStyle = '#ffffff';
          ctx.fillRect(0, 0, s, s);
        }
        ctx.drawImage(img, 0, 0, s, s);
        out[s] = c.toDataURL('image/png');
      });
      resolve(out);
    };
    img.src = url;
  });
};
</script>
</body></html>'''

svg = SVG.replace('__NAVY__', NAVY)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, 'w', encoding='utf-8').write(HTML.replace('__SVG__', svg))
print('written:', OUT)
