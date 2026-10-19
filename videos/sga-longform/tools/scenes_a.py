"""Scenes s01-s06 (CH1 hook, CH2 location). 1920x1080 px; content safe area y 130-820 (captions below).
@P/ = assets/photos/, @B/ = assets/brochure/. T('phrase') = scene-local time the phrase is spoken."""

S = {}

# shared Toronto map (also used by s28)
MAP_SVG = """<svg class="abs" id="{id}-map" style="left:{x}px;top:{y}px;width:1000px;height:640px" viewBox="0 0 1000 640">
  <path class="mp-lake" d="M-120 585 C 80 560, 230 640, 420 600 S 760 520, 1120 560" fill="none" stroke="#5f8fd6" stroke-width="6" stroke-linecap="round" stroke-dasharray="1 0"/>
  <path class="mp-out" d="M120 120 L560 70 L900 96 L930 300 L960 420 L820 470 L660 520 L520 560 L360 570 L230 540 L140 470 L90 330 Z" fill="rgba(245,239,227,.06)" stroke="#f5efe3" stroke-width="5" stroke-linejoin="round"/>
  <path class="mp-in" d="M110 330 L940 330" fill="none" stroke="rgba(245,239,227,.25)" stroke-width="3" stroke-dasharray="10 10"/>
</svg>"""

PIN = """<div class="abs pin" id="{id}" style="left:{x}px;top:{y}px;width:64px;height:84px"><div class="glow" id="{id}-g"></div><svg viewBox="0 0 64 84" style="position:absolute;inset:0;width:64px;height:84px"><path d="M32 82 C 32 82, 4 48, 4 30 A28 28 0 1 1 60 30 C 60 48, 32 82, 32 82 Z" fill="{c}"/><circle cx="32" cy="30" r="11" fill="#14254a"/></svg></div>"""
PIN_CSS = """
R .pin .glow{position:absolute;left:-28px;top:44px;width:120px;height:60px;border-radius:50%;background:radial-gradient(ellipse,rgba(232,185,49,.75) 0%,rgba(232,185,49,0) 70%)}
"""

# ---------------------------------------------------------------- S01 hook "60"
S["s01"] = dict(
    css="""
R .full img{filter:saturate(.35)}
R #s01-dim{opacity:.65}
R .dust{position:absolute;width:6px;height:6px;border-radius:50%;background:#e8b931;opacity:0}
R #s01-num{left:0;right:0;top:250px;text-align:center;font-size:330px;color:#fff}
""",
    bg="""        <div class="full" id="s01-ph"><img src="@P/campus-02-class-desks.jpg" alt="" /><div class="sweep" id="s01-sw"></div></div>
        <div class="dim" id="s01-dim"></div>""",
    body="""
          <div class="chip" id="s01-c1" style="left:150px;top:150px">온타리오주 공립학교</div>
          <div class="chip" id="s01-c2" style="left:520px;top:150px">2년</div>
          <div class="abs num" id="s01-num">60</div>
          <div class="abs" id="s01-ul" style="left:760px;top:600px;width:400px;height:10px;background:#c8102e;border-radius:6px"></div>
          <div class="abs hd" id="s01-lab" style="left:0;right:0;top:640px;text-align:center;font-size:52px">10학년 평균</div>
          <div class="abs hd" id="s01-no" style="left:0;right:0;top:720px;text-align:center;font-size:40px;color:#ff8a8a">지원할 수 있는 대학, 거의 없음</div>
          <div class="abs" id="s01-dusts" style="inset:0"></div>""",
    js="""
kb('#s01-ph img',0,D,{s:1.0,x:-1},{s:1.10,x:1});
sweep('#s01-sw',0.15);
let seed=7;const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647;};
for(let i=0;i<26;i++){const d=document.createElement('div');d.className='dust';d.style.left=(80+rnd()*1760)+'px';d.style.top=(200+rnd()*700)+'px';q('#s01-dusts').appendChild(d);
  const st=rnd()*3;tl.fromTo(d,{opacity:0,y:0},{opacity:0.15+rnd()*0.5,y:-60-rnd()*120,duration:3+rnd()*3,ease:'sine.inOut',yoyo:true,repeat:Math.max(0,Math.floor(D/6)-1)},st);}
inn('#s01-c1',T('온타리오주'),{x:-30,y:0});pop('#s01-c2',T('2년을'));
slam('#s01-num',T('평균 점수는')-0.3,{d:0.45});odo('#s01-num',T('평균 점수는')-0.3,1.3);
inn('#s01-lab',T('평균 점수는')+0.3,{y:20});
grow('#s01-ul',T('60점'),0.5,'50% 50%');
tl.to('#s01-num',{color:'#ff6b6b',duration:0.6},T('지원할'));
inn('#s01-no',T('지원할'),{y:16});
""",
    sfx=[("impact", "T('평균 점수는')+0.15")],
)

# ---------------------------------------------------------------- S02 freedom -> trap
S["s02"] = dict(
    css="""
R #s02-bgp img{filter:blur(10px) saturate(.6)}
R .box{position:absolute;top:420px;width:400px;height:200px;border-radius:28px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:64px;letter-spacing:-.02em}
R .box.c{background:#f5efe3;color:#14254a}
R .box.r{background:#c8102e;color:#fff}
""",
    bg="""        <div class="full" id="s02-bgp" style="opacity:.28"><img src="@P/campus-01-class-whiteboard.jpg" alt="" /></div>""",
    body="""
          <div class="abs hd" id="s02-h" style="left:0;right:0;top:170px;text-align:center;font-size:60px">공립학교가 나빠서가 아닙니다</div>
          <div class="abs b" id="s02-h2" style="left:0;right:0;top:260px;text-align:center;font-size:36px;color:#e8b931">과목도, 공부도 스스로 관리하는 시스템</div>
          <div class="box c" id="s02-b1" style="left:150px">자유</div>
          <div class="box c" id="s02-b2" style="left:760px">관리 공백</div>
          <div class="box r" id="s02-b3" style="left:1370px">성적 하락</div>
          <svg class="abs" style="left:550px;top:470px;width:210px;height:100px" viewBox="0 0 210 100"><path id="s02-a1" d="M14 50 L180 50 M150 22 L186 50 L150 78" fill="none" stroke="#e8b931" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <svg class="abs" style="left:1160px;top:470px;width:210px;height:100px" viewBox="0 0 210 100"><path id="s02-a2" d="M14 50 L180 50 M150 22 L186 50 L150 78" fill="none" stroke="#e8b931" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <div class="chip" id="s02-k1" style="left:205px;top:660px">대학처럼 스스로</div>
          <div class="chip" id="s02-k2" style="left:770px;top:660px">담임·학원 관리 없음</div>""",
    js="""
kb('#s02-bgp img',0,D,{s:1.05},{s:1.12});
inn('#s02-h',T('공립학교가'),{y:24});
inn('#s02-h2',T('캐나다 고등학교는'),{y:16});
pop('#s02-b1',T('스스로 관리'));inn('#s02-k1',T('스스로 관리')+0.3,{y:12});
draw('#s02-a1',T('담임 선생님과'),0.6);pop('#s02-b2',T('담임 선생님과')+0.5);inn('#s02-k2',T('학원 관리')+0.2,{y:12});
draw('#s02-a2',T('이 자유가'),0.6);stamp('#s02-b3',T('함정이'),-3);
""",
    sfx=[("pop", "T('스스로 관리')"), ("pop", "T('담임 선생님과')+0.5"), ("stamp", "T('함정이')+0.25")],
)

# ---------------------------------------------------------------- S03 intro SGA
S["s03"] = dict(
    css="""
R #s03-cov{left:310px;top:150px;width:1300px;height:731px}
R .toc{font-size:28px;padding:10px 24px}
""",
    bg="",
    body="""
          <div class="ph frame" id="s03-cov"><img src="@B/cover.jpg" alt="" /></div>
          <div class="abs" id="s03-crestw" style="left:180px;top:170px;width:400px;height:452px"><img src="@P/logo-crest.png" alt="" style="width:100%;height:100%;object-fit:contain" /></div>
          <div class="abs h" id="s03-t1" style="left:660px;top:230px;font-size:104px;white-space:nowrap">ST. GEORGE ACADEMY</div>
          <div class="abs hd" id="s03-t2" style="left:664px;top:370px;font-size:42px;color:#e8b931;white-space:nowrap">토론토 노스욕 · 9~12학년 사립고 · 1994년 설립</div>
          <div class="abs b" id="s03-t3" style="left:664px;top:450px;font-size:32px;color:rgba(255,255,255,.8);white-space:nowrap">AA Canada · 학교 직접 미팅 자료로 정리</div>
          <div class="chip toc" id="s03-k0" style="left:180px;top:700px">01 위치</div>
          <div class="chip toc" id="s03-k1" style="left:375px;top:700px">02 졸업장</div>
          <div class="chip toc" id="s03-k2" style="left:600px;top:700px">03 입학 시기</div>
          <div class="chip toc" id="s03-k3" style="left:855px;top:700px">04 관리</div>
          <div class="chip toc" id="s03-k4" style="left:1050px;top:700px">05 영어</div>
          <div class="chip toc" id="s03-k5" style="left:1245px;top:700px">06 생활</div>
          <div class="chip toc" id="s03-k6" style="left:1440px;top:700px">07 대학</div>
          <div class="chip toc" id="s03-k7" style="left:1635px;top:700px">08 정리</div>""",
    js="""
flip('#s03-cov',0.05,{d:0.8});kb('#s03-cov img',0,D,{s:1.0},{s:1.08});
tl.to('#s03-cov',{opacity:0,scale:0.86,y:40,duration:0.5,ease:'power2.in'},T('노스욕에 있는')-0.5);
tl.fromTo('#s03-crestw',{clipPath:'circle(0% at 50% 50%)',opacity:1},{clipPath:'circle(75% at 50% 50%)',opacity:1,duration:0.9,ease:'power3.inOut'},T('노스욕에 있는'));
mask('#s03-t1',T('세인트조지'),0.8,'l');
inn('#s03-t2',T('SGA입니다'),{y:16});
inn('#s03-t3',T('AA Canada가'),{y:12});
pop(['#s03-k0','#s03-k1','#s03-k2','#s03-k3','#s03-k4','#s03-k5','#s03-k6','#s03-k7'],T('받은 자료로'),0.08);
""",
    sfx=[("whoosh", "T('노스욕에 있는')")],
)

# ---------------------------------------------------------------- S04 location map
S["s04"] = dict(
    css=PIN_CSS + """
R #s04-aer{left:1000px;top:150px;width:820px;height:520px}
R #s04-st1{left:1060px;top:270px;width:780px;height:288px}
R #s04-st2{left:1260px;top:470px;width:440px;height:330px}
""",
    bg="",
    body=MAP_SVG.format(id="s04", x=100, y=170) + """
          <div class="abs l" id="s04-tor" style="left:420px;top:420px;font-size:40px;color:rgba(245,239,227,.55)">TORONTO</div>
          <div class="abs l" id="s04-lk" style="left:700px;top:790px;font-size:24px;color:#8fb3ec">LAKE ONTARIO</div>
""" + PIN.format(id="s04-pin", x=568, y=190, c="#e8b931") + """
          <div class="abs hd" id="s04-ny" style="left:650px;top:205px;font-size:44px;white-space:nowrap">노스욕 <span class="gold">North York</span></div>
          <div class="ph frame" id="s04-aer"><img src="@P/town-03-northyork-aerial.jpg" alt="" /><div class="lab">노스욕 중심가</div></div>
          <div class="ph frame" id="s04-st1"><img src="@P/town-12-nyc-station.jpg" alt="" /></div>
          <div class="ph frame" id="s04-st2"><img src="@P/town-11-subway.jpg" alt="" /></div>
          <div class="chip cream" id="s04-c1" style="left:150px;top:720px">5 Park Home Ave</div>
          <div class="chip gold" id="s04-c2" style="left:470px;top:720px">North York Centre역</div>""",
    js="""
draw('#s04-map .mp-out',T('먼저 위치')-0.2,1.4);draw('#s04-map .mp-lake',T('먼저 위치')+0.2,1.2);
inn('#s04-tor',T('먼저 위치')+0.8,{y:10});inn('#s04-lk',T('먼저 위치')+1.0,{y:10});
tl.fromTo('#s04-pin',{y:-260,opacity:0},{y:0,opacity:1,duration:0.6,ease:'bounce.out'},T('토론토 북쪽'));
tl.fromTo('#s04-pin-g',{scale:0.5,opacity:0},{scale:1.4,opacity:1,duration:0.9,ease:'sine.inOut',yoyo:true,repeat:Math.max(0,Math.floor((D-T('토론토 북쪽'))/0.9)-1)},T('토론토 북쪽')+0.5);
inn('#s04-ny',T('노스욕 중심가'),{x:-20,y:0});
tl.fromTo('#s04-aer',{opacity:0,scale:0.2,x:-420,y:-80},{opacity:1,scale:1,x:0,y:0,duration:0.8,ease:'power3.out'},T('노스욕 중심가')+0.3);
kb('#s04-aer img',T('노스욕 중심가'),D,{s:1.0},{s:1.12,x:-2});
outt('#s04-aer',T('지하철')-0.3,{s:0.9});
inn('#s04-st1',T('지하철'),{y:-60,r0:-6,r:-2});inn('#s04-st2',T('지하철')+0.5,{y:60,r0:6,r:2});
pop('#s04-c1',T('지하철')+0.4);pop('#s04-c2',T('노스욕 센터역'));
""",
    sfx=[("pop", "T('토론토 북쪽')+0.45"), ("whoosh", "T('지하철')")],
)

# ---------------------------------------------------------------- S05 "토론토의 대치동"
S["s05"] = dict(
    css="""
R .bc{position:absolute;top:240px;width:500px;height:380px;padding:24px}
R .bc .im{width:100%;height:250px;border-radius:16px;overflow:hidden;background:#fff;display:flex;align-items:center;justify-content:center}
R .bc .im img{max-width:100%;max-height:100%;object-fit:contain}
R .bc .t{font-size:36px;margin-top:20px;text-align:center}
R #s05-big{left:0;right:0;top:330px;text-align:center;font-size:170px;color:#e8b931;perspective:900px}
""",
    bg="",
    body="""
          <div class="chip gold" id="s05-c0" style="left:150px;top:150px">SGA에서 5~10분</div>
          <div class="card bc" id="s05-b1" style="left:320px"><div class="im"><img src="@P/town-09-tdsb.jpg" alt="" /></div><div class="t">토론토 공립교육청</div></div>
          <div class="card bc" id="s05-b2" style="left:1100px"><div class="im"><img src="@P/town-10-tcdsb-logo.jpg" alt="" /></div><div class="t">토론토 가톨릭교육청</div></div>
          <div class="ph frame" id="s05-p1" style="left:430px;top:660px;width:330px;height:190px"><img src="@P/town-07-earl-haig.jpg" alt="" /></div>
          <div class="ph frame" id="s05-p2" style="left:800px;top:660px;width:330px;height:190px"><img src="@P/town-08-cardinal-carter.jpg" alt="" /></div>
          <div class="chip cream" id="s05-c1" style="left:1170px;top:725px">주변 명문 공립고</div>
          <div class="abs h" id="s05-big">토론토의 대치동</div>
          <div class="chip" id="s05-c2" style="left:800px;top:560px">학군 동네</div>""",
    js="""
pop('#s05-c0',T('5분에서'));
flip('#s05-b1',T('토론토 공립교육청'));flip('#s05-b2',T('가톨릭교육청'));
pop(['#s05-p1','#s05-p2'],T('이름난 공립'),0.15);inn('#s05-c1',T('이름난 공립')+0.4,{x:-20,y:0});
outt(['#s05-b1','#s05-b2','#s05-p1','#s05-p2','#s05-c1','#s05-c0'],T('한국으로 치면')-0.2,{s:0.9});
kin('#s05-big',T('한국으로 치면')+0.3,0.05);
pop('#s05-c2',T('학군 동네'));
""",
    sfx=[("whoosh", "T('한국으로 치면')"), ("impact", "T('대치동')")],
)

# ---------------------------------------------------------------- S06 neighborhood grid
ICONS = {
    "book": '<path d="M6 8 h14 a4 4 0 0 1 4 4 v22 a4 4 0 0 0 -4 -4 H6 Z M42 8 H28 a4 4 0 0 0 -4 4 v22 a4 4 0 0 1 4 -4 h14 Z" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linejoin="round"/>',
    "bag": '<path d="M9 16 h30 l-3 24 H12 Z M17 16 v-4 a7 7 0 0 1 14 0 v4" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linejoin="round"/>',
    "food": '<path d="M14 6 v14 a4 4 0 0 0 8 0 V6 M18 6 v36 M34 6 c-6 4 -6 16 0 18 v18" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="round"/>',
    "art": '<path d="M24 6 a18 18 0 1 0 0 36 c3 0 4-3 2-5 s-1-6 3-6 h5 a8 8 0 0 0 8-8 C42 13 34 6 24 6 Z" fill="none" stroke="currentColor" stroke-width="3.4"/><circle cx="15" cy="21" r="3" fill="currentColor"/><circle cx="24" cy="14" r="3" fill="currentColor"/><circle cx="33" cy="20" r="3" fill="currentColor"/>',
    "train": '<rect x="10" y="6" width="28" height="30" rx="7" fill="none" stroke="currentColor" stroke-width="3.4"/><path d="M10 22 h28 M16 36 l-5 7 M32 36 l5 7" stroke="currentColor" stroke-width="3.4" stroke-linecap="round"/><circle cx="18" cy="29" r="2.5" fill="currentColor"/><circle cx="30" cy="29" r="2.5" fill="currentColor"/>',
}


def icon_chip(cid, icon, label, x, y):
    return (f'<div class="chip ic" id="{cid}" style="left:{x}px;top:{y}px"><svg viewBox="0 0 48 48" class="ico">{ICONS[icon]}</svg>'
            f'<span>{label}</span></div>')


S["s06"] = dict(
    css="""
R .g{position:absolute;width:570px;height:310px}
R .ic{display:flex;align-items:center;gap:14px;color:#fff}
R .ico{width:40px;height:40px;color:#e8b931}
""",
    bg="",
    body="""
          <div class="ph frame g" id="s06-g1" style="left:110px;top:140px"><img src="@P/town-14-library.jpg" alt="" /><div class="lab">공립 도서관</div></div>
          <div class="ph frame g" id="s06-g2" style="left:710px;top:140px"><img src="@P/town-04-mall.jpg" alt="" /><div class="lab">쇼핑몰</div></div>
          <div class="ph frame g" id="s06-g3" style="left:110px;top:480px"><img src="@P/town-05-foodcourt.jpg" alt="" /><div class="lab">푸드코트</div></div>
          <div class="ph frame g" id="s06-g4" style="left:710px;top:480px"><img src="@P/town-20-artcentre.jpg" alt="" /><div class="lab">아트센터</div></div>
""" + "\n".join([
        icon_chip("s06-i1", "book", "도서관", 1380, 160),
        icon_chip("s06-i2", "bag", "쇼핑몰", 1380, 280),
        icon_chip("s06-i3", "food", "푸드코트", 1380, 400),
        icon_chip("s06-i4", "art", "아트센터", 1380, 520),
        icon_chip("s06-i5", "train", "지하철", 1380, 640)]) + """
          <div class="pill" id="s06-p" style="left:1380px;top:752px">걸어서 해결</div>
          <div class="card" id="s06-cd" data-layout-allow-overlap style="left:170px;top:330px;width:1140px;height:200px;display:flex;align-items:center;justify-content:center"><div class="h" style="font-size:66px">안전하고, <span class="red">할 게 있는</span> 동네</div></div>""",
    js="""
flip('#s06-g1',T('공립 도서관'));pop('#s06-i1',T('공립 도서관'));
flip('#s06-g2',T('쇼핑몰'));pop('#s06-i2',T('쇼핑몰'));
flip('#s06-g3',T('푸드코트'));pop('#s06-i3',T('푸드코트'));
flip('#s06-g4',T('아트센터'));pop('#s06-i4',T('아트센터'));pop('#s06-i5',T('아트센터')+0.5);
['#s06-g1','#s06-g2','#s06-g3','#s06-g4'].forEach((s,i)=>kb(s+' img',T('공립 도서관'),D,{s:1.0},{s:1.08,x:(i%2?-1.5:1.5)}));
pop('#s06-p',T('걸어서'));
tl.to(['#s06-g1','#s06-g2','#s06-g3','#s06-g4'],{opacity:0.35,duration:0.5},T('아이를 혼자'));
inn('#s06-cd',T('안전하고'),{y:30,s:0.92});
""",
    sfx=[("pop", "T('공립 도서관')"), ("pop", "T('쇼핑몰')"), ("pop", "T('푸드코트')"), ("pop", "T('아트센터')")],
)
