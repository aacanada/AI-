"""Generate the three 1080x1920 shorts as standalone compositions + their thumbnails.

Run from the project root:  python3 -I tools/shorts.py
Outputs: short-a-quota.html, short-b-europe.html, short-c-graduation.html, thumbs/*.html
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
SHORTS_ROOT = os.path.join(os.path.dirname(ROOT), "vernon-shorts")
P = "assets/photos/"
VDIR = "assets/voice-shorts"
LEAD, TAIL = 0.4, 2.2


def cues(n):
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
    return rows, dur


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
R .scap{position:absolute;left:0;right:0;top:1400px;display:flex;justify-content:center;z-index:90}
R .scap span{display:inline-block;max-width:940px;background:rgba(22,50,79,.9);color:#FAF6EF;font-weight:800;font-size:50px;line-height:1.3;padding:12px 30px;border-radius:16px;text-align:center}
R .brand{position:absolute;left:60px;top:190px;z-index:80}
R .endph{position:absolute;inset:0;overflow:hidden}
R .endph img{width:100%;height:100%;object-fit:cover;object-position:50% 20%}
R .endsh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(22,50,79,0) 25%,rgba(22,50,79,.92) 62%)}
R .endcard{position:absolute;left:60px;top:1010px;width:960px;height:330px;background:#FAF6EF;border-radius:30px;padding:40px 48px}
"""


def end_html(sid, head):
    return f"""
          <div class="endph" id="{sid}-eph"><img src="{P}01b-hero-lake-jump-vertical.jpg" alt="" /></div>
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

# ---------------------------------------------------------------- A: quota
SHORTS.append(dict(
    sid="sa", file="short-a-quota", n=1,
    body=f"""
          <div class="abs h" id="sa-h1" style="left:60px;top:300px;width:960px;font-size:100px;line-height:1.15">한국 학생 많은 학교,<br />걱정이세요?</div>
          <div class="pol" id="sa-p1" style="left:170px;top:620px;width:740px;height:660px"><div class="ph"><img src="{P}18-students-lockers.jpg" alt="" /></div><div class="cap">Vernon, BC</div></div>
          <div class="chip lake" id="sa-c1" style="left:60px;top:300px">캐나다 BC주 버논 공립학교</div>
          <div class="abs h" id="sa-pct" style="left:60px;top:380px;font-size:220px;color:#1F8A99;font-variant-numeric:tabular-nums;line-height:1">0%</div>
          <div class="abs hd" id="sa-pctl" style="left:66px;top:610px;font-size:56px">현지 캐나다 학생</div>
          <div class="abs" id="sa-grid" style="left:210px;top:720px;width:660px;height:660px"></div>
          <div class="abs" id="sa-s1" style="left:60px;top:380px"><div class="h" id="sa-s1n" style="font-size:200px;color:#1F8A99;font-variant-numeric:tabular-nums;line-height:1">0</div><div class="hd" style="font-size:56px;margin-top:10px">국제학생 전체</div></div>
          <div class="abs" id="sa-s2" style="left:60px;top:800px"><div class="h" id="sa-s2n" style="font-size:200px;color:#E8572B;font-variant-numeric:tabular-nums;line-height:1">0</div><div class="hd" style="font-size:56px;margin-top:10px">출신 국가</div></div>
          <div class="chip sand" id="sa-lock" style="left:60px;top:380px;font-size:44px;padding:16px 34px">학교별 한국 학생 정원 상한</div>
          <div class="abs" id="sa-seats" style="left:142px;top:600px;width:800px;height:160px"></div>
          <div class="abs hd" id="sa-sl" style="left:60px;top:820px;width:960px;font-size:56px;line-height:1.3">졸업생이 나가야<br />자리가 생깁니다</div>
          <div class="abs" id="sa-circ" style="left:300px;top:540px;width:480px;height:480px;border-radius:50%;overflow:hidden;border:12px solid #fff;box-shadow:0 20px 44px rgba(22,50,79,.3)"><img src="{P}16-classroom-overhead.jpg" alt="" style="width:100%;height:100%;object-fit:cover" /></div>
          <div class="abs h" id="sa-eng" style="left:60px;top:1080px;width:960px;text-align:center;font-size:72px">교실도 복도도 <span style="color:#146A77">영어</span></div>
{end_html("sa", "학교별 남은 자리 문의")}""",
    js="""
inn('#sa-h1',0.15,{y:40,d:0.5});pol('#sa-p1',0.5,-3);
outt(['#sa-h1','#sa-p1'],R[1]-0.3,{y:-40});
inn('#sa-c1',R[1],{s:0.7,y:0});inn('#sa-pct',R[1]+0.2,{y:30});count('#sa-pct',0,95,R[1]+0.3,2.2,v=>Math.round(v)+'%');inn('#sa-pctl',R[1]+1.0,{y:16});
(function(){const g=q('#sa-grid');for(let i=0;i<100;i++){const d=document.createElement('div');d.className='dot'+(i>=95?' k':'');d.style.cssText='position:absolute;width:52px;height:52px;border-radius:50%;background:'+(i>=95?'#E8572B':'#1F8A99')+';left:'+((i%10)*66)+'px;top:'+(Math.floor(i/10)*66)+'px';g.appendChild(d);}})();
qa('#sa-grid div').forEach((d,i)=>tl.fromTo(d,{scale:0,opacity:0},{scale:1,opacity:1,duration:0.3,ease:'power3.out'},R[1]+0.3+((i%10)+Math.floor(i/10))*0.04));
outt(['#sa-c1','#sa-pct','#sa-pctl','#sa-grid'],R[2]-0.3,{y:-30});
inn('#sa-s1',R[2],{y:40});count('#sa-s1n',0,300,R[2]+0.1,1.4,v=>Math.round(v)+'+');
inn('#sa-s2',R[2]+0.9,{y:40});count('#sa-s2n',0,20,R[2]+1.0,1.0,v=>Math.round(v)+'+');
outt(['#sa-s1','#sa-s2'],R[3]-0.3,{y:-30});
inn('#sa-lock',R[3],{s:0.6,y:0});
(function(){const g=q('#sa-seats');for(let i=0;i<5;i++){const d=document.createElement('div');d.id='sa-q'+i;d.style.cssText='position:absolute;width:140px;height:140px;border-radius:26px;background:#1F8A99;top:0;left:'+(i*164)+'px';g.appendChild(d);}})();
qa('#sa-seats div').forEach((d,i)=>tl.fromTo(d,{scale:0},{scale:1,duration:0.4,ease:'power3.out'},R[3]+0.6+i*0.1));
tl.to('#sa-q2',{opacity:0.15,scale:0.8,duration:0.5},R[4]);inn('#sa-sl',R[4]+0.2,{y:20});
tl.to('#sa-q2',{backgroundColor:'#E8572B',opacity:1,scale:1,duration:0.5,ease:'power3.out'},R[4]+1.6);
outt(['#sa-lock','#sa-seats','#sa-sl'],R[4]+3.0,{y:-30});
inn('#sa-circ',R[4]+3.2,{s:0.3,y:0,d:0.7});inn('#sa-eng',R[4]+3.6,{y:24});
outt(['#sa-circ','#sa-eng'],R[5]-0.3);
""" + end_js("sa", "R[5]-0.2"),
))

# ---------------------------------------------------------------- B: europe
SHORTS.append(dict(
    sid="sb", file="short-b-europe", n=2,
    body=f"""
          <div class="abs" id="sb-hph" style="left:0;top:0;width:1080px;height:1920px;overflow:hidden"><img src="{P}03-magical-hillside.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 50%" /></div>
          <div class="abs" id="sb-hsh" style="inset:0;background:linear-gradient(180deg,rgba(22,50,79,0) 40%,rgba(22,50,79,.88) 68%)"></div>
          <div class="abs h" id="sb-h1" style="left:60px;top:1000px;width:960px;font-size:96px;line-height:1.15;color:#fff">유럽 부모들은<br />캐나다 어디로<br />보낼까?</div>
          <div class="chip" id="sb-x1" style="left:60px;top:320px;font-size:48px;padding:14px 36px">밴쿠버</div>
          <div class="chip" id="sb-x2" style="left:380px;top:320px;font-size:48px;padding:14px 36px">토론토</div>
          <div class="abs h" id="sb-s1" style="left:280px;top:310px;font-size:64px;color:#E8572B">✕</div>
          <div class="abs h" id="sb-s2" style="left:600px;top:310px;font-size:64px;color:#E8572B">✕</div>
          <div class="abs h" id="sb-v" style="left:60px;top:440px;font-size:190px;color:#146A77;line-height:1">버논</div>
          <div class="abs b" id="sb-vs" style="left:66px;top:650px;font-size:44px;color:#4A5F78">BC주 오카나간의 휴양 도시</div>
          <div class="abs" id="sb-pano" style="left:0;top:760px;width:1080px;height:520px;overflow:hidden"><img src="{P}02-okanagan-panorama.jpg" alt="" id="sb-panoimg" style="position:absolute;left:0;top:0;height:520px;width:auto" /></div>
          <svg class="abs" id="sb-map" style="left:0;top:330px;width:1080px;height:760px" viewBox="0 0 1080 760">
            <defs><pattern id="sb-wd" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="4" fill="#16324F" opacity=".2"/></pattern></defs>
            <path d="M40 260 C 140 170, 380 180, 440 280 C 470 380, 400 460, 320 490 C 230 510, 120 490, 70 420 C 30 360, 20 310, 40 260Z" fill="url(#sb-wd)"/>
            <path d="M700 230 C 790 190, 960 200, 1010 260 C 1050 330, 1000 400, 910 420 C 820 440, 730 400, 700 340 C 680 300, 675 260, 700 230Z" fill="url(#sb-wd)"/>
            <path id="sb-a1" d="M860 300 C 700 90, 420 110, 200 360" fill="none" stroke="#E8572B" stroke-width="10" stroke-linecap="round"/>
            <path id="sb-a2" d="M920 350 C 740 190, 440 210, 206 372" fill="none" stroke="#E8572B" stroke-width="10" stroke-linecap="round" opacity=".7"/>
            <circle cx="200" cy="370" r="22" fill="#E8572B"/>
            <text x="120" y="320" font-family="Pretendard" font-weight="800" font-size="40" fill="#16324F">VERNON</text>
            <text x="790" y="480" font-family="Pretendard" font-weight="800" font-size="40" fill="#16324F">EUROPE</text>
          </svg>
          <div class="chip solid" id="sb-c1" style="left:60px;top:1150px;font-size:46px;padding:14px 34px">국제학생 중 유럽 출신 최다</div>
          <div class="chip lake" id="sb-c2" style="left:60px;top:300px;font-size:44px;padding:14px 34px">스위스 같은 분위기의 호수 도시</div>
          <div class="pol" id="sb-p1" style="left:70px;top:420px;width:900px;height:560px"><div class="ph"><img src="{P}13-group-photo-lake.jpg" alt="" /></div><div class="cap">Vernon international students</div></div>
          <div class="pol" id="sb-p2" style="left:640px;top:880px;width:340px;height:420px"><div class="ph"><img src="{P}12-dock-group.jpg" alt="" /></div></div>
          <div class="abs" id="sb-fl" style="left:0;top:280px;width:1080px;height:760px;overflow:hidden"><img src="{P}04-students-canada-flag.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:35% 50%" id="sb-flimg" /></div>
          <div class="abs h" id="sb-fe" style="left:60px;top:1090px;width:960px;font-size:84px;line-height:1.2">같은 교실,<br />다른 나라 친구들</div>
{end_html("sb", "버논 조기유학 상담")}""",
    js="""
kb('#sb-hph img',0,R[1],{s:1.0},{s:1.1});inn('#sb-h1',0.15,{y:40,d:0.5});
outt(['#sb-hph','#sb-hsh','#sb-h1'],R[1]-0.3);
inn('#sb-x1',R[1],{s:0.7,y:0});inn('#sb-x2',R[1]+0.5,{s:0.7,y:0});inn('#sb-s1',R[1]+0.6,{s:2,y:0,d:0.3,e:'power4.out'});inn('#sb-s2',R[1]+1.1,{s:2,y:0,d:0.3,e:'power4.out'});tl.to(['#sb-x1','#sb-x2'],{opacity:0.45,duration:0.3},R[1]+1.3);
inn('#sb-v',R[1]+1.6,{y:40,d:0.6});inn('#sb-vs',R[1]+2.2,{y:16});
tl.fromTo('#sb-pano',{clipPath:'inset(0 0 0 100%)'},{clipPath:'inset(0 0 0 0%)',duration:0.8,ease:'power3.inOut'},R[1]+2.0);
tl.fromTo('#sb-panoimg',{x:0},{x:-(1780-1080),duration:R[2]-R[1],ease:'none'},R[1]+2.0);
outt(['#sb-x1','#sb-x2','#sb-s1','#sb-s2','#sb-v','#sb-vs','#sb-pano'],R[2]-0.3,{y:-30});
tl.fromTo('#sb-map',{opacity:0},{opacity:1,duration:0.5},R[2]);draw('#sb-a1',R[2]+0.3,1.2);draw('#sb-a2',R[2]+0.6,1.2);
inn('#sb-c1',R[2]+1.6,{y:20});
outt(['#sb-map','#sb-c1'],R[3]-0.3);
inn('#sb-c2',R[3],{s:0.7,y:0});pol('#sb-p1',R[3]+0.2,-3);pol('#sb-p2',R[3]+1.6,5);
outt(['#sb-c2','#sb-p1','#sb-p2'],R[4]-0.3,{y:-30});
tl.fromTo('#sb-fl',{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:0.8,ease:'power3.inOut'},R[4]-0.2);kb('#sb-flimg',R[4]-0.2,R[5]-R[4],{s:1},{s:1.08});
inn('#sb-fe',R[4]+0.5,{y:30});
outt(['#sb-fl','#sb-fe'],R[5]-0.3);
""" + end_js("sb", "R[5]-0.2"),
))

# ---------------------------------------------------------------- C: graduation
SHORTS.append(dict(
    sid="sc", file="short-c-graduation", n=3,
    body=f"""
          <div class="abs h" id="sc-h1" style="left:60px;top:300px;width:960px;font-size:100px;line-height:1.15">고1 마치고 가면<br />졸업까지 몇 학기?</div>
          <div class="pol" id="sc-p1" style="left:170px;top:640px;width:740px;height:560px"><div class="ph"><img src="{P}32-school-vernon-secondary.jpg" alt="" /></div><div class="cap">Vernon Secondary</div></div>
          <div class="abs l" id="sc-top" style="left:600px;top:300px;width:420px;text-align:right;font-size:34px">80학점 = BC주 졸업</div>
          <div class="abs" id="sc-track" style="left:700px;top:360px;width:300px;height:920px;border-radius:28px;background:#F1EADF;border:4px solid rgba(22,50,79,.22)"></div>
          <div class="abs" id="sc-b0" style="left:700px;top:820px;width:300px;height:460px;background:#1F8A99;border-radius:0 0 28px 28px"></div>
          <div class="abs" id="sc-b1" style="left:700px;top:636px;width:300px;height:184px;background:#4E8A1E;border-bottom:6px solid #FAF6EF"></div>
          <div class="abs" id="sc-b2" style="left:700px;top:452px;width:300px;height:184px;background:#3A7016;border-bottom:6px solid #FAF6EF"></div>
          <div class="abs" id="sc-b3" style="left:700px;top:360px;width:300px;height:92px;background:#9BC95E;border-bottom:6px solid #FAF6EF;border-radius:28px 28px 0 0"></div>
          <div class="abs hd" id="sc-b0l" style="left:720px;top:1000px;width:260px;text-align:center;font-size:36px;color:#fff;line-height:1.3">한국 고1<br />성적으로<br />≈ 40</div>
          <div class="abs hd" id="sc-b1l" style="left:720px;top:700px;width:260px;text-align:center;font-size:36px;color:#fff">1학기 +16</div>
          <div class="abs hd" id="sc-b2l" style="left:720px;top:516px;width:260px;text-align:center;font-size:36px;color:#fff">2학기 +16</div>
          <div class="abs hd" id="sc-b3l" style="left:720px;top:380px;width:260px;text-align:center;font-size:32px;color:#16324F">3학기 +8</div>
          <div class="abs h" id="sc-num" style="left:60px;top:520px;font-size:240px;color:#146A77;font-variant-numeric:tabular-nums;line-height:1">0</div>
          <div class="abs hd" id="sc-numl" style="left:70px;top:770px;font-size:60px">학점</div>
          <div class="chip solid" id="sc-three" style="left:60px;top:880px;font-size:46px;padding:14px 34px">계산상 3학기</div>
          <div class="chip lake" id="sc-kor" style="left:60px;top:1200px;font-size:38px;padding:12px 28px">현지 한국어 10·11·12 수강 가능</div>
          <svg class="abs" id="sc-cap" style="left:70px;top:990px;width:220px;height:190px" viewBox="0 0 200 170"><path d="M100 20 L190 60 L100 100 L10 60 Z" fill="#16324F"/><path d="M50 80 L50 125 C 70 145, 130 145, 150 125 L150 80 L100 102 Z" fill="#16324F"/><path d="M180 64 L180 120" stroke="#E8572B" stroke-width="8" stroke-linecap="round"/></svg>
          <div class="abs b" id="sc-fn" style="left:60px;top:1300px;width:960px;font-size:34px;color:#4A5F78">* 영어 수준에 따라 기간은 달라질 수 있습니다</div>
{end_html("sc", "우리 아이 졸업 계산 문의")}""",
    js="""
inn('#sc-h1',0.15,{y:40,d:0.5});pol('#sc-p1',0.5,-3);
outt(['#sc-h1','#sc-p1'],R[1]-0.3,{y:-40});
tl.fromTo('#sc-track',{scaleY:0,transformOrigin:'50% 100%'},{scaleY:1,duration:0.8,ease:'power3.inOut'},R[1]);inn('#sc-top',R[1]+0.6,{y:12});
function up(el,at,d){tl.fromTo(el,{scaleY:0,opacity:0,transformOrigin:'50% 100%'},{scaleY:1,opacity:1,duration:d,ease:'power3.out'},at);}
up('#sc-b0',R[2]+0.4,0.9);inn('#sc-b0l',R[2]+1.0,{y:10});inn('#sc-num',R[2]+0.4,{y:0});inn('#sc-numl',R[2]+0.6,{y:10});
count('#sc-num',0,40,R[2]+0.4,1.2,v=>Math.round(v));
up('#sc-b1',R[3]+0.3,0.6);inn('#sc-b1l',R[3]+0.6,{y:10});count('#sc-num',40,56,R[3]+0.3,0.6,v=>Math.round(v));
up('#sc-b2',R[3]+1.6,0.6);inn('#sc-b2l',R[3]+1.9,{y:10});count('#sc-num',56,72,R[3]+1.6,0.6,v=>Math.round(v));
up('#sc-b3',R[3]+2.9,0.5);inn('#sc-b3l',R[3]+3.1,{y:10});count('#sc-num',72,80,R[3]+2.9,0.5,v=>Math.round(v));
inn('#sc-kor',R[3]+0.8,{s:0.6,y:0});inn('#sc-three',R[3]+3.2,{s:0.6,y:0});inn('#sc-cap',R[3]+3.8,{s:0,y:0,d:0.6});
inn('#sc-fn',R[4],{y:12});
outt(['#sc-kor','#sc-top','#sc-track','#sc-b0','#sc-b1','#sc-b2','#sc-b3','#sc-b0l','#sc-b1l','#sc-b2l','#sc-b3l','#sc-num','#sc-numl','#sc-three','#sc-cap','#sc-fn'],R[5]-0.3);
""" + end_js("sc", "R[5]-0.2"),
))


def build(sh):
    sid = sh["sid"]
    rows, vdur = cues(sh["n"])
    D = round(LEAD + vdur + TAIL, 2)
    R = json.dumps([r["t"] for r in rows])
    css = (BASE_CSS + SHORT_CSS).replace("R ", f"#{sid} ").replace("R{", f"#{sid}{{")
    caps = []
    for r in rows:
        parts = chunks(r["text"])
        tot = sum(len(p) for p in parts); acc = 0
        for k, p in enumerate(parts):
            a = r["t"] + (r["end"] - r["t"]) * acc / tot
            acc += len(p)
            b = r["t"] + (r["end"] - r["t"]) * acc / tot if k < len(parts) - 1 else r["end"] + 0.25
            caps.append([round(a, 3), round(b - a, 3), p.replace("캔로그", "canlog")])
    for i in range(len(caps) - 1):
        if caps[i][0] + caps[i][1] > caps[i + 1][0]:
            caps[i][1] = round(caps[i + 1][0] - caps[i][0] - 0.02, 3)
    cap_html = "\n".join(
        f'      <div id="{sid}-cap{i:02d}" class="clip scap" data-start="{a}" data-duration="{d}" data-track-index="20"><span>{t}</span></div>'
        for i, (a, d, t) in enumerate(caps))
    bed_len = round(D, 2)
    auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0, "v": 0}, {"t": 1, "v": 0.12}, {"t": round(bed_len - 2, 2), "v": 0.12}, {"t": bed_len, "v": 0}]}]})
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
        <div class="chip solid brand" id="{sid}-brand">버논 조기유학 · AA캐나다</div>
{sh["body"]}
      </div>
      <audio id="{sid}-vo" src="{VDIR}/line{sh['n']:02d}.mp3" data-start="{LEAD}" data-duration="{round(vdur, 2)}" data-track-index="10" data-volume="1"></audio>
      <audio id="{sid}-bgm" src="assets/music/bgm-a.mp3" data-start="0" data-duration="{bed_len}" data-track-index="11" data-volume="1" data-automation='{auto}'></audio>
{cap_html}
    </div>
    <script>
      (function () {{
        const root = document.getElementById("{sid}");
        const D = {D};
        const R = {R};
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
    link = os.path.join(pdir, "assets")
    if not os.path.lexists(link):
        os.symlink(os.path.relpath(os.path.join(ROOT, "assets"), pdir), link)
    for name, src in (("package.json", "package.json"), ("hyperframes.json", "hyperframes.json")):
        data = json.load(open(os.path.join(ROOT, src)))
        if name == "package.json":
            data["name"] = sh["file"]; data.pop("devDependencies", None)
        json.dump(data, open(os.path.join(pdir, name), "w"), indent=2, ensure_ascii=False)
    open(os.path.join(pdir, "index.html"), "w", encoding="utf-8").write(html)
    print(sh["file"], "duration", D, "captions", len(caps))


for sh in SHORTS:
    build(sh)

# Re-apply the voiceover carve to each short's music bed.
CARVE = os.path.expanduser("~/.claude/skills/hyperframes-audio/scripts/carve.mjs")
if os.path.exists(CARVE) and os.path.isdir(os.path.join(ROOT, "node_modules", "@hyperframes", "core")):
    for sh in SHORTS:
        subprocess.run(["node", CARVE, "--comp", "index.html", "--bed", sh["sid"] + "-bgm", "--voice", sh["sid"] + "-vo",
                        "--core", ROOT], cwd=os.path.join(SHORTS_ROOT, sh["file"]), check=True, stdout=subprocess.DEVNULL)
    print("carve applied")
