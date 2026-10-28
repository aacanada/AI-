# Generates shorts/hf/<id>/index.html (9:16 HyperFrames) + shorts/<id>/sfx.json from shorts/<id>/cues.json
# Usage: python3 build_shorts.py a b c d
import json, sys, html, os

P = '/home/user/AI-/plans/vancouver-esl-free-edu/shorts'
RED, CREAM, INK, BAND, WINE = '#C8102E', '#FFF8F2', '#2B2B2B', '#FFD6CF', '#7A1B26'
E = html.escape
MAPLE = ('<svg viewBox="-2015 -2000 4030 4030" class="maple" style="{st}"><path fill="{fill}" d="m-90 2030 45-863a95 95 0 0 0-111-98l-859 151 116-320a65 65 0 0 0-20-73l-941-762 212-99a65 65 0 0 0 34-79l-186-572 542 115a65 65 0 0 0 73-38l105-247 423 454a65 65 0 0 0 111-57l-204-1052 327 189a65 65 0 0 0 91-27l332-652 332 652a65 65 0 0 0 91 27l327-189-204 1052a65 65 0 0 0 111 57l423-454 105 247a65 65 0 0 0 73 38l542-115-186 572a65 65 0 0 0 34 79l212 99-941 762a65 65 0 0 0-20 73l116 320-859-151a95 95 0 0 0-111 98l45 863z"/></svg>')
SRC_BC = '출처: BC Ministry of Education and Child Care, Eligibility of Students for Operating Grant Funding (2026.10.27 확인)'

CSS = f'''
@font-face {{ font-family:"BHS"; src:url("fonts/BlackHanSans-Regular.ttf"); }}
@font-face {{ font-family:"NotoKR"; src:url("fonts/NotoSansKR.ttf"); font-weight:100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:{CREAM}; }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; font-family:"NotoKR",sans-serif; color:{INK}; background:{CREAM}; }}
.maple {{ position:absolute; }}
.abs {{ position:absolute; }}
.row {{ display:flex; align-items:center; }}
.bh {{ font-family:"BHS"; font-weight:400; letter-spacing:-1px; line-height:1.08; }}
.n9 {{ font-weight:900; letter-spacing:-1px; }}
.red {{ color:{RED}; font-style:normal; }}
.hook {{ left:0; width:1080px; text-align:center; }}
.band {{ display:inline-block; background:{BAND}; border-left:14px solid {RED}; padding:12px 30px; border-radius:10px; font-weight:900; }}
.pill {{ display:inline-block; background:{RED}; color:#fff; font-weight:900; border-radius:50px; padding:12px 34px; }}
.doc {{ background:#fff; border-radius:14px; box-shadow:0 18px 50px rgba(122,27,38,0.22); overflow:hidden; transform-origin:0 0; }}
.hl {{ border:6px solid {RED}; border-radius:8px; opacity:0; }}
.badge {{ width:84px; height:84px; border-radius:50%; background:{RED}; color:#fff; display:flex; align-items:center; justify-content:center; font-family:"BHS"; font-size:56px; opacity:0; box-shadow:0 8px 20px rgba(200,16,46,0.35); }}
.stamp {{ color:{RED}; border:9px solid {RED}; border-radius:22px; padding:10px 34px; font-weight:900; background:rgba(255,248,242,0.95); text-align:center; }}
.slamtag {{ background:{RED}; color:#fff; border-radius:28px; font-weight:900; font-size:52px; text-align:center; padding:34px 20px; box-shadow:0 24px 60px rgba(200,16,46,0.35); opacity:0; }}
.slamtag b {{ display:block; font-family:"BHS"; font-weight:400; font-size:170px; line-height:1.1; }}
.check {{ display:flex; gap:26px; align-items:flex-start; font-size:52px; font-weight:900; line-height:1.3; opacity:0; }}
.check b {{ display:flex; width:84px; height:84px; flex:none; border-radius:50%; background:{RED}; color:#fff; align-items:center; justify-content:center; font-size:50px; }}
.check small {{ display:block; font-size:38px; font-weight:700; color:{WINE}; }}
.card {{ border-radius:24px; overflow:hidden; box-shadow:0 22px 60px rgba(122,27,38,0.25); }}
.lane {{ left:60px; width:960px; background:rgba(255,214,207,0.5); border-radius:26px; padding:26px 30px; opacity:0; }}
.lname {{ font-family:"BHS"; font-size:72px; color:{RED}; }}
.lname small {{ font-family:"NotoKR"; font-weight:900; font-size:38px; color:{WINE}; margin-left:18px; }}
.nodes {{ display:flex; flex-wrap:wrap; align-items:center; gap:14px; margin-top:18px; }}
.node {{ background:#fff; border:5px solid {RED}; border-radius:18px; padding:10px 22px; font-size:38px; font-weight:900; white-space:nowrap; opacity:0; }}
.node.strong {{ background:{RED}; color:#fff; }}
.arr {{ font-size:46px; font-weight:900; color:{RED}; opacity:0; }}
.bar {{ height:88px; border-radius:44px; background:{RED}; color:#fff; display:flex; align-items:center; justify-content:center; font-size:44px; font-weight:900; transform-origin:0 50%; }}
.ck3 {{ left:60px; width:960px; display:flex; gap:30px; align-items:flex-start; opacity:0; }}
.ck3 > b {{ display:flex; width:110px; height:110px; flex:none; border-radius:26px; background:{RED}; color:#fff; font-family:"BHS"; font-weight:400; font-size:76px; align-items:center; justify-content:center; }}
.ck3 span {{ display:block; font-size:60px; font-weight:900; line-height:1.25; }}
.ck3 small {{ display:inline-block; font-size:40px; font-weight:700; color:{WINE}; margin-top:8px; }}
.src {{ left:60px; width:960px; font-size:24px; font-weight:500; color:#7d6a6a; }}
#logo {{ position:absolute; right:40px; top:60px; width:104px; height:100px; }}
#foot {{ position:absolute; left:0; width:1080px; top:1500px; text-align:center; font-size:32px; font-weight:700; color:{WINE}; }}
.cap {{ position:absolute; left:60px; width:960px; top:1290px; display:flex; justify-content:center; }}
.cap span {{ background:rgba(43,43,43,0.9); color:#fff; font-size:54px; font-weight:700; line-height:1.3; padding:14px 34px; border-radius:16px; text-align:center; letter-spacing:-0.5px; }}
'''

HELPERS = '''
const tl = gsap.timeline({ paused: true });
function pop(s,t){ tl.fromTo(s,{opacity:0,y:40},{opacity:1,y:0,duration:0.45,ease:"power3.out"},t); }
function slam(s,t){ tl.fromTo(s,{opacity:0,scale:1.9},{opacity:1,scale:1,duration:0.3,ease:"power4.in"},t);
  tl.fromTo(s,{x:0},{x:7,duration:0.05,yoyo:true,repeat:3,ease:"none"},t+0.3); }
function stamp(s,t){ tl.fromTo(s,{opacity:0,scale:2.6,rotation:-14},{opacity:1,scale:1,rotation:-7,duration:0.28,ease:"power4.in"},t); }
function wipe(s,t){ tl.fromTo(s,{opacity:0,clipPath:"inset(0% 100% 0% 0%)"},{opacity:1,clipPath:"inset(0% 0% 0% 0%)",duration:0.55,ease:"power2.out"},t); }
function box(s,t){ tl.fromTo(s,{opacity:0,scale:1.06},{opacity:1,scale:1,duration:0.35,ease:"power2.out"},t); }
function chip(s,t){ tl.fromTo(s,{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"},t); }
function out(s,t){ tl.to(s,{opacity:0,duration:0.3},t); }
function count(s,to,t,d){ const el=document.querySelector(s); const o={v:0};
  tl.fromTo(o,{v:0},{v:to,duration:d,ease:"power2.out",onUpdate(){ el.textContent=Math.round(o.v).toLocaleString("en-US"); }},t); }
'''


def build(sid):
    D = json.load(open(f'{P}/{sid}/cues.json', encoding='utf-8'))
    CUES, TOTAL = D['cues'], D['total']
    JS, SFX = [], []

    def c(pre):
        return next(q['start'] for q in CUES if q['text'].startswith(pre))

    def cin(sub, frac=0.0):
        q = next(q for q in CUES if sub in q['text'])
        i = q['text'].index(sub)
        return q['start'] + (q['end'] - q['start']) * (i / len(q['text']) + frac)

    def js(s): JS.append(s)
    def sfx(t, f, g=-14): SFX.append({'t': round(max(0, t), 3), 'file': f, 'gain': g})

    foot = sid != 'a'
    last_end = CUES[-1]['end']
    body = ''
    if sid == 'a':
        S = 0.98
        BX = [(30, 228, 860, 66), (83, 299, 819, 181), (83, 483, 819, 108), (83, 593, 819, 75)]
        boxes = ''.join(f'<div id="a-b{i}" class="abs hl" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>' for i, (x, y, w, h) in enumerate(BX))
        badges = ''.join(f'<div id="a-n{i}" class="abs badge" style="left:6px;top:{int(520 + (BX[i][1] + BX[i][3] / 2) * S - 42)}px">{i}</div>' for i in (1, 2, 3))
        body = f'''
<div id="a-h1" class="abs hook bh" style="top:200px;font-size:112px">영어 점수 없어도</div>
<div id="a-h2" class="abs hook bh" style="top:330px;font-size:128px">학비 면제 <span class="red">최대 1년</span></div>
<div id="a-g1" class="abs" style="left:0;top:0;width:1080px;height:1280px">
  <div id="a-band" class="abs hook" style="top:600px"><div class="band" style="font-size:56px">사설 어학원 어학연수로 시작</div></div>
  <div id="a-chip" class="abs hook" style="top:760px"><div class="pill" style="font-size:52px">아이 공립학교 학비 면제</div></div>
</div>
<div id="a-docw" class="abs doc" style="left:94px;top:520px;width:910px;height:675px;opacity:0">
  <img src="assets/cap_bc_clause.png" style="width:910px;display:block">{boxes}
</div>
{badges}
<div id="a-src" class="abs src" style="top:1200px;opacity:0">{SRC_BC}</div>
<div id="a-max" class="abs slamtag" style="left:110px;top:640px;width:860px">어학연수 중에도<b>최대 1년</b>거주자 인정</div>
'''
        js('pop("#a-h1", 0.05); slam("#a-h2", 0.45);'); sfx(0.45, 'impact-bass-2.mp3', -13)
        js(f'wipe("#a-band", {c("이제는"):.3f}); chip("#a-chip", {c("아이 학비 면제"):.3f});'); sfx(c('아이 학비 면제'), 'pop.mp3', -16)
        tb = c('BC주 교육부')
        js(f'out("#a-g1", {tb - 0.3:.3f}); tl.fromTo("#a-docw", {{opacity:0, y:60, scale:{S * 0.9}}}, {{opacity:1, y:0, scale:{S}, duration:0.6, ease:"power3.out"}}, {tb:.3f}); pop("#a-src", {tb + 0.4:.3f});')
        sfx(tb, 'whoosh-short.mp3', -17)
        js(f'box("#a-b0", {c("1년 이상"):.3f});')
        for i, pre in ((1, '하나'), (2, '둘,'), (3, '셋,')):
            js(f'box("#a-b{i}", {c(pre):.3f}); chip("#a-n{i}", {c(pre):.3f});'); sfx(c(pre), 'impact-bass-1.mp3', -16)
        tm = cin('최대 1년까지 거주자')
        js(f'tl.to("#a-docw", {{opacity:0.25, duration:0.3}}, {tm - 0.3:.3f}); slam("#a-max", {tm:.3f});'); sfx(tm, 'impact-bass-2.mp3', -13)
    elif sid == 'b':
        body = f'''
<div id="b-t" class="abs hook" style="top:150px"><div class="pill" style="font-size:40px">밴쿠버 자녀무상교육</div></div>
<div id="b-h1" class="abs hook bh" style="top:250px;font-size:120px">사립 컬리지는</div>
<div id="b-h2" class="abs hook bh" style="top:385px;font-size:150px;color:{RED}">학위 과정만</div>
<div id="b-g1" class="abs" style="left:0;top:0;width:1080px;height:1280px">
  <div id="b-crop" class="abs doc" style="left:40px;top:580px;width:1000px;height:200px;opacity:0">
    <img src="assets/cap_bc_clause.png" style="position:absolute;left:-30px;top:-86px;width:1100px">
  </div>
  <div id="b-src" class="abs src" style="top:790px;opacity:0">{SRC_BC}</div>
  <div id="b-c1" class="abs check" style="left:60px;top:860px"><b>✓</b><span>1년 이상 학업 허가 학생비자</span></div>
  <div id="b-c2" class="abs check" style="left:60px;top:990px"><b>✓</b><span>공립: 학위 · 디플로마<small>사립: <em class="red" style="font-style:normal">학위</em> 과정만</small></span></div>
</div>
<div id="b-g2" class="abs" style="left:0;top:0;width:1080px;height:1280px">
  <div id="b-stamp" class="abs" style="left:240px;top:640px;opacity:0"><div class="stamp bh" style="font-size:110px;width:600px">사립 = 학위</div></div>
  <div id="b-x" class="abs hook n9" style="top:960px;font-size:60px;opacity:0"><span style="text-decoration:line-through;text-decoration-color:{RED};text-decoration-thickness:6px">사립 디플로마 · 수료증</span> <span class="red">✕</span></div>
</div>
<div id="b-card" class="abs card" style="left:220px;top:520px;width:640px;opacity:0"><img src="assets/card_c1.png" style="width:640px;display:block"></div>
<div id="b-assoc" class="abs hook" style="top:1035px"><div class="band" style="font-size:50px">사립 컬리지 준학사 = Associate Degree</div></div>
'''
        js('pop("#b-t", 0.05); pop("#b-h1", 0.2); slam("#b-h2", 0.6);'); sfx(0.6, 'impact-bass-2.mp3', -13)
        js(f'tl.fromTo("#b-crop", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.5}}, {c("부모가 학생"):.3f}); pop("#b-src", {c("부모가 학생") + 0.3:.3f});')
        js(f'pop("#b-c1", {c("첫째"):.3f}); pop("#b-c2", {c("둘째"):.3f});'); sfx(c('첫째'), 'pop.mp3', -16); sfx(c('둘째'), 'pop.mp3', -16)
        ts = cin('사립은 학위')
        js(f'out("#b-g1", {ts - 0.5:.3f}); stamp("#b-stamp", {ts:.3f});'); sfx(ts + 0.2, 'impact-bass-2.mp3', -13)
        js(f'pop("#b-x", {c("사립 컬리지의 디플로마"):.3f});'); sfx(c('수료증') + 0.2, 'impact-bass-1.mp3', -17)
        tc = c('그래서 저희가')
        js(f'out("#b-g2", {tc - 0.3:.3f}); tl.fromTo("#b-card", {{opacity:0, y:80, rotation:4}}, {{opacity:1, y:0, rotation:1.5, duration:0.6, ease:"power3.out"}}, {tc:.3f}); wipe("#b-assoc", {c("어소시에이트") - 0.3:.3f});')
        sfx(tc, 'whoosh-short.mp3', -17)
    elif sid == 'c':
        body = f'''
<div id="c-t" class="abs hook" style="top:150px"><div class="pill" style="font-size:40px">밴쿠버 자녀무상교육 추천</div></div>
<div id="c-h1" class="abs hook bh" style="top:250px;font-size:140px"><span class="red">플랜 A</span> vs <span style="color:{WINE}">플랜 B</span></div>
<div id="c-g1" class="abs" style="left:0;top:0;width:1080px;height:1280px">
  <div id="c-la" class="abs lane" style="top:430px">
    <div class="lname">플랜 A<small>영어 점수 있음</small></div>
    <div class="nodes"><div id="c-a1" class="node">Duolingo 90 / IELTS 5.0</div><div id="c-aa" class="arr">→</div><div id="c-a2" class="node strong">알렉산더 준학사 (학위)</div></div>
    <div id="c-ack" class="n9" style="font-size:40px;color:{WINE};margin-top:16px;opacity:0">✓ 처음부터 자녀 학비 면제 조건</div>
  </div>
  <div id="c-lb" class="abs lane" style="top:855px">
    <div class="lname">플랜 B<small>영어 점수 없음</small></div>
    <div class="nodes"><div id="c-b1" class="node">조건부 입학허가</div><div id="c-ba1" class="arr">→</div><div id="c-b2" class="node">어학연수 최대 1년</div><div id="c-ba2" class="arr">→</div><div id="c-b3" class="node strong">준학사</div></div>
  </div>
  <div id="c-bar" class="abs bar" style="left:60px;top:1200px;width:960px;height:76px">자녀 공립학교 학비 면제 대상</div>
</div>
<div id="c-fee" class="abs" style="left:60px;top:520px;width:960px;opacity:0">
  <div class="n9" style="font-size:50px">참고: 밴쿠버 교육청 국제학생 학비</div>
  <div class="row" style="align-items:baseline;margin-top:30px"><span class="bh" style="font-size:80px;color:{WINE}">CAD</span><span id="c-f1" class="bh" style="font-size:220px;color:{RED};margin-left:24px">0</span></div>
  <div class="n9" style="font-size:44px">/ 1년 학비</div>
  <div class="row" style="align-items:baseline;margin-top:40px"><span class="n9" style="font-size:54px">+ 의료보험 CAD</span><span id="c-f2" class="bh" style="font-size:110px;color:{RED};margin-left:18px">0</span></div>
  <div style="font-size:32px;font-weight:700;color:#6b5a5a;margin-top:30px">2027-28학년도, VSB 국제교육부</div>
</div>
'''
        js('pop("#c-t", 0.05); slam("#c-h1", 0.35);'); sfx(0.35, 'impact-bass-2.mp3', -13)
        js(f'pop("#c-la", {c("플랜 A."):.3f}); chip("#c-a1", {c("듀오링고"):.3f}); pop("#c-aa", {c("알렉산더 준학사로") - 0.2:.3f}); chip("#c-a2", {c("알렉산더 준학사로"):.3f}); pop("#c-ack", {c("학위 과정이니까"):.3f});')
        js(f'pop("#c-lb", {c("플랜 B."):.3f}); chip("#c-b1", {c("알렉산더 조건부"):.3f}); pop("#c-ba1", {c("어학원에서") - 0.2:.3f}); chip("#c-b2", {c("어학원에서"):.3f}); pop("#c-ba2", {c("그다음 준학사") - 0.2:.3f}); chip("#c-b3", {c("그다음 준학사"):.3f});')
        for k in ('플랜 A.', '듀오링고', '알렉산더 준학사로', '플랜 B.', '알렉산더 조건부', '어학원에서', '그다음 준학사'):
            sfx(c(k), 'pop.mp3', -16)
        js(f'tl.fromTo("#c-bar", {{scaleX:0}}, {{scaleX:1, duration:1.4, ease:"power2.inOut"}}, {c("어학연수 최대 1년"):.3f});'); sfx(c('어학연수 최대 1년'), 'sparkle.mp3', -19)
        tf = c('참고로')
        js(f'out("#c-g1", {tf - 0.3:.3f}); tl.to("#c-fee", {{opacity:1, duration:0.4}}, {tf:.3f}); count("#c-f1", 17000, {cin("17,000") - 0.6:.3f}, 1.1); count("#c-f2", 1400, {c("의료보험"):.3f}, 0.9);')
        sfx(tf - 0.3, 'whoosh-short.mp3', -17); sfx(cin('17,000') + 0.5, 'impact-bass-2.mp3', -14); sfx(c('의료보험') + 0.9, 'impact-bass-1.mp3', -16)
    elif sid == 'd':
        body = f'''
<div id="d-t" class="abs hook" style="top:150px"><div class="pill" style="font-size:40px">밴쿠버 자녀무상교육</div></div>
<div id="d-h1" class="abs hook bh" style="top:250px;font-size:112px">신청 전 꼭 확인</div>
<div id="d-h2" class="abs hook bh" style="top:370px;font-size:170px;color:{RED}">3가지</div>
<div id="d-k1" class="abs ck3" style="top:590px"><b>1</b><div><span>부모 학생비자 <em class="red" style="font-style:normal">1년 이상</em></span></div></div>
<div id="d-k2" class="abs ck3" style="top:740px"><b>2</b><div><span>학위 과정 <em class="red" style="font-style:normal">조건부 입학</em> 필수</span><small>어학연수만 단독 ✕</small></div></div>
<div id="d-k2b" class="abs" style="left:200px;top:905px;opacity:0"><div class="band" style="font-size:38px">1년 초과 → 국제학생 학비 대상 가능</div></div>
<div id="d-k3" class="abs ck3" style="top:995px"><b>3</b><div><span>최종 판단은 교육청</span><small>등록 서류를 처음부터 제대로</small></div></div>
<div id="d-stamp" class="abs" style="left:790px;top:960px;opacity:0"><div class="stamp" style="font-size:38px">최종 판단<br>= 교육청</div></div>
'''
        js('pop("#d-t", 0.05); pop("#d-h1", 0.15); slam("#d-h2", 0.5);'); sfx(0.5, 'impact-bass-2.mp3', -13)
        for k, pre in (('k1', '첫째'), ('k2', '둘째'), ('k3', '셋째')):
            js(f'pop("#d-{k}", {c(pre):.3f});'); sfx(c(pre), 'pop.mp3', -15)
        js(f'pop("#d-k2b", {c("어학연수가 1년을"):.3f}); stamp("#d-stamp", {cin("교육청이 합니다"):.3f});'); sfx(cin('교육청이 합니다') + 0.2, 'impact-bass-2.mp3', -13)

    # end contact pill
    body += f'<div id="end" class="abs hook" style="top:1185px;opacity:0"><div class="pill" style="font-size:44px;background:{INK}">상담: 카카오톡 canlog · 02-567-4345</div></div>'
    if sid == 'a': js(f'out("#a-src", {last_end:.3f});')
    js(f'pop("#end", {last_end + 0.1:.3f});')
    caps = ''
    for i, q in enumerate(CUES):
        nxt = CUES[i + 1]['start'] if i + 1 < len(CUES) else q['end'] + 0.6
        d = min(q['end'] + 0.15, nxt - 0.02) - q['start']
        caps += f'<div id="cap{i}" class="clip cap" data-start="{q["start"]:.3f}" data-duration="{d:.3f}" data-track-index="1"><span>{E(q["text"])}</span></div>\n'
    deco = MAPLE.format(st='right:-200px;top:-120px;width:640px', fill='#F9E3DE') + MAPLE.format(st='left:-160px;top:1560px;width:520px', fill='#FBEAE6')
    footdiv = f'<div id="foot" class="clip" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="3">※ 최종 적용 여부는 거주지 교육청이 결정합니다</div>' if foot else ''
    page = f'''<!doctype html>
<html lang="ko"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="vendor/gsap.min.js"></script><style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{TOTAL:.3f}">
{deco}
<img id="logo" class="clip" src="assets/aa-canada-logo-transparent.png" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="2">
{body}
{footdiv}
{caps}
</div>
<script>
{HELPERS}
{chr(10).join(JS)}
tl.to("#root", {{opacity:1, duration:0.01}}, {TOTAL - 0.05:.3f});
window.__timelines["main"] = tl;
</script>
</body></html>'''
    os.makedirs(f'{P}/src', exist_ok=True); open(f'{P}/src/short_{sid}.html', 'w', encoding='utf-8').write(page)
    SFX.sort(key=lambda x: x['t'])
    json.dump({'total': TOTAL, 'sfx': SFX}, open(f'{P}/{sid}/sfx.json', 'w'), indent=1)
    print(sid, 'total', TOTAL, 'sfx', len(SFX))


for s in sys.argv[1:]:
    build(s)
