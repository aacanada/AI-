"""Scenes 01-07. Coordinates are 1920x1080 px. Cue list R comes from timing.json."""

P = "assets/photos/"

S = {}

# ---------------------------------------------------------------- 01 hook
S["01-hook"] = dict(
    bg="""        <div class="abs" id="s01-dark" style="inset:0;background:#16324F"></div>
        <div class="ghost" style="left:-40px;top:560px;color:rgba(250,246,239,.05)">고교학점제</div>""",
    css="""
R .w{color:#FAF6EF}
R #s01-photo{position:absolute;inset:0;overflow:hidden;opacity:0}
R #s01-photo img{width:100%;height:100%;object-fit:cover;object-position:50% 40%}
R #s01-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(22,50,79,0) 30%,rgba(22,50,79,.86) 92%);opacity:0}
R .pin{position:absolute;width:44px;height:44px;border-radius:50% 50% 50% 0;background:#FAF6EF}
""",
    body=f"""
          <div class="abs l w" id="s01-k1" style="left:160px;top:250px;font-size:28px;color:#F3C969">중3 · 고1 자녀를 둔 부모님</div>
          <div class="abs h w" id="s01-k2" style="left:154px;top:300px;font-size:104px">요즘 고민, 많으시죠</div>
          <div class="abs h w" id="s01-k3" style="left:154px;top:470px;font-size:150px">5등급 내신</div>
          <div class="chip" id="s01-k3b" style="left:160px;top:410px;background:transparent;border-color:#F3C969;color:#F3C969">고교학점제</div>
          <svg class="abs" id="s01-crack" style="left:140px;top:440px;width:900px;height:240px" viewBox="0 0 900 240"><path d="M10 120 L120 96 L190 150 L280 70 L360 140 L450 90 L520 170 L610 110 L700 150 L790 80 L890 120" fill="none" stroke="#E8572B" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <div class="abs b w" id="s01-k4" style="left:160px;top:690px;font-size:38px;color:rgba(250,246,239,.8)">한 번 미끄러지면 되돌리기 어려운 구조</div>
          <div class="abs" id="s01-map" style="left:0;top:0;width:1920px;height:1080px">
            <div class="abs" style="left:260px;top:560px;width:1400px;height:4px;background:rgba(250,246,239,.25)" id="s01-line"></div>
            <div class="pin" id="s01-p1" style="left:300px;top:500px"></div>
            <div class="abs hd w" id="s01-p1t" style="left:250px;top:600px;font-size:40px">밴쿠버</div>
            <div class="pin" id="s01-p2" style="left:1560px;top:500px"></div>
            <div class="abs hd w" id="s01-p2t" style="left:1510px;top:600px;font-size:40px">토론토</div>
            <div class="abs hd w" id="s01-q" style="left:900px;top:380px;width:120px;text-align:center;font-size:120px;color:#F3C969">?</div>
            <div class="abs b w" id="s01-k5" style="left:560px;top:690px;width:800px;text-align:center;font-size:38px;color:rgba(250,246,239,.85)">대부분의 조기유학 이야기는 여기서 멈춥니다</div>
          </div>
          <div id="s01-photo"><img src="{P}01c-hero-lake-jump-notext.jpg" alt="" /></div>
          <div id="s01-shade"></div>
          <div class="abs script" id="s01-t1" style="left:150px;top:520px;font-size:130px;color:#fff">Vernon,</div>
          <div class="abs h" id="s01-t2" style="left:150px;top:660px;font-size:104px;color:#fff">아는 사람만 아는 캐나다</div>
          <div class="abs b" id="s01-t3" style="left:156px;top:792px;font-size:34px;color:rgba(250,246,239,.92)">브리티시컬럼비아주 · 오카나간 밸리</div>
          <div class="flash" id="s01-flash"></div>""",
    js="""
inn('#s01-k1',R[0],{y:20});inn('#s01-k2',R[0]+0.2,{y:40});
outt('#s01-k1',R[1]-0.4);outt('#s01-k2',R[1]-0.4,{y:-30});
inn('#s01-k3b',R[1],{s:0.7});inn('#s01-k3',R[1]+0.25,{y:50,d:0.7});
draw('#s01-crack path',R[1]+2.0,0.7);
tl.to('#s01-k3',{x:-14,duration:0.08,ease:'none',repeat:3,yoyo:true},R[1]+2.6);
inn('#s01-k4',R[1]+2.4,{y:20});
outt(['#s01-k3','#s01-k3b','#s01-crack','#s01-k4'],R[2]-0.4);
grow('#s01-line',R[2],1.0);
inn('#s01-p1',R[2]+0.6,{y:-60,e:'power3.out'});inn('#s01-p1t',R[2]+0.8,{y:10});
inn('#s01-p2',R[2]+1.4,{y:-60});inn('#s01-p2t',R[2]+1.6,{y:10});
inn('#s01-k5',R[2]+2.6,{y:20});
inn('#s01-q',R[3]-0.2,{y:-200,d:0.7});
tl.fromTo('#s01-flash',{opacity:0},{opacity:1,duration:0.12,ease:'none'},R[3]+1.6);
tl.set('#s01-photo',{opacity:1},R[3]+1.72);tl.set(['#s01-map','#s01-dark'],{opacity:0},R[3]+1.72);
tl.to('#s01-flash',{opacity:0,duration:0.6,ease:'power2.out'},R[3]+1.74);
kb('#s01-photo img',R[3]+1.72,D-R[3]-1.72,{s:1.0,y:-2},{s:1.09,y:2});
tl.fromTo('#s01-shade',{opacity:0},{opacity:1,duration:1.2},R[4]-0.6);
inn('#s01-t1',R[4]-0.2,{y:30,r0:-10,r:-5,d:0.9});inn('#s01-t2',R[4]+0.5,{y:40});inn('#s01-t3',R[4]+1.2,{y:16});
""",
)

# ---------------------------------------------------------------- 02 two minds
S["02-two-minds"] = dict(
    bg="""        <div class="glow" style="left:620px;top:200px;width:700px;height:700px"></div>""",
    css="""""",
    body=f"""
          <div class="abs hd" id="s02-t" style="left:120px;top:92px;font-size:68px">부모님의 두 마음</div>
          <div class="pol" id="s02-a" style="left:150px;top:200px;width:500px;height:590px"><div class="ph"><img src="{P}18-students-lockers.jpg" alt="" /></div><div class="cap">like a Canadian kid</div></div>
          <div class="abs hd" id="s02-al" style="left:170px;top:820px;font-size:44px">캐나다 아이처럼</div>
          <div class="chip lake" id="s02-ac1" style="left:690px;top:300px">현지 친구들과</div>
          <div class="chip lake" id="s02-ac2" style="left:690px;top:380px">부대끼며 자라는 유학</div>
          <div class="pol" id="s02-b" style="left:1270px;top:200px;width:500px;height:590px"><div class="ph"><img src="{P}17-classroom-writing.jpg" alt="" /></div><div class="cap">a great university</div></div>
          <div class="abs hd" id="s02-bl" style="left:1290px;top:820px;font-size:44px">좋은 대학</div>
          <svg class="abs" id="s02-arrow" style="left:680px;top:430px;width:560px;height:280px" viewBox="0 0 560 280">
            <path id="s02-c1" d="M10 40 C 200 40, 230 140, 470 140" fill="none" stroke="#1F8A99" stroke-width="10" stroke-linecap="round"/>
            <path id="s02-c2" d="M10 240 C 200 240, 230 140, 470 140" fill="none" stroke="#1F8A99" stroke-width="10" stroke-linecap="round"/>
            <path id="s02-c3" d="M440 108 L500 140 L440 172" fill="none" stroke="#1F8A99" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <div class="abs l" id="s02-same" style="left:760px;top:720px;width:400px;text-align:center;font-size:34px;color:#146A77">같은 방향</div>""",
    js="""
inn('#s02-t',R[0],{y:30});
pol('#s02-a',R[1],-6);inn('#s02-al',R[1]+0.6,{y:16});
inn('#s02-ac1',R[2],{x:-30,y:0});inn('#s02-ac2',R[2]+0.5,{x:-30,y:0});
outt(['#s02-ac1','#s02-ac2'],R[3]-0.3);
pol('#s02-b',R[3],5);inn('#s02-bl',R[3]+0.6,{y:16});
draw('#s02-c1',R[4],1.1);draw('#s02-c2',R[4]+0.1,1.1);draw('#s02-c3',R[4]+1.1,0.4);
inn('#s02-same',R[4]+1.4,{y:16});
tl.to('#s02-a',{x:40,duration:1.2,ease:'power2.inOut'},R[4]+0.3);tl.to('#s02-b',{x:-40,duration:1.2,ease:'power2.inOut'},R[4]+0.3);
""",
)

# ---------------------------------------------------------------- 03 university
S["03-university"] = dict(
    bg=f"""        <div class="abs" style="inset:0;opacity:.10"><img src="{P}17-classroom-writing.jpg" alt="" style="width:100%;height:100%;object-fit:cover;filter:blur(18px)" /></div>
        <div class="glow warm" style="left:1300px;top:-100px;width:700px;height:700px"></div>""",
    css="""
R .uc{width:520px;height:400px;padding:36px}
R .uc .k{font-size:24px;color:#146A77}
R .uc .n{font-size:44px;margin:8px 0 26px}
R .uc .i{font-size:34px;font-weight:500;line-height:1.7;opacity:0}
""",
    body="""
          <div class="abs hd" id="s03-t" style="left:120px;top:92px;font-size:68px">대학이 보는 것</div>
          <div class="abs" id="s03-cards" style="left:0;top:0;width:1920px;height:1080px">
            <div class="card uc" id="s03-c1" style="left:120px;top:220px"><div class="l k">CANADA</div><div class="hd n">캐나다 대학</div><div class="i" id="s03-c1a">내신 성적</div><div class="i" id="s03-c1b">학과별 필수 과목</div></div>
            <div class="card uc" id="s03-c2" style="left:700px;top:220px"><div class="l k">USA</div><div class="hd n">미국 대학</div><div class="i" id="s03-c2a">내신 + 비교과</div><div class="i" id="s03-c2b">에세이</div></div>
            <div class="card uc" id="s03-c3" style="left:1280px;top:220px"><div class="l k">KOREA</div><div class="hd n">한국 해외고 전형</div><div class="i" id="s03-c3a">성적 · 비교과</div><div class="i" id="s03-c3b">에세이 · 인터뷰</div></div>
          </div>
          <div class="abs" id="s03-stamp" style="left:560px;top:330px;width:800px;height:220px;border:8px solid #16324F;border-radius:28px;background:#FAF6EF"></div>
          <div class="abs h" id="s03-stampt" style="left:560px;top:380px;width:800px;text-align:center;font-size:84px">입학보다 버티는 힘</div>
          <div class="abs b" id="s03-sub" style="left:460px;top:600px;width:1000px;text-align:center;font-size:40px">대학 1학년, 결국 <b>영어의 기초 체력</b></div>
          <div class="hlbar" id="s03-h1" style="left:120px;top:742px;width:390px"></div>
          <div class="hlbar" id="s03-h2" style="left:600px;top:742px;width:560px"></div>
          <div class="hlbar" id="s03-h3" style="left:1250px;top:742px;width:400px"></div>
          <div class="abs h" id="s03-k1" style="left:120px;top:672px;font-size:72px">탄탄한 영어</div>
          <div class="abs h" id="s03-k2" style="left:600px;top:672px;font-size:72px">믿을 수 있는 내신</div>
          <div class="abs h" id="s03-k3" style="left:1250px;top:672px;font-size:72px">진짜 비교과</div>
          <div class="abs hd" id="s03-qq" style="left:120px;top:800px;font-size:44px;color:#146A77">이 세 가지가 자연스럽게 만들어지는 곳은?</div>""",
    js="""
inn('#s03-t',R[0],{y:30});
inn('#s03-c1',R[1],{y:60});inn('#s03-c1a',R[1]+2.6,{y:14});inn('#s03-c1b',R[1]+4.2,{y:14});
inn('#s03-c2',R[2],{y:60});inn('#s03-c2a',R[2]+0.9,{y:14});inn('#s03-c2b',R[2]+2.2,{y:14});
inn('#s03-c3',R[3],{y:60});inn('#s03-c3a',R[3]+3.3,{y:14});inn('#s03-c3b',R[3]+4.6,{y:14});
tl.to('#s03-cards',{opacity:0.18,duration:0.6},R[4]+1.2);
inn('#s03-stamp',R[4]+1.4,{s:1.5,y:0,d:0.45,e:'power4.out'});inn('#s03-stampt',R[4]+1.45,{s:1.5,y:0,d:0.45,e:'power4.out'});
inn('#s03-sub',R[5],{y:20});
outt(['#s03-stamp','#s03-stampt','#s03-sub'],R[6]-0.2,{s:0.9});
tl.to('#s03-cards',{opacity:0,duration:0.5},R[6]-0.2);
inn('#s03-k1',R[6]+1.2,{y:30});grow('#s03-h1',R[6]+1.5,0.6);
inn('#s03-k2',R[6]+2.4,{y:30});grow('#s03-h2',R[6]+2.7,0.6);
inn('#s03-k3',R[6]+4.0,{y:30});grow('#s03-h3',R[6]+4.3,0.6);
inn('#s03-qq',R[7],{y:20});
tl.to(['#s03-k1','#s03-k2','#s03-k3','#s03-h1','#s03-h2','#s03-h3'],{y:-300,duration:0.8,ease:'power3.inOut'},R[7]-0.3);
tl.to('#s03-qq',{y:-300,duration:0.8,ease:'power3.inOut'},R[7]+0.6);
""",
)

# ---------------------------------------------------------------- 04 where
S["04-where"] = dict(
    bg="""        <div class="ghost" style="left:900px;top:700px">OKANAGAN</div>""",
    css="""
R .city{position:absolute;width:26px;height:26px;border-radius:50%;background:#16324F}
R .vpin{position:absolute;width:56px;height:56px;border-radius:50% 50% 50% 0;background:#E8572B}
R .ring{position:absolute;width:140px;height:140px;border-radius:50%;border:6px solid #1F8A99}
R .tile{position:absolute;width:380px;height:300px;border-radius:22px;overflow:hidden;box-shadow:0 14px 30px rgba(22,50,79,.22)}
R .tile img{width:100%;height:100%;object-fit:cover}
R .tile .tl{position:absolute;left:16px;bottom:14px;background:rgba(22,50,79,.85);color:#FAF6EF;font-weight:800;font-size:26px;padding:6px 16px;border-radius:99px}
""",
    body=f"""
          <div class="abs" id="s04-map" style="left:0;top:0;width:1920px;height:1080px">
            <div class="abs hd" id="s04-mt" style="left:120px;top:92px;font-size:60px">지도를 펼쳐 보면</div>
            <svg class="abs" style="left:0;top:0;width:1920px;height:1080px" viewBox="0 0 1920 1080">
              <path id="s04-coast" d="M180 980 C 240 820, 300 760, 360 700 C 420 640, 380 560, 450 480 C 520 400, 500 300, 560 220" fill="none" stroke="rgba(22,50,79,.22)" stroke-width="6" stroke-dasharray="2 14" stroke-linecap="round"/>
              <ellipse id="s04-ok" cx="1250" cy="560" rx="46" ry="230" transform="rotate(12 1250 560)" fill="#1F8A99" opacity=".0"/>
              <ellipse id="s04-ka" cx="1440" cy="420" rx="28" ry="120" transform="rotate(-8 1440 420)" fill="#1F8A99" opacity=".0"/>
              <path id="s04-fly" d="M420 720 C 700 520, 1000 520, 1270 690" fill="none" stroke="#E8572B" stroke-width="7" stroke-dasharray="18 14" stroke-linecap="round"/>
              <path id="s04-road" d="M1270 700 C 1330 600, 1360 470, 1370 330" fill="none" stroke="#16324F" stroke-width="7" stroke-linecap="round"/>
            </svg>
            <div class="city" id="s04-van" style="left:407px;top:707px"></div>
            <div class="abs hd" id="s04-vant" style="left:330px;top:750px;font-size:40px">밴쿠버</div>
            <div class="chip" id="s04-flyt" style="left:700px;top:470px">✈ 비행기 45분</div>
            <div class="city" id="s04-kel" style="left:1257px;top:687px"></div>
            <div class="abs hd" id="s04-kelt" style="left:1030px;top:730px;font-size:36px">켈로나 공항</div>
            <div class="chip" id="s04-roadt" style="left:1420px;top:560px">차로 30분</div>
            <div class="abs b" id="s04-okt" style="left:1000px;top:420px;font-size:28px;color:#146A77">오카나간 호수</div>
            <div class="abs b" id="s04-kat" style="left:1500px;top:440px;font-size:28px;color:#146A77">칼라말카 호수</div>
            <div class="ring" id="s04-ring" style="left:1300px;top:258px"></div>
            <div class="vpin" id="s04-pin" style="left:1342px;top:270px"></div>
            <div class="abs h" id="s04-vt" style="left:1420px;top:250px;font-size:64px">버논</div>
          </div>
          <div class="abs" id="s04-pano" style="left:0;top:0;width:1920px;height:600px;overflow:hidden"><img src="{P}02-okanagan-panorama.jpg" alt="" style="height:600px;width:auto;display:block" id="s04-panoimg" /></div>
          <div class="chip solid" id="s04-i1" style="left:120px;top:640px">인구 5.8만</div>
          <div class="chip solid" id="s04-i2" style="left:400px;top:640px">오카나간 밸리 45만</div>
          <div class="chip solid" id="s04-i3" style="left:810px;top:640px">켈로나까지 40~50분</div>
          <div class="abs script" id="s04-cal" style="left:120px;top:250px;font-size:96px;color:#1F8A99">California of Canada</div>
          <div class="abs h" id="s04-calk" style="left:120px;top:390px;font-size:84px">캐나다의 캘리포니아</div>
          <div class="tile" id="s04-s1" style="left:1040px;top:120px"><img src="{P}11-kayak-lake.jpg" alt="" /><div class="tl">여름</div></div>
          <div class="tile" id="s04-s2" style="left:1440px;top:120px"><img src="{P}04-students-canada-flag.jpg" alt="" /><div class="tl">호수</div></div>
          <div class="tile" id="s04-s3" style="left:1040px;top:450px"><img src="{P}07-park-autumn.jpg" alt="" /><div class="tl">가을</div></div>
          <div class="tile" id="s04-s4" style="left:1440px;top:450px"><img src="{P}05-silverstar-ski-powder.jpg" alt="" /><div class="tl">겨울 스키</div></div>
          <div class="chip lake" id="s04-temp1" style="left:120px;top:560px">여름 30~35°C · 수영·카약</div>
          <div class="chip lake" id="s04-temp2" style="left:120px;top:650px">겨울 0~5°C · 세계적 스키장</div>""",
    js="""
inn('#s04-mt',R[0],{y:20});
inn('#s04-van',R[1],{s:0,y:0});inn('#s04-vant',R[1]+0.2,{y:10});
(function(){const p=q('#s04-fly');const L=p.getTotalLength();tl.fromTo(p,{strokeDashoffset:L,strokeDasharray:'18 14'},{strokeDashoffset:0,duration:1.4,ease:'power2.inOut'},R[1]+0.4);})();
tl.fromTo('#s04-fly',{opacity:0},{opacity:1,duration:0.2},R[1]+0.4);
inn('#s04-flyt',R[1]+1.0,{s:0.6,y:0});
inn('#s04-kel',R[1]+1.8,{s:0,y:0});inn('#s04-kelt',R[1]+2.0,{y:10});
draw('#s04-road',R[1]+3.2,0.8);inn('#s04-roadt',R[1]+3.6,{s:0.6,y:0});
tl.fromTo('#s04-ok',{opacity:0},{opacity:0.75,duration:0.8},R[2]);inn('#s04-okt',R[2]+0.3,{y:10});
tl.fromTo('#s04-ka',{opacity:0},{opacity:0.75,duration:0.8},R[2]+1.0);inn('#s04-kat',R[2]+1.3,{y:10});
inn('#s04-pin',R[2]+2.2,{y:-160,d:0.7});inn('#s04-vt',R[2]+2.6,{x:-20,y:0});
tl.fromTo('#s04-ring',{scale:0.4,opacity:0.9},{scale:1.4,opacity:0,duration:1.4,ease:'power2.out',repeat:1},R[2]+2.8);
outt('#s04-map',R[3]-0.4);
tl.fromTo('#s04-pano',{clipPath:'inset(0 0 0 100%)'},{clipPath:'inset(0 0 0 0%)',duration:0.9,ease:'power3.inOut'},R[3]-0.3);
tl.fromTo('#s04-panoimg',{x:0},{x:-(2055-1920),duration:R[5]-R[3],ease:'none'},R[3]-0.3);
inn('#s04-i1',R[3]+0.6,{s:0.7,y:0});inn('#s04-i2',R[3]+3.2,{s:0.7,y:0});inn('#s04-i3',R[3]+6.8,{s:0.7,y:0});
outt(['#s04-i1','#s04-i2','#s04-i3'],R[4]-0.3);
tl.to('#s04-pano',{opacity:0,duration:0.6},R[4]-0.3);
inn('#s04-cal',R[4],{y:30,r0:-6,d:0.9});inn('#s04-calk',R[4]+0.7,{y:30});
tl.to(['#s04-cal','#s04-calk'],{y:-110,duration:0.8,ease:'power3.inOut'},R[5]-0.2);
pol('#s04-s1',R[5],-2);pol('#s04-s2',R[5]+0.8,2);inn('#s04-temp1',R[5]+0.6,{x:-30,y:0});
pol('#s04-s3',R[6]-0.2,1);pol('#s04-s4',R[6]+0.6,-2);inn('#s04-temp2',R[6]+0.8,{x:-30,y:0});
qa('.tile img').forEach((im,i)=>kb(im,R[5]+i*0.6,D-R[5],{s:1},{s:1.08}));
""",
)

# ---------------------------------------------------------------- 05 SP1
S["05-sp1-english"] = dict(
    bg=f"""        <div class="full" id="s05-photo"><img src="{P}15-classroom-teacher.jpg" alt="" /></div>""",
    css="""
R .dot{position:absolute;width:26px;height:26px;border-radius:50%;background:#2BA7B8}
R .dot.k{background:#E8572B}
R .seat{position:absolute;width:64px;height:64px;border-radius:14px;background:#2BA7B8}
R .stat .n{font-weight:900;font-size:58px;color:#7FD3DE;font-variant-numeric:tabular-nums}
R .stat .t{font-weight:500;font-size:24px;color:#FAF6EF}
""",
    body="""
          <div class="panel" id="s05-panel" style="left:56px;top:56px;width:800px;height:830px"></div>
          <div class="sticker" id="s05-st" style="left:100px;top:96px">SELLING POINT 01</div>
          <div class="abs hd" id="s05-t" style="left:100px;top:160px;font-size:66px;color:#FAF6EF">영어만 쓰는 교실</div>
          <div class="abs" id="s05-grid" style="left:100px;top:270px;width:330px;height:330px"></div>
          <div class="abs h" id="s05-pct" style="left:470px;top:300px;font-size:150px;color:#7FD3DE;font-variant-numeric:tabular-nums">0%</div>
          <div class="abs b" id="s05-pctl" style="left:478px;top:470px;font-size:32px;color:#FAF6EF">현지 캐나다 학생</div>
          <div class="abs stat" id="s05-a" style="left:100px;top:630px"><div class="n" id="s05-an">0</div><div class="t">SD22 전체 학생</div></div>
          <div class="abs stat" id="s05-b" style="left:380px;top:630px"><div class="n" id="s05-bn">0</div><div class="t">국제학생</div></div>
          <div class="abs stat" id="s05-c" style="left:610px;top:630px"><div class="n" id="s05-cn">0</div><div class="t">출신 국가</div></div>
          <div class="chip sand" id="s05-lock" style="left:100px;top:770px">학교별 한국 학생 정원 상한</div>
          <div class="abs" id="s05-seats" style="left:960px;top:610px;width:880px;height:240px">
            <div class="abs" style="left:0;top:0;width:880px;height:240px;border-radius:28px;background:rgba(250,246,239,.94)"></div>
            <div class="abs l" style="left:40px;top:28px;font-size:24px;color:#16324F">한국 학생 자리</div>
            <div class="seat" id="s05-q1" style="left:40px;top:90px"></div><div class="seat" id="s05-q2" style="left:124px;top:90px"></div><div class="seat" id="s05-q3" style="left:208px;top:90px"></div><div class="seat" id="s05-q4" style="left:292px;top:90px"></div><div class="seat" id="s05-q5" style="left:376px;top:90px"></div>
            <div class="abs b" id="s05-qa" style="left:490px;top:86px;width:360px;font-size:32px;line-height:1.4;color:#16324F">졸업생이 나가야<br />자리가 생깁니다</div>
          </div>
          <div class="abs" id="s05-circ" style="left:1300px;top:150px;width:460px;height:460px;border-radius:50%;overflow:hidden;border:10px solid #FAF6EF;box-shadow:0 18px 40px rgba(22,50,79,.35)"><img src="assets/photos/16-classroom-overhead.jpg" alt="" style="width:100%;height:100%;object-fit:cover" /></div>
          <div class="chip" id="s05-ce" style="left:1250px;top:640px">교실 · 복도 · 클럽 모두 영어</div>""",
    js="""
(function(){const g=q('#s05-grid');for(let i=0;i<100;i++){const d=document.createElement('div');d.className='dot'+(i>=95?' k':'');d.style.left=(i%10)*33+'px';d.style.top=Math.floor(i/10)*33+'px';g.appendChild(d);}})();
kb('#s05-photo img',0,D,{s:1.02},{s:1.1,x:-2});
tl.fromTo('#s05-panel',{x:-900},{x:0,duration:0.8,ease:'power3.out'},0.2);
inn('#s05-st',R[0],{r0:-14,r:-4,s:0.6,y:0});inn('#s05-t',R[0]+0.3,{y:24});
qa('#s05-grid .dot').forEach((d,i)=>tl.fromTo(d,{scale:0,opacity:0},{scale:1,opacity:1,duration:0.35,ease:'power3.out'},R[1]+((i%10)+Math.floor(i/10))*0.045));
count('#s05-pct',0,95,R[1]+0.3,2.4,v=>Math.round(v)+'%');inn('#s05-pctl',R[1]+1.2,{y:12});
inn('#s05-a',R[2],{y:20});count('#s05-an',0,8600,R[2],1.6,v=>Math.round(v).toLocaleString('en-US'));
inn('#s05-b',R[2]+2.2,{y:20});count('#s05-bn',0,300,R[2]+2.2,1.4,v=>Math.round(v)+'+');
inn('#s05-c',R[2]+3.6,{y:20});count('#s05-cn',0,20,R[2]+3.6,1.2,v=>Math.round(v)+'+');
inn('#s05-lock',R[3],{s:0.6,y:0,d:0.5});
inn('#s05-seats',R[3]+1.6,{y:40});
qa('#s05-seats .seat').forEach((s,i)=>tl.fromTo(s,{scale:0},{scale:1,duration:0.4,ease:'power3.out'},R[3]+1.9+i*0.1));
tl.to('#s05-q3',{opacity:0.15,scale:0.8,duration:0.5},R[4]+1.0);
inn('#s05-qa',R[4]+0.4,{y:12});
tl.fromTo('#s05-q3',{backgroundColor:'#2BA7B8'},{backgroundColor:'#E8572B',duration:0.1},R[4]+2.6);
tl.to('#s05-q3',{opacity:1,scale:1,duration:0.5,ease:'power3.out'},R[4]+2.6);
outt('#s05-seats',R[5]-0.3,{y:30});
inn('#s05-circ',R[5],{s:0.3,y:0,d:0.7});inn('#s05-ce',R[5]+0.8,{y:16});
""",
)

# ---------------------------------------------------------------- 06 SP2
S["06-sp2-europe"] = dict(
    bg="""        <div class="wipe"></div>""",
    css="""
R .arc{fill:none;stroke:#E8572B;stroke-width:8;stroke-linecap:round}
""",
    body=f"""
          <div class="abs" id="s06-map" style="left:0;top:0;width:1920px;height:1080px">
            <svg class="abs" style="left:0;top:0;width:1920px;height:1080px" viewBox="0 0 1920 1080">
              <defs><pattern id="s06-wd" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="4" fill="#16324F" opacity=".18"/></pattern></defs>
              <path d="M150 260 C 300 170, 640 180, 730 280 C 780 390, 690 480, 580 520 C 460 550, 320 530, 230 450 C 160 380, 110 320, 150 260Z" fill="url(#s06-wd)"/>
              <path d="M1230 230 C 1350 180, 1560 190, 1630 260 C 1680 330, 1620 410, 1510 440 C 1390 460, 1270 420, 1230 350 C 1200 300, 1195 260, 1230 230Z" fill="url(#s06-wd)"/>
              <path class="arc" id="s06-a1" d="M1420 300 C 1100 90, 600 110, 360 380"/>
              <path class="arc" id="s06-a2" d="M1490 350 C 1150 180, 660 200, 366 392" opacity=".75"/>
              <path class="arc" id="s06-a3" d="M1360 380 C 1100 300, 660 310, 372 400" opacity=".55"/>
            </svg>
            <div class="abs" id="s06-ring" style="left:300px;top:330px;width:130px;height:130px;border-radius:50%;border:6px solid #1F8A99"></div>
            <div class="abs" id="s06-pin" style="left:349px;top:379px;width:32px;height:32px;border-radius:50%;background:#E8572B"></div>
            <div class="abs hd" id="s06-vl" style="left:250px;top:300px;font-size:36px">VERNON</div>
            <div class="abs hd" id="s06-el" style="left:1400px;top:470px;font-size:40px">EUROPE</div>
          </div>
          <div class="sticker" id="s06-st" style="left:120px;top:96px">SELLING POINT 02</div>
          <div class="abs hd" id="s06-t" style="left:120px;top:160px;font-size:68px">유럽 부모들이 고르는 곳</div>
          <div class="pol" id="s06-p1" style="left:160px;top:520px;width:560px;height:330px"><div class="ph"><img src="{P}13-group-photo-lake.jpg" alt="" /></div><div class="cap">Vernon international students</div></div>
          <div class="pol" id="s06-p2" style="left:760px;top:540px;width:230px;height:320px"><div class="ph"><img src="{P}12-dock-group.jpg" alt="" /></div></div>
          <div class="chip solid" id="s06-c1" style="left:1150px;top:600px">독일 등 유럽 출신 최다</div>
          <div class="chip" id="s06-c2" style="left:1150px;top:690px">"스위스 같은 분위기"</div>
          <div class="chip" id="s06-c3" style="left:1150px;top:780px">대도시 대신 버논</div>
          <div class="abs h" id="s06-q" style="left:1150px;top:250px;width:700px;font-size:62px;line-height:1.25">꼼꼼히 따져 보고<br />고른 곳</div>
          <div class="hlbar" id="s06-qh" style="left:1150px;top:398px;width:300px"></div>
          <div class="abs" id="s06-split" style="left:0;top:0;width:960px;height:1080px;overflow:hidden"><img src="{P}04-students-canada-flag.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:40% 50%" id="s06-splitimg" /></div>
          <div class="abs h" id="s06-end" style="left:1060px;top:360px;width:760px;font-size:84px;line-height:1.2">같은 교실,<br />다른 나라 친구들</div>
          <div class="abs b" id="s06-end2" style="left:1064px;top:600px;width:740px;font-size:36px;color:#4A5F78">캐나다 친구들, 유럽에서 온 친구들과 함께</div>""",
    js="""
inn('#s06-st',R[0],{r0:-14,r:-4,s:0.6,y:0});inn('#s06-t',R[0]+0.3,{y:24});
draw('#s06-a1',R[0]+1.2,1.4);draw('#s06-a2',R[0]+1.6,1.4);draw('#s06-a3',R[0]+2.0,1.4);
inn('#s06-el',R[0]+1.0,{y:10});inn('#s06-vl',R[0]+2.6,{y:10});
inn('#s06-pin',R[0]+2.7,{s:0,y:0});
tl.fromTo('#s06-ring',{scale:0.3,opacity:1},{scale:1.5,opacity:0,duration:1.4,ease:'power2.out',repeat:2},R[0]+2.8);
inn('#s06-c1',R[0]+3.6,{x:30,y:0});
pol('#s06-p1',R[1],-3);inn('#s06-c2',R[1]+1.4,{x:30,y:0});
pol('#s06-p2',R[2],5);inn('#s06-c3',R[2]+0.6,{x:30,y:0});
tl.to('#s06-map',{opacity:0.25,duration:0.6},R[3]-0.2);
inn('#s06-q',R[3],{y:30});grow('#s06-qh',R[3]+1.0,0.6);
tl.to(['#s06-p1','#s06-p2'],{scale:1.04,duration:3,ease:'sine.inOut'},R[4]);
tl.fromTo('#s06-split',{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:0.9,ease:'power3.inOut'},R[5]-0.4);
outt(['#s06-map','#s06-st','#s06-t','#s06-p1','#s06-p2','#s06-c1','#s06-c2','#s06-c3','#s06-q','#s06-qh'],R[5]-0.4);
kb('#s06-splitimg',R[5]-0.4,D-R[5]+0.4,{s:1.0},{s:1.07});
inn('#s06-end',R[5]+0.4,{y:30});inn('#s06-end2',R[5]+1.2,{y:16});
""",
)

# ---------------------------------------------------------------- 07 SP3
S["07-sp3-living"] = dict(
    bg="""        <div class="ghost" style="left:760px;top:740px">OKANAGAN</div>""",
    css="""
R .bub{position:absolute;background:#fff;border:4px solid #16324F;border-radius:40px;padding:24px 40px;font-weight:800;font-size:52px;white-space:nowrap}
R .res{position:absolute;font-weight:700;font-size:34px;letter-spacing:.02em;white-space:nowrap}
R .res b{display:inline-block;width:46px;height:46px;border-radius:50%;background:#1F8A99;vertical-align:middle;margin-right:18px}
""",
    body=f"""
          <div class="abs" id="s07-col" style="left:0;top:0;width:730px;height:1080px;overflow:hidden"><img src="{P}03-magical-hillside.jpg" alt="" id="s07-colimg" style="position:absolute;left:-160px;top:0;height:1260px;width:auto" /></div>
          <div class="sticker" id="s07-st" style="left:800px;top:96px">SELLING POINT 03</div>
          <div class="abs hd" id="s07-t" style="left:800px;top:160px;font-size:66px">생활 수준이 높은 동네</div>
          <div class="bub" id="s07-b1" style="left:900px;top:380px">작은 도시면 시골 아니에요?</div>
          <div class="abs" id="s07-no" style="left:1500px;top:330px;width:250px;height:250px;border-radius:50%;border:10px solid #E8572B;color:#E8572B;font-weight:900;font-size:76px;display:flex;align-items:center;justify-content:center">아니요</div>
          <div class="abs b" id="s07-sub" style="left:800px;top:262px;font-size:36px;color:#4A5F78">캐나다 사람들이 은퇴 후 살고 싶어 하는 휴양 도시</div>
          <div class="abs" id="s07-pano" style="left:800px;top:340px;width:1000px;height:290px;overflow:hidden;border-radius:22px"><img src="{P}02-okanagan-panorama.jpg" alt="" id="s07-panoimg" style="position:absolute;top:-25px;left:0;height:340px;width:auto;display:block" /></div>
          <div class="res" id="s07-r1" style="left:800px;top:660px"><b></b>PREDATOR RIDGE 골프 리조트</div>
          <div class="res" id="s07-r2" style="left:800px;top:730px"><b style="background:#7FB236"></b>SILVER STAR 스키 리조트</div>
          <div class="res" id="s07-r3" style="left:800px;top:800px"><b style="background:#E8572B"></b>SPARKLING HILL 스파 리조트</div>
          <div class="pol" id="s07-a1" style="left:820px;top:340px;width:320px;height:300px"><div class="ph"><img src="{P}11-kayak-lake.jpg" alt="" /></div><div class="cap">summer</div></div>
          <div class="pol" id="s07-a2" style="left:1170px;top:330px;width:320px;height:300px"><div class="ph"><img src="{P}06-ski-student.jpg" alt="" /></div><div class="cap">winter</div></div>
          <div class="pol" id="s07-a3" style="left:1520px;top:345px;width:300px;height:290px"><div class="ph"><img src="{P}08-pumpkin-patch.jpg" alt="" /></div><div class="cap">autumn</div></div>
          <div class="chip lake" id="s07-c1" style="left:820px;top:720px">여유 있는</div>
          <div class="chip lake" id="s07-c2" style="left:1040px;top:720px">안전한</div>
          <div class="chip lake" id="s07-c3" style="left:1220px;top:720px">교육에 관심이 높은</div>
          <div class="pol" id="s07-h1" style="left:820px;top:330px;width:310px;height:320px"><div class="ph"><img src="{P}21-homestay-house.jpg" alt="" /></div><div class="cap">homestay</div></div>
          <div class="pol" id="s07-h2" style="left:1160px;top:320px;width:340px;height:330px"><div class="ph"><img src="{P}20-host-family.jpg" alt="" /></div><div class="cap">host family</div></div>
          <div class="pol" id="s07-h3" style="left:1530px;top:335px;width:300px;height:315px"><div class="ph"><img src="{P}22-homestay-kitchen.jpg" alt="" /></div><div class="cap">dinner</div></div>
          <div class="chip solid" id="s07-d1" style="left:820px;top:720px">1인 1실</div>
          <div class="chip solid" id="s07-d2" style="left:1000px;top:720px">교육청이 고른 캐나다 가정</div>
          <div class="chip solid" id="s07-d3" style="left:1420px;top:720px">24시간 담당자</div>""",
    js="""
tl.fromTo('#s07-colimg',{y:-180},{y:0,duration:R[3],ease:'sine.inOut'},0);
tl.fromTo('#s07-col',{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:0.9,ease:'power3.inOut'},0.1);
inn('#s07-st',R[0],{r0:-14,r:-4,s:0.6,y:0});inn('#s07-t',R[0]+0.3,{y:24});
inn('#s07-b1',R[1],{s:0.7,y:20});inn('#s07-no',R[1]+3.0,{s:2.2,y:0,r0:-20,r:-8,d:0.35,e:'power4.out'});
outt(['#s07-b1','#s07-no'],R[2]-0.3,{s:0.9});
inn('#s07-sub',R[2],{y:16});
tl.fromTo('#s07-pano',{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:0.9,ease:'power3.inOut'},R[3]);
tl.fromTo('#s07-panoimg',{x:0},{x:-160,duration:R[5]-R[3],ease:'none'},R[3]);
inn('#s07-r1',R[4],{x:-30,y:0});inn('#s07-r2',R[4]+1.9,{x:-30,y:0});inn('#s07-r3',R[4]+3.6,{x:-30,y:0});
outt(['#s07-pano','#s07-r1','#s07-r2','#s07-r3'],R[5]-0.3);
pol('#s07-a1',R[5],-4);pol('#s07-a2',R[5]+1.4,3);pol('#s07-a3',R[5]+3.0,-2);
inn('#s07-c1',R[6],{s:0.7,y:0});inn('#s07-c2',R[6]+0.8,{s:0.7,y:0});inn('#s07-c3',R[6]+1.8,{s:0.7,y:0});
outt(['#s07-a1','#s07-a2','#s07-a3','#s07-c1','#s07-c2','#s07-c3'],R[7]-0.3,{y:-30});
outt('#s07-sub',R[7]-0.3);
pol('#s07-h1',R[7]+0.2,-3);pol('#s07-h2',R[7]+0.9,2);pol('#s07-h3',R[7]+1.6,-2);
inn('#s07-d1',R[8]+0.6,{s:0.7,y:0});inn('#s07-d2',R[8]+1.6,{s:0.7,y:0});inn('#s07-d3',R[8]+3.2,{s:0.7,y:0});
""",
)
