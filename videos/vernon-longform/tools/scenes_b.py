"""Scenes 08-14."""

P = "assets/photos/"
S = {}

# ---------------------------------------------------------------- 08 SP4
ELECT = ["드라마", "밴드", "오케스트라", "로보틱스", "컴퓨터", "비즈니스", "법", "사진", "프랑스어"]
_chip_pos = [(120, 470), (300, 470), (450, 470), (680, 470), (120, 560), (300, 560), (520, 560), (630, 560), (120, 650)]
_elect_html = "\n".join(
    f'          <div class="chip" id="s08-e{i}" style="left:{x}px;top:{y}px">{t}</div>'
    for i, (t, (x, y)) in enumerate(zip(ELECT, _chip_pos))
)
SCHOOLS = [
    ("32-school-vernon-secondary", "Vernon Secondary", "1,075명 · 가장 큰 종합 학교"),
    ("30-school-seaton", "W.L. Seaton", "1,000명 · 예술 · 프랑스어 몰입"),
    ("33-school-kalamalka", "Kalamalka", "650명 · 높은 학업 기준"),
    ("34-school-fulton", "Clarence Fulton", "775명 · 운동 · 예술"),
    ("31-school-charles-bloom", "Charles Bloom", "375명 · 작은 마을 분위기"),
]
_school_html = "\n".join(
    f'''          <div class="card sc" id="s08-k{i}" style="left:1300px;top:420px"><div class="ph"><img src="{P}{f}.jpg" alt="" /></div><div class="hd sn" data-layout-allow-overlap>{n}</div><div class="b sd" data-layout-allow-overlap>{d}</div></div>'''
    for i, (f, n, d) in enumerate(SCHOOLS)
)
ACAD = [("축구", "#1F8A99"), ("아이스하키", "#16324F"), ("알파인 스키", "#7FB236"), ("프리스타일 스키", "#1F8A99"), ("노르딕 스키", "#16324F"),
        ("골프", "#7FB236"), ("야구", "#1F8A99"), ("배구", "#16324F"), ("댄스", "#7FB236"), ("어스퀘스트", "#E8572B")]
_acad_html = "\n".join(
    f'          <div class="ac" id="s08-a{i}" style="left:{120 + (i % 5) * 330}px;top:{400 + (i // 5) * 190}px"><b style="background:{c}"></b><span>{t}</span></div>'
    for i, (t, c) in enumerate(ACAD)
)

S["08-sp4-school"] = dict(
    bg="""        <div class="wipe" data-layout-allow-overflow></div>
        <div class="glow" style="left:600px;top:500px;width:700px;height:700px"></div>""",
    css="""
R .sc{width:460px;height:400px;padding:14px}
R .sc .ph{width:100%;height:230px;border-radius:14px;overflow:hidden}
R .sc .sn{font-size:38px;margin-top:16px}
R .sc .sd{font-size:26px;color:#4A5F78;margin-top:4px}
R .ac{position:absolute;width:300px;height:160px;background:#fff;border-radius:22px;border:3px solid rgba(22,50,79,.12);box-shadow:0 10px 24px rgba(22,50,79,.10)}
R .ac b{position:absolute;left:28px;top:28px;width:52px;height:52px;border-radius:50%}
R .ac span{position:absolute;left:28px;top:96px;font-weight:800;font-size:34px;white-space:nowrap}
""",
    body=f"""
          <div class="sticker" id="s08-st" style="left:120px;top:96px">추천 포인트 04</div>
          <div class="abs hd" id="s08-t" style="left:120px;top:160px;width:900px;font-size:66px">캐나다 학생과 같은 교실</div>
          <div class="abs b" id="s08-t2" style="left:122px;top:250px;font-size:36px;color:#4A5F78">국제학교가 아닌 정규 공립학교</div>
          <div class="pol" id="s08-p1" style="left:1130px;top:150px;width:640px;height:500px"><div class="ph"><img src="{P}16-classroom-overhead.jpg" alt="" /></div><div class="cap">same classroom</div></div>
          <div class="pol" id="s08-p2" style="left:1000px;top:520px;width:420px;height:330px"><div class="ph"><img src="{P}15-classroom-teacher.jpg" alt="" /></div></div>
          <div class="abs l" id="s08-el" style="left:122px;top:410px;font-size:24px;color:#146A77">선택 과목</div>
{_elect_html}
          <div class="abs" id="s08-map" style="left:806px;top:0;width:1114px;height:1080px;overflow:hidden"><img src="{P}40-map-playground.jpg" alt="" id="s08-mapimg" style="position:absolute;left:-600px;top:-80px;height:1240px;width:auto" /></div>
          <div class="abs h" id="s08-five" style="left:120px;top:330px;font-size:260px;color:#1F8A99;line-height:1">5</div>
          <div class="abs hd" id="s08-fivet" style="left:300px;top:460px;font-size:56px">곳의 고등학교</div>
{_school_html}
          <div class="abs" id="s08-cover" style="left:1300px;top:110px;width:500px;height:647px;box-shadow:0 20px 44px rgba(22,50,79,.3)"><img src="{P}41-academies-cover.jpg" alt="" style="width:100%;height:100%;object-fit:cover" /></div>
          <div class="abs hd" id="s08-at" style="left:120px;top:300px;font-size:52px">스포츠 · 특기 아카데미</div>
{_acad_html}
          <div class="abs" id="s08-doc" style="left:260px;top:330px;width:380px;height:500px;background:#fff;border-radius:22px;border:4px solid #16324F;box-shadow:0 18px 40px rgba(22,50,79,.18)">
            <div class="abs hd" style="left:36px;top:36px;font-size:40px">대학 지원서</div>
            <div class="abs" style="left:36px;top:120px;width:300px;height:14px;border-radius:7px;background:rgba(22,50,79,.15)"></div>
            <div class="abs" style="left:36px;top:160px;width:250px;height:14px;border-radius:7px;background:rgba(22,50,79,.15)"></div>
            <div class="abs" style="left:36px;top:200px;width:280px;height:14px;border-radius:7px;background:rgba(22,50,79,.15)"></div>
            <div class="chip lake" style="left:36px;top:270px;font-size:26px">아카데미</div>
            <div class="chip lake" style="left:36px;top:340px;font-size:26px">방과후 클럽</div>
            <div class="chip lake" style="left:36px;top:410px;font-size:26px">지역 봉사</div>
          </div>
          <div class="abs b" id="s08-f1" style="left:760px;top:440px;font-size:44px">비교과는 따로 만드는 게 아니라</div>
          <div class="abs h" id="s08-f2" style="left:756px;top:510px;font-size:112px;color:#146A77">생활 그 자체</div>""",
    js="""
inn('#s08-st',R[0],{r0:-14,r:-4,s:0.6,y:0});inn('#s08-t',R[0]+0.3,{y:24});
inn('#s08-t2',R[1]+0.4,{y:14});pol('#s08-p1',R[1]+0.2,3);pol('#s08-p2',R[1]+3.0,-4);
inn('#s08-el',R[2],{y:10});
for(let i=0;i<9;i++){inn('#s08-e'+i,R[2]+0.9+i*0.72,{y:-70,s:0.8,d:0.55});}
outt(['#s08-p1','#s08-p2','#s08-el','#s08-t2'].concat([0,1,2,3,4,5,6,7,8].map(i=>'#s08-e'+i)),R[3]-0.4,{y:20});
tl.fromTo('#s08-map',{clipPath:'inset(0 0 0 100%)'},{clipPath:'inset(0 0 0 0%)',duration:0.9,ease:'power3.inOut'},R[3]-0.3);
tl.fromTo('#s08-mapimg',{x:0,y:0,scale:1},{x:-260,y:-60,scale:1.12,duration:R[6]-R[3],ease:'sine.inOut'},R[3]-0.3);
inn('#s08-five',R[3],{s:0.4,y:0,d:0.7});inn('#s08-fivet',R[3]+0.3,{x:-20,y:0});
const T=[R[4],R[4]+3.0,R[5],R[5]+2.7,R[5]+4.9];
for(let i=0;i<5;i++){
  tl.fromTo('#s08-k'+i,{x:620,opacity:0,rotation:6},{x:0,opacity:1,rotation:0,duration:0.75,ease:'power3.out'},T[i]);
  for(let j=0;j<i;j++){ tl.to('#s08-k'+j,{x:-(i-j)*170,scale:1-(i-j)*0.08,opacity:(i-j)===1?0.3:0,duration:0.75,ease:'power3.out'},T[i]); }
}
outt(['#s08-map','#s08-five','#s08-fivet','#s08-k0','#s08-k1','#s08-k2','#s08-k3','#s08-k4'],R[6]-0.4);
tl.fromTo('#s08-cover',{opacity:0,x:300,rotation:12},{opacity:1,x:0,rotation:-4,duration:0.9,ease:'power3.out'},R[6]);
inn('#s08-at',R[6]+0.5,{y:20});
tl.to('#s08-cover',{x:700,rotation:14,opacity:0,duration:0.7,ease:'power3.in'},R[7]-0.2);
for(let i=0;i<10;i++){inn('#s08-a'+i,R[7]+i*0.72,{s:0.6,y:30,d:0.5});}
outt(['#s08-at','#s08-st','#s08-t'].concat([0,1,2,3,4,5,6,7,8,9].map(i=>'#s08-a'+i)),R[8]-0.3,{s:0.85});
inn('#s08-doc',R[8]+0.1,{y:60,r0:-8,r:-2,d:0.8});
inn('#s08-f1',R[8]+2.2,{y:16});inn('#s08-f2',R[8]+3.6,{y:30,d:0.7});
""",
)

# ---------------------------------------------------------------- 09 SP5
S["09-sp5-graduation"] = dict(
    bg="""        <div class="ghost" style="left:1200px;top:620px;font-size:420px">80</div>""",
    css="""
R .blk{position:absolute;top:420px;height:150px}
R .blk span{position:absolute;left:24px;top:52px;font-weight:800;font-size:34px;color:#fff;white-space:nowrap}
""",
    body="""
          <div class="sticker" id="s09-st" style="left:120px;top:96px">추천 포인트 05</div>
          <div class="abs hd" id="s09-t" style="left:120px;top:160px;font-size:66px">졸업이 빠릅니다</div>
          <div class="abs l" id="s09-endl" style="left:1440px;top:350px;width:360px;text-align:right;font-size:28px">80학점 = BC주 졸업</div>
          <div class="abs" id="s09-track" style="left:120px;top:420px;width:1680px;height:150px;border-radius:24px;background:#F1EADF;border:3px solid rgba(22,50,79,.22)"></div>
          <div class="blk" id="s09-b0" style="left:120px;width:840px;background:#1F8A99;border-radius:24px 0 0 24px"><span>한국 고1 성적 + 한국어 학점 ≈ 40</span></div>
          <div class="blk" id="s09-b1" style="left:960px;width:336px;background:#5E9E22;border-left:5px solid #FAF6EF"><span>1학기 +16</span></div>
          <div class="blk" id="s09-b2" style="left:1296px;width:336px;background:#7FB236;border-left:5px solid #FAF6EF"><span>2학기 +16</span></div>
          <div class="blk" id="s09-b3" style="left:1632px;width:168px;background:#9BC95E;border-left:5px solid #FAF6EF;border-radius:0 24px 24px 0"><span>+8</span></div>
          <div class="abs h" id="s09-num" style="left:120px;top:610px;font-size:180px;color:#146A77;font-variant-numeric:tabular-nums;line-height:1">0</div>
          <div class="abs hd" id="s09-numl" style="left:420px;top:700px;font-size:48px">학점</div>
          <div class="chip solid" id="s09-three" style="left:640px;top:690px">계산상 3학기</div>
          <svg class="abs" id="s09-cap" style="left:1600px;top:600px;width:200px;height:170px" viewBox="0 0 200 170"><path d="M100 20 L190 60 L100 100 L10 60 Z" fill="#16324F"/><path d="M50 80 L50 125 C 70 145, 130 145, 150 125 L150 80 L100 102 Z" fill="#16324F"/><path d="M180 64 L180 120" stroke="#E8572B" stroke-width="8" stroke-linecap="round"/></svg>
          <div class="abs b" id="s09-fn" style="left:120px;top:830px;font-size:30px;color:#4A5F78">* 영어 수준 · ESL 이수 여부에 따라 기간이 달라집니다</div>""",
    js="""
inn('#s09-st',R[0],{r0:-14,r:-4,s:0.6,y:0});inn('#s09-t',R[0]+0.3,{y:24});
grow('#s09-track',R[1],0.9);inn('#s09-endl',R[1]+0.8,{y:12});
grow('#s09-b0',R[2]+0.5,0.9);inn('#s09-num',R[2]+0.5,{y:0});inn('#s09-numl',R[2]+0.7,{y:10});
count('#s09-num',0,40,R[2]+0.5,1.2,v=>Math.round(v));
grow('#s09-b1',R[3]+0.4,0.7);count('#s09-num',40,56,R[3]+0.4,0.7,v=>Math.round(v));
grow('#s09-b2',R[3]+2.0,0.7);count('#s09-num',56,72,R[3]+2.0,0.7,v=>Math.round(v));
grow('#s09-b3',R[3]+3.6,0.5);count('#s09-num',72,80,R[3]+3.6,0.5,v=>Math.round(v));
inn('#s09-three',R[3]+3.0,{s:0.6,y:0});
inn('#s09-cap',R[3]+4.3,{s:0,y:0,d:0.6});
inn('#s09-fn',R[4],{y:12});
""",
)

# ---------------------------------------------------------------- 10 SP6
DAYS = ["월", "화", "수", "목", "금", "토", "일"]
ROWS = ["수업", "방과후", "저녁", "공부"]
_tt = []
for i, d in enumerate(DAYS):
    _tt.append(f'<div class="abs l" style="left:{230 + i * 150}px;top:300px;width:136px;text-align:center;font-size:26px">{d}</div>')
for j, r in enumerate(ROWS):
    _tt.append(f'<div class="abs l" style="left:120px;top:{370 + j * 115}px;font-size:24px;color:#4A5F78">{r}</div>')
# cells: (row, col_start, span, color, label, id)
CELLS = [
    (0, 0, 5, "#1F8A99", "학교 정규 수업", "c0"), (0, 6, 1, "#4E8A1E", "봉사", "c1"),
    (1, 0, 1, "#4E8A1E", "클럽", "c2"), (1, 1, 1, "#4E8A1E", "리더십", "c3"), (1, 2, 1, "#4E8A1E", "경기", "c4"),
    (1, 3, 1, "#E8572B", "1:1 튜터링", "c5"), (1, 4, 1, "#4E8A1E", "봉사", "c6"), (1, 6, 1, "#E8572B", "카운셀링", "c7"),
    (2, 0, 7, "#F3C969", "호스트 가족과 저녁", "c8"),
    (3, 0, 5, "#16324F", "시험 대비 공부", "c9"), (3, 5, 1, "#E8572B", "에세이", "c10"), (3, 6, 1, "#16324F", "공부", "c11"),
]
for (r, c, sp, col, lab, cid) in CELLS:
    txt = "#16324F" if col == "#F3C969" else "#fff"
    _tt.append(f'<div class="cell" id="s10-{cid}" style="left:{220 + c * 150}px;top:{350 + r * 115}px;width:{sp * 150 - 12}px;background:{col};color:{txt}">{lab}</div>')
_tt_html = "\n".join("            " + x for x in _tt)
CHECKS = ["주 1회 2시간 1:1 튜터링", "주 1회 에세이 첨삭", "정기 카운셀링", "휴대폰 사용 지도", "월 1회 이상 한식"]
_ck_html = "\n".join(
    f'          <div class="ck" id="s10-k{i}" style="left:1330px;top:{340 + i * 90}px"><b>✓</b>{t}</div>' for i, t in enumerate(CHECKS)
)

S["10-sp6-care"] = dict(
    bg="""        <div class="glow" style="left:1100px;top:150px;width:800px;height:800px"></div>""",
    css="""
R .cell{position:absolute;height:100px;border-radius:14px;font-weight:800;font-size:24px;display:flex;align-items:center;justify-content:center;white-space:nowrap}
R .ck{position:absolute;font-weight:700;font-size:34px;white-space:nowrap}
R .ck b{display:inline-block;width:52px;height:52px;border-radius:50%;background:#4E8A1E;color:#fff;text-align:center;line-height:52px;margin-right:18px;font-size:30px}
R .duty{position:absolute;background:#16324F;color:#FAF6EF;font-weight:800;font-size:32px;padding:14px 30px;border-radius:99px;white-space:nowrap}
R .stp{position:absolute;width:520px;border-radius:26px 26px 0 0;color:#fff;padding:36px}
R .stp .sn{font-weight:900;font-size:48px}
R .stp .sd{font-weight:500;font-size:28px;margin-top:10px;line-height:1.5}
""",
    body=f"""
          <div class="sticker" id="s10-st" style="left:120px;top:96px">추천 포인트 06</div>
          <div class="abs hd" id="s10-t" style="left:120px;top:160px;font-size:66px">현지 한국인 선생님의 관리</div>
          <div class="card" id="s10-o1" style="left:120px;top:320px;width:430px;height:150px;padding:30px"><div class="l" style="font-size:22px;color:#146A77">SCHOOL DISTRICT 22</div><div class="hd" style="font-size:44px;margin-top:6px">버논 교육청</div></div>
          <div class="abs h" id="s10-plus" style="left:580px;top:345px;font-size:80px;color:#1F8A99">+</div>
          <div class="card" id="s10-o2" style="left:660px;top:320px;width:430px;height:150px;padding:30px"><div class="l" style="font-size:22px;color:#146A77">LOCAL CARE</div><div class="hd" style="font-size:44px;margin-top:6px">토탈 에듀케어</div></div>
          <div class="panel" id="s10-tc" style="left:1180px;top:300px;width:620px;height:420px"></div>
          <div class="abs" id="s10-av" style="left:1240px;top:350px;width:150px;height:150px;border-radius:50%;background:#F3C969"></div>
          <div class="abs h" id="s10-16" style="left:1420px;top:345px;font-size:120px;color:#7FD3DE;font-variant-numeric:tabular-nums">16년</div>
          <div class="abs hd" id="s10-tct" style="left:1240px;top:540px;font-size:44px;color:#FAF6EF">버논 거주 한국인 선생님</div>
          <div class="abs b" id="s10-tcs" style="left:1240px;top:610px;font-size:30px;color:rgba(250,246,239,.85)">학교 · 홈스테이 · 부모님 사이의 연결</div>
          <div class="duty" id="s10-d0" style="left:120px;top:540px">출결 확인</div>
          <div class="duty" id="s10-d1" style="left:370px;top:540px">성적 확인</div>
          <div class="duty" id="s10-d2" style="left:120px;top:630px">학교 담당 선생님 방문</div>
          <div class="duty" id="s10-d3" style="left:120px;top:720px">홈스테이 생활</div>
          <div class="chip sand" id="s10-rep" style="left:500px;top:720px">→ 부모님께 보고</div>
          <div class="abs" id="s10-tt" style="left:0;top:0;width:1920px;height:1080px">
{_tt_html}
          </div>
          <div class="pol" id="s10-din" style="left:1480px;top:60px;width:320px;height:250px"><div class="ph"><img src="{P}22-homestay-kitchen.jpg" alt="" /></div></div>
{_ck_html}
          <div class="abs hd" id="s10-lv" style="left:120px;top:300px;font-size:50px">관리 강도는 가정에 맞게</div>
          <div class="stp" id="s10-s0" style="left:120px;top:620px;height:280px;background:#7FB236"><div class="sn">정착 프로그램</div><div class="sd">현지 정착 지원</div></div>
          <div class="stp" id="s10-s1" style="left:690px;top:500px;height:400px;background:#1F8A99"><div class="sn">가디언 케어</div><div class="sd">월 1회 면담 · 출결·성적 관리 · 생활 전반</div></div>
          <div class="stp" id="s10-s2" style="left:1260px;top:380px;height:520px;background:#16324F"><div class="sn">에듀 가이드</div><div class="sd">1:1 튜터링 · 에세이 첨삭 · 대학 진학 프로젝트까지</div></div>""",
    js="""
inn('#s10-st',R[0],{r0:-14,r:-4,s:0.6,y:0});inn('#s10-t',R[0]+0.3,{y:24});
inn('#s10-o1',R[1]+0.3,{y:40});inn('#s10-plus',R[1]+2.4,{s:0,y:0});inn('#s10-o2',R[1]+2.6,{y:40});
inn('#s10-tc',R[2],{x:60,y:0,d:0.7});inn('#s10-av',R[2]+0.3,{s:0,y:0});
count('#s10-16',0,16,R[2]+0.6,1.4,v=>Math.round(v)+'년');inn('#s10-16',R[2]+0.6,{y:0});
inn('#s10-tct',R[2]+1.2,{y:14});inn('#s10-tcs',R[2]+2.0,{y:10});
inn('#s10-d0',R[3],{s:0.6,y:0});inn('#s10-d1',R[3]+0.9,{s:0.6,y:0});inn('#s10-d2',R[3]+2.4,{s:0.6,y:0});inn('#s10-d3',R[3]+4.2,{s:0.6,y:0});
inn('#s10-rep',R[3]+5.8,{x:-30,y:0});
outt(['#s10-o1','#s10-o2','#s10-plus','#s10-tc','#s10-av','#s10-16','#s10-tct','#s10-tcs','#s10-d0','#s10-d1','#s10-d2','#s10-d3','#s10-rep'],R[4]-0.4,{y:-20});
tl.fromTo('#s10-tt .l',{opacity:0},{opacity:1,duration:0.4,stagger:0.04},R[4]);
const rowAt={c0:R[5],c1:R[5]+0.3,c2:R[5]+1.6,c3:R[5]+1.75,c4:R[5]+1.9,c5:R[5]+2.05,c6:R[5]+2.2,c7:R[5]+2.35,c8:R[5]+3.2,c9:R[7],c10:R[7]+0.3,c11:R[7]+0.45};
Object.keys(rowAt).forEach(k=>grow('#s10-'+k,rowAt[k],0.5));
pol('#s10-din',R[5]+3.6,4);
tl.to(['#s10-c5','#s10-c10','#s10-c7'],{scale:1.08,duration:0.3,yoyo:true,repeat:1,ease:'power2.inOut'},R[6]);
inn('#s10-k0',R[6],{x:30,y:0});inn('#s10-k1',R[6]+1.8,{x:30,y:0});inn('#s10-k2',R[6]+3.6,{x:30,y:0});
inn('#s10-k3',R[7]+0.6,{x:30,y:0});inn('#s10-k4',R[8],{x:30,y:0});
outt(['#s10-tt','#s10-din','#s10-k0','#s10-k1','#s10-k2','#s10-k3','#s10-k4'].concat(Object.keys(rowAt).map(k=>'#s10-'+k)),R[9]-0.4,{y:-20});
inn('#s10-lv',R[9],{y:20});
tl.fromTo('#s10-s0',{y:300,opacity:0},{y:0,opacity:1,duration:0.8,ease:'power3.out'},R[10]);
tl.fromTo('#s10-s1',{y:420,opacity:0},{y:0,opacity:1,duration:0.8,ease:'power3.out'},R[10]+1.9);
tl.fromTo('#s10-s2',{y:540,opacity:0},{y:0,opacity:1,duration:0.8,ease:'power3.out'},R[11]);
""",
)

# ---------------------------------------------------------------- 11 case
NODES = [
    (220, "2020 · VSS 입학", "수학 클럽 · 축구팀"),
    (520, "저널 시작", "사진 · 영상 기록"),
    (820, "2021 · 봉사", "도서관 · 사이언스 센터"),
    (1120, "수학경시 입선", "캐나다 수학학회"),
    (1420, "2022", "U of T 조건부 입학"),
]
_nodes = []
for i, (x, a, b) in enumerate(NODES):
    _nodes.append(f'<div class="nd" id="s11-n{i}" style="left:{x - 18}px;top:452px"></div>')
    _nodes.append(f'<div class="abs" id="s11-t{i}" style="left:{x - 130}px;top:510px;width:260px;text-align:center"><div class="hd" style="font-size:32px">{a}</div><div class="b" style="font-size:26px;color:#4A5F78;margin-top:6px">{b}</div></div>')
_nodes_html = "\n".join("          " + x for x in _nodes)

S["11-case"] = dict(
    bg="",
    css="""
R .nd{position:absolute;width:36px;height:36px;border-radius:50%;background:#1F8A99;border:6px solid #FAF6EF;box-shadow:0 0 0 3px #1F8A99}
""",
    body=f"""
          <div class="abs hd" id="s11-h" style="left:120px;top:92px;font-size:66px">실제 사례</div>
          <div class="card" id="s11-sc" style="left:100px;top:200px;width:300px;height:210px;padding:10px"><img src="{P}32-school-vernon-secondary.jpg" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:14px" /></div>
          <div class="abs" id="s11-line" style="left:160px;top:466px;width:1620px;height:8px;border-radius:4px;background:#16324F;transform-origin:0 50%"></div>
{_nodes_html}
          <div class="abs" id="s11-ring" style="left:1630px;top:380px;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle,rgba(232,87,43,.35) 0%,rgba(232,87,43,0) 70%)"></div>
          <div class="abs" id="s11-fn" style="left:1694px;top:444px;width:52px;height:52px;border-radius:50%;background:#E8572B;border:6px solid #FAF6EF"></div>
          <div class="abs" id="s11-ft" style="left:1200px;top:220px;width:620px;text-align:right"><div class="l" style="font-size:24px;color:#E8572B">FINAL</div><div class="h" style="font-size:52px;color:#E8572B">U of T</div><div class="hd" style="font-size:34px">Computer Science 최종 합격</div></div>
          <div class="hlbar" id="s11-hl" style="left:300px;top:790px;width:500px"></div>
          <div class="abs h" id="s11-c" style="left:120px;top:720px;font-size:84px">버논의 평범한 일상이 만든 결과</div>""",
    js="""
inn('#s11-h',R[0],{y:24});
const LS=[R[1],R[2],R[3],R[4],R[4]+2.6,R[5]];
const frac=[60/1620,360/1620,660/1620,960/1620,1260/1620,1];
tl.fromTo('#s11-line',{scaleX:0},{scaleX:frac[0],duration:0.6,ease:'power3.out'},LS[0]);
for(let i=1;i<6;i++)tl.to('#s11-line',{scaleX:frac[i],duration:0.9,ease:'power3.inOut'},LS[i]-0.3);
pol('#s11-sc',R[1]+0.2,-3);
for(let i=0;i<5;i++){inn('#s11-n'+i,LS[i]+0.3,{s:0,y:0,d:0.5});inn('#s11-t'+i,LS[i]+0.5,{y:16});}
inn('#s11-fn',R[5]+0.6,{s:0,y:0,d:0.5});inn('#s11-ring',R[5]+0.6,{s:0.2,y:0,d:1.0});inn('#s11-ft',R[5]+0.8,{y:20});
inn('#s11-c',R[6],{y:24});grow('#s11-hl',R[6]+1.4,0.6);
""",
    no_out=True,
)

# ---------------------------------------------------------------- 12 cost
COST = [
    ("기본형", 29900, ["학비 · 홈스테이", "가디언 지정 · 의료보험", "교육청 활동비"], "#16324F"),
    ("+ 정착 프로그램", 33900, ["기본형 포함", "현지 정착 지원"], "#16324F"),
    ("가디언 케어", 37500, ["월 1회 면담", "출결 · 성적 관리"], "#16324F"),
    ("에듀 가이드", 44150, ["1:1 튜터링 · 첨삭", "대학 진학 프로젝트"], "#146A77"),
]
_cost = []
for i, (n, v, items, col) in enumerate(COST):
    x = 120 + i * 430
    border = "border:5px solid #1F8A99;" if i == 3 else ""
    li = "".join(f'<div class="ci">✓ {t}</div>' for t in items)
    _cost.append(f'<div class="card cc" id="s12-c{i}" style="left:{x}px;top:270px;{border}"><div class="l cn" style="color:{col}">{n}</div><div class="h cv" id="s12-v{i}" style="color:{col}">$0</div>{li}</div>')
_cost_html = "\n".join("          " + x for x in _cost)

S["12-cost"] = dict(
    bg="""        <div class="ghost" style="left:-40px;top:720px">CAD</div>""",
    css="""
R .cc{width:400px;height:430px;padding:36px}
R .cc .cn{font-size:26px}
R .cc .cv{font-size:76px;margin:14px 0 24px;font-variant-numeric:tabular-nums}
R .cc .ci{font-weight:500;font-size:28px;line-height:1.8}
""",
    body=f"""
          <div class="abs hd" id="s12-t" style="left:120px;top:92px;font-size:66px">비용은 투명하게</div>
          <div class="chip lake" id="s12-p" style="left:700px;top:104px">2026.9 – 2027.6 · 두 학기 · 캐나다달러</div>
{_cost_html}
          <div class="abs b" id="s12-fn" style="left:120px;top:760px;font-size:30px;color:#4A5F78">항공료 · 개인 용돈 별도 · 2026년 10월 기준, 금액은 바뀔 수 있습니다</div>""",
    js="""
inn('#s12-t',R[0],{y:24});inn('#s12-p',R[0]+1.0,{s:0.7,y:0});
const CT=[R[1]+0.5,R[2],R[2]+2.9,R[3]];const V=[29900,33900,37500,44150];
for(let i=0;i<4;i++){inn('#s12-c'+i,CT[i],{y:60,d:0.7});count('#s12-v'+i,0,V[i],CT[i]+0.2,1.3,v=>'$'+Math.round(v).toLocaleString('en-US'));
  tl.fromTo('#s12-c'+i+' .ci',{opacity:0,x:-14},{opacity:1,x:0,duration:0.4,stagger:0.35,ease:'power2.out'},CT[i]+0.9);}
inn('#s12-fn',R[4],{y:12});
""",
)

# ---------------------------------------------------------------- 13 summer prep
S["13-summer-prep"] = dict(
    bg="",
    css="""
R .mo{position:absolute;top:330px;font-weight:700;font-size:30px;letter-spacing:.06em}
""",
    body="""
          <div class="chip" id="s13-tag" style="left:120px;top:96px;border-style:dashed;font-size:24px">입학 전 준비 단계</div>
          <div class="abs hd" id="s13-t" style="left:120px;top:170px;font-size:62px">입학 전 여름 두 달, 켈로나에서 준비</div>
          <div class="mo" id="s13-m6" style="left:120px">6월</div><div class="mo" id="s13-m7" style="left:560px">7월</div><div class="mo" id="s13-m8" style="left:1000px">8월</div><div class="mo" id="s13-m9" style="left:1500px;color:#E8572B">9월</div>
          <div class="abs" id="s13-am" style="left:120px;top:390px;width:1270px;height:130px;border-radius:22px 22px 0 0;background:#1F8A99"></div>
          <div class="abs" id="s13-pm" style="left:120px;top:520px;width:1270px;height:130px;border-radius:0 0 22px 22px;background:#7FB236"></div>
          <div class="abs hd" id="s13-aml" style="left:160px;top:430px;font-size:40px;color:#fff">오전 · 영어</div>
          <div class="abs hd" id="s13-pml" style="left:160px;top:560px;font-size:40px;color:#fff">오후 · 수학 · 역사 과목 용어</div>
          <svg class="abs" id="s13-ar" style="left:1400px;top:470px;width:90px;height:100px" viewBox="0 0 90 100"><path d="M5 50 H70 M48 26 L74 50 L48 74" fill="none" stroke="#E8572B" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <div class="card" id="s13-c" style="left:1500px;top:390px;width:300px;height:260px;padding:36px"><div class="h" style="font-size:60px;color:#E8572B;line-height:1.15">버논<br />입학</div></div>
          <div class="abs h" id="s13-e" style="left:120px;top:730px;font-size:62px">첫 한 달의 적응기를, 미리 지나고 오기</div>""",
    js="""
inn('#s13-tag',R[0],{s:0.7,y:0});inn('#s13-t',R[0]+0.3,{y:24});
['#s13-m6','#s13-m7','#s13-m8'].forEach((m,i)=>inn(m,R[1]+i*0.5,{y:10}));
grow('#s13-am',R[1]+0.4,2.4);grow('#s13-pm',R[1]+0.7,2.4);
inn('#s13-aml',R[2],{x:-20,y:0});inn('#s13-pml',R[2]+1.8,{x:-20,y:0});
inn('#s13-m9',R[2]+2.6,{y:10});draw('#s13-ar path',R[2]+2.8,0.5);inn('#s13-c',R[2]+3.1,{s:0.7,y:0});
inn('#s13-e',R[3],{y:20});
""",
)

# ---------------------------------------------------------------- 14 CTA
SPS = ["영어만 쓰는 교실", "유럽 부모들이 고르는 곳", "생활 수준이 높은 동네", "캐나다 공교육 + 비교과", "빠른 졸업", "현지 한국인 선생님의 관리"]
_sp = []
for i, t in enumerate(SPS):
    x = 120 + (i % 3) * 580
    y = 260 + (i // 3) * 240
    _sp.append(f'<div class="card spc" id="s14-p{i}" style="left:{x}px;top:{y}px"><div class="sticker" style="left:30px;top:30px;font-size:20px">추천 포인트 0{i + 1}</div><div class="hd" style="position:absolute;left:30px;top:100px;font-size:40px">{t}</div></div>')
_sp_html = "\n".join("          " + x for x in _sp)

S["14-cta"] = dict(
    bg="",
    css="""
R .bg{background:#16324F}
R .spc{width:540px;height:200px}
""",
    body=f"""
          <div class="abs" id="s14-paper" style="inset:0;background:#FAF6EF"></div>
          <div class="abs hd" id="s14-t" style="left:120px;top:92px;font-size:66px">정리하면</div>
{_sp_html}
          <div class="full" id="s14-photo"><img src="{P}01-hero-lake-jump.jpg" alt="" style="object-position:50% 25%" /></div>
          <div class="abs" id="s14-bar" style="left:0;top:680px;width:1920px;height:220px;background:rgba(22,50,79,.95)"></div>
          <div class="abs hd" id="s14-m1" style="left:120px;top:720px;font-size:52px;color:#FAF6EF">캐나다 아이처럼 자라는 것, 그리고 좋은 대학</div>
          <div class="abs b" id="s14-m1s" style="left:122px;top:800px;font-size:34px;color:#F3C969">두 마음을 버논에서 함께</div>
          <div class="abs hd" id="s14-m2" style="left:120px;top:720px;font-size:52px;color:#FAF6EF">학교별 한국 학생 자리는 한정되어 있습니다</div>
          <div class="abs b" data-layout-allow-overlap id="s14-m2s" style="left:122px;top:800px;font-size:34px;color:#F3C969">9월 학기 등록 핵심 시기 · 지금부터 3월까지</div>
          <div class="abs b" data-layout-allow-overlap id="s14-m3s" style="left:122px;top:800px;font-size:34px;color:#F3C969">학교별 잔여석 · 맞는 학교·관리 옵션 · 대학 로드맵</div>
          <div class="card" id="s14-aa" style="left:1360px;top:705px;width:440px;height:170px;padding:28px;background:#FAF6EF"><div class="h" style="font-size:56px">AA캐나다</div><div class="b" style="font-size:26px;color:#4A5F78;margin-top:6px">자세한 상담은 설명란 링크로</div></div>""",
    js="""
inn('#s14-t',R[0],{y:24});
const PT=[R[1],R[1]+1.6,R[1]+3.6,R[2],R[2]+1.8,R[2]+3.0];
for(let i=0;i<6;i++){tl.fromTo('#s14-p'+i,{opacity:0,x:500,rotation:8},{opacity:1,x:0,rotation:(i%2?1.5:-1.5),duration:0.75,ease:'power3.out'},PT[i]);}
tl.to(['#s14-p0','#s14-p1','#s14-p2','#s14-p3','#s14-p4','#s14-p5','#s14-t'],{opacity:0,scale:0.9,duration:0.5,ease:'power2.in'},R[3]-0.2);
tl.to('#s14-paper',{opacity:0,duration:0.6},R[3]+0.2);
tl.fromTo('#s14-photo',{clipPath:'circle(0% at 50% 50%)'},{clipPath:'circle(75% at 50% 50%)',duration:1.1,ease:'power3.inOut'},R[3]-0.1);
kb('#s14-photo img',R[3]-0.1,D-R[3],{s:1.0},{s:1.08});
tl.fromTo('#s14-bar',{yPercent:100,opacity:0},{yPercent:0,opacity:1,duration:0.7,ease:'power3.out'},R[3]+0.8);
inn('#s14-m1',R[3]+1.1,{y:16});inn('#s14-m1s',R[3]+2.6,{y:12});
outt(['#s14-m1','#s14-m1s'],R[4]-0.3);
inn('#s14-m2',R[4],{y:16});inn('#s14-m2s',R[4]+3.4,{y:12});
outt('#s14-m2s',R[5]-0.3);inn('#s14-m3s',R[5],{y:12});
inn('#s14-aa',R[6],{x:60,y:0,d:0.7});
""",
)
