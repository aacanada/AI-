"""Generate the three 1080x1920 VanWest prep shorts as standalone HyperFrames projects.

Run from the project root:  python3 -I tools/shorts.py
Outputs: ../vanwest-shorts/short-*/index.html (assets symlinked to this project)
"""
import difflib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import BASE_CSS, FONTS, JS_HELPERS  # noqa: E402

ROOT = os.path.dirname(HERE)
SHORTS_ROOT = os.path.join(os.path.dirname(ROOT), "vanwest-shorts")
P = "assets/photos/"
VDIR = "assets/voice-shorts"
LEAD, TAIL = 0.4, 2.4
MUSIC = 0.4
CAP_FIX = (("캔로그", "canlog"), ("밴 웨스트", "밴웨스트"))


def timing(n):
    al = json.load(open(os.path.join(ROOT, VDIR, f"line{n:02d}.align.json"), encoding="utf-8"))
    stt = json.load(open(os.path.join(ROOT, VDIR, f"line{n:02d}.stt.json"), encoding="utf-8"))
    text = al["text"]
    sc, st = [], []
    for w in stt["words"]:
        if w.get("type") != "word":
            continue
        for ch in w["text"]:
            if not ch.isspace():
                sc.append(ch); st.append((w["start"], w["end"]))
    tc = [(k, c) for k, c in enumerate(text) if not c.isspace()]
    m = {}
    for a, b, size in difflib.SequenceMatcher(None, [c for _, c in tc], sc, autojunk=False).get_matching_blocks():
        for x in range(size):
            m[tc[a + x][0]] = st[b + x]

    def at(k, end=False):
        for j in (range(k, -1, -1) if end else range(k, len(text))):
            if j in m:
                return m[j][1] if end else m[j][0]

    rows, pos = [], 0
    for row in text.split("\n"):
        rows.append({"t": round(LEAD + at(pos), 2), "end": round(LEAD + at(pos + len(row) - 1, True), 2), "text": row})
        pos += len(row) + 1
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                         os.path.join(ROOT, VDIR, f"line{n:02d}.mp3")]))
    mark = lambda sub: round(LEAD + at(text.index(sub)), 2)  # noqa: E731
    return rows, dur, mark


def chunks(text, mx=16):
    words, out, cur = text.split(), [], ""
    for w in words:
        nxt = (cur + " " + w).strip()
        if len(nxt) > mx and cur:
            out.append(cur); cur = w
        else:
            cur = nxt
    if cur:
        if out and len(cur) <= 4:
            out[-1] += " " + cur
        else:
            out.append(cur)
    return out


SHORT_CSS = """
R .scap{position:absolute;left:0;right:0;top:1420px;display:flex;justify-content:center;z-index:90}
R .scap span{display:inline-block;max-width:940px;background:rgba(22,50,79,.9);color:#FAF6EF;font-weight:800;font-size:50px;line-height:1.3;padding:12px 30px;border-radius:16px;text-align:center}
R .brand{position:absolute;left:60px;top:190px;z-index:80}
R .endph{position:absolute;inset:0;overflow:hidden}
R .endph img{width:100%;height:100%;object-fit:cover;object-position:30% 35%}
R .endsh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(22,50,79,0) 25%,rgba(22,50,79,.92) 60%)}
R .endcard{position:absolute;left:60px;top:1010px;width:960px;height:330px;background:#FAF6EF;border-radius:30px;padding:40px 48px}
R .blk{position:absolute;left:60px;width:960px;border-radius:30px;padding:34px 44px;color:#fff}
R .blk .k{font-weight:700;font-size:32px;letter-spacing:.08em;opacity:.9}
R .blk .v{font-weight:900;font-size:66px;margin-top:8px;line-height:1.2}
R .wc{position:absolute;left:60px;width:960px;height:150px;border-radius:28px;background:#fff;box-shadow:0 14px 30px rgba(22,50,79,.15);padding:30px 44px}
R .wc b{font-weight:900;font-size:66px;color:#16324F}
R .wc span{position:absolute;right:44px;top:44px;font-weight:800;font-size:52px;color:#146A77}
R .wk{position:absolute;width:465px;height:150px;border-radius:26px;background:#fff;border:4px solid rgba(22,50,79,.14);padding:22px 30px;color:#16324F}
R .wk .n{font-weight:800;font-size:30px;color:#146A77}
R .wk .v{font-weight:800;font-size:42px;margin-top:6px}
R .slot{position:absolute;width:280px;height:70px;border-radius:16px;background:#1F8A99;color:#fff;font-weight:800;font-size:32px;text-align:center;line-height:70px}
R .slot span{position:absolute;left:0;right:0;top:0}
R .slot .sb{opacity:0}
"""


def end_html(sid, head):
    return f"""
          <div class="endph" id="{sid}-eph"><img src="{P}50-vanwest-students.jpg" alt="" /></div>
          <div class="endsh" id="{sid}-esh"></div>
          <div class="abs h" id="{sid}-eh" style="left:60px;top:820px;width:960px;font-size:72px;color:#fff">{head}</div>
          <div class="endcard" id="{sid}-ec"><div class="h" style="font-size:76px">AA캐나다</div><div class="hd" style="font-size:50px;margin-top:18px">전화 02-567-4345</div><div class="hd" style="font-size:50px;margin-top:6px">카카오톡 <span style="color:#146A77">canlog</span></div></div>"""


def end_js(sid, at):
    return f"""
tl.fromTo('#{sid}-eph',{{opacity:0}},{{opacity:1,duration:0.6}},{at});kb('#{sid}-eph img',{at},D-{at},{{s:1.0}},{{s:1.08}});
tl.fromTo('#{sid}-esh',{{opacity:0}},{{opacity:1,duration:0.6}},{at});
inn('#{sid}-eh',{at}+0.3,{{y:30}});inn('#{sid}-ec',{at}+0.6,{{y:60,d:0.7}});
"""


SHORTS = []

# ---------------------------------------------------------------- A: English from day one
BUB = [("Hi! Where are you from?", 60, 330, -3), ("Open your textbook!", 420, 470, 2), ("Group project due Friday!", 90, 610, 2)]
SHORTS.append(dict(
    sid="sa", file="short-a-english", n=1, marks={"kel": "켈로나의", "am": "오전에는", "pm": "오후에는", "wk": "기간은"},
    body=f"""
          <div class="abs" id="sa-ph" style="left:0;top:0;width:1080px;height:1920px;overflow:hidden"><img src="{P}15-classroom-teacher.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:60% 50%" /></div>
          <div class="abs" id="sa-sh" style="inset:0;background:linear-gradient(180deg,rgba(22,50,79,.2) 0%,rgba(22,50,79,.35) 50%,rgba(22,50,79,.9) 75%)"></div>
          {"".join(f'<div class="abs" id="sa-b{i}" style="left:{x}px;top:{y}px;background:#FAF6EF;border-radius:34px;padding:22px 36px;font-weight:800;font-size:48px;white-space:nowrap;box-shadow:0 14px 30px rgba(0,0,0,.25)">{t}</div>' for i, (t, x, y, r) in enumerate(BUB))}
          <div class="abs h" id="sa-h1" style="left:60px;top:1000px;width:960px;font-size:104px;line-height:1.15;color:#fff">첫날부터<br /><span style="color:#F3C969">모든 대화가 영어</span></div>
          <div class="abs h" id="sa-pct" style="left:60px;top:330px;font-size:230px;color:#1F8A99;font-variant-numeric:tabular-nums;line-height:1">0%</div>
          <div class="abs hd" id="sa-pctl" style="left:66px;top:570px;font-size:58px">현지 캐나다 학생</div>
          <div class="abs" id="sa-grid" style="left:210px;top:690px;width:660px;height:660px"></div>
          <div class="chip sand" id="sa-k0" style="left:60px;top:300px;font-size:44px;padding:16px 34px">버논에 가기 전, 켈로나에서</div>
          <div class="pol" id="sa-p1" style="left:110px;top:420px;width:860px;height:720px"><div class="ph"><img src="{P}60-campus-exterior.jpg" alt="" /></div><div class="cap">VanWest College · Kelowna</div></div>
          <div class="chip solid" id="sa-k1" style="left:60px;top:1210px;font-size:44px;padding:16px 34px">버논까지 차로 약 40분</div>
          <div class="blk" id="sa-am" style="top:320px;height:260px;background:#1F8A99"><div class="k">오전</div><div class="v">아카데믹 영어<br />EAP</div></div>
          <div class="blk" id="sa-pm" style="top:610px;height:260px;background:#16324F"><div class="k" style="color:#F3C969">오후</div><div class="v">공립학교<br />수업 용어</div></div>
          <div class="abs" id="sa-sl" style="left:60px;top:960px;width:960px;height:240px">
            <div class="abs" style="left:0;top:90px;width:960px;height:20px;border-radius:10px;background:rgba(22,50,79,.15)"></div>
            <div class="abs" id="sa-fill" style="left:0;top:90px;width:960px;height:20px;border-radius:10px;background:#E8572B;transform-origin:0 50%"></div>
            <div class="abs h" style="left:0;top:130px;font-size:60px">8주</div>
            <div class="abs h" style="left:820px;top:130px;font-size:60px">24주</div>
            <div class="abs hd" id="sa-wk" style="left:280px;top:0;width:400px;text-align:center;font-size:58px;color:#C2410C">기간 선택</div>
          </div>
{end_html("sa", "버논 조기유학 준비 상담")}""",
    js="""
kb('#sa-ph img',0,R[1],{s:1.12},{s:1.0});
qa('[id^=sa-b]').forEach((b,i)=>tl.fromTo(b,{opacity:0,scale:0.4,rotation:0},{opacity:1,scale:1,rotation:[-3,2,2][i],duration:0.45,ease:'back.out(2)'},0.3+i*0.6));
inn('#sa-h1',0.6,{y:40});
outt(['#sa-ph','#sa-sh','#sa-h1','#sa-b0','#sa-b1','#sa-b2'],R[1]-0.3);
inn('#sa-pct',R[1],{y:30});count('#sa-pct',0,95,R[1]+0.1,2.0,v=>Math.round(v)+'%');inn('#sa-pctl',R[1]+0.8,{y:16});
(function(){const g=q('#sa-grid');for(let i=0;i<100;i++){const d=document.createElement('div');d.style.cssText='position:absolute;width:52px;height:52px;border-radius:50%;background:'+(i>=95?'#E8572B':'#1F8A99')+';left:'+((i%10)*66)+'px;top:'+(Math.floor(i/10)*66)+'px';g.appendChild(d);}})();
qa('#sa-grid div').forEach((d,i)=>tl.fromTo(d,{scale:0,opacity:0},{scale:1,opacity:1,duration:0.3,ease:'power3.out'},R[1]+0.2+((i%10)+Math.floor(i/10))*0.035));
outt(['#sa-pct','#sa-pctl','#sa-grid'],R[2]-0.3,{y:-30});
inn('#sa-k0',R[2],{s:0.7,y:0});pol('#sa-p1',M.kel-0.2,-3);kb('#sa-p1 img',M.kel-0.2,R[3]-M.kel,{s:1},{s:1.1});inn('#sa-k1',M.kel+1.0,{y:20});
outt(['#sa-k0','#sa-p1','#sa-k1'],R[3]-0.3,{y:-30});
inn('#sa-am',M.am-0.2,{x:-60,y:0});inn('#sa-pm',M.pm-0.2,{x:-60,y:0});
inn('#sa-sl',M.wk-0.3,{y:30});tl.fromTo('#sa-fill',{scaleX:0.33},{scaleX:1,duration:1.6,ease:'power2.inOut'},M.wk+0.4);
outt(['#sa-am','#sa-pm','#sa-sl'],R[4]-0.3,{y:-30});
""" + end_js("sa", "R[4]-0.2"),
))

# ---------------------------------------------------------------- B: terms
WORDS = [("equation", "방정식", "eq"), ("perimeter", "둘레", "pe"), ("denominator", "분모", "de")]
WEEKS = ["쓰기·공부 요령", "수학", "진로·생활", "역사와 문화", "영어 읽기·쓰기", "디자인·예술", "과학", "건강과 체력"]
SHORTS.append(dict(
    sid="sb", file="short-b-terms", n=2, marks={"eq": "방정식", "pe": "둘레", "de": "분모", "hist": "역사", "w": "8주 동안"},
    body=f"""
          <div class="abs h" id="sb-h1" style="left:60px;top:320px;width:960px;font-size:100px;line-height:1.15">캐나다 수학 시간,<br /><span style="color:#E8572B">왜 막힐까?</span></div>
          <div class="pol" id="sb-p1" style="left:150px;top:650px;width:780px;height:640px"><div class="ph"><img src="{P}63-campus-classroom.jpg" alt="" /></div><div class="cap">math class</div></div>
          <div class="abs h" id="sb-a" style="left:60px;top:400px;font-size:80px;color:#4A5F78">수학을 못 하는 게<br />아니라</div>
          <div class="abs" id="sb-strike" style="left:50px;top:470px;width:740px;height:12px;background:#E8572B;border-radius:6px"></div>
          <div class="abs h" id="sb-b" style="left:60px;top:680px;font-size:120px;line-height:1.15"><span style="background:linear-gradient(transparent 62%,#F3C969 62%)">용어</span>를<br />모르는 것</div>
          {"".join(f'<div class="wc" id="sb-w{i}" style="top:{330 + i * 190}px"><b>{e}</b><span>{k}</span></div>' for i, (e, k, _) in enumerate(WORDS))}
          {"".join(f'<div class="abs" id="sb-s{i}" style="left:{60 + i * 330}px;top:930px;width:300px;height:200px;border-radius:28px;background:#16324F;color:#FAF6EF;text-align:center;font-weight:900;font-size:76px;line-height:200px">{t}</div>' for i, t in enumerate(["역사", "지리", "문학"]))}
          <div class="abs hd" id="sb-s-l" style="left:60px;top:1160px;font-size:44px;color:#E8572B">더 어려운 과목</div>
          <div class="abs hd" id="sb-wt" style="left:60px;top:300px;width:960px;font-size:56px;line-height:1.3">밴웨스트 공립학교 준비 과정<br /><span style="color:#146A77">8주 · 매주 다른 과목 용어</span></div>
          {"".join(f'<div class="wk" id="sb-k{i}" style="left:{60 + (i % 2) * 495}px;top:{500 + (i // 2) * 175}px"><div class="n">{i + 1}주</div><div class="v">{w}</div></div>' for i, w in enumerate(WEEKS))}
{end_html("sb", "입학 전 8주의 준비")}""",
    js="""
inn('#sb-h1',0.15,{y:40,d:0.5});pol('#sb-p1',0.5,-3);kb('#sb-p1 img',0.5,R[1],{s:1},{s:1.1});
outt(['#sb-h1','#sb-p1'],R[1]-0.3,{y:-40});
inn('#sb-a',R[1],{y:24});tl.fromTo('#sb-strike',{scaleX:0,transformOrigin:'0% 50%'},{scaleX:1,duration:0.5},R[1]+1.4);
inn('#sb-b',R[1]+2.0,{y:30});
outt(['#sb-a','#sb-strike','#sb-b'],R[2]-0.3,{y:-30});
inn('#sb-w0',M.eq-0.2,{x:-60,y:0});inn('#sb-w1',M.pe-0.2,{x:-60,y:0});inn('#sb-w2',M.de-0.2,{x:-60,y:0});
qa('#sb-s0,#sb-s1,#sb-s2').forEach((s,i)=>inn(s,M.hist+i*0.5,{y:40,s:0.8}));inn('#sb-s-l',M.hist+1.6,{y:16});
outt(['#sb-w0','#sb-w1','#sb-w2','#sb-s0','#sb-s1','#sb-s2','#sb-s-l'],R[3]-0.3,{y:-30});
inn('#sb-wt',R[3],{y:20});
qa('.wk').forEach((w,i)=>{inn(w,R[3]+0.5+i*0.12,{y:30,d:0.45});tl.to(w,{backgroundColor:'#146A77',borderColor:'#146A77',color:'#fff',duration:0.3},M.w+0.3+i*0.45);tl.to(w.querySelector('.n'),{color:'#FAF6EF',duration:0.3},M.w+0.3+i*0.45);});
outt(qa('.wk').concat(['#sb-wt']),R[4]-0.3,{y:-30});
""" + end_js("sb", "R[4]-0.2"),
))

# ---------------------------------------------------------------- C: ESL
def _col(sid, i, x, y, esl):
    return "".join(
        f'<div class="slot{" esl" if k < esl else ""}" id="{sid}-{i}-{k}" style="left:{x}px;top:{y + k * 84}px"><span class="sa">정규 과목</span><span class="sb">ESL</span></div>'
        for k in range(4))


SHORTS.append(dict(
    sid="sc", file="short-c-esl", n=3, marks={"esl": "ESL이", "two": "2년", "camp": "켈로나", "fee": "학비는", "450": "9주"},
    body=f"""
          <div class="abs h" id="sc-h1" style="left:60px;top:300px;width:960px;font-size:96px;line-height:1.15">고1 마치고 가면<br /><span style="color:#146A77">3학기 졸업?</span></div>
          <div class="pol" id="sc-p1" style="left:150px;top:640px;width:780px;height:600px"><div class="ph"><img src="{P}32-school-vernon-secondary.jpg" alt="" /></div><div class="cap">Vernon Secondary</div></div>
          <div class="abs hd" id="sc-t" style="left:60px;top:300px;font-size:56px">한 학기 = 4과목</div>
          <div class="abs" id="sc-cols" style="left:0;top:0;width:1080px;height:1920px">
            {_col("sc", 0, 60, 420, 1)}{_col("sc", 1, 400, 420, 0)}{_col("sc", 2, 740, 420, 0)}
            <div class="abs l" style="left:60px;top:760px;font-size:30px">1학기</div><div class="abs l" style="left:400px;top:760px;font-size:30px">2학기</div><div class="abs l" style="left:740px;top:760px;font-size:30px">3학기</div>
          </div>
          <div class="abs" id="sc-ext" style="left:0;top:0;width:1080px;height:1920px">
            {_col("sc", 3, 60, 860, 0)}{_col("sc", 4, 400, 860, 0)}
            <div class="abs l" style="left:60px;top:1200px;font-size:30px">4학기</div><div class="abs l" style="left:400px;top:1200px;font-size:30px">…</div>
          </div>
          <div class="abs h" id="sc-two" style="left:740px;top:930px;font-size:80px;color:#E8572B;line-height:1.1">2년<br />가까이</div>
          <div class="pol" id="sc-p2" style="left:110px;top:300px;width:860px;height:620px"><div class="ph"><img src="{P}60-campus-exterior.jpg" alt="" /></div><div class="cap">VanWest College · Kelowna</div></div>
          <div class="chip solid" id="sc-k" style="left:60px;top:960px;font-size:44px;padding:16px 34px">입학 전, 켈로나에서 영어 준비</div>
          <div class="abs" id="sc-f0" style="left:60px;top:1060px;width:465px;height:200px;border-radius:28px;background:#fff;border:4px solid rgba(22,50,79,.14);padding:28px 34px"><div class="l" style="font-size:30px;color:#4A5F78">8주</div><div class="h" style="font-size:72px;color:#146A77">$500<span style="font-size:34px;color:#4A5F78"> /주</span></div></div>
          <div class="abs" id="sc-f1" style="left:555px;top:1060px;width:465px;height:200px;border-radius:28px;background:#fff;border:4px solid rgba(22,50,79,.14);padding:28px 34px"><div class="l" style="font-size:30px;color:#4A5F78">9 – 24주</div><div class="h" style="font-size:72px;color:#146A77">$450<span style="font-size:34px;color:#4A5F78"> /주</span></div></div>
          <div class="abs b" id="sc-fn" style="left:62px;top:1280px;font-size:28px;color:#4A5F78">CAD · 교재비 주당 $20 별도 · 2026.10 기준</div>
{end_html("sc", "우리 아이 준비 기간 상담")}""",
    js="""
inn('#sc-h1',0.15,{y:40,d:0.5});pol('#sc-p1',0.5,-3);kb('#sc-p1 img',0.5,R[1],{s:1},{s:1.1});
outt(['#sc-h1','#sc-p1'],R[1]-0.3,{y:-40});
inn('#sc-t',R[1],{y:20});
qa('#sc-cols .slot').forEach((s,i)=>inn(s,R[1]+0.3+i*0.06,{y:20,d:0.35}));inn(qa('#sc-cols .l'),R[1]+1.0,{y:10});
function flip(el,at){tl.to(el,{backgroundColor:'#E8572B',duration:0.3},at);tl.to(el.querySelector('.sa'),{opacity:0,duration:0.2},at);tl.to(el.querySelector('.sb'),{opacity:1,duration:0.2},at+0.1);}
flip(q('#sc-0-0'),M.esl+0.2);
flip(q('#sc-1-0'),R[2]+0.4);flip(q('#sc-0-1'),R[2]+0.7);flip(q('#sc-1-1'),R[2]+1.0);
qa('#sc-ext .slot').forEach((s,i)=>inn(s,R[2]+1.4+i*0.06,{y:20,d:0.35}));inn(qa('#sc-ext .l'),R[2]+1.8,{y:10});
inn('#sc-two',M.two,{x:40,y:0});
outt(['#sc-t','#sc-cols','#sc-ext','#sc-two'],R[3]-0.3,{y:-30});
pol('#sc-p2',R[3],-2);kb('#sc-p2 img',R[3],R[4]-R[3],{s:1},{s:1.1});inn('#sc-k',M.camp+0.6,{y:20});
inn('#sc-f0',M.fee,{y:40});inn('#sc-f1',M['450'],{y:40});inn('#sc-fn',M['450']+0.8,{y:10});
outt(['#sc-p2','#sc-k','#sc-f0','#sc-f1','#sc-fn'],R[4]-0.3,{y:-30});
""" + end_js("sc", "R[4]-0.2"),
))


def build(sh):
    sid = sh["sid"]
    rows, vdur, mark = timing(sh["n"])
    D = round(LEAD + vdur + TAIL, 2)
    R = json.dumps([r["t"] for r in rows])
    M = json.dumps({k: mark(v) for k, v in sh["marks"].items()})
    css = (BASE_CSS + SHORT_CSS).replace("R ", f"#{sid} ").replace("R{", f"#{sid}{{")
    caps = []
    for r in rows:
        txt = r["text"]
        for a, b in CAP_FIX:
            txt = txt.replace(a, b)
        parts = chunks(txt)
        tot = sum(len(p) for p in parts); acc = 0
        for k, p in enumerate(parts):
            a = r["t"] + (r["end"] - r["t"]) * acc / tot
            acc += len(p)
            b = r["t"] + (r["end"] - r["t"]) * acc / tot if k < len(parts) - 1 else r["end"] + 0.25
            caps.append([round(a, 3), round(b - a, 3), p])
    for i in range(len(caps) - 1):
        if caps[i][0] + caps[i][1] > caps[i + 1][0]:
            caps[i][1] = round(caps[i + 1][0] - caps[i][0] - 0.02, 3)
    cap_html = "\n".join(
        f'      <div id="{sid}-cap{i:02d}" class="clip scap" data-start="{a}" data-duration="{d}" data-track-index="20"><span>{t}</span></div>'
        for i, (a, d, t) in enumerate(caps))
    auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0, "v": 0}, {"t": 1, "v": MUSIC}, {"t": round(D - 2, 2), "v": MUSIC}, {"t": D, "v": 0}]}]})
    html = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{FONTS}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #FAF6EF; }}
{css}
    </style>
  </head>
  <body>
    <div id="{sid}" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{D}">
      <div class="bg"></div>
      <div class="grain"></div>
      <div class="glow" style="left:300px;top:500px;width:900px;height:900px"></div>
      <div class="stage">
{sh["body"]}
        <div class="chip solid brand" id="{sid}-brand">버논 조기유학 준비 · AA캐나다</div>
      </div>
      <audio id="{sid}-vo" src="{VDIR}/line{sh['n']:02d}.mp3" data-start="{LEAD}" data-duration="{round(vdur, 2)}" data-track-index="10" data-volume="1"></audio>
      <audio id="{sid}-bgm" src="assets/music/bgm-a.mp3" data-start="0" data-duration="{D}" data-track-index="11" data-volume="1" data-automation='{auto}'></audio>
{cap_html}
    </div>
    <script>
      (function () {{
        const root = document.getElementById("{sid}");
        const D = {D};
        const R = {R};
        const M = {M};
{JS_HELPERS}
        tl.fromTo(q('.stage'),{{opacity:0}},{{opacity:1,duration:0.3}},0);
        tl.fromTo(q('.stage'),{{scale:1,transformOrigin:'50% 45%'}},{{scale:1.025,duration:D,ease:'none'}},0);
        qa('.glow').forEach(g=>tl.fromTo(g,{{scale:0.92}},{{scale:1.08,duration:2.5,ease:'sine.inOut',yoyo:true,repeat:Math.max(0,Math.floor(D/2.5)-1)}},0));
        inn('#{sid}-brand',0.1,{{y:-20}});
{sh["js"]}
        window.__timelines["{sid}"] = tl;
      }})();
    </script>
  </body>
</html>
"""
    pdir = os.path.join(SHORTS_ROOT, sh["file"])
    os.makedirs(pdir, exist_ok=True)
    for link, target in (("assets", "assets"), ("node_modules", "node_modules")):
        lp = os.path.join(pdir, link)
        if not os.path.lexists(lp):
            os.symlink(os.path.relpath(os.path.join(ROOT, target), pdir), lp)
    for name in ("package.json", "hyperframes.json"):
        data = json.load(open(os.path.join(ROOT, name)))
        if name == "package.json":
            data["name"] = sh["file"]; data.pop("devDependencies", None)
        json.dump(data, open(os.path.join(pdir, name), "w"), indent=2, ensure_ascii=False)
    open(os.path.join(pdir, "index.html"), "w", encoding="utf-8").write(html)
    print(sh["file"], "duration", D, "captions", len(caps))


for sh in SHORTS:
    build(sh)

CARVE = os.path.expanduser("~/.claude/skills/hyperframes-audio/scripts/carve.mjs")
if os.path.exists(CARVE) and os.path.isdir(os.path.join(ROOT, "node_modules", "@hyperframes", "core")):
    for sh in SHORTS:
        subprocess.run(["node", CARVE, "--comp", "index.html", "--bed", sh["sid"] + "-bgm", "--voice", sh["sid"] + "-vo",
                        "--strength", "0.5", "--core", ROOT], cwd=os.path.join(SHORTS_ROOT, sh["file"]), check=True, stdout=subprocess.DEVNULL)
    print("carve applied")
