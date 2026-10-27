# Generates hf/index.html (HyperFrames composition) + video/sfx.json from video/timing.json.
# Usage: python3 build.py [timing.json]
import json, sys, os, html

P = '/home/user/AI-/plans/vancouver-esl-free-edu'
TJ = sys.argv[1] if len(sys.argv) > 1 else P + '/video/timing.json'
T = json.load(open(TJ, encoding='utf-8'))
SC = {s['id']: s for s in T['scenes']}
CUES = T['cues']
TOTAL = T['total']

RED, CREAM, INK, BAND, WINE = '#C8102E', '#FFF8F2', '#2B2B2B', '#FFD6CF', '#7A1B26'
SFX = []  # (time, file, gain_db)


def c(prefix, scene=None):
    """Start time of the first cue whose text starts with prefix."""
    for q in CUES:
        if (scene is None or q['scene'] == scene) and q['text'].startswith(prefix):
            return q['start']
    raise KeyError(prefix)


def cin(sub, scene=None, frac=0.0):
    """Approximate time a substring is spoken inside a cue (linear by chars)."""
    for q in CUES:
        if (scene is None or q['scene'] == scene) and sub in q['text']:
            i = q['text'].index(sub)
            return q['start'] + (q['end'] - q['start']) * (i / max(1, len(q['text'])) + frac)
    raise KeyError(sub)


def sfx(t, f, g=-14):
    SFX.append({'t': round(t, 3), 'file': f, 'gain': g})


E = html.escape
MAPLE = ('<svg viewBox="-2015 -2000 4030 4030" class="maple" style="{st}"><path fill="{fill}" d="m-90 2030 45-863a95 95 0 0 0-111-98l-859 151 116-320a65 65 0 0 0-20-73l-941-762 212-99a65 65 0 0 0 34-79l-186-572 542 115a65 65 0 0 0 73-38l105-247 423 454a65 65 0 0 0 111-57l-204-1052 327 189a65 65 0 0 0 91-27l332-652 332 652a65 65 0 0 0 91 27l327-189-204 1052a65 65 0 0 0 111 57l423-454 105 247a65 65 0 0 0 73 38l542-115-186 572a65 65 0 0 0 34 79l212 99-941 762a65 65 0 0 0-20 73l116 320-859-151a95 95 0 0 0-111 98l45 863z"/></svg>')

JS = []  # timeline statements


def js(s):
    JS.append(s)


def scene(sid, num, title, inner):
    s = SC[sid]
    tag = '' if not num else (f'<div class="tag" id="{sid}-tag"><span class="tagnum">{num}</span>'
                              f'<span class="tagtxt">{E(title)}</span></div>')
    js(f'pop("#{sid}-tag", {s["start"] + 0.35:.3f});' if num else '')
    deco = MAPLE.format(st='right:-140px;top:-120px;width:620px;opacity:1', fill='#F9E3DE') + \
        MAPLE.format(st='left:-120px;bottom:-160px;width:420px;opacity:1', fill='#FBEAE6')
    return f'<section id="{sid}" class="scene">{deco}{tag}{inner}</section>'


# ---------- s01 opening ----------
s = SC['s01']; t0 = s['start']
s01 = scene('s01', None, '', f'''
<div id="s01-a" class="center col">
  <div id="s01-q" class="bh" style="font-size:150px;color:{INK}">영어 점수 <span style="color:{RED}">없어도?</span></div>
  <div id="s01-sub" class="nk9" style="font-size:52px;color:{WINE};margin-top:26px">밴쿠버 자녀무상교육</div>
</div>
<div id="s01-b" class="abs" style="left:110px;top:250px;width:900px">
  <div id="s01-b1" class="nk9" style="font-size:58px;color:{INK}">사설 어학원 어학연수로 시작</div>
  <div id="s01-b2" class="bh" style="font-size:230px;line-height:1.05;color:{RED};margin-top:10px">최대 1년</div>
  <div id="s01-b3" class="band nk9" style="font-size:64px">아이 학비 면제</div>
</div>
<div id="s01-doc" class="abs doc" style="left:1040px;top:250px;width:780px">
  <img src="assets/cap_bc_title.png" style="width:780px;display:block">
</div>
<div id="s01-docstamp" class="abs stamp" style="left:1480px;top:640px;font-size:44px">BC주 규정 원문</div>
<div id="s01-hello" class="abs row" style="left:110px;top:760px">
  <img src="assets/aa-canada-logo-transparent.png" style="width:92px;height:92px">
  <div class="nk9" style="font-size:52px;color:{INK};margin-left:22px">안녕하세요, <span style="color:{RED}">AA Canada</span>입니다</div>
</div>
''')
js(f'slam("#s01-q", {t0 + 0.6:.3f}); sfx_mark();'); sfx(t0 + 0.6, 'impact-bass-1.mp3', -15)
js(f'pop("#s01-sub", {c("영어 점수가 없으면", "s01"):.3f});')
tb = c('이제는', 's01')
js(f'tl.to("#s01-a", {{opacity:0, y:-60, duration:0.45, ease:"power2.in"}}, {tb - 0.1:.3f});')
js(f'pop("#s01-b1", {tb + 0.3:.3f});')
js(f'slam("#s01-b2", {cin("최대 1년", "s01"):.3f});'); sfx(cin('최대 1년', 's01'), 'impact-bass-2.mp3', -14)
js(f'wipe("#s01-b3", {c("아이 학비 면제", "s01"):.3f});'); sfx(c('아이 학비 면제', 's01'), 'whoosh-short.mp3', -18)
td = c('오늘은 BC', 's01') - 0.4
js(f'tl.fromTo("#s01-doc", {{x:900, rotation:18, scale:1.3, opacity:0}}, {{x:0, rotation:-3, scale:1, opacity:1, duration:0.55, ease:"power4.in"}}, {td:.3f});')
js(f'tl.fromTo("#s01-doc", {{y:0}}, {{y:8, duration:0.08, yoyo:true, repeat:1}}, {td + 0.55:.3f});')
sfx(td, 'whoosh.mp3', -16); sfx(td + 0.55, 'impact-bass-1.mp3', -15)
js(f'stamp("#s01-docstamp", {c("화면에 띄워", "s01"):.3f});'); sfx(c('화면에 띄워', 's01') + 0.2, 'impact-bass-2.mp3', -17)
js(f'pop("#s01-hello", {c("안녕하세요", "s01"):.3f});'); sfx(c('안녕하세요', 's01'), 'chime.mp3', -20)

# ---------- s02 principle ----------
s = SC['s02']; t0 = s['start']
PERSON = (f'<svg viewBox="0 0 40 40" style="width:58px;height:58px;flex:none"><circle cx="20" cy="13" r="8" fill="{RED}"/>'
          f'<path d="M5 38c0-9 7-15 15-15s15 6 15 15z" fill="{RED}"/></svg>')
s02 = scene('s02', '01', '원리', f'''
<div id="s02-a" class="abs" style="left:0;top:0;width:1920px;height:1080px">
  <div id="s02-h" class="abs nk9" style="left:110px;top:170px;font-size:60px;color:{INK}">BC주 공립학교 무료 = 아이가 <span style="color:{RED}">거주자</span>로 인정</div>
  <div id="s02-r1" class="abs chip row" style="left:110px;top:360px">{PERSON}<span>시민권자 · 영주권자 부모</span></div>
  <div id="s02-r2" class="abs chip row" style="left:110px;top:520px">{PERSON}<span>학생비자 · 취업비자 부모</span><em style="font-style:normal;color:{WINE};font-size:32px;margin-left:16px">(일정 조건)</em></div>
  <div id="s02-arrow" class="abs" style="left:1010px;top:470px;width:300px;height:12px;background:{RED};border-radius:6px"></div>
  <div id="s02-arrowhead" class="abs" style="left:1300px;top:452px;width:0;height:0;border-top:24px solid rgba(200,16,46,0);border-bottom:24px solid rgba(200,16,46,0);border-left:36px solid {RED}"></div>
  <div id="s02-stamp" class="abs stampc" style="left:1400px;top:330px">거주자</div>
  <div id="s02-free" class="abs band nk9" style="left:110px;top:700px;font-size:50px">교육청 학비 ✕ · 공립학교 무료</div>
</div>
<div id="s02-b" class="abs" style="left:0;top:0;width:1920px;height:1080px;opacity:0">
  <div id="s02-btitle" class="abs nk9" style="left:110px;top:130px;font-size:46px;color:{INK}">BC주 교육부 · 운영 지원금 대상 학생 규정</div>
  <div id="s02-docw" class="abs doc" style="left:250px;top:215px;width:1010px;height:570px">
    <img src="assets/cap_bc_title.png" style="width:1010px;display:block">
    <div id="s02-ul1" class="abs ul" style="left:22px;top:392px;width:388px"></div>
    <div id="s02-ul2" class="abs ul" style="left:418px;top:392px;width:158px"></div>
    <div id="s02-st" class="abs hlbox" style="left:12px;top:450px;width:160px;height:110px"></div>
  </div>
  <div id="s02-y1" class="abs bigyear" style="left:1330px;top:300px">2011<small>시행</small></div>
  <div id="s02-y2" class="abs bigyear" style="left:1330px;top:470px">2013<small>개정</small></div>
  <div id="s02-cur" class="abs stamp" style="left:1340px;top:650px;font-size:48px">현재 유효 · Current</div>
  <div class="abs src">출처: BC Ministry of Education and Child Care, Eligibility of Students for Operating Grant Funding (2026.10.27 확인)</div>
</div>
''')
js(f'pop("#s02-h", {c("BC주에서 아이가", "s02") - 0.2:.3f});')
js(f'stamp("#s02-stamp", {cin("거주자", "s02"):.3f});'); sfx(cin('거주자', 's02') + 0.2, 'impact-bass-2.mp3', -15)
js(f'slideIn("#s02-r1", {c("시민권자나", "s02"):.3f});'); sfx(c('시민권자나', 's02'), 'pop.mp3', -18)
js(f'slideIn("#s02-r2", {c("부모가 일정", "s02"):.3f});'); sfx(c('부모가 일정', 's02'), 'pop.mp3', -18)
js(f'grow("#s02-arrow", {c("부모가 일정", "s02") + 1.2:.3f}); pop("#s02-arrowhead", {c("부모가 일정", "s02") + 1.6:.3f});')
js(f'wipe("#s02-free", {cin("교육청이 학비", "s02"):.3f});')
tb = c('이 기준을', 's02')
js(f'tl.to("#s02-a", {{opacity:0, duration:0.4}}, {tb - 0.2:.3f}); tl.to("#s02-b", {{opacity:1, duration:0.5}}, {tb - 0.1:.3f});')
sfx(tb - 0.2, 'whoosh-short.mp3', -18)
js(f'tl.fromTo("#s02-docw", {{scale:0.92, y:40}}, {{scale:1.0, y:0, duration:1.0, ease:"power3.out"}}, {tb:.3f}); tl.to("#s02-docw", {{scale:1.06, duration:{SC["s02"]["start"] + SC["s02"]["dur"] - tb - 1.2:.2f}, ease:"none"}}, {tb + 1.0:.3f});')
ty = c('2011년에', 's02')
js(f'draw("#s02-ul1", {ty:.3f}); slam("#s02-y1", {ty:.3f});'); sfx(ty, 'impact-bass-1.mp3', -17)
js(f'draw("#s02-ul2", {cin("2013년", "s02"):.3f}); slam("#s02-y2", {cin("2013년", "s02"):.3f});'); sfx(cin('2013년', 's02'), 'impact-bass-1.mp3', -17)
js(f'boxOn("#s02-st", {c("지금도 유효한", "s02"):.3f}); stamp("#s02-cur", {c("지금도 유효한", "s02") + 0.1:.3f});'); sfx(c('지금도 유효한', 's02') + 0.3, 'impact-bass-2.mp3', -16)

# ---------- s03 basic conditions ----------
s = SC['s03']; t0 = s['start']
s03 = scene('s03', '02', '기본 조건', f'''
<div id="s03-h" class="abs nk9" style="left:110px;top:140px;font-size:52px;color:{INK}">부모가 <span style="color:{RED}">학생</span>일 때 기본 조건 2가지</div>
<div id="s03-docw" class="abs doc" style="left:90px;top:250px;width:910px;height:675px;transform-origin:0 0">
  <img src="assets/cap_bc_clause.png" style="width:910px;display:block">
  <div class="abs dim" style="left:0;top:0;width:910px;height:78px"></div>
  <div class="abs dim" style="left:0;top:222px;width:910px;height:453px"></div>
  <div id="s03-g" class="abs hlbox" style="left:26px;top:78px;width:875px;height:144px;border-color:#2E8B3A"></div>
  <div id="s03-ulp" class="abs ul" style="left:390px;top:186px;width:440px"></div>
</div>
<div id="s03-c1" class="abs check" style="left:1060px;top:270px"><b>✓</b><span>1년 이상 학업 허가 학생비자</span></div>
<div id="s03-c2" class="abs check" style="left:1060px;top:400px"><b>✓</b><span>공립: 학위 · 디플로마<br>사립: <em class="red">학위</em> 과정</span></div>
<div id="s03-stamp" class="abs stampc" style="left:1240px;top:560px;font-size:64px;width:420px;height:200px;border-radius:30px">사립 = 학위</div>
<div id="s03-x" class="abs xrow nk9" style="left:1100px;top:800px">사립 디플로마 · 수료증 <span class="red">✕</span></div>
<div id="s03-card" class="abs card" style="left:1180px;top:200px;width:620px"><img src="assets/card_c1.png" style="width:620px;display:block"></div>
<div id="s03-assoc" class="abs band nk9" style="left:1010px;top:710px;font-size:42px;white-space:nowrap">사립 컬리지 준학사 = Associate Degree</div>
''')
js(f'pop("#s03-h", {t0 + 0.6:.3f});')
js(f'tl.fromTo("#s03-docw", {{opacity:0, y:50, scale:0.9}}, {{opacity:1, y:0, scale:1, duration:0.7, ease:"power3.out"}}, {t0 + 1.0:.3f});')
js(f'boxOn("#s03-g", {c("첫째", "s03") - 0.3:.3f});')
js(f'check("#s03-c1", {c("첫째", "s03"):.3f});'); sfx(c('첫째', 's03'), 'pop.mp3', -17)
js(f'check("#s03-c2", {c("둘째", "s03"):.3f});'); sfx(c('둘째', 's03'), 'pop.mp3', -17)
js(f'draw("#s03-ulp", {c("또는 사립이라면", "s03"):.3f});')
js(f'stamp("#s03-stamp", {cin("사립은 학위", "s03"):.3f});'); sfx(cin('사립은 학위', 's03') + 0.2, 'impact-bass-2.mp3', -14)
js(f'pop("#s03-x", {c("사립 컬리지의 디플로마", "s03"):.3f}); tl.fromTo("#s03-x .red", {{scale:3, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:"power4.in"}}, {c("수료증", "s03"):.3f});')
sfx(c('수료증', 's03') + 0.3, 'impact-bass-1.mp3', -18)
tcard = c('그래서 저희가', 's03')
js(f'tl.to(["#s03-c1","#s03-c2","#s03-stamp","#s03-x"], {{opacity:0, duration:0.35}}, {tcard - 0.35:.3f});')
js(f'tl.fromTo("#s03-card", {{opacity:0, x:200, rotation:8}}, {{opacity:1, x:0, rotation:2, duration:0.6, ease:"power3.out"}}, {tcard:.3f});'); sfx(tcard, 'whoosh-short.mp3', -18)
js(f'wipe("#s03-assoc", {c("어소시에이트", "s03") - 0.4:.3f});')

# ---------- s04 key clause ----------
s = SC['s04']; t0 = s['start']
BX = [(87, 303, 811, 173), (87, 487, 811, 100), (87, 597, 811, 67)]
boxes = ''.join(f'<div id="s04-b{i+1}" class="abs hlbox" style="left:{x-4}px;top:{y-4}px;width:{w+8}px;height:{h+8}px"></div>' for i, (x, y, w, h) in enumerate(BX))
s04 = scene('s04', '03', '핵심 조항', f'''
<div id="s04-a" class="center col">
  <div id="s04-q" class="bh" style="font-size:120px;color:{INK}">영어 점수가 <span style="color:{RED}">없는</span> 부모님은?</div>
  <div id="s04-core" class="stamp" style="font-size:64px;margin-top:40px">오늘의 핵심</div>
</div>
<div id="s04-b" class="abs" style="left:0;top:0;width:1920px;height:1080px;opacity:0">
  <div id="s04-docw" class="abs doc" style="left:80px;top:150px;width:910px;height:675px;transform-origin:0 0">
    <img src="assets/cap_bc_clause.png" style="width:910px;display:block">
    <div id="s04-dimtop" class="abs dim" style="left:0;top:0;width:910px;height:228px"></div>
    <div id="s04-par" class="abs hlbox" style="left:30px;top:228px;width:860px;height:66px;border-color:{WINE}"></div>
    {boxes}
    <div id="s04-eqa1" class="abs ul" style="left:470px;top:370px;width:400px"></div>
    <div id="s04-eqa2" class="abs ul" style="left:90px;top:404px;width:186px"></div>
    <div id="s04-yr1" class="abs ul" style="left:640px;top:404px;width:240px;height:7px"></div>
    <div id="s04-yr2" class="abs ul" style="left:90px;top:438px;width:52px;height:7px"></div>
  </div>
  <div id="s04-all" class="abs nk9" style="left:1150px;top:170px;font-size:42px;color:{INK}">1년 이상 학업 허가 + <span class="red">3가지 모두</span></div>
  <div id="s04-n1" class="abs num"><b>①</b><div><span>EQA 인증 기관</span><small>최대 1년 영어 과정 수강</small></div></div>
  <div id="s04-eqa" class="abs pill" style="left:1220px;top:380px">EQA = BC주 교육품질인증</div>
  <div id="s04-n2" class="abs num" style="top:470px"><b>②</b><div><span>학위 과정 입학허가</span><small>공립 학위·디플로마 / 사립 학위</small></div></div>
  <div id="s04-n3" class="abs num" style="top:640px"><b>③</b><div><span>조건부 입학</span><small>영어 과정 수료가 조건</small></div></div>
  <div id="s04-max" class="abs slamtag" style="left:1180px;top:300px">어학연수 중에도<b>최대 1년</b>거주자 인정</div>
  <div class="abs src">출처: BC Ministry of Education and Child Care, Eligibility of Students for Operating Grant Funding (2026.10.27 확인)</div>
</div>
<div id="s04-c" class="abs" style="left:0;top:0;width:1920px;height:1080px;opacity:0">
  <div id="s04-vs1" class="abs vs" style="left:110px;top:220px"><small>규정에 없는 말</small><span>'대학 부설'<br>제한</span><b class="red">✕</b></div>
  <div id="s04-vs2" class="abs vs vsok" style="left:640px;top:220px"><small>규정 문구</small><span>EQA<br>지정 기관</span><b>✓</b></div>
  <div id="s04-res" class="abs band nk9" style="left:110px;top:720px;font-size:54px">EQA 인증 <span class="red">사설 어학원</span>도 같은 기준</div>
  <div id="s04-card" class="abs card" style="left:1220px;top:170px;width:600px"><img src="assets/card_c2.png" style="width:600px;display:block"></div>
</div>
''')
js(f'slam("#s04-q", {t0 + 0.7:.3f});'); sfx(t0 + 0.7, 'impact-bass-1.mp3', -15)
js(f'stamp("#s04-core", {cin("핵심", "s04"):.3f});'); sfx(cin('핵심', 's04') + 0.2, 'impact-bass-2.mp3', -14)
tb = c('규정 바로 아래', 's04')
js(f'tl.to("#s04-a", {{opacity:0, scale:0.9, duration:0.4}}, {tb - 0.3:.3f}); tl.to("#s04-b", {{opacity:1, duration:0.4}}, {tb - 0.1:.3f});'); sfx(tb - 0.3, 'whoosh.mp3', -17)
js(f'tl.fromTo("#s04-docw", {{scale:0.85, x:-40}}, {{scale:1.06, x:0, duration:0.9, ease:"power3.out"}}, {tb:.3f});')
js(f'boxOn("#s04-par", {c("1년 이상 학업이", "s04"):.3f}); pop("#s04-all", {c("다음 세 가지", "s04"):.3f});')
B = [c('하나, EQA', 's04'), c('둘, 공립', 's04'), c('셋, 그', 's04')]
for i, tt in enumerate(B):
    js(f'boxOn("#s04-b{i+1}", {tt - 0.1:.3f}); numIn("#s04-n{i+1}", {tt:.3f});')
    if i: js(f'tl.to("#s04-b{i}", {{boxShadow:"0 0 0 0 rgba(200,16,46,0)", duration:0.3}}, {tt - 0.1:.3f});')
    sfx(tt, 'impact-bass-1.mp3', -16)
js(f'pop("#s04-eqa", {c("그러니까 BC주", "s04"):.3f}); draw("#s04-eqa1", {c("그러니까 BC주", "s04"):.3f}); draw("#s04-eqa2", {c("그러니까 BC주", "s04") + 0.35:.3f});')
js(f'tl.to("#s04-eqa", {{opacity:0, duration:0.3}}, {B[1] - 0.3:.3f});')
tm = c('이 세 가지가 맞으면', 's04')
js(f'tl.to(["#s04-n1","#s04-n2","#s04-n3","#s04-all"], {{opacity:0.0, duration:0.35}}, {tm - 0.1:.3f});')
tmax = cin('최대 1년까지 거주자', 's04')
js(f'slam("#s04-max", {tmax:.3f}); draw("#s04-yr1", {tmax:.3f}); draw("#s04-yr2", {tmax + 0.3:.3f});'); sfx(tmax, 'impact-bass-2.mp3', -13)
tc = c('규정에는', 's04')
js(f'tl.to("#s04-b", {{opacity:0, duration:0.4}}, {tc - 0.35:.3f}); tl.to("#s04-c", {{opacity:1, duration:0.4}}, {tc - 0.2:.3f});'); sfx(tc - 0.35, 'whoosh-short.mp3', -18)
js(f'pop("#s04-vs1", {tc:.3f}); tl.fromTo("#s04-vs1 b", {{scale:3, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:"power4.in"}}, {cin("제한이 없고", "s04"):.3f});')
sfx(cin('제한이 없고', 's04') + 0.3, 'impact-bass-1.mp3', -17)
js(f'pop("#s04-vs2", {c("EQA 지정 기관이라고만", "s04"):.3f}); tl.fromTo("#s04-vs2 b", {{scale:3, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:"power4.in"}}, {c("EQA 지정 기관이라고만", "s04") + 0.8:.3f});')
sfx(c('EQA 지정 기관이라고만', 's04') + 1.1, 'chime.mp3', -19)
js(f'wipe("#s04-res", {c("그래서 EQA", "s04"):.3f});')
js(f'tl.fromTo("#s04-card", {{opacity:0, y:120, rotation:-6}}, {{opacity:1, y:0, rotation:-2, duration:0.6, ease:"power3.out"}}, {c("그래서 EQA", "s04") + 0.5:.3f});')

# ---------- s05 VSB ----------
s = SC['s05']; t0 = s['start']
VS = 1.16
s05 = scene('s05', '04', '밴쿠버 교육청 FAQ', f'''
<div id="s05-h" class="abs nk9" style="left:110px;top:140px;font-size:50px;color:{INK}">주정부 문서만이 아닙니다 → <span class="red">밴쿠버 교육청(VSB)</span> 신규 등록 안내</div>
<div id="s05-docw" class="abs doc" style="left:110px;top:230px;width:1020px;height:505px;transform-origin:0 0">
  <img src="assets/cap_vsb_ell.png" style="width:1020px;display:block">
  <div id="s05-q" class="abs hlbox" style="left:10px;top:0;width:1000px;height:102px;border-color:{WINE}"></div>
  <div id="s05-k1" class="abs hlbox" style="left:40px;top:186px;width:970px;height:142px"></div>
  <div id="s05-k2" class="abs hlbox" style="left:40px;top:330px;width:970px;height:70px"></div>
  <div id="s05-k3" class="abs hlbox" style="left:40px;top:402px;width:970px;height:66px"></div>
  <div id="s05-u1" class="abs ul" style="left:378px;top:289px;width:600px;height:5px"></div>
  <div id="s05-u2" class="abs ul" style="left:70px;top:323px;width:772px;height:5px"></div>
</div>
<div id="s05-badge" class="abs stamp" style="left:1380px;top:560px;font-size:42px;width:460px;text-align:center">1년 초과 시<br>국제학생 학비 가능</div>
<div class="abs src">출처: Vancouver School Board, Newcomer Welcome Centre FAQ (2026.10.27 확인)</div>
''')
js(f'pop("#s05-h", {t0 + 0.6:.3f});')
js(f'tl.fromTo("#s05-docw", {{opacity:0, scale:{VS*0.9:.3f}, y:40}}, {{opacity:1, scale:{VS:.3f}, y:0, duration:0.8, ease:"power3.out"}}, {c("밴쿠버 교육청 신규", "s05"):.3f});'); sfx(c('밴쿠버 교육청 신규', 's05'), 'whoosh-short.mp3', -18)
js(f'boxOn("#s05-q", {c("학생비자 1년", "s05"):.3f});')
tk = c('이 세 가지 조건을', 's05')
for i in range(3):
    js(f'boxOn("#s05-k{i+1}", {tk + i * 0.55:.3f});'); sfx(tk + i * 0.55, 'pop.mp3', -19)
tu = c('다만 1년이', 's05')
js(f'tl.to(["#s05-q","#s05-k1","#s05-k2","#s05-k3"], {{opacity:0.25, duration:0.3}}, {tu - 0.2:.3f});')
js(f'draw("#s05-u1", {tu:.3f}); draw("#s05-u2", {tu + 0.6:.3f}); stamp("#s05-badge", {tu + 1.4:.3f});'); sfx(tu + 1.6, 'impact-bass-2.mp3', -16)

# ---------- s06 Alexander ----------
s = SC['s06']; t0 = s['start']
NOW = ['ILSC', 'Kaplan', 'SGIC', 'Oxford International']
NOW_T = [cin('아이엘에스씨', 's06'), cin('캐플란', 's06'), cin('에스지아이씨', 's06'), cin('옥스퍼드', 's06')]
SOON = ['VanWest', 'CCEL', 'VGC']
SOON_T = [cin('밴웨스트', 's06'), cin('씨씨이엘', 's06'), cin('브이지씨', 's06')]
now_html = ''.join(f'<div id="s06-n{i}" class="school"{' style="font-size:30px"' if len(n) > 12 else ''}>{E(n)}</div>' for i, n in enumerate(NOW))
soon_html = ''.join(f'<div id="s06-s{i}" class="school soon">{E(n)}<small>곧 가능</small></div>' for i, n in enumerate(SOON))
FLOW = [('디포짓', 'CAD 5,000'), ('조건부', '입학허가'), ('협약 어학원 ESL', '최대 1년'), ('알렉산더', '준학사')]
flow_html = ''
for i, (a, b) in enumerate(FLOW):
    flow_html += f'<div id="s06-f{i}" class="fnode"><small>{E(a)}</small><span>{E(b)}</span></div>'
    if i < 3: flow_html += f'<div id="s06-fa{i}" class="farrow"></div>'
s06 = scene('s06', '05', '알렉산더 컬리지 조건부 오퍼', f'''
<div id="s06-h" class="abs nk9" style="left:110px;top:135px;font-size:48px;color:{INK}">조건부 입학, 실제로 내주는 학교? → <span class="red">Alexander College</span> <span style="font-size:34px;color:{WINE}">(2026년 10월부터)</span></div>
<div id="s06-flow" class="abs row" style="left:110px;top:240px;width:1700px;justify-content:space-between">{flow_html}</div>
<div id="s06-dep" class="abs pill" style="left:110px;top:420px">디포짓은 나중에 알렉산더 학비로 사용</div>
<div id="s06-grid" class="abs" style="left:110px;top:520px;width:1700px">
  <div class="row" style="gap:22px"><div class="glabel">지금 가능</div>{now_html}</div>
  <div class="row" style="gap:22px;margin-top:22px"><div class="glabel" style="background:{WINE}">곧 가능</div>{soon_html}</div>
</div>
<div id="s06-eqa" class="abs stamp" style="left:1290px;top:760px;font-size:40px">✓ 모두 BC EQA 지정 기관</div>
<div id="s06-doc" class="abs pill" style="left:110px;top:800px;background:{INK};color:#fff">학교: 교육청 확인용 입학 서류 지원 (공식 안내)</div>
''')
js(f'pop("#s06-h", {t0 + 0.6:.3f});')
js(f'tl.fromTo("#s06-h .red", {{scale:1.6, opacity:0}}, {{scale:1, opacity:1, duration:0.4, ease:"back.out(2)"}}, {c("알렉산더 컬리지가", "s06"):.3f});'); sfx(c('알렉산더 컬리지가', 's06'), 'impact-bass-1.mp3', -17)
FT = [cin('디포짓 5,000', 's06'), c('이수를 조건으로', 's06'), cin('어학연수 기간은', 's06'), cin('어학연수 기간은', 's06') + 1.4]
for i, tt in enumerate(FT):
    js(f'nodeIn("#s06-f{i}", {tt:.3f});'); sfx(tt, 'pop.mp3', -17)
    if i: js(f'grow("#s06-fa{i-1}", {tt - 0.35:.3f});')
js(f'slam("#s06-f0 span", {FT[0] + 0.1:.3f});'); sfx(FT[0] + 0.1, 'impact-bass-2.mp3', -16)
js(f'pop("#s06-dep", {c("디포짓은 나중에", "s06"):.3f});')
js(f'pop("#s06-grid .glabel", {c("지금 바로", "s06") - 0.2:.3f});')
for i, tt in enumerate(NOW_T):
    js(f'chipIn("#s06-n{i}", {tt - 0.1:.3f});'); sfx(tt - 0.1, 'click-soft.mp3', -14)
for i, tt in enumerate(SOON_T):
    js(f'chipIn("#s06-s{i}", {tt - 0.1:.3f});'); sfx(tt - 0.1, 'click-soft.mp3', -14)
js(f'stamp("#s06-eqa", {c("모두 BC 정부", "s06") + 0.3:.3f});'); sfx(c('모두 BC 정부', 's06') + 0.5, 'impact-bass-2.mp3', -15)
js(f'tl.to("#s06-dep", {{opacity:0, duration:0.3}}, {c("학교에서도", "s06") - 0.3:.3f}); pop("#s06-doc", {c("학교에서도", "s06"):.3f});')

# ---------- s07 plans ----------
s = SC['s07']; t0 = s['start']
s07 = scene('s07', '06', 'AA Canada 추천 플랜', f'''
<div id="s07-h" class="abs nk9" style="left:110px;top:135px;font-size:50px;color:{INK}">밴쿠버 자녀무상교육 추천 플랜 <span class="red">2가지</span></div>
<div id="s07-lanes" class="abs" style="left:0;top:0;width:1920px;height:1080px">
  <div id="s07-la" class="abs lane" style="top:250px"><div class="lname">플랜 A<small>영어 점수 있음</small></div></div>
  <div id="s07-a1" class="abs lnode" style="left:520px;top:262px">Duolingo 90 / IELTS 5.0</div>
  <div id="s07-aa" class="abs farrow" style="left:1030px;top:302px;width:90px"></div>
  <div id="s07-a2" class="abs lnode strong" style="left:1140px;top:262px">알렉산더 준학사 (학위)</div>
  <div id="s07-ack" class="abs pill" style="left:1140px;top:380px">처음부터 자녀 학비 면제 조건</div>
  <div id="s07-lb" class="abs lane" style="top:490px"><div class="lname">플랜 B<small>영어 점수 없음</small></div></div>
  <div id="s07-b1" class="abs lnode" style="left:520px;top:502px">조건부 입학허가</div>
  <div id="s07-ba1" class="abs farrow" style="left:880px;top:542px;width:60px"></div>
  <div id="s07-b2" class="abs lnode" style="left:960px;top:502px">협약 어학원 어학연수<small> 최대 1년</small></div>
  <div id="s07-ba2" class="abs farrow" style="left:1475px;top:542px;width:50px"></div>
  <div id="s07-b3" class="abs lnode strong" style="left:1545px;top:502px">준학사</div>
  <div id="s07-bar" class="abs freebar" style="left:520px;top:660px;width:1300px"><span>자녀 공립학교 학비 면제 대상</span></div>
  <div id="s07-sum" class="abs nk7" style="left:520px;top:780px;font-size:40px;color:{WINE}">부모님은 영어 준비 · 아이는 처음부터 공립학교</div>
</div>
<div id="s07-fee" class="abs" style="left:110px;top:250px;width:1000px;opacity:0">
  <div class="nk9" style="font-size:44px;color:{INK}">참고: 밴쿠버 교육청 국제학생 학비</div>
  <div class="row" style="align-items:baseline;margin-top:30px"><span class="bh" style="font-size:72px;color:{WINE}">CAD</span><span id="s07-fee1" class="bh" style="font-size:200px;color:{RED};margin-left:24px">0</span></div>
  <div class="nk7" style="font-size:40px;color:{INK}">/ 1년 학비</div>
  <div id="s07-ins" class="row" style="align-items:baseline;margin-top:40px"><span class="nk9" style="font-size:48px;color:{INK}">+ 의료보험 CAD</span><span id="s07-fee2" class="bh" style="font-size:96px;color:{RED};margin-left:18px">0</span></div>
  <div class="nk7" style="font-size:28px;color:#6b5a5a;margin-top:30px">2027-28학년도, VSB 국제교육부</div>
</div>
<div id="s07-card" class="abs card" style="left:1240px;top:190px;width:580px"><img src="assets/card_table.png" style="width:580px;display:block"></div>
''')
js(f'pop("#s07-h", {t0 + 0.6:.3f});')
js(f'slideIn("#s07-la", {c("플랜 A", "s07"):.3f});'); sfx(c('플랜 A', 's07'), 'whoosh-short.mp3', -18)
js(f'nodeIn("#s07-a1", {c("듀오링고", "s07"):.3f});'); sfx(c('듀오링고', 's07'), 'pop.mp3', -17)
js(f'grow("#s07-aa", {c("알렉산더 준학사로", "s07") - 0.2:.3f}); nodeIn("#s07-a2", {c("알렉산더 준학사로", "s07"):.3f});'); sfx(c('알렉산더 준학사로', 's07'), 'pop.mp3', -17)
js(f'pop("#s07-ack", {c("학위 과정이니까", "s07"):.3f});')
js(f'slideIn("#s07-lb", {c("플랜 B", "s07"):.3f});'); sfx(c('플랜 B', 's07'), 'whoosh-short.mp3', -18)
js(f'nodeIn("#s07-b1", {c("알렉산더 조건부", "s07"):.3f});'); sfx(c('알렉산더 조건부', 's07'), 'pop.mp3', -17)
js(f'grow("#s07-ba1", {c("어학원에서", "s07") - 0.3:.3f}); nodeIn("#s07-b2", {c("어학원에서", "s07"):.3f});'); sfx(c('어학원에서', 's07'), 'pop.mp3', -17)
js(f'grow("#s07-ba2", {c("그다음 준학사", "s07") - 0.2:.3f}); nodeIn("#s07-b3", {c("그다음 준학사", "s07"):.3f});'); sfx(c('그다음 준학사', 's07'), 'pop.mp3', -17)
js(f'tl.fromTo("#s07-bar", {{scaleX:0}}, {{scaleX:1, duration:1.6, ease:"power2.inOut"}}, {c("어학연수 최대 1년", "s07"):.3f});'); sfx(c('어학연수 최대 1년', 's07'), 'sparkle.mp3', -20)
js(f'pop("#s07-sum", {c("부모님은 영어", "s07"):.3f});')
tf = c('참고로', 's07')
js(f'tl.to("#s07-lanes", {{opacity:0, duration:0.4}}, {tf - 0.3:.3f}); tl.to("#s07-fee", {{opacity:1, duration:0.4}}, {tf:.3f});'); sfx(tf - 0.3, 'whoosh.mp3', -18)
js(f'tl.fromTo("#s07-card", {{opacity:0, x:160, rotation:6}}, {{opacity:1, x:0, rotation:1.5, duration:0.6, ease:"power3.out"}}, {tf + 0.3:.3f});')
js(f'count("#s07-fee1", 17000, {cin("17,000", "s07") - 0.6:.3f}, 1.1);'); sfx(cin('17,000', 's07') + 0.5, 'impact-bass-2.mp3', -15)
js(f'count("#s07-fee2", 1400, {c("의료보험", "s07"):.3f}, 0.9);'); sfx(c('의료보험', 's07') + 0.9, 'impact-bass-1.mp3', -17)

# ---------- s08 checks ----------
s = SC['s08']; t0 = s['start']
s08 = scene('s08', '07', '신청 전 꼭 확인할 3가지', f'''
<div id="s08-k1" class="abs ck3" style="top:200px"><b>1</b><div><span>부모 학생비자 <em class="red">1년 이상</em></span></div></div>
<div id="s08-k2" class="abs ck3" style="top:370px"><b>2</b><div><span>학위 과정 <em class="red">조건부 입학</em> 필수</span><small>어학연수만 단독 ✕</small></div></div>
<div id="s08-k2b" class="abs pill" style="left:220px;top:540px">어학연수 1년 초과 → 국제학생 학비 대상 가능</div>
<div id="s08-k3" class="abs ck3" style="top:640px"><b>3</b><div><span>최종 판단은 교육청</span><small>등록 서류를 처음부터 제대로</small></div></div>
<div id="s08-stamp" class="abs stampc" style="left:880px;top:610px;width:330px;height:170px;font-size:44px;border-radius:26px">최종 판단<br>= 교육청</div>
<div id="s08-card" class="abs card" style="left:1260px;top:200px;width:560px"><img src="assets/card_c3.png" style="width:560px;display:block"></div>
''')
js(f'tl.fromTo("#s08-card", {{opacity:0, y:80}}, {{opacity:1, y:0, duration:0.6, ease:"power3.out"}}, {t0 + 0.6:.3f});')
for k, key in [('k1', '첫째'), ('k2', '둘째'), ('k3', '셋째')]:
    js(f'slideIn("#s08-{k}", {c(key, "s08"):.3f});'); sfx(c(key, 's08'), 'pop.mp3', -16)
js(f'pop("#s08-k2b", {c("어학연수가 1년을", "s08"):.3f});')
js(f'stamp("#s08-stamp", {cin("교육청이 합니다", "s08"):.3f});'); sfx(cin('교육청이 합니다', 's08') + 0.2, 'impact-bass-2.mp3', -14)
js(f'tl.fromTo("#s08-k3 small", {{backgroundSize:"0% 100%"}}, {{backgroundSize:"100% 100%", duration:0.8}}, {c("등록 서류를", "s08"):.3f});')

# ---------- s09 closing ----------
s = SC['s09']; t0 = s['start']; tend = t0 + s['dur']
s09 = scene('s09', None, '', f'''
<div id="s09-l1" class="abs nk9" style="left:110px;top:170px;font-size:54px;color:{INK}">블로그 · 홈페이지에 <span class="red">BC주 규정 원문 링크</span></div>
<div id="s09-l1b" class="abs nk7" style="left:110px;top:250px;font-size:40px;color:{WINE}">+ 4개 주 조건 비교 정리</div>
<div id="s09-ab" class="abs row" style="left:110px;top:360px;gap:30px"><div class="planbig">플랜 A?</div><div class="planbig b">플랜 B?</div></div>
<div id="s09-l2" class="abs nk7" style="left:110px;top:540px;font-size:42px;color:{INK}">아이 나이 · 부모님 영어 상황을 남겨 주세요</div>
<div id="s09-kakao" class="abs row" style="left:110px;top:630px;gap:24px"><div class="pill big">댓글</div><div class="pill big" style="background:{INK};color:#fff">카카오톡 canlog</div><div class="pill big" style="background:#fff;color:{RED};border:3px solid {RED}">02-567-4345</div></div>
<div id="s09-logo" class="abs col" style="left:1340px;top:250px;align-items:center">
  <img src="assets/aa-canada-logo-transparent.png" style="width:360px;height:348px">
  <div class="bh" style="font-size:96px;color:{RED};margin-top:20px">AA Canada</div>
</div>
<div id="s09-fade" class="abs" style="left:0;top:0;width:1920px;height:1080px;background:{CREAM};opacity:0"></div>
''')
js(f'pop("#s09-l1", {t0 + 0.6:.3f}); pop("#s09-l1b", {c("비교는", "s09"):.3f});')
js(f'slam("#s09-ab .planbig:nth-child(1)", {cin("플랜 A", "s09"):.3f}); slam("#s09-ab .planbig:nth-child(2)", {cin("B가", "s09"):.3f});')
sfx(cin('플랜 A', 's09'), 'impact-bass-1.mp3', -17); sfx(cin('B가', 's09'), 'impact-bass-1.mp3', -17)
js(f'pop("#s09-l2", {c("아이 나이", "s09"):.3f}); pop("#s09-kakao", {c("카카오톡", "s09") - 0.3:.3f});')
js(f'tl.fromTo("#s09-logo", {{opacity:0, scale:0.6, rotation:-20}}, {{opacity:1, scale:1, rotation:0, duration:0.8, ease:"back.out(1.6)"}}, {c("AA Canada였습니다", "s09") - 0.3:.3f});')
sfx(c('AA Canada였습니다', 's09') - 0.3, 'chime.mp3', -17)
js(f'tl.to("#s09-fade", {{opacity:1, duration:1.0}}, {tend - 1.1:.3f});')

# ---------- persistent overlays: logo, footnote, subtitles ----------
s04s, s09s = SC['s04']['start'], SC['s09']['start']
over = f'''
<img id="logo" class="clip" src="assets/aa-canada-logo-transparent.png" data-start="0.4" data-duration="{s09s - 0.4:.3f}" data-track-index="2">
<div id="foot" class="clip" data-start="{s04s:.3f}" data-duration="{s09s - s04s:.3f}" data-track-index="3">※ 최종 적용 여부는 거주지 교육청이 결정합니다</div>
'''
for i, q in enumerate(CUES):
    nxt = CUES[i + 1]['start'] if i + 1 < len(CUES) else q['end'] + 1
    d = min(q['end'] + 0.15, nxt - 0.02) - q['start']
    over += f'<div id="cap{i}" class="clip cap" data-start="{q["start"]:.3f}" data-duration="{d:.3f}" data-track-index="1">{E(q["text"])}</div>\n'

trans = []
SHADERS = {'s02': 'light-leak', 's04': 'cinematic-zoom', 's09': 'light-leak'}
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
.center {{ position:absolute; left:0; top:0; width:1920px; height:1000px; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.bh {{ font-family:"BHS", sans-serif; font-weight:400; letter-spacing:-1px; }}
.nk9 {{ font-weight:900; letter-spacing:-1px; }}
.nk7 {{ font-weight:700; }}
.red {{ color:{RED}; font-style:normal; }}
.band {{ display:inline-block; background:{BAND}; color:{INK}; padding:10px 28px; border-left:12px solid {RED}; border-radius:8px; }}
.tag {{ position:absolute; left:64px; top:40px; display:flex; align-items:center; gap:16px; }}
.tagnum {{ display:inline-block; background:{RED}; color:#fff; font-family:"BHS"; font-size:36px; padding:6px 16px; border-radius:12px; }}
.tagtxt {{ font-weight:900; font-size:34px; color:{WINE}; }}
.doc {{ background:#fff; border-radius:14px; box-shadow:0 18px 50px rgba(122,27,38,0.22); overflow:hidden; }}
.doc img {{ border-radius:14px; }}
.dim {{ background:rgba(255,248,242,0.72); }}
.hlbox {{ border:6px solid {RED}; border-radius:8px; opacity:0; box-shadow:0 0 0 0 rgba(200,16,46,0); }}
.ul {{ height:6px; background:{RED}; border-radius:3px; transform-origin:0 50%; }}
.src {{ left:110px; top:892px; font-size:21px; font-weight:500; color:#7d6a6a; }}
.stamp {{ display:inline-block; color:{RED}; border:7px solid {RED}; border-radius:16px; padding:8px 26px; font-weight:900; background:rgba(255,248,242,0.92); }}
.stampc {{ width:330px; height:330px; border-radius:50%; border:12px solid {RED}; color:{RED}; display:flex; align-items:center; justify-content:center; text-align:center; font-family:"BHS"; font-size:96px; background:rgba(255,248,242,0.94); }}
.chip {{ background:#fff; border-radius:60px; padding:18px 40px 18px 22px; gap:20px; font-size:48px; font-weight:900; box-shadow:0 10px 30px rgba(122,27,38,0.14); }}
.bigyear {{ font-family:"BHS"; font-size:130px; color:{RED}; line-height:1; }}
.bigyear small {{ font-family:"NotoKR"; font-weight:900; font-size:44px; color:{INK}; margin-left:18px; }}
.check {{ display:flex; gap:24px; align-items:flex-start; font-size:46px; font-weight:900; line-height:1.3; }}
.check b {{ display:flex; width:70px; height:70px; flex:none; border-radius:50%; background:{RED}; color:#fff; align-items:center; justify-content:center; font-size:44px; }}
.xrow {{ font-size:50px; color:{INK}; text-decoration:line-through; text-decoration-color:{RED}; text-decoration-thickness:5px; }}
.xrow .red {{ display:inline-block; text-decoration:none; font-size:70px; margin-left:12px; }}
.card {{ border-radius:22px; overflow:hidden; box-shadow:0 22px 60px rgba(122,27,38,0.25); }}
.num {{ left:1150px; top:300px; width:700px; display:flex; gap:26px; align-items:center; opacity:0; }}
.num b {{ font-family:"BHS"; font-size:110px; color:{RED}; line-height:1; font-weight:400; }}
.num span {{ display:block; font-size:52px; font-weight:900; }}
.num small {{ display:block; font-size:34px; font-weight:700; color:{WINE}; margin-top:4px; }}
.pill {{ display:inline-block; background:{BAND}; color:{WINE}; font-weight:900; font-size:34px; padding:10px 26px; border-radius:40px; }}
.pill.big {{ font-size:46px; padding:16px 36px; background:{RED}; color:#fff; }}
.slamtag {{ width:680px; padding:30px 40px; background:{RED}; color:#fff; border-radius:24px; font-weight:900; font-size:44px; text-align:center; opacity:0; box-shadow:0 20px 50px rgba(200,16,46,0.35); }}
.slamtag b {{ display:block; font-family:"BHS"; font-weight:400; font-size:132px; line-height:1.1; }}
.vs {{ width:470px; height:420px; background:#fff; border-radius:26px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; box-shadow:0 14px 40px rgba(122,27,38,0.16); }}
.vs small {{ font-size:32px; font-weight:700; color:#8a7777; }}
.vs span {{ font-size:62px; font-weight:900; line-height:1.25; margin:16px 0; }}
.vs b {{ display:inline-block; font-size:96px; line-height:1; }}
.vsok {{ border:6px solid {RED}; }}
.vsok b {{ color:{RED}; }}
.fnode {{ width:330px; height:150px; background:#fff; border-radius:22px; border:5px solid {RED}; display:flex; flex-direction:column; align-items:center; justify-content:center; box-shadow:0 12px 30px rgba(122,27,38,0.16); }}
.fnode small {{ font-size:32px; font-weight:700; color:{WINE}; }}
.fnode span {{ display:inline-block; font-size:52px; font-weight:900; color:{INK}; }}
#s06-f0 span {{ color:{RED}; }} #s06-h .red {{ display:inline-block; }}
#s06-f3 {{ background:{RED}; }} #s06-f3 small, #s06-f3 span {{ color:#fff; }}
.farrow {{ width:70px; height:10px; background:{RED}; border-radius:5px; transform-origin:0 50%; }}
.glabel {{ width:190px; flex:none; background:{RED}; color:#fff; font-weight:900; font-size:34px; text-align:center; padding:26px 0; border-radius:16px; }}
.school {{ width:330px; height:100px; background:#fff; border:4px solid {RED}; border-radius:16px; display:flex; flex-direction:column; align-items:center; justify-content:center; font-size:38px; font-weight:900; color:{INK}; opacity:0; white-space:nowrap; letter-spacing:-1px; }}
.school.soon {{ border:4px dashed {WINE}; color:{WINE}; }}
.school small {{ font-size:22px; font-weight:700; color:{WINE}; }}
.lane {{ left:110px; width:1710px; height:150px; background:rgba(255,214,207,0.45); border-radius:22px; }}
.lname {{ position:absolute; left:28px; top:22px; font-family:"BHS"; font-size:64px; color:{RED}; line-height:1.05; }}
.lname small {{ display:block; font-family:"NotoKR"; font-weight:900; font-size:28px; color:{WINE}; }}
.lnode {{ height:90px; padding:0 34px; display:flex; align-items:center; background:#fff; border:4px solid {RED}; border-radius:18px; font-size:40px; font-weight:900; white-space:nowrap; }}
.lnode small {{ font-size:30px; color:{RED}; margin-left:8px; }}
.lnode.strong {{ background:{RED}; color:#fff; }}
.freebar {{ height:84px; background:{RED}; border-radius:42px; transform-origin:0 50%; display:flex; align-items:center; justify-content:center; color:#fff; font-size:42px; font-weight:900; }}
.ck3 {{ left:110px; width:1080px; display:flex; gap:30px; align-items:center; opacity:0; }}
.ck3 b {{ display:flex; width:96px; height:96px; flex:none; border-radius:22px; background:{RED}; color:#fff; font-family:"BHS"; font-weight:400; font-size:64px; align-items:center; justify-content:center; }}
.ck3 span {{ display:block; font-size:56px; font-weight:900; }}
.ck3 small {{ display:inline-block; font-size:36px; font-weight:700; color:{WINE}; margin-top:6px; background-image:linear-gradient({BAND},{BAND}); background-repeat:no-repeat; background-size:0% 100%; padding:0 8px; }}
.ck3 em {{ font-style:normal; }}
.planbig {{ font-family:"BHS"; font-size:120px; color:#fff; background:{RED}; padding:10px 46px; border-radius:26px; }}
.planbig.b {{ background:{WINE}; }}
#logo {{ position:absolute; right:48px; top:26px; width:84px; height:81px; }}
#foot {{ position:absolute; right:48px; bottom:16px; font-size:24px; font-weight:700; color:{WINE}; background:rgba(255,248,242,0.85); padding:2px 10px; border-radius:6px; }}
.capc {{ position:absolute; left:0; top:0; width:1920px; height:1080px; }}
.cap {{ position:absolute; left:50%; bottom:62px; transform:translateX(-50%); max-width:1640px; white-space:nowrap; background:rgba(43,43,43,0.88); color:#fff; font-size:46px; font-weight:700; padding:12px 34px; border-radius:14px; letter-spacing:-0.5px; }}
'''

HELPERS = '''
const tl = gsap.timeline({ paused: true });
function pop(s, t){ tl.fromTo(s, {opacity:0, y:30}, {opacity:1, y:0, duration:0.5, ease:"power3.out"}, t); }
function slideIn(s, t){ tl.fromTo(s, {opacity:0, x:-80}, {opacity:1, x:0, duration:0.55, ease:"power3.out"}, t); }
function slam(s, t){ tl.fromTo(s, {opacity:0, scale:1.9}, {opacity:1, scale:1, duration:0.32, ease:"power4.in"}, t);
  tl.fromTo(s, {x:0}, {x:6, duration:0.05, yoyo:true, repeat:3, ease:"none"}, t + 0.32); }
function stamp(s, t){ tl.fromTo(s, {opacity:0, scale:2.6, rotation:-14}, {opacity:1, scale:1, rotation:-7, duration:0.28, ease:"power4.in"}, t); }
function wipe(s, t){ tl.fromTo(s, {opacity:0, clipPath:"inset(0% 100% 0% 0%)"}, {opacity:1, clipPath:"inset(0% 0% 0% 0%)", duration:0.6, ease:"power2.out"}, t); }
function draw(s, t){ tl.fromTo(s, {scaleX:0}, {scaleX:1, duration:0.6, ease:"power2.out"}, t); }
function grow(s, t){ tl.fromTo(s, {scaleX:0, transformOrigin:"0% 50%"}, {scaleX:1, duration:0.4, ease:"power2.out"}, t); }
function boxOn(s, t){ tl.fromTo(s, {opacity:0, scale:1.06}, {opacity:1, scale:1, duration:0.35, ease:"power2.out"}, t);
  tl.fromTo(s, {boxShadow:"0 0 0 0 rgba(200,16,46,0.55)"}, {boxShadow:"0 0 0 18px rgba(200,16,46,0)", duration:0.9, ease:"power1.out"}, t + 0.2); }
function numIn(s, t){ tl.fromTo(s, {opacity:0, x:80}, {opacity:1, x:0, duration:0.5, ease:"back.out(1.6)"}, t); }
function nodeIn(s, t){ tl.fromTo(s, {opacity:0, y:40, scale:0.85}, {opacity:1, y:0, scale:1, duration:0.45, ease:"back.out(1.8)"}, t); }
function chipIn(s, t){ tl.fromTo(s, {opacity:0, scale:0.5}, {opacity:1, scale:1, duration:0.35, ease:"back.out(2.2)"}, t); }
function check(s, t){ tl.fromTo(s, {opacity:0, x:60}, {opacity:1, x:0, duration:0.45, ease:"power3.out"}, t);
  tl.fromTo(s + " b", {scale:0, rotation:-90}, {scale:1, rotation:0, duration:0.4, ease:"back.out(2)"}, t + 0.15); }
function count(s, to, t, d){ const el = document.querySelector(s); const o = {v:0};
  tl.fromTo(o, {v:0}, {v:to, duration:d, ease:"power2.out", onUpdate(){ el.textContent = Math.round(o.v).toLocaleString("en-US"); }}, t);
  tl.fromTo(s, {scale:1}, {scale:1.08, duration:0.12, yoyo:true, repeat:1}, t + d); }
function sfx_mark(){}
'''

scenes_html = s01 + s02 + s03 + s04 + s05 + s06 + s07 + s08 + s09
page = f'''<!doctype html>
<html lang="ko" data-resolution="landscape">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>밴쿠버 자녀무상교육 — 영어 점수 없어도 어학연수 1년 무상?</title>
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
{HELPERS}
{chr(10).join(x for x in JS if x)}
HyperShader.init({{
  bgColor: "{CREAM}", accentColor: "{RED}",
  scenes: {json.dumps(ids)},
  transitions: {json.dumps(trans)},
  timeline: tl,
}});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
open(P + '/hf/index.html', 'w', encoding='utf-8').write(page)
SFX.sort(key=lambda x: x['t'])
json.dump({'total': TOTAL, 'scenes': T['scenes'], 'sfx': SFX}, open(P + '/video/sfx.json', 'w'), ensure_ascii=False, indent=1)
print('wrote index.html', len(page), 'bytes;', len(SFX), 'sfx;', len(CUES), 'cues; total', TOTAL)
