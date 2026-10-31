# Generates hf/index.html (HyperFrames composition) + video/sfx.json from video/timing.json.
# Usage: python3 build.py
import json, html

P = '/home/user/AI-/plans/montreal-multilang-longform'
T = json.load(open(P + '/video/timing.json', encoding='utf-8'))
SC = {s['id']: s for s in T['scenes']}
CUES = T['cues']
TOTAL = T['total']
CHECKED = '2026.10.31 확인'

RED, CREAM, INK, BAND, WINE = '#C8102E', '#FFF8F2', '#2B2B2B', '#FFD6CF', '#7A1B26'
SFX = []
JS = []
E = html.escape


def c(prefix, scene):
    """Start time of the first cue in scene whose text starts with prefix."""
    for q in CUES:
        if q['scene'] == scene and q['text'].startswith(prefix):
            return q['start']
    raise KeyError(prefix)


def cin(sub, scene, frac=0.0):
    """Approximate time a substring is spoken inside a cue (linear by chars)."""
    for q in CUES:
        if q['scene'] == scene and sub in q['text']:
            i = q['text'].index(sub)
            return q['start'] + (q['end'] - q['start']) * (i / max(1, len(q['text'])) + frac)
    raise KeyError(sub)


def sfx(t, f, g=-14):
    SFX.append({'t': round(t, 3), 'file': f, 'gain': g})


def js(s):
    JS.append(s)


MAPLE = ('<svg viewBox="-2015 -2000 4030 4030" class="maple" data-layout-allow-overflow style="{st}"><path fill="{fill}" d="m-90 2030 45-863a95 95 0 0 0-111-98l-859 151 116-320a65 65 0 0 0-20-73l-941-762 212-99a65 65 0 0 0 34-79l-186-572 542 115a65 65 0 0 0 73-38l105-247 423 454a65 65 0 0 0 111-57l-204-1052 327 189a65 65 0 0 0 91-27l332-652 332 652a65 65 0 0 0 91 27l327-189-204 1052a65 65 0 0 0 111 57l423-454 105 247a65 65 0 0 0 73 38l542-115-186 572a65 65 0 0 0 34 79l212 99-941 762a65 65 0 0 0-20 73l116 320-859-151a95 95 0 0 0-111 98l45 863z"/></svg>')


def scene(sid, num, title, inner, src=None):
    s = SC[sid]
    tag = '' if not num else (f'<div class="tag" id="{sid}-tag"><span class="tagnum">{num}</span>'
                              f'<span class="tagtxt">{E(title)}</span></div>')
    if num:
        js(f'pop("#{sid}-tag", {s["start"] + 0.35:.3f});')
    srch = f'<div class="abs src" id="{sid}-src">{E(src)}</div>' if src else ''
    deco = MAPLE.format(st='right:-140px;top:-120px;width:620px', fill='#F9E3DE') + \
        MAPLE.format(st='left:-120px;bottom:-160px;width:420px', fill='#FBEAE6')
    return f'<section id="{sid}" class="scene">{deco}{tag}{srch}{inner}</section>'


def src_in(sid, t):
    js(f'tl.fromTo("#{sid}-src", {{opacity:0}}, {{opacity:1, duration:0.5}}, {t:.3f});')


# ---------- s01 opening ----------
k = 's01'; t0 = SC[k]['start']
s01 = scene(k, None, '', f'''
<div id="s01-w" class="abs" style="left:0;top:0;width:1920px;height:1080px">
  <div id="s01-en" class="abs bh kin" style="left:170px;top:150px;color:{INK}">영어?</div>
  <div id="s01-fr" class="abs bh kin" style="left:700px;top:340px;color:{RED}">불어?</div>
  <div id="s01-es" class="abs bh kin" style="left:1000px;top:530px;color:{WINE}">스페인어?</div>
</div>
<div id="s01-title" class="center col" style="align-items:center">
  <div id="s01-t1" class="bh" style="font-size:150px;color:{RED};line-height:1.05">몬트리올</div>
  <div id="s01-t2" class="bh" style="font-size:150px;color:{INK};line-height:1.05">자녀무상교육</div>
  <div id="s01-t3" class="band nk9" style="font-size:52px;margin-top:34px">숫자와 공식 자료로 답합니다</div>
</div>
<div id="s01-hello" class="abs row" style="left:0;top:770px;width:1920px;justify-content:center">
  <img src="assets/aa-canada-logo-transparent.png" style="width:96px;height:93px">
  <div class="nk9" style="font-size:52px;color:{INK};margin-left:22px">안녕하세요, <span class="red">AA Canada</span>입니다</div>
</div>
''')
for sel, tt in [('#s01-en', cin('영어에', k)), ('#s01-fr', cin('불어까지', k)), ('#s01-es', cin('스페인어', k))]:
    js(f'slam("{sel}", {tt:.3f});'); sfx(tt, 'impact-bass-1.mp3', -16)
tt = c('몬트리올 자녀', k)
js(f'tl.to("#s01-w", {{opacity:0, scale:0.86, duration:0.45, ease:"power2.in"}}, {tt - 0.35:.3f});'); sfx(tt - 0.35, 'whoosh-short.mp3', -18)
js(f'slam("#s01-t1", {tt:.3f}); slam("#s01-t2", {tt + 0.25:.3f});'); sfx(tt + 0.25, 'impact-bass-2.mp3', -14)
js(f'wipe("#s01-t3", {c("오늘은", k):.3f});')
js(f'tl.to("#s01-title", {{y:-110, duration:0.6, ease:"power2.inOut"}}, {c("안녕하세요", k) - 0.5:.3f});')
js(f'pop("#s01-hello", {c("안녕하세요", k):.3f});'); sfx(c('안녕하세요', k), 'chime.mp3', -20)

# ---------- s02 numbers ----------
k = 's02'; t0 = SC[k]['start']
DW = 1060; DS = DW / 1375  # cap_statcan_montreal 1375x413


def bx(x0, y0, x1, y1, pad=6):
    return f'left:{x0 * DS - pad:.0f}px;top:{y0 * DS - pad:.0f}px;width:{(x1 - x0) * DS + 2 * pad:.0f}px;height:{(y1 - y0) * DS + 2 * pad:.0f}px'


s02 = scene(k, '01', '숫자로 보는 몬트리올', f'''
<div id="s02-docw" class="abs doc" style="left:90px;top:200px;width:{DW}px;height:{413 * DS:.0f}px">
  <img src="assets/cap_statcan_montreal.png" style="width:{DW}px;display:block">
  <div id="s02-hl1" class="abs hlbox" style="{bx(793, 96, 1174, 132)}"></div>
  <div id="s02-hl2" class="abs hlbox" style="{bx(88, 136, 212, 172)}"></div>
  <div id="s02-ul" class="abs ul" style="left:{548 * DS:.0f}px;top:{228 * DS:.0f}px;width:{66 * DS:.0f}px"></div>
</div>
<div id="s02-n1" class="abs slamnum" style="left:1230px;top:190px"><small>3개 언어로 대화 가능</small><b class="nw">5명 중 1명</b><small>몬트리올 대도시권 · 2021</small></div>
<div id="s02-n2" class="abs slamnum" style="left:1230px;top:550px"><small>2개 언어 이상</small><b><span id="s02-pct">69.8</span>%</b><small>캐나다 대도시 중 가장 높음</small></div>
<div id="s02-defw" class="abs doc" style="left:90px;top:610px;width:880px;height:{188 * 880 / 1375:.0f}px">
  <img src="assets/cap_statcan_definition.png" style="width:880px;display:block">
</div>
<div id="s02-defl" class="abs pill" style="left:90px;top:{610 + 188 * 880 / 1375 + 18:.0f}px">대화 가능 = 본인 응답 · 유창함 보장 ✕</div>
<div id="s02-band" class="abs band nk9" style="left:1230px;top:870px;font-size:40px">여러 언어가 특별하지 않은 도시</div>
''', src='출처: Statistics Canada, The Daily, 2022.8.17 (2021 인구조사) · ' + CHECKED)
tt = c('캐나다 통계청', k)
js(f'tl.fromTo("#s02-docw", {{x:-900, rotation:-14, scale:1.25, opacity:0}}, {{x:0, rotation:-1.5, scale:1, opacity:1, duration:0.55, ease:"power4.in"}}, {tt - 0.3:.3f});')
js(f'tl.fromTo("#s02-docw", {{y:0}}, {{y:8, duration:0.08, yoyo:true, repeat:1}}, {tt + 0.25:.3f});')
sfx(tt - 0.3, 'whoosh.mp3', -17); sfx(tt + 0.25, 'impact-bass-1.mp3', -16); src_in(k, tt)
th = cin('다섯 명', k)
js(f'boxOn("#s02-hl1", {th - 0.5:.3f}); boxOn("#s02-hl2", {th - 0.2:.3f});')
js(f'slam("#s02-n1", {th:.3f});'); sfx(th, 'impact-bass-2.mp3', -14)
tp = c('두 개 언어', k)
js(f'draw("#s02-ul", {tp:.3f}); slam("#s02-n2", {tp:.3f}); countDec("#s02-pct", 69.8, {tp:.3f}, 1.1);'); sfx(tp + 1.1, 'impact-bass-2.mp3', -15)
td = c('대화할 수 있다는', k)
js(f'tl.to(["#s02-hl1","#s02-hl2"], {{opacity:0.25, duration:0.3}}, {td - 0.2:.3f});')
js(f'tl.fromTo("#s02-defw", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out"}}, {td:.3f});'); sfx(td, 'whoosh-short.mp3', -19)
js(f'pop("#s02-defl", {td + 0.8:.3f});')
js(f'wipe("#s02-band", {c("그래도 아이가", k):.3f});')

# ---------- s03 tuition ----------
k = 's03'; t0 = SC[k]['start']
s03 = scene(k, '02', '학비', f'''
<div id="s03-card" class="abs lawcard" style="left:150px;top:170px;width:1240px">
  <div id="s03-h" class="bh" style="font-size:96px;color:{RED};line-height:1.1">퀘벡 교육법 3.1조</div>
  <div class="lawrule"></div>
  <div id="s03-l1" class="lawline"><b>1</b><span>부모가 <em id="s03-res" class="hl">퀘벡에 거주</em>하는 미성년 자녀<br>→ <em id="s03-free" class="red hl">공립 초·중등 무상</em></span></div>
  <div id="s03-l2" class="lawline"><b>2</b><span>필요 서류: 부모-자녀 관계 증빙<br>+ 퀘벡 거주 증빙</span></div>
  <div id="s03-l3" class="lawline"><b>3</b><span>면제는 <em class="red">수업료</em>, 학용품 등은 별도</span></div>
</div>
<div id="s03-stamp" class="abs stampc" style="left:1450px;top:240px">수업료<br>면제</div>
<div id="s03-final" class="abs stamp" style="left:1420px;top:640px;font-size:46px">최종 판단은 교육청</div>
''', src='출처: 퀘벡 교육부, 국제학생 학비 면제 지침(2024.1판) 12~13쪽 · ' + CHECKED)
js(f'tl.fromTo("#s03-card", {{opacity:0, y:50}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, {t0 + 0.7:.3f});')
th = c('퀘벡 교육법', k)
js(f'slam("#s03-h", {th:.3f});'); sfx(th, 'impact-bass-1.mp3', -16); src_in(k, th)
for i, key in enumerate(['부모가 퀘벡에', '퀘벡 교육부 지침', '면제되는 건']):
    js(f'lineIn("#s03-l{i + 1}", {c(key, k):.3f});'); sfx(c(key, k), 'pop.mp3', -18)
js(f'tl.fromTo("#s03-res", {{backgroundSize:"0% 100%"}}, {{backgroundSize:"100% 100%", duration:0.7}}, {cin("거주하는", k):.3f});')
js(f'tl.fromTo("#s03-res", {{scale:1}}, {{scale:1.08, duration:0.25, yoyo:true, repeat:1}}, {cin("거주하는", k):.3f});')
js(f'tl.fromTo("#s03-free", {{backgroundSize:"0% 100%"}}, {{backgroundSize:"100% 100%", duration:0.8}}, {cin("무상으로", k):.3f});')
ts = cin('수업료', k)
js(f'stamp("#s03-stamp", {ts:.3f});'); sfx(ts + 0.2, 'impact-bass-2.mp3', -14)
js(f'stamp("#s03-final", {c("최종 판단은", k):.3f});'); sfx(c('최종 판단은', k) + 0.2, 'impact-bass-1.mp3', -18)

# ---------- s04 welcome class ----------
k = 's04'; t0 = SC[k]['start']
RS = 0.86  # cap_cssdm_ratio 1375x763, cropped to 940 px of width


def rbx(x0, y0, x1, y1, pad=6):
    return f'left:{x0 * RS - pad:.0f}px;top:{y0 * RS - pad:.0f}px;width:{(x1 - x0) * RS + 2 * pad:.0f}px;height:{(y1 - y0) * RS + 2 * pad:.0f}px'


s04 = scene(k, '03', '웰컴 클래스', f'''
<div id="s04-ok" class="abs nk9" style="left:110px;top:150px;font-size:56px;color:{INK}">불어를 한마디도 못 해도 <span class="red">괜찮습니다</span></div>
<div id="s04-flow" class="abs" style="left:0;top:0;width:1920px;height:1080px">
  <div id="s04-f1" class="abs fnode" style="left:110px;top:330px"><span>입학</span></div>
  <div id="s04-a1" class="abs farrow" style="left:380px;top:420px"></div>
  <div id="s04-f2" class="abs wbox" style="left:480px;top:250px">
    <div class="wtitle">웰컴 클래스 <small>불어 집중</small></div>
    <div id="s04-fr" class="wfr">classe d'accueil</div>
    <div id="s04-w1" class="wli">말하기 · 읽기 · 쓰기</div>
    <div id="s04-w2" class="wli">불어 전문 교사</div>
    <div id="s04-w3" class="wli"><em class="red">최대 17명</em></div>
  </div>
  <div id="s04-a2" class="abs farrow" style="left:1250px;top:420px"></div>
  <div id="s04-f3" class="abs fnode" style="left:1350px;top:330px"><span>일반 반</span></div>
  <svg id="s04-dash" class="abs" style="left:880px;top:160px;width:640px;height:120px;overflow:visible" viewBox="0 0 640 120">
    <path id="s04-dpath" d="M10 110 C 160 -20, 470 -20, 620 160" fill="none" stroke="{WINE}" stroke-width="6" stroke-dasharray="16 12"/>
  </svg>
  <div id="s04-dlab" class="abs pill" style="left:1040px;top:110px">학교에 따라 일부 수업은 일반 반에서</div>
  <div id="s04-per" class="abs" style="left:110px;top:680px;width:1700px">
    <div class="nk9" style="font-size:40px;color:{INK}">기간: <span class="red">정해진 기간 없음</span> · 아이마다 다름</div>
    <div class="axis"><div id="s04-range" class="range">보통 10~20개월</div></div>
  </div>
</div>
<div id="s04-cmp" class="abs" style="left:0;top:0;width:1920px;height:1080px;opacity:0">
  <div id="s04-docw" class="abs doc" style="left:90px;top:170px;width:{940 * RS:.0f}px;height:{763 * RS:.0f}px">
    <img src="assets/cap_cssdm_ratio.png" data-layout-allow-overflow style="width:{1375 * RS:.0f}px;display:block">
    <div id="s04-h17" class="abs hlbox" style="{rbx(110, 642, 400, 698)}"></div>
    <div id="s04-h28" class="abs hlbox" style="{rbx(110, 207, 450, 264)}"></div>
  </div>
  <div id="s04-n17" class="abs slamnum" style="left:1060px;top:190px"><small>웰컴 클래스 (중등) 최대</small><b><span id="s04-c17">17</span>명</b></div>
  <div id="s04-vs" class="abs bh" style="left:1335px;top:462px;font-size:64px;color:{WINE}">vs</div>
  <div id="s04-n28" class="abs slamnum grey" style="left:1060px;top:550px"><small>일반 중등 1학년 최대</small><b><span id="s04-c28">28</span>명</b></div>
  <div id="s04-small" class="abs band nk9" style="left:1060px;top:835px;font-size:44px">같은 처지 친구들과 <span class="red">작은 반</span>에서 시작</div>
</div>
''', src='출처: CSSDM, Ratio maître-élèves (' + CHECKED + ')')
js(f'pop("#s04-ok", {t0 + 0.7:.3f});')
tf = c('공립학교에는', k)
js(f'nodeIn("#s04-f1", {tf:.3f}); grow("#s04-a1", {tf + 0.3:.3f}); nodeIn("#s04-f2", {tf + 0.5:.3f}); grow("#s04-a2", {tf + 0.9:.3f}); nodeIn("#s04-f3", {tf + 1.1:.3f});')
sfx(tf, 'pop.mp3', -18); sfx(tf + 0.5, 'pop.mp3', -18); sfx(tf + 1.1, 'pop.mp3', -18)
js(f'wipe("#s04-fr", {c("불어로는", k):.3f});')
js(f'chipIn("#s04-w1", {cin("말하기", k):.3f}); chipIn("#s04-w2", {c("불어를 가르치는", k) + 0.3:.3f});')
sfx(cin('말하기', k), 'click-soft.mp3', -16)
tm = c('몬트리올 교육청', k)
js(f'chipIn("#s04-w3", {tm - 0.6:.3f});')
js(f'tl.to("#s04-flow", {{opacity:0, duration:0.4}}, {tm - 0.1:.3f}); tl.to("#s04-ok", {{opacity:0, duration:0.4}}, {tm - 0.1:.3f}); tl.to("#s04-cmp", {{opacity:1, duration:0.4}}, {tm:.3f});')
sfx(tm, 'whoosh-short.mp3', -18); src_in(k, tm)
js(f'tl.fromTo("#s04-docw", {{scale:0.9, y:40}}, {{scale:1, y:0, duration:0.8, ease:"power3.out"}}, {tm:.3f});')
t17 = cin('최대 17명', k)
js(f'boxOn("#s04-h17", {t17 - 0.3:.3f}); slam("#s04-n17", {t17:.3f}); countUp("#s04-c17", 17, {t17:.3f}, 0.7);'); sfx(t17 + 0.3, 'impact-bass-2.mp3', -14)
t28 = cin('최대 28명', k)
js(f'boxOn("#s04-h28", {t28 - 0.3:.3f}); pop("#s04-vs", {t28 - 0.3:.3f}); slam("#s04-n28", {t28:.3f}); countUp("#s04-c28", 28, {t28:.3f}, 0.7);'); sfx(t28 + 0.3, 'impact-bass-1.mp3', -15)
js(f'wipe("#s04-small", {c("같은 처지의", k):.3f});')
tp = c('기간은', k)
js(f'tl.to("#s04-cmp", {{opacity:0, duration:0.4}}, {tp - 0.4:.3f}); tl.set("#s04-src", {{opacity:0}}, {tp - 0.1:.3f}); tl.to("#s04-flow", {{opacity:1, duration:0.4}}, {tp - 0.3:.3f});')
sfx(tp - 0.4, 'whoosh-short.mp3', -19)
js(f'pop("#s04-per", {tp:.3f}); tl.fromTo("#s04-range", {{scaleX:0}}, {{scaleX:1, duration:1.2, ease:"power2.out"}}, {cin("10개월", k):.3f});')
sfx(cin('10개월', k), 'sparkle.mp3', -21)
td = c('학교에 따라서는', k)
js(f'tl.fromTo("#s04-dpath", {{strokeDashoffset:900, opacity:0}}, {{strokeDashoffset:0, opacity:1, duration:1.0, ease:"power2.out"}}, {td:.3f}); pop("#s04-dlab", {td + 0.6:.3f});')
js(f'tl.set("#s04-dpath", {{strokeDasharray:"16 12"}}, 0);')

# ---------- s05 English ----------
k = 's05'; t0 = SC[k]['start']
grades = ''.join(f'<div id="s05-g{i}" class="gnode"><b>{i}</b><small>학년</small></div>' for i in range(1, 7))
s05 = scene(k, '04', '영어', f'''
<div id="s05-h" class="abs nk9" style="left:110px;top:160px;font-size:52px;color:{INK}">퀘벡 초등학교 영어 수업</div>
<div id="s05-line" class="abs gline" style="left:150px;top:395px;width:880px"></div>
<div id="s05-gs" class="abs row" style="left:110px;top:330px;gap:42px">{grades}</div>
<div id="s05-reg" class="abs ebox" style="left:110px;top:520px">초1부터 <em class="red">정규 수업</em><small>주 평균 1시간 정도</small></div>
<div id="s05-int" class="abs ebox alt" style="left:640px;top:520px">5·6학년<small>일부 학교 집중 영어</small></div>
<div id="s05-n" class="abs slamnum" style="left:1200px;top:240px"><small>영어 · 불어 모두 하는 사람</small><b><span id="s05-pct">56.4</span>%</b><small>몬트리올 대도시권, 2021 인구조사</small></div>
<div id="s05-out" class="abs band nk9" style="left:1200px;top:640px;font-size:42px">학교 밖에서도 <span class="red">영어</span>를 접할 기회</div>
''', src='출처: 캐나다 통계청 98-200-X2021013 (2021 인구조사) · 퀘벡 교육부 · ' + CHECKED)
js(f'pop("#s05-h", {t0 + 0.6:.3f});')
tr = c('퀘벡 학교에서', k)
js(f'grow("#s05-line", {tr:.3f});')
for i in range(1, 7):
    js(f'chipIn("#s05-g{i}", {tr + 0.12 * i:.3f});')
sfx(tr, 'sparkle.mp3', -21)
t1 = cin('1학년부터', k)
js(f'tl.to("#s05-g1", {{backgroundColor:"{RED}", color:"#fff", scale:1.15, duration:0.3}}, {t1:.3f}); slideIn("#s05-reg", {t1 + 0.2:.3f});'); sfx(t1, 'pop.mp3', -17)
js(f'tl.fromTo("#s05-reg small", {{backgroundSize:"0% 100%"}}, {{backgroundSize:"100% 100%", duration:0.7}}, {c("주 평균", k):.3f});')
ti = c('일부 학교는', k)
js(f'tl.to(["#s05-g5","#s05-g6"], {{backgroundColor:"{WINE}", color:"#fff", scale:1.15, duration:0.3}}, {ti + 0.4:.3f}); slideIn("#s05-int", {ti + 0.6:.3f});'); sfx(ti + 0.4, 'pop.mp3', -17)
tn = cin('56.4', k)
js(f'slam("#s05-n", {tn - 0.3:.3f}); countDec("#s05-pct", 56.4, {tn - 0.3:.3f}, 1.0);'); sfx(tn + 0.7, 'impact-bass-2.mp3', -14); src_in(k, tn - 0.3)
js(f'wipe("#s05-out", {cin("학교 밖에서도", k):.3f});')

# ---------- s06 Spanish ----------
k = 's06'; t0 = SC[k]['start']
SCH = [('잔 망스', 'Jeanne-Mance', '시내', 'PEI · 3~5학년', c('시내의', k)),
       ('콜레주 생루이', 'Collège Saint-Louis', '라신', 'PEI · 3~4학년', c('라신의', k)),
       ('데 수르스', 'des Sources', '서부', 'PEI + 선택과목', c('서부의', k)),
       ('장 그루', 'Jean-Grou', '동부', '1학년부터', c('동부의', k))]
cards = ''.join(f'<div id="s06-c{i}" class="abs scard" style="left:{110 + i * 432}px;top:430px"><div class="sloc">{E(loc)}</div>'
                f'<div class="sko">{E(ko)}</div><div class="sfr">{E(fr)}</div><div class="sdet">{E(det)}</div></div>'
                for i, (ko, fr, loc, det, _) in enumerate(SCH))
s06 = scene(k, '05', '스페인어', f'''
<div id="s06-h" class="abs bh" style="left:110px;top:150px;font-size:96px;color:{INK}">스페인어 = <span class="red">학교 선택</span></div>
<div id="s06-pei" class="abs pill" style="left:110px;top:290px;font-size:40px">공립학교 · 국제 교육과정 PEI 운영 학교</div>
{cards}
''', src='출처: 각 학교 · 몬트리올 교육청 안내 · ' + CHECKED)
js(f'slam("#s06-h", {t0 + 0.7:.3f});'); sfx(t0 + 0.7, 'impact-bass-1.mp3', -16)
js(f'pop("#s06-pei", {c("공립학교 중에서도", k):.3f});'); src_in(k, c('공립학교 중에서도', k))
for i, s_ in enumerate(SCH):
    js(f'cardIn("#s06-c{i}", {s_[4]:.3f});'); sfx(s_[4], 'pop.mp3', -17)

# ---------- s07 our son ----------
k = 's07'; t0 = SC[k]['start']
s07 = scene(k, '06', '4개 국어는 목표', f'''
<div id="s07-kin" class="center col" style="align-items:center">
  <div class="row" style="gap:40px">
    <div id="s07-k1" class="bh kin2" style="color:{INK}">영어</div><div id="s07-d1" class="bh kin2" style="color:{BAND}">·</div>
    <div id="s07-k2" class="bh kin2" style="color:{RED}">불어</div><div id="s07-d2" class="bh kin2" style="color:{BAND}">·</div>
    <div id="s07-k3" class="bh kin2" style="color:{WINE}">독일어</div>
  </div>
</div>
<div id="s07-eq" class="abs row" style="left:0;top:330px;width:1920px;justify-content:center;gap:26px;opacity:0">
  <div id="s07-e1" class="lang">한국어</div><div id="s07-p1" class="plus">+</div><div id="s07-e2" class="lang">불어</div><div id="s07-p2" class="plus">+</div>
  <div id="s07-e3" class="lang">영어</div><div id="s07-p3" class="plus">+</div><div id="s07-e4" class="lang alpha">α</div>
</div>
<div id="s07-goal" class="abs stamp" style="left:0;top:560px;width:620px;margin-left:650px;text-align:center;font-size:72px">4개 국어 = 목표</div>
<div id="s07-nostat" class="abs pill" style="left:0;top:740px;margin-left:700px;font-size:38px">※ 공식 통계 없음 · 어디까지나 목표</div>
''')
tk = c('저희 아들도', k)
js(f'slam("#s07-k1", {cin("영어와", k):.3f}); slam("#s07-k2", {cin("불어에", k):.3f}); slam("#s07-k3", {cin("독일어", k):.3f});')
js(f'pop(["#s07-d1","#s07-d2"], {cin("불어에", k):.3f});')
for w in ['영어와', '불어에', '독일어']:
    sfx(cin(w, k), 'impact-bass-1.mp3', -17)
te = c('한국어를 집에서', k)
js(f'tl.to("#s07-kin", {{opacity:0, y:-80, duration:0.4}}, {te - 0.3:.3f}); tl.to("#s07-eq", {{opacity:1, duration:0.3}}, {te:.3f});'); sfx(te - 0.3, 'whoosh-short.mp3', -18)
for i, (w, frac) in enumerate([('한국어를', 0), ('불어,', 0), ('영어에', 0), ('하나를', 0)]):
    tt = cin(w, k) + (0.3 if i == 0 else 0)
    js(f'chipIn("#s07-e{i + 1}", {tt:.3f});'); sfx(tt, 'pop.mp3', -18)
    if i: js(f'pop("#s07-p{i}", {tt - 0.15:.3f});')
tg = cin('목표가', k)
js(f'stamp("#s07-goal", {tg:.3f});'); sfx(tg + 0.2, 'impact-bass-2.mp3', -14)
js(f'pop("#s07-nostat", {cin("공식 통계", k):.3f});')

# ---------- s08 reality check ----------
k = 's08'; t0 = SC[k]['start']
s08 = scene(k, '07', '주의할 점', f'''
<div id="s08-k1" class="abs ck3" style="top:200px"><b>1</b><div><span>PEI는 <em class="red">선발제</em></span><small>성적과 서류로 선발</small></div></div>
<div id="s08-k2" class="abs ck3" style="top:380px"><b>2</b><div><span>중간 입학 시 <em class="red">스페인어 보충</em> 필요</span><small>5학년은 입학이 안 되는 학교도</small></div></div>
<div id="s08-k3" class="abs ck3" style="top:560px"><b>3</b><div><span>프로그램은 <em class="red">매년 변동</em></span><small>지원 전 학교에 꼭 확인</small></div></div>
<div id="s08-age" class="abs col" style="left:1340px;top:200px;align-items:center">
  <div class="nk9" style="font-size:44px;color:{INK}">아이가 어릴수록</div>
  <svg viewBox="0 0 200 300" style="width:170px;height:250px;margin:10px 0"><path id="s08-arr" d="M100 290 L100 40 M40 100 L100 30 L160 100" fill="none" stroke="{RED}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <div class="bh" style="font-size:86px;color:{RED}">선택지 ↑</div>
</div>
''', src='출처: 각 학교 PEI 입학 안내 · ' + CHECKED)
for kk, key in [('k1', '피이아이는'), ('k2', '중간에'), ('k3', '프로그램은')]:
    js(f'slideIn("#s08-{kk}", {c(key, k):.3f});'); sfx(c(key, k), 'pop.mp3', -16)
src_in(k, c('피이아이는', k))
js(f'tl.fromTo("#s08-k2 small", {{backgroundSize:"0% 100%"}}, {{backgroundSize:"100% 100%", duration:0.8}}, {c("5학년은", k):.3f});')
ta = c('그래서 아이가', k)
js(f'tl.fromTo("#s08-age", {{opacity:0, y:80}}, {{opacity:1, y:0, duration:0.6, ease:"back.out(1.6)"}}, {ta:.3f});'); sfx(ta, 'sparkle.mp3', -19)
js(f'tl.fromTo("#s08-k3 small", {{backgroundSize:"0% 100%"}}, {{backgroundSize:"100% 100%", duration:0.8}}, {cin("확인하셔야", k):.3f});')

# ---------- s09 closing ----------
k = 's09'; t0 = SC[k]['start']; tend = t0 + SC[k]['dur']
s09 = scene(k, None, '', f'''
<div id="s09-sum" class="abs" style="left:0;top:0;width:1920px;height:1080px">
  <div id="s09-h" class="abs bh" style="left:110px;top:110px;font-size:80px;color:{INK}">몬트리올 = <span class="red">3개 언어</span>가 흔한 도시</div>
  <div id="s09-r1" class="abs sumrow" style="top:290px"><b>불어</b><span>웰컴 클래스에서 시작</span></div>
  <div id="s09-r2" class="abs sumrow" style="top:450px"><b>영어</b><span>정규 수업과 생활</span></div>
  <div id="s09-r3" class="abs sumrow" style="top:610px"><b>스페인어</b><span>학교 선택으로</span></div>
</div>
<div id="s09-cta" class="abs" style="left:0;top:0;width:1920px;height:1080px;opacity:0">
  <div id="s09-kakao" class="abs row" style="left:110px;top:170px;gap:24px"><div class="pill big" style="background:{INK};color:#fff;opacity:1">카카오톡 canlog</div><div class="nk9" style="font-size:46px;color:{INK}">자녀 학년만 보내 주세요</div></div>
  <div id="s09-q" class="abs qcard" style="left:110px;top:340px"><small>우리 아이는?</small><div class="row" style="gap:30px"><div class="planbig">저학년?</div><div class="planbig b">고학년?</div></div></div>
  <div id="s09-cm" class="abs pill big" style="left:110px;top:700px">댓글로 남겨 주세요</div>
  <div id="s09-logo" class="abs col" style="left:1300px;top:260px;align-items:center">
    <img src="assets/aa-canada-logo-transparent.png" style="width:380px;height:368px">
    <div class="bh" style="font-size:96px;color:{RED};margin-top:20px">AA Canada</div>
  </div>
</div>
<div id="s09-fade" class="abs" style="left:0;top:0;width:1920px;height:1080px;background:{CREAM};opacity:0"></div>
''')
js(f'pop("#s09-h", {c("몬트리올은 세 개", k):.3f});')
for i, (w, fn) in enumerate([('불어는', cin), ('영어는 정규', c), ('스페인어는 학교', c)]):
    tt = fn(w, k)
    js(f'slideIn("#s09-r{i + 1}", {tt:.3f});'); sfx(tt, 'pop.mp3', -17)
tk = c('카카오톡', k)
js(f'tl.to("#s09-sum", {{opacity:0, duration:0.4}}, {tk - 1.2:.3f}); tl.to("#s09-cta", {{opacity:1, duration:0.4}}, {tk - 1.0:.3f});'); sfx(tk - 1.2, 'whoosh-short.mp3', -18)
js(f'pop("#s09-kakao", {tk - 0.2:.3f});')
js(f'pop("#s09-q small", {c("마지막으로", k):.3f}); slam("#s09-q .planbig:nth-child(1)", {cin("저학년", k):.3f}); slam("#s09-q .planbig:nth-child(2)", {cin("고학년", k):.3f});')
sfx(cin('저학년', k), 'impact-bass-1.mp3', -17); sfx(cin('고학년', k), 'impact-bass-1.mp3', -17)
js(f'pop("#s09-cm", {c("댓글로", k):.3f});')
tl_ = c('AA Canada였습니다', k)
js(f'tl.fromTo("#s09-logo", {{opacity:0, scale:0.6, rotation:-20}}, {{opacity:1, scale:1, rotation:0, duration:0.8, ease:"back.out(1.6)"}}, {tl_ - 0.4:.3f});'); sfx(tl_ - 0.4, 'chime.mp3', -17)
js(f'tl.to("#s09-fade", {{opacity:1, duration:1.0}}, {tend - 1.1:.3f});')

# ---------- persistent overlays: logo, footnote, subtitles ----------
s03s, s09s = SC['s03']['start'], SC['s09']['start']
over = f'''
<img id="logo" class="clip" src="assets/aa-canada-logo-transparent.png" data-start="0.4" data-duration="{s09s - 0.4:.3f}" data-track-index="2">
<div id="foot" class="clip" data-start="{s03s:.3f}" data-duration="{s09s - s03s:.3f}" data-track-index="3">※ 프로그램과 입학 조건은 매년 바뀌며, 최종 판단은 교육청과 학교가 합니다 ({CHECKED})</div>
'''
for i, q in enumerate(CUES):
    nxt = CUES[i + 1]['start'] if i + 1 < len(CUES) else q['end'] + 1
    d = min(q['end'] + 0.15, nxt - 0.02) - q['start']
    over += f'<div id="cap{i}" class="clip cap" data-start="{q["start"]:.3f}" data-duration="{d:.3f}" data-track-index="1">{E(q["show"])}</div>\n'

trans = []
SHADERS = {'s02': 'light-leak', 's04': 'cinematic-zoom', 's07': 'light-leak', 's09': 'light-leak'}
ids = [s['id'] for s in T['scenes']]
for a, b in zip(ids, ids[1:]):
    tt = SC[b]['start'] - 0.45
    trans.append({'time': round(tt, 3), 'shader': SHADERS.get(b, 'cross-warp-morph'), 'duration': 0.9})
    sfx(tt, 'whoosh.mp3', -19)

CSS = f'''
@font-face {{ font-family: "BHS"; src: url("fonts/BlackHanSans-Regular.ttf"); font-weight: 400; }}
@font-face {{ font-family: "NotoKR"; src: url("fonts/NotoSansKR.ttf"); font-weight: 100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1920px; height:1080px; overflow:hidden; background:{CREAM}; }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; font-family:"NotoKR", sans-serif; color:{INK}; }}
.scene {{ position:absolute; left:0; top:0; width:1920px; height:1080px; overflow:hidden; background-color:{CREAM}; }}
.maple {{ position:absolute; }}
.abs {{ position:absolute; }}
.row {{ display:flex; flex-direction:row; align-items:center; }}
.col {{ display:flex; flex-direction:column; }}
.center {{ position:absolute; left:0; top:0; width:1920px; height:960px; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.bh {{ font-family:"BHS", sans-serif; font-weight:400; letter-spacing:-1px; }}
.nk9 {{ font-weight:900; letter-spacing:-1px; }}
.red {{ color:{RED}; font-style:normal; }}
.band {{ display:inline-block; background:{BAND}; color:{INK}; padding:10px 28px; border-left:12px solid {RED}; border-radius:8px; white-space:nowrap; }}
.tag {{ position:absolute; left:64px; top:40px; display:flex; align-items:center; gap:16px; }}
.tagnum {{ display:inline-block; background:{RED}; color:#fff; font-family:"BHS"; font-size:36px; padding:6px 16px; border-radius:12px; }}
.tagtxt {{ font-weight:900; font-size:34px; color:{WINE}; }}
.src {{ left:66px; top:100px; font-size:28px; font-weight:500; color:#7d6a6a; opacity:0; }}
.kin {{ font-size:230px; line-height:1; opacity:0; }}
.kin2 {{ font-size:190px; line-height:1; opacity:0; }}
.doc {{ background:#fff; border-radius:14px; box-shadow:0 18px 50px rgba(122,27,38,0.22); overflow:hidden; opacity:0; }}
#s04-docw {{ opacity:1; }}
.hlbox {{ border:6px solid {RED}; border-radius:8px; opacity:0; }}
.ul {{ height:6px; background:{RED}; border-radius:3px; transform-origin:0 50%; transform:scaleX(0); }}
.stamp {{ display:inline-block; color:{RED}; border:7px solid {RED}; border-radius:16px; padding:8px 26px; font-weight:900; background:rgba(255,248,242,0.94); opacity:0; }}
.stampc {{ width:330px; height:330px; border-radius:50%; border:12px solid {RED}; color:{RED}; display:flex; align-items:center; justify-content:center; text-align:center; font-family:"BHS"; font-size:86px; line-height:1.1; background:rgba(255,248,242,0.94); opacity:0; }}
.slamnum {{ width:620px; padding:26px 36px; background:{RED}; color:#fff; border-radius:24px; text-align:center; opacity:0; box-shadow:0 20px 50px rgba(200,16,46,0.3); }}
.slamnum small {{ display:block; font-weight:900; font-size:36px; }}
.slamnum b {{ display:block; font-family:"BHS"; font-weight:400; font-size:132px; line-height:1.1; }}
.slamnum b.nw {{ font-size:112px; white-space:nowrap; }}
.slamnum.grey {{ background:#fff; color:{INK}; border:5px solid #b9a9a9; box-shadow:0 14px 40px rgba(122,27,38,0.12); }}
.pill {{ display:inline-block; background:{BAND}; color:{WINE}; font-weight:900; font-size:34px; padding:10px 26px; border-radius:40px; white-space:nowrap; opacity:0; }}
.pill.big {{ font-size:46px; padding:16px 36px; background:{RED}; color:#fff; }}
.lawcard {{ background:#fff; border-radius:26px; padding:46px 60px; box-shadow:0 22px 60px rgba(122,27,38,0.18); border-top:14px solid {RED}; opacity:0; }}
.lawrule {{ height:4px; background:{BAND}; margin:22px 0 10px; }}
.lawline {{ display:flex; gap:26px; align-items:flex-start; margin-top:26px; opacity:0; }}
.lawline b {{ display:flex; width:64px; height:64px; flex:none; border-radius:16px; background:{RED}; color:#fff; font-family:"BHS"; font-weight:400; font-size:44px; align-items:center; justify-content:center; }}
.lawline span {{ font-size:46px; font-weight:900; line-height:1.3; }}
.lawline em {{ font-style:normal; }}
.hl {{ display:inline-block; background-image:linear-gradient({BAND},{BAND}); background-repeat:no-repeat; background-size:0% 100%; padding:0 6px; }}
.fnode {{ width:250px; height:180px; background:#fff; border-radius:22px; border:5px solid {RED}; display:flex; align-items:center; justify-content:center; box-shadow:0 12px 30px rgba(122,27,38,0.16); opacity:0; }}
.fnode span {{ font-size:54px; font-weight:900; color:{INK}; }}
.farrow {{ width:80px; height:12px; background:{RED}; border-radius:6px; transform-origin:0 50%; transform:scaleX(0); }}
.wbox {{ width:740px; height:350px; background:{RED}; border-radius:28px; padding:28px 40px; color:#fff; box-shadow:0 22px 60px rgba(200,16,46,0.3); opacity:0; }}
.wtitle {{ font-family:"BHS"; font-size:66px; line-height:1.1; }}
.wtitle small {{ font-family:"NotoKR"; font-weight:900; font-size:34px; margin-left:12px; background:#fff; color:{RED}; padding:2px 14px; border-radius:20px; vertical-align:middle; }}
.wfr {{ font-size:34px; font-weight:700; font-style:italic; margin:6px 0 18px; opacity:0; }}
.wli {{ display:inline-block; background:#fff; color:{INK}; font-weight:900; font-size:38px; padding:8px 22px; border-radius:14px; margin:0 12px 12px 0; opacity:0; }}
.wli em {{ font-style:normal; }}
#s04-dash path {{ opacity:0; }}
#s04-per {{ opacity:0; }}
.axis {{ position:relative; margin-top:20px; width:1300px; height:84px; background:repeating-linear-gradient(90deg, #f0dcd6 0 2px, rgba(255,248,242,0) 2px 100px); border-bottom:4px solid #d9c3bd; }}
.range {{ position:absolute; left:300px; top:6px; width:560px; height:72px; border-radius:36px; background:{RED}; color:#fff; font-weight:900; font-size:38px; display:flex; align-items:center; justify-content:center; transform-origin:0 50%; transform:scaleX(0); }}
.gline {{ height:10px; background:{BAND}; border-radius:5px; transform-origin:0 50%; transform:scaleX(0); }}
.gnode {{ width:110px; height:130px; background:#fff; border:5px solid {RED}; border-radius:20px; display:flex; flex-direction:column; align-items:center; justify-content:center; color:{INK}; opacity:0; }}
.gnode b {{ font-family:"BHS"; font-weight:400; font-size:66px; line-height:1; }}
.gnode small {{ font-weight:900; font-size:28px; }}
.ebox {{ width:480px; padding:26px 32px; background:#fff; border-radius:22px; border-left:14px solid {RED}; font-size:48px; font-weight:900; box-shadow:0 12px 30px rgba(122,27,38,0.14); opacity:0; }}
.ebox.alt {{ border-left-color:{WINE}; }}
.ebox small {{ display:block; font-size:34px; color:{WINE}; margin-top:8px; background-image:linear-gradient({BAND},{BAND}); background-repeat:no-repeat; background-size:0% 100%; }}
.ebox em {{ font-style:normal; }}
.scard {{ width:400px; height:340px; background:#fff; border-radius:24px; border-top:14px solid {RED}; padding:26px 30px; box-shadow:0 16px 40px rgba(122,27,38,0.16); opacity:0; }}
.sloc {{ display:inline-block; background:{BAND}; color:{WINE}; font-weight:900; font-size:30px; padding:4px 18px; border-radius:20px; }}
.sko {{ font-family:"BHS"; font-size:58px; color:{INK}; margin-top:18px; line-height:1.1; white-space:nowrap; letter-spacing:-1px; }}
.sfr {{ font-size:28px; font-weight:700; color:#7d6a6a; margin-top:4px; white-space:nowrap; }}
.sdet {{ font-size:40px; font-weight:900; color:{RED}; margin-top:30px; }}
.lang {{ background:#fff; border:5px solid {RED}; border-radius:22px; padding:20px 40px; font-size:66px; font-weight:900; color:{INK}; opacity:0; }}
.lang.alpha {{ background:{RED}; color:#fff; }}
.plus {{ font-family:"BHS"; font-size:80px; color:{WINE}; opacity:0; }}
.ck3 {{ left:110px; width:1150px; display:flex; gap:30px; align-items:center; opacity:0; }}
.ck3 b {{ display:flex; width:96px; height:96px; flex:none; border-radius:22px; background:{RED}; color:#fff; font-family:"BHS"; font-weight:400; font-size:64px; align-items:center; justify-content:center; }}
.ck3 span {{ display:block; font-size:54px; font-weight:900; }}
.ck3 small {{ display:inline-block; font-size:36px; font-weight:700; color:{WINE}; margin-top:6px; background-image:linear-gradient({BAND},{BAND}); background-repeat:no-repeat; background-size:0% 100%; padding:0 8px; }}
.ck3 em {{ font-style:normal; }}
#s08-age {{ opacity:0; }}
.sumrow {{ left:110px; display:flex; align-items:center; gap:34px; opacity:0; }}
.sumrow b {{ width:300px; text-align:center; background:{RED}; color:#fff; font-family:"BHS"; font-weight:400; font-size:64px; padding:12px 0; border-radius:20px; }}
.sumrow span {{ font-size:62px; font-weight:900; }}
.qcard {{ background:#fff; border-radius:28px; padding:30px 44px; box-shadow:0 16px 40px rgba(122,27,38,0.16); }}
.qcard small {{ display:block; font-size:44px; font-weight:900; color:{WINE}; margin-bottom:18px; opacity:0; }}
.planbig {{ font-family:"BHS"; font-size:110px; color:#fff; background:{RED}; padding:10px 46px; border-radius:26px; opacity:0; }}
.planbig.b {{ background:{WINE}; }}
#s09-kakao, #s09-logo {{ opacity:0; }}
#logo {{ position:absolute; right:48px; top:26px; width:84px; height:81px; }}
#foot {{ position:absolute; left:0; bottom:8px; width:1920px; text-align:center; font-size:28px; font-weight:700; color:{WINE}; }}
.cap {{ position:absolute; left:50%; bottom:56px; transform:translateX(-50%); width:max-content; max-width:1640px; text-align:center; background:rgba(43,43,43,0.88); color:#fff; font-size:46px; font-weight:700; line-height:1.3; padding:12px 34px; border-radius:14px; letter-spacing:-0.5px; }}
'''

HELPERS = '''
function pop(s, t){ tl.fromTo(s, {opacity:0, y:30}, {opacity:1, y:0, duration:0.5, ease:"power3.out"}, t); }
function slideIn(s, t){ tl.fromTo(s, {opacity:0, x:-80}, {opacity:1, x:0, duration:0.55, ease:"power3.out"}, t); }
function lineIn(s, t){ tl.fromTo(s, {opacity:0, x:-60}, {opacity:1, x:0, duration:0.5, ease:"power3.out"}, t);
  tl.fromTo(s + " b", {scale:0, rotation:-90}, {scale:1, rotation:0, duration:0.4, ease:"back.out(2)"}, t + 0.1); }
function slam(s, t){ tl.fromTo(s, {opacity:0, scale:1.9}, {opacity:1, scale:1, duration:0.32, ease:"power4.in"}, t);
  tl.fromTo(s, {x:0}, {x:6, duration:0.05, yoyo:true, repeat:3, ease:"none"}, t + 0.32); }
function stamp(s, t){ tl.fromTo(s, {opacity:0, scale:2.6, rotation:-14}, {opacity:1, scale:1, rotation:-7, duration:0.28, ease:"power4.in"}, t); }
function wipe(s, t){ tl.fromTo(s, {opacity:0, clipPath:"inset(0% 100% 0% 0%)"}, {opacity:1, clipPath:"inset(0% 0% 0% 0%)", duration:0.6, ease:"power2.out"}, t); }
function draw(s, t){ tl.fromTo(s, {scaleX:0}, {scaleX:1, duration:0.6, ease:"power2.out"}, t); }
function grow(s, t){ tl.fromTo(s, {scaleX:0, transformOrigin:"0% 50%"}, {scaleX:1, duration:0.4, ease:"power2.out"}, t); }
function boxOn(s, t){ tl.fromTo(s, {opacity:0, scale:1.08}, {opacity:1, scale:1, duration:0.35, ease:"power2.out"}, t);
  tl.fromTo(s, {boxShadow:"0 0 0 0 rgba(200,16,46,0.55)"}, {boxShadow:"0 0 0 18px rgba(200,16,46,0)", duration:0.9, ease:"power1.out"}, t + 0.2); }
function nodeIn(s, t){ tl.fromTo(s, {opacity:0, y:40, scale:0.85}, {opacity:1, y:0, scale:1, duration:0.45, ease:"back.out(1.8)"}, t); }
function chipIn(s, t){ tl.fromTo(s, {opacity:0, scale:0.5}, {opacity:1, scale:1, duration:0.35, ease:"back.out(2.2)"}, t); }
function cardIn(s, t){ tl.fromTo(s, {opacity:0, y:120, rotation:-4}, {opacity:1, y:0, rotation:0, duration:0.55, ease:"back.out(1.5)"}, t); }
function countUp(s, to, t, d){ const el = document.querySelector(s); const o = {v:0};
  tl.fromTo(o, {v:0}, {v:to, duration:d, ease:"power2.out", onUpdate(){ el.textContent = Math.round(o.v); }}, t); }
function countDec(s, to, t, d){ const el = document.querySelector(s); const o = {v:0};
  tl.fromTo(o, {v:0}, {v:to, duration:d, ease:"power2.out", onUpdate(){ el.textContent = o.v.toFixed(1); }}, t);
  tl.fromTo(s, {scale:1}, {scale:1.08, duration:0.12, yoyo:true, repeat:1}, t + d); }
'''

scenes_html = s01 + s02 + s03 + s04 + s05 + s06 + s07 + s08 + s09
page = f'''<!doctype html>
<html lang="ko" data-resolution="landscape">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>몬트리올 자녀무상교육 — 우리 아이 영어·불어·스페인어까지 가능할까?</title>
<script src="vendor/gsap.min.js"></script>
<script src="vendor/shader-transitions.global.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="{TOTAL:.3f}">
{scenes_html}
{over}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = HyperShader.init({{
  bgColor: "{CREAM}", accentColor: "{RED}",
  scenes: {json.dumps(ids)},
  transitions: {json.dumps(trans)},
}});
{HELPERS}
{chr(10).join(x for x in JS if x)}
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
open(P + '/hf/index.html', 'w', encoding='utf-8').write(page)
SFX.sort(key=lambda x: x['t'])
json.dump({'total': TOTAL, 'scenes': T['scenes'], 'sfx': SFX}, open(P + '/video/sfx.json', 'w'), ensure_ascii=False, indent=1)
print('wrote index.html', len(page), 'bytes;', len(SFX), 'sfx;', len(CUES), 'cues; total', TOTAL)
