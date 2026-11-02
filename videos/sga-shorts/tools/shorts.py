"""SGA shorts specs (plans/sga-shorts/SHORTS_BRIEF.md). 1080x1920, visuals in y 280-1340, captions 1380-1560.
rows = [(caption/display text, TTS text)] - TTS spells out acronyms/numbers. T('phrase') = when the display phrase is spoken.
@P/ = assets/photos/, @B/ = assets/brand/. Facts only from the brief."""

SHORTS = {}

CHECK = '<svg viewBox="0 0 60 60" style="width:{w}px;height:{w}px"><circle cx="30" cy="30" r="28" fill="#2ec27e"/><path class="ck" d="M16 31 L26 41 L45 20" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ENV = '<svg viewBox="0 0 80 56" style="width:96px;height:67px"><rect x="2" y="2" width="76" height="52" rx="8" fill="#f5efe3"/><path d="M4 6 L40 32 L76 6" fill="none" stroke="#14254a" stroke-width="5" stroke-linejoin="round"/></svg>'

# ------------------------------------------------------------------ 1. "6학점만 더 들으면 졸업?"
steps = ["ESL C", "ESL D", "ESL E", "ENG 3U", "ENG 4U"]
stairs = "".join(
    f'<div class="st{" g" if i == 4 else ""}" id="k1-st{i}" style="left:{95 + i * 178}px;top:{1180 - (110 + i * 70)}px;height:{110 + i * 70}px"><span>{n}</span></div>'
    for i, n in enumerate(steps))
g12 = "".join(f'<div class="g12" id="k1-g{i}" style="left:{95 + i * 178}px">12학년 과목</div>' for i in range(5))
SHORTS[1] = dict(
    slug="credits", title="6학점만 더 들으면 졸업?", hook=2.0,
    rows=[
        ("'몇 과목만 더 들으면 졸업'이라는 말, 유학생에게는 거의 맞지 않습니다.", "몇 과목만 더 들으면 졸업이라는 말, 유학생에게는 거의 맞지 않습니다."),
        ("대학은 12학년 과목 점수로 지원하는데, 유학생은 영어 시험 결과에 따라 ESL부터 한 단계씩 올라가야 하거든요.",
         "대학은 십이 학년 과목 점수로 지원하는데, 유학생은 영어 시험 결과에 따라 이에스엘부터 한 단계씩 올라가야 하거든요."),
        ("영어만 보통 다섯 과목, 여기에 12학년 과목을 더하면 최소 10학점 안팎이 현실적인 숫자입니다.",
         "영어만 보통 다섯 과목, 여기에 십이 학년 과목을 더하면 최소 십 학점 안팎이 현실적인 숫자입니다."),
        ("우리 아이 학점은 성적표로 계산해 드립니다.", "우리 아이 학점은 성적표로 계산해 드립니다."),
        ("카카오톡 canlog.", "카카오톡 캔로그."),
    ],
    keys=["거의 맞지 않습니다", "ESL", "최소 10학점", "canlog"],
    photos=["campus-04"],
    css="""
R .full img{filter:saturate(.45)}
R #k1-six{left:0;right:0;top:560px;text-align:center;font-size:300px}
R #k1-x{left:300px;top:470px;width:480px;height:480px}
R .st{position:absolute;width:170px;border-radius:16px 16px 0 0;background:#f5efe3;color:#14254a;display:flex;justify-content:center;padding-top:16px}
R .st span{font-weight:900;font-size:34px;white-space:nowrap}
R .st.g{background:#e8b931}
R .g12{position:absolute;top:1262px;width:170px;height:84px;border-radius:14px;background:#14254a;border:3px solid #e8b931;color:#f5efe3;font-weight:800;font-size:24px;line-height:1.2;display:flex;align-items:center;justify-content:center;text-align:center}
R #k1-tot{left:110px;top:370px;width:860px;height:320px;display:flex;flex-direction:column;align-items:center;justify-content:center}
R #k1-doc{left:290px;top:640px;width:500px;height:420px;padding:44px 40px}
R #k1-doc .ln{height:18px;border-radius:9px;background:rgba(20,37,74,.18);margin-top:24px}
""",
    bg="""        <div class="full" id="k1-ph"><img src="@P/campus-04.jpg" alt="" /></div>
        <div class="dim" style="opacity:.74"></div>""",
    body=f"""
          <div class="abs b" id="k1-q" style="left:0;right:0;top:450px;text-align:center;font-size:44px;color:rgba(255,255,255,.85)">"몇 과목만 더 들으면 졸업"</div>
          <div class="abs h" id="k1-six">6학점?</div>
          <svg class="abs" id="k1-x" viewBox="0 0 300 300"><circle cx="150" cy="150" r="130" fill="none" stroke="#c8102e" stroke-width="18"/><path d="M85 85 L215 215 M215 85 L85 215" stroke="#c8102e" stroke-width="26" stroke-linecap="round"/></svg>
          <div class="chip cream" id="k1-c" style="left:170px;top:290px;font-size:34px">대학 지원 = 12학년 과목 점수</div>
          <div class="abs" id="k1-stairs" style="inset:0">{stairs}
            <div class="abs hd gold" id="k1-need" style="left:760px;top:745px;width:300px;font-size:30px;white-space:nowrap">대학 지원 필수</div>
            <div class="abs hd" id="k1-eng" style="left:95px;top:1188px;width:890px;text-align:center;font-size:36px;border-top:5px solid #e8b931;padding-top:10px">영어만 보통 5과목</div></div>
          {g12}
          <div class="card" id="k1-tot"><div class="num" style="font-size:140px;color:#14254a">최소 <span id="k1-n">10</span>학점~</div><div class="hd red" style="font-size:40px;margin-top:6px">현실적인 숫자</div><div class="b" id="k1-note" style="font-size:26px;margin-top:10px;color:#4a5878">영어 배치고사 결과와 이전 성적에 따라 달라집니다</div></div>
          <div class="card" id="k1-doc"><div class="t" style="font-size:52px">성적표</div><div class="ln" style="width:90%"></div><div class="ln" style="width:70%"></div><div class="ln" style="width:85%"></div><div class="ln" style="width:60%"></div>
            <div class="pill" style="left:40px;top:300px;font-size:36px">→ 필요 학점 계산</div></div>""",
    js="""
kb('#k1-ph img',0,D,{s:1.0},{s:1.10});
tl.fromTo('#k1-six',{scale:1.7},{scale:1,duration:0.4,ease:'power4.in'},0);shake(0.4);
inn('#k1-q',0.3,{y:16});
stamp('#k1-x',1.0,-12);
outt(['#k1-q','#k1-six','#k1-x'],T('대학은 12학년')-0.3,{s:0.8});
pop('#k1-c',T('대학은 12학년'));
const ST=['#k1-st0','#k1-st1','#k1-st2','#k1-st3','#k1-st4'].map(s=>q(s));
grow(ST,T('ESL부터')-0.2,0.5,'50% 100%','y');tl.fromTo(ST,{opacity:0},{opacity:1,duration:0.25,stagger:0.18},T('ESL부터')-0.2);
inn('#k1-need',T('한 단계씩'),{y:10});
inn('#k1-eng',T('영어만 보통'),{y:12});
pop(['#k1-g0','#k1-g1','#k1-g2','#k1-g3','#k1-g4'],T('12학년 과목을 더하면'),0.1);
outt('#k1-c',T('최소 10학점')-0.3);
slam('#k1-tot',T('최소 10학점'));odo('#k1-n',T('최소 10학점'),0.9);
inn('#k1-note',T('현실적인'),{y:6});
tl.to(['#k1-stairs','#k1-tot','#k1-g0','#k1-g1','#k1-g2','#k1-g3','#k1-g4'].map(s=>q(s)),{opacity:0,duration:0.5},T('우리 아이 학점은')-0.2);
flip('#k1-doc',T('우리 아이 학점은'));
""",
    sfx=[("impact", "0.4"), ("stamp", "1.3"), ("pop", "T('대학은 12학년')"), ("pop", "T('12학년 과목을 더하면')"), ("impact", "T('최소 10학점')+0.42")],
    thumb=dict(photo="campus-04", lines=[("6학점이면", "#fff"), ("졸업?", "#ff3b4f")], pill="유학생 현실 학점 계산", stamp=True),
    upload=dict(
        title="6학점만 더 들으면 졸업? 유학생 현실 학점 계산 | 토론토 사립고 SGA",
        first="캐나다 조기유학 토론토 사립고, 졸업까지 실제로 몇 학점이 필요한지 정리했습니다.",
        body="대학은 12학년 과목 점수로 지원합니다. 유학생은 영어 시험 결과에 따라 ESL부터 단계별로 올라가야 해서, 영어만 보통 다섯 과목, 12학년 과목을 더하면 최소 10학점 안팎이 현실적인 숫자입니다. 관리형 사립고 SGA(St. George Academy)와 함께 학생별 학점 계획을 무료로 계산해 드립니다.",
        note="※ 필요 학점은 영어 배치고사 결과, 전공, 이전 성적에 따라 달라집니다. 자료: 2026 SGA 공식 브로셔, AA Canada-SGA 미팅(2026년 3월).",
        tags="#캐나다조기유학 #토론토조기유학 #토론토사립고 #관리형조기유학 #OSSD #ESL #캐나다고등학교 #AACanada #shorts"),
)

# ------------------------------------------------------------------ 2. "성적표가 2주마다 옵니다"
pos5 = [(330, "2주"), (480, "2주"), (630, "중간"), (780, "2주"), (960, "기말")]
d1 = "".join(f'<div class="dt" id="k2-d{i}" style="left:{x}px;top:{880 - 20}px"></div><div class="dl" id="k2-e{i}" style="left:{x - 60}px;top:{910}px">{n}</div>' for i, (x, n) in enumerate([(630, "중간"), (960, "기말")]))
d2 = "".join(f'<div class="dt g" id="k2-f{i}" style="left:{x}px;top:{1100 - 20}px"></div><div class="dl" id="k2-h{i}" style="left:{x - 60}px;top:{1130}px">{n}</div>' for i, (x, n) in enumerate(pos5))
rows2 = [("영어 (ESL D)", "82", "양호", "제출", "적극"), ("수학 11", "88", "양호", "1건 지연", "보통")]
th2 = "".join(f'<div class="th c{i}">{h}</div>' for i, h in enumerate(["과목", "점수", "출석", "과제", "태도"]))
tr2 = "".join("".join(f'<div class="td c{i}" style="top:{220 + r * 74}px">{v}</div>' for i, v in enumerate(row)) for r, row in enumerate(rows2))
vals = [84, 82, 79, 76, 79, 83, 86, 88]
gx = lambda k: 60 + k * 116
gy = lambda v: 330 - (v - 70) * 15
p1 = " ".join(f"{'M' if k == 0 else 'L'}{gx(k)} {gy(v)}" for k, v in enumerate(vals[:4]))
p2 = " ".join(f"{'M' if k == 0 else 'L'}{gx(k + 3)} {gy(v)}" for k, v in enumerate(vals[3:]))
gd = "".join(f'<circle id="k2-p{k}" cx="{gx(k)}" cy="{gy(v)}" r="13" fill="{"#c8102e" if v < 80 else ("#2ec27e" if k > 3 else "#f5efe3")}"/>' for k, v in enumerate(vals))
SHORTS[2] = dict(
    slug="biweekly", title="성적표가 2주마다 옵니다", hook=1.8,
    rows=[
        ("보통 학교 성적표는 한 학기에 두 번, 중간과 기말입니다.", "보통 학교 성적표는 한 학기에 두 번, 중간과 기말입니다."),
        ("SGA는 2주마다 나옵니다.", "에스지에이는 이 주마다 나옵니다."),
        ("한 학기에 다섯 번이에요.", "한 학기에 다섯 번이에요."),
        ("점수뿐 아니라 출석, 과제, 수업 태도까지 선생님 코멘트로 적혀 부모님 이메일로 바로 갑니다.",
         "점수뿐 아니라 출석, 과제, 수업 태도까지 선생님 코멘트로 적혀 부모님 이메일로 바로 갑니다."),
        ("대학 원서에는 11학년과 12학년 중간 성적이 중요하니까, 점수가 모자라면 미리 조정할 수 있어요.",
         "대학 원서에는 십일 학년과 십이 학년 중간 성적이 중요하니까, 점수가 모자라면 미리 조정할 수 있어요."),
        ("카카오톡 canlog로 상담해 보세요.", "카카오톡 캔로그로 상담해 보세요."),
    ],
    keys=["2주마다", "다섯 번", "선생님 코멘트", "미리 조정", "canlog"],
    photos=["campus-03", "campus-02"],
    css="""
R .full img{filter:saturate(.5)}
R #k2-big{left:0;right:0;top:420px;text-align:center;font-size:170px;color:#e8b931;perspective:900px}
R .ln{position:absolute;left:300px;width:700px;height:6px;border-radius:3px;background:rgba(245,239,227,.45)}
R .dt{position:absolute;width:40px;height:40px;margin-left:-20px;border-radius:50%;background:#f5efe3}
R .dt.g{background:#e8b931}
R .dl{position:absolute;width:120px;text-align:center;font-weight:800;font-size:28px;margin-left:-20px}
R .rl{position:absolute;left:70px;width:220px;font-weight:900;font-size:40px}
R .cnt{position:absolute;top:1180px;width:420px;text-align:center}
R #k2-rc{left:60px;top:440px;width:960px;height:560px}
R .th,.td{position:absolute;font-weight:800;font-size:30px;color:#14254a;white-space:nowrap}
R .th{top:150px;color:#c8102e;font-size:26px}
R #k2-rc .c0{left:40px} R #k2-rc .c1{left:330px} R #k2-rc .c2{left:460px} R #k2-rc .c3{left:600px} R #k2-rc .c4{left:800px}
R .cm{position:absolute;left:40px;top:390px;width:880px;padding:20px 24px;border-radius:16px;background:#fff;border:3px solid rgba(20,37,74,.15);font-weight:700;font-size:28px;color:#14254a}
R #k2-g{left:80px;top:480px;width:920px;height:520px}
""",
    bg="""        <div class="full" id="k2-ph"><img src="@P/campus-03.jpg" alt="" /></div>
        <div class="full" id="k2-ph2" style="opacity:0"><img src="@P/campus-02.jpg" alt="" /></div>
        <div class="dim" style="opacity:.76"></div>""",
    body=f"""
          <div class="abs h" id="k2-big">2주마다</div>
          <div class="abs" id="k2-cmp" style="inset:0">
            <div class="rl" id="k2-r1" style="top:855px">일반 학교</div><div class="ln" id="k2-l1" style="top:877px"></div>{d1}
            <div class="rl gold" id="k2-r2" style="top:1075px">SGA</div><div class="ln" id="k2-l2" style="top:1097px;background:#e8b931"></div>{d2}
            <div class="cnt" id="k2-c1" style="left:90px"><div class="num" style="font-size:110px;color:rgba(245,239,227,.7)">2</div><div class="hd" style="font-size:34px">번 / 한 학기</div></div>
            <div class="cnt" id="k2-c2" style="left:570px"><div class="num gold" style="font-size:110px" id="k2-n">5</div><div class="hd" style="font-size:34px">번 / 한 학기</div></div></div>
          <div class="card" id="k2-rc"><div class="t" style="position:absolute;left:40px;top:44px;font-size:44px">2주 리포트</div><div class="tag" style="right:36px;top:48px">예시 화면</div>
            {th2}{tr2}<div class="cm" id="k2-cm"><span style="color:#c8102e">교사 코멘트 </span>수업 참여가 좋아졌어요. 과제 기한을 지켜 주세요.</div></div>
          <div class="abs" id="k2-env" style="left:200px;top:1080px">{ENV}</div>
          <div class="chip cream" id="k2-par" style="left:640px;top:1080px;font-size:36px">부모님 이메일</div>
          <div class="chip cream" id="k2-key" style="left:100px;top:330px;font-size:32px">대학 원서 = 11학년 + 12학년 중간 성적</div>
          <svg class="abs" id="k2-g" viewBox="0 0 920 520">
            <path id="k2-tg" d="M30 {gy(80)} L900 {gy(80)}" stroke="#e8b931" stroke-width="4" stroke-dasharray="14 12" fill="none"/>
            <path id="k2-l1g" d="{p1}" stroke="#f5efe3" stroke-width="7" fill="none" stroke-linejoin="round"/>
            <path id="k2-l2g" d="{p2}" stroke="#2ec27e" stroke-width="7" fill="none" stroke-linejoin="round"/>{gd}</svg>
          <div class="abs hd gold" id="k2-tl" style="left:110px;top:{480 + gy(80) + 14}px;font-size:26px;white-space:nowrap">목표 학과 기준</div>
          <div class="pill" id="k2-ea" style="left:{80 + gx(3) - 70}px;top:{480 + gy(76) + 40}px;background:#c8102e;color:#fff;font-size:34px">미리 조정</div>""",
    js="""
kb('#k2-ph img',0,D,{s:1.0},{s:1.08});
tl.fromTo('#k2-big',{scale:1.5},{scale:1,duration:0.4,ease:'power4.in'},0);shake(0.4);
grow('#k2-l1',0.2,0.6);pop(['#k2-d0','#k2-d1'],0.6,0.15);
grow('#k2-l2',0.5,0.6);pop(['#k2-f0','#k2-f1','#k2-f2','#k2-f3','#k2-f4'],0.9,0.1);
inn(['#k2-r1','#k2-r2'],0.2,{x:-20,y:0,st:0.2});
inn(['#k2-e0','#k2-e1'],T('중간과 기말'),{y:10,st:0.2});inn('#k2-c1',T('한 학기에 두 번'),{s:0.6,y:0});
inn(['#k2-h0','#k2-h1','#k2-h2','#k2-h3','#k2-h4'],T('2주마다 나옵니다'),{y:10,st:0.12});
slam('#k2-c2',T('다섯 번'));odo('#k2-n',T('다섯 번'),0.7);
tl.to(['#k2-big','#k2-cmp'].map(s=>q(s)),{opacity:0,y:-40,duration:0.45,ease:'power2.in'},T('점수뿐')-0.4);
tl.to('#k2-ph2',{opacity:1,duration:0.8},T('점수뿐')-0.4);kb('#k2-ph2 img',T('점수뿐')-0.4,D,{s:1.0},{s:1.08});
flip('#k2-rc',T('점수뿐'));
inn(qa('#k2-rc .th'),T('점수뿐')+0.4,{y:10,st:0.06});
inn(qa('#k2-rc .td.c0'),T('점수뿐')+0.6,{y:10,st:0.1});inn(qa('#k2-rc .td.c1'),T('점수뿐')+0.8,{y:10,st:0.1});
inn(qa('#k2-rc .td.c2'),T('출석,'),{y:10,st:0.1});inn(qa('#k2-rc .td.c3'),T('과제,'),{y:10,st:0.1});inn(qa('#k2-rc .td.c4'),T('수업 태도'),{y:10,st:0.1});
inn('#k2-cm',T('선생님 코멘트'),{y:14});
tl.fromTo('#k2-env',{opacity:0,x:-120,y:40,scale:0.6},{opacity:1,x:280,y:0,scale:1,duration:0.8,ease:'power2.out'},T('부모님 이메일로'));pop('#k2-par',T('부모님 이메일로')+0.6);
tl.to(['#k2-rc','#k2-env','#k2-par'].map(s=>q(s)),{opacity:0,y:-40,duration:0.4,ease:'power2.in'},T('대학 원서에는')-0.35);
pop('#k2-key',T('대학 원서에는'));
draw('#k2-tg',T('11학년과'),0.7);inn('#k2-tl',T('11학년과')+0.3,{x:-10,y:0});
draw('#k2-l1g',T('중간 성적이'),1.4,'none');pop(['#k2-p0','#k2-p1','#k2-p2','#k2-p3'],T('중간 성적이'),0.4);
stamp('#k2-ea',T('미리 조정'),-6);
draw('#k2-l2g',T('미리 조정')+0.3,1.3,'none');pop(['#k2-p4','#k2-p5','#k2-p6','#k2-p7'],T('미리 조정')+0.4,0.3);
""",
    sfx=[("whoosh", "0.0"), ("pop", "0.9"), ("impact", "T('다섯 번')+0.42"), ("whoosh", "T('점수뿐')-0.4"), ("whoosh", "T('부모님 이메일로')"), ("stamp", "T('미리 조정')+0.3")],
    thumb=dict(photo="campus-03", lines=[("성적표가", "#fff"), ("2주마다", "#e8b931"), ("옵니다", "#fff")], pill="토론토 관리형 사립고 SGA"),
    upload=dict(
        title="성적표가 2주마다 옵니다 | 토론토 관리형 사립고 SGA",
        first="캐나다 조기유학 토론토 관리형 사립고 SGA는 성적표가 한 학기에 다섯 번, 2주마다 나옵니다.",
        body="점수뿐 아니라 출석, 과제, 수업 태도까지 선생님 코멘트로 적혀 부모님 이메일로 바로 갑니다. 대학 원서에는 11학년과 12학년 중간 성적이 중요해서, 점수가 모자라면 미리 조정할 수 있어요.",
        note="※ 영상 속 성적표는 예시 화면입니다. 자료: 2026 SGA 공식 브로셔, AA Canada-SGA 미팅(2026년 3월).",
        tags="#캐나다조기유학 #토론토조기유학 #토론토사립고 #관리형조기유학 #캐나다고등학교 #StGeorgeAcademy #AACanada #shorts"),
)

# ------------------------------------------------------------------ 3. "캐나다 학년은 한국보다 반 년 빠릅니다"
import math  # noqa: E402

mx3 = lambda k: 110 + k * 48  # 18 months from September
ticks3 = "".join(f'<div class="tk" style="left:{mx3(k) - 2}px"></div>' for k in range(19))
tlab3 = "".join(f'<div class="tl" style="left:{mx3(k) - 40}px">{n}</div>' for k, n in [(0, "9월"), (6, "3월"), (12, "9월"), (18, "3월")])


def _arc(cx, cy, r, a0, a1):
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    return f"M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}"


months3 = ["9월", "11월", "2월", "4월", "여름"]
ring3, lab3 = "", ""
for i, m in enumerate(months3):
    a0 = -90 + i * 72 + 4
    a1 = a0 + 64
    ring3 += f'<path class="seg0" d="{_arc(300, 300, 240, a0, a1)}"/><path class="seg" id="k3-g{i}" d="{_arc(300, 300, 240, a0, a1)}"/>'
    am = math.radians((a0 + a1) / 2)
    lab3 += f'<div class="ml" id="k3-l{i}" style="left:{240 + 300 + 335 * math.cos(am) - 80:.0f}px;top:{460 + 300 + 335 * math.sin(am) - 32:.0f}px">{m}</div>'
seasons3 = [("trip-autumn-03", 0), ("trip-autumn-01", 1), ("ev-christmas-01", 2), ("ev-easter-02", 3), ("trip-island-03", 4)]
bgs3 = "".join(f'        <div class="full sz" id="k3-b{i}" style="opacity:{1 if i == 0 else 0}"><img src="@P/{n}.jpg" alt="" /></div>\n' for n, i in seasons3)
nodes3 = [("12월", "한국 성적"), ("1월", "상담"), ("2월·4월", "바로 입학")]
nd3 = "".join(
    f'<div class="nd{" g" if i == 2 else ""}" id="k3-n{i}" style="top:{430 + i * 290}px"><div class="m">{a}</div><div class="s">{b}</div><div class="cw">{CHECK.format(w=70)}</div></div>'
    for i, (a, b) in enumerate(nodes3))
SHORTS[3] = dict(
    slug="intake", title="캐나다 학년은 한국보다 반 년 빠릅니다", hook=1.8,
    rows=[
        ("캐나다 학년은 한국보다 반 년 빠릅니다.", "캐나다 학년은 한국보다 반 년 빠릅니다."),
        ("9월에만 입학할 수 있으면 학년을 맞추느라 1년 가까이 손해 보는 경우가 많아요.", "구월에만 입학할 수 있으면 학년을 맞추느라 일 년 가까이 손해 보는 경우가 많아요."),
        ("그래서 입학 시기가 많다는 건 한국 학생에게 특히 중요합니다.", "그래서 입학 시기가 많다는 건 한국 학생에게 특히 중요합니다."),
        ("SGA는 9월, 11월, 2월, 4월, 여름 학기로 1년에 다섯 번 입학할 수 있습니다.", "에스지에이는 구월, 십일월, 이월, 사월, 여름 학기로 일 년에 다섯 번 입학할 수 있습니다."),
        ("12월에 한국 성적이 나오면 1월에 상담하고, 2월이나 4월에 바로 시작하는 방법이 있어요.", "십이월에 한국 성적이 나오면 일월에 상담하고, 이월이나 사월에 바로 시작하는 방법이 있어요."),
        ("카카오톡 canlog로 상담해 보세요.", "카카오톡 캔로그로 상담해 보세요."),
    ],
    keys=["반 년 빠릅니다", "1년 가까이 손해", "특히 중요", "다섯 번", "2월이나 4월", "canlog"],
    photos=[n for n, _ in seasons3],
    css="""
R .full img{filter:saturate(.6)}
R .tk{position:absolute;top:840px;width:4px;height:20px;background:rgba(245,239,227,.5)}
R .tl{position:absolute;top:874px;width:80px;text-align:center;font-weight:700;font-size:30px;color:rgba(245,239,227,.85)}
R .bar{position:absolute;height:96px;border-radius:16px;display:flex;align-items:center;padding-left:24px;font-weight:900;font-size:38px;white-space:nowrap}
R .rowl{position:absolute;left:110px;font-weight:900;font-size:40px}
R .seg0{fill:none;stroke:rgba(245,239,227,.18);stroke-width:70}
R .seg{fill:none;stroke:#e8b931;stroke-width:70}
R .ml{position:absolute;width:160px;text-align:center;font-weight:900;font-size:46px}
R .nd{position:absolute;left:190px;width:700px;height:220px;border-radius:28px;background:#f5efe3;color:#14254a;display:flex;flex-direction:column;align-items:center;justify-content:center}
R .nd.g{background:#e8b931}
R .nd .m{font-weight:900;font-size:96px;letter-spacing:-.03em;line-height:1}
R .nd .s{font-weight:800;font-size:42px;margin-top:8px}
R .cw{position:absolute;right:-24px;top:-24px}
R .dn{position:absolute;left:520px;width:40px;height:60px}
""",
    bg=bgs3 + '        <div class="dim" style="opacity:.78"></div>',
    body=f"""
          <div class="abs" id="k3-tlg" style="inset:0">
            <div class="abs h" id="k3-hd" style="left:0;right:0;top:320px;text-align:center;font-size:96px">반 년 차이</div>
            <div class="rowl" id="k3-ck" style="top:500px">캐나다</div>
            <div class="bar" id="k3-cb" style="left:{mx3(0)}px;top:560px;width:{mx3(10) - mx3(0)}px;background:#e8b931;color:#14254a">9월 시작</div>
            <div class="rowl" id="k3-kk" style="top:680px">한국</div>
            <div class="bar" id="k3-kb" style="left:{mx3(6)}px;top:740px;width:{mx3(18) - mx3(6)}px;background:#f5efe3;color:#14254a">3월 시작</div>
            <div class="abs" id="k3-ax" style="left:110px;top:846px;width:{mx3(18) - mx3(0)}px;height:6px;background:rgba(245,239,227,.5)"></div>{ticks3}{tlab3}
            <svg class="abs" style="left:{mx3(0)}px;top:470px;width:{mx3(6) - mx3(0)}px;height:50px" viewBox="0 0 288 50"><path id="k3-ar" d="M6 25 L282 25 M28 6 L6 25 L28 44 M260 6 L282 25 L260 44" fill="none" stroke="#e8b931" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <div class="card" id="k3-red" style="left:90px;top:1000px;width:900px;height:120px;background:#c8102e;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:50px">9월만 입학 = 1년 가까이 손해</div></div>
          <div class="card" id="k3-imp" style="left:110px;top:620px;width:860px;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center"><div class="hd" style="font-size:52px">입학 시기가 많다는 것</div><div class="h red" style="font-size:96px;margin-top:10px">특히 중요</div></div>
          <div class="abs" id="k3-rg" style="inset:0">
            <svg class="abs" id="k3-ring" style="left:240px;top:460px;width:600px;height:600px" viewBox="0 0 600 600">{ring3}</svg>{lab3}
            <div class="abs" id="k3-mid" style="left:240px;top:460px;width:600px;height:600px;display:flex;flex-direction:column;align-items:center;justify-content:center"><div class="num gold" style="font-size:170px" id="k3-n5">5</div><div class="hd" style="font-size:42px">번 입학 / 1년</div></div></div>
          {nd3}
          <svg class="abs dn" style="top:655px" viewBox="0 0 40 60"><path id="k3-a0" d="M20 4 L20 52 M6 38 L20 54 L34 38" fill="none" stroke="#e8b931" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <svg class="abs dn" style="top:945px" viewBox="0 0 40 60"><path id="k3-a1" d="M20 4 L20 52 M6 38 L20 54 L34 38" fill="none" stroke="#e8b931" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    js="""
kb('#k3-b0 img',0,D,{s:1.0},{s:1.1});
tl.fromTo('#k3-hd',{scale:1.6},{scale:1,duration:0.4,ease:'power4.in'},0);shake(0.4);
grow('#k3-cb',0.0,0.6);grow('#k3-kb',0.2,0.6);inn(['#k3-ck','#k3-kk'],0.0,{x:-20,y:0,st:0.15});
grow('#k3-ax',0.3,0.6);draw('#k3-ar',0.9,0.5);
stamp('#k3-red',T('9월에만'),-2);
tl.to('#k3-tlg',{opacity:0,y:-40,duration:0.4,ease:'power2.in'},T('그래서 입학 시기가')-0.4);
tl.fromTo('#k3-imp',{opacity:0,scale:1.5},{opacity:1,scale:1,duration:0.4,ease:'power4.in'},T('그래서 입학 시기가'));shake(T('그래서 입학 시기가')+0.4);
tl.to('#k3-imp',{opacity:0,y:-40,duration:0.4,ease:'power2.in'},T('SGA는 9월')-0.4);
tl.fromTo('#k3-rg',{opacity:0},{opacity:1,duration:0.3,immediateRender:true},T('SGA는 9월')-0.1);
const MT=[T('SGA는 9월'),T('11월,'),T('2월,'),T('4월,'),T('여름 학기')];
for(let i=0;i<5;i++){draw('#k3-g'+i,MT[i],0.4,'power2.out');pop('#k3-l'+i,MT[i]);
  if(i>0){tl.to('#k3-b'+i,{opacity:1,duration:0.5},MT[i]-0.1);kb('#k3-b'+i+' img',MT[i]-0.1,6,{s:1.0},{s:1.08});}}
inn('#k3-mid',T('다섯 번'),{s:0.7,y:0});odo('#k3-n5',T('다섯 번'),0.7);
tl.to('#k3-rg',{opacity:0,y:-40,duration:0.4,ease:'power2.in'},T('12월에')-0.4);
pop('#k3-n0',T('12월에'));draw('#k3-n0 .ck',T('12월에')+0.5,0.35);
draw('#k3-a0',T('1월에 상담'),0.35);pop('#k3-n1',T('1월에 상담')+0.15);draw('#k3-n1 .ck',T('1월에 상담')+0.6,0.35);
draw('#k3-a1',T('2월이나 4월'),0.35);pop('#k3-n2',T('2월이나 4월')+0.15);draw('#k3-n2 .ck',T('2월이나 4월')+0.6,0.35);
""",
    sfx=[("impact", "0.4"), ("stamp", "T('9월에만')+0.3"), ("pop", "T('SGA는 9월')"), ("pop", "T('2월,')"), ("pop", "T('여름 학기')"),
         ("pop", "T('12월에')"), ("pop", "T('1월에 상담')+0.15"), ("pop", "T('2월이나 4월')+0.15")],
    thumb=dict(photo="trip-autumn-03", lines=[("캐나다 학년은", "#fff"), ("반 년", "#e8b931"), ("빠릅니다", "#fff")], pill="1년에 5번 입학하는 토론토 사립고"),
    upload=dict(
        title="캐나다 학년은 한국보다 반 년 빠릅니다 | 토론토 사립고 입학 시기",
        first="캐나다 조기유학 토론토 관리형 사립고 SGA는 1년에 다섯 번 입학할 수 있습니다.",
        body="캐나다 학년은 한국보다 반 년 빠릅니다. 9월에만 입학할 수 있으면 학년을 맞추느라 1년 가까이 손해 보는 경우가 많아요. SGA는 9월, 11월, 2월, 4월, 여름 학기로 입학할 수 있어서, 12월에 한국 성적이 나오면 1월에 상담하고 2월이나 4월에 바로 시작할 수 있습니다.",
        note="※ 자료: 2026 SGA 공식 브로셔, AA Canada-SGA 미팅(2026년 3월). 입학 가능 학기와 학점 인정은 학생별 성적표 심사 후 확정됩니다.",
        tags="#캐나다조기유학 #토론토조기유학 #토론토사립고 #관리형조기유학 #캐나다입학시기 #StGeorgeAcademy #AACanada #shorts"),
)

# ------------------------------------------------------------------ 5. "토론토의 대치동, 노스욕"
MAP5 = """<svg class="abs" id="k5-map" style="left:40px;top:560px;width:1000px;height:640px" viewBox="0 0 1000 640">
  <path class="mp-lake" d="M-120 585 C 80 560, 230 640, 420 600 S 760 520, 1120 560" fill="none" stroke="#5f8fd6" stroke-width="6" stroke-linecap="round"/>
  <path class="mp-out" d="M120 120 L560 70 L900 96 L930 300 L960 420 L820 470 L660 520 L520 560 L360 570 L230 540 L140 470 L90 330 Z" fill="rgba(245,239,227,.06)" stroke="#f5efe3" stroke-width="5" stroke-linejoin="round"/>
</svg>"""
PIN5 = """<div class="abs" id="k5-pin" style="left:508px;top:560px;width:64px;height:84px"><div id="k5-pin-g" style="position:absolute;left:-28px;top:44px;width:120px;height:60px;border-radius:50%;background:radial-gradient(ellipse,rgba(232,185,49,.75) 0%,rgba(232,185,49,0) 70%)"></div><svg viewBox="0 0 64 84" style="position:absolute;inset:0;width:64px;height:84px"><path d="M32 82 C 32 82, 4 48, 4 30 A28 28 0 1 1 60 30 C 60 48, 32 82, 32 82 Z" fill="#e8b931"/><circle cx="32" cy="30" r="11" fill="#14254a"/></svg></div>"""
grid5 = [("town-14-library", "도서관"), ("town-03", "쇼핑몰"), ("town-05-foodcourt", "푸드코트"), ("town-20-artcentre", "아트센터")]
g5 = "".join(f'<div class="ph frame g" id="k5-g{i}" style="left:{70 + (i % 2) * 480}px;top:{420 + (i // 2) * 420}px"><img src="@P/{n}.jpg" alt="" /><div class="lab">{l}</div></div>' for i, (n, l) in enumerate(grid5))
SHORTS[5] = dict(
    slug="northyork", title="토론토의 대치동, 노스욕", hook=1.8,
    rows=[
        ("SGA는 토론토 북쪽 노스욕 중심가에 있습니다.", "에스지에이는 토론토 북쪽 노스욕 중심가에 있습니다."),
        ("지하철 노스욕 센터역이 가까워서 겨울 통학도 편해요.", "지하철 노스욕 센터역이 가까워서 겨울 통학도 편해요."),
        ("학교에서 5분에서 10분 거리에 토론토 공립교육청과 가톨릭교육청이 모두 있고,", "학교에서 오 분에서 십 분 거리에 토론토 공립교육청과 가톨릭교육청이 모두 있고,"),
        ("한국으로 치면 대치동 같은 학군 동네예요.", "한국으로 치면 대치동 같은 학군 동네예요."),
        ("옆에는 큰 도서관과 쇼핑몰, 푸드코트, 아트센터까지 걸어서 해결됩니다.", "옆에는 큰 도서관과 쇼핑몰, 푸드코트, 아트센터까지 걸어서 해결됩니다."),
        ("카카오톡 canlog로 상담해 보세요.", "카카오톡 캔로그로 상담해 보세요."),
    ],
    keys=["노스욕 센터역", "5분에서 10분", "대치동", "걸어서", "canlog"],
    photos=["town-04", "town-01", "town-12-nyc-station", "town-11-subway", "town-09-tdsb", "town-10-tcdsb-logo", "town-14-library", "town-03",
            "town-05-foodcourt", "town-20-artcentre"],
    css="""
R .full img{filter:saturate(.6)}
R #k5-big{left:0;right:0;top:330px;text-align:center;font-size:130px;color:#e8b931;perspective:900px}
R .st{position:absolute;left:90px;width:900px}
R .bc{position:absolute;left:130px;width:820px;height:330px;padding:24px;display:flex;align-items:center;gap:30px}
R .bc .im{width:260px;height:260px;border-radius:16px;overflow:hidden;background:#fff;display:flex;align-items:center;justify-content:center;flex:none}
R .bc .im img{max-width:100%;max-height:100%;object-fit:contain}
R .bc .t{font-size:44px;line-height:1.25;width:450px}
R .g{width:460px;height:380px}
""",
    bg="""        <div class="full" id="k5-b0"><img src="@P/town-04.jpg" alt="" /></div>
        <div class="full" id="k5-b1" style="opacity:0"><img src="@P/town-01.jpg" alt="" /></div>
        <div class="dim" style="opacity:.74"></div>""",
    body=f"""
          <div class="abs h" id="k5-big">토론토의 대치동</div>
          <div class="abs hd" id="k5-sub" style="left:0;right:0;top:490px;text-align:center;font-size:52px">노스욕 <span class="gold">North York</span></div>
          <div class="abs" id="k5-mapg" style="inset:0">{MAP5}
            <div class="abs l" id="k5-tor" style="left:330px;top:820px;font-size:44px;color:rgba(245,239,227,.6)">TORONTO</div>
            {PIN5}</div>
          <div class="ph frame st" id="k5-s1" style="top:420px;height:332px"><img src="@P/town-12-nyc-station.jpg" alt="" /></div>
          <div class="ph frame st" id="k5-s2" style="top:800px;height:440px;left:190px;width:700px"><img src="@P/town-11-subway.jpg" alt="" /></div>
          <div class="chip gold" id="k5-c1" style="left:290px;top:1270px;font-size:38px">North York Centre역</div>
          <div class="pill" id="k5-c2" style="left:300px;top:300px;font-size:42px">학교에서 5~10분</div>
          <div class="card bc" id="k5-e1" style="top:430px"><div class="im"><img src="@P/town-09-tdsb.jpg" alt="" /></div><div class="t">토론토 공립교육청</div></div>
          <div class="card bc" id="k5-e2" style="top:820px"><div class="im"><img src="@P/town-10-tcdsb-logo.jpg" alt="" /></div><div class="t">토론토 가톨릭교육청</div></div>
          <div class="card" id="k5-dc" style="left:110px;top:640px;width:860px;height:260px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#e8b931"><div class="h" style="font-size:120px;color:#14254a">대치동</div><div class="hd" style="font-size:40px;color:#14254a">같은 학군 동네</div></div>
          {g5}
          <div class="pill" id="k5-walk" style="left:330px;top:1270px;font-size:44px">걸어서 해결</div>""",
    js="""
kb('#k5-b0 img',0,D,{s:1.0,x:-1},{s:1.12,x:1});
tl.fromTo('#k5-big',{scale:1.25},{scale:1,duration:0.4,ease:'power4.in'},0);shake(0.4);
inn('#k5-sub',0.5,{y:16});
draw('#k5-map .mp-out',0.6,1.2);draw('#k5-map .mp-lake',0.9,1.0);inn('#k5-tor',1.2,{y:10});
tl.fromTo('#k5-pin',{y:-240,opacity:0},{y:0,opacity:1,duration:0.6,ease:'bounce.out'},T('노스욕 중심가'));
tl.fromTo('#k5-pin-g',{scale:0.5,opacity:0},{scale:1.4,opacity:1,duration:0.9,yoyo:true,repeat:3,ease:'sine.inOut'},T('노스욕 중심가')+0.5);
tl.to(['#k5-big','#k5-sub','#k5-mapg'].map(s=>q(s)),{opacity:0,y:-40,duration:0.4,ease:'power2.in'},T('지하철')-0.35);
tl.to('#k5-b1',{opacity:1,duration:0.6},T('지하철')-0.35);kb('#k5-b1 img',T('지하철')-0.35,D,{s:1.0},{s:1.1});
inn('#k5-s1',T('지하철'),{y:-60,r0:-5,r:-2});inn('#k5-s2',T('지하철')+0.5,{y:60,r0:5,r:2});pop('#k5-c1',T('노스욕 센터역'));
tl.to(['#k5-s1','#k5-s2','#k5-c1'].map(s=>q(s)),{opacity:0,y:-40,duration:0.4,ease:'power2.in'},T('학교에서 5분')-0.35);
pop('#k5-c2',T('학교에서 5분'));flip('#k5-e1',T('토론토 공립교육청'));flip('#k5-e2',T('가톨릭교육청'));
tl.to(['#k5-e1','#k5-e2'].map(s=>q(s)),{opacity:0.15,duration:0.4},T('한국으로 치면')-0.2);
tl.fromTo('#k5-dc',{opacity:0,scale:1.6},{opacity:1,scale:1,duration:0.4,ease:'power4.in'},T('대치동'));shake(T('대치동')+0.4);
tl.to(['#k5-c2','#k5-e1','#k5-e2','#k5-dc'].map(s=>q(s)),{opacity:0,y:-40,duration:0.4,ease:'power2.in'},T('옆에는')-0.35);
flip('#k5-g0',T('큰 도서관'));flip('#k5-g1',T('쇼핑몰'));flip('#k5-g2',T('푸드코트'));flip('#k5-g3',T('아트센터'));
['#k5-g0','#k5-g1','#k5-g2','#k5-g3'].forEach((s,i)=>kb(s+' img',T('큰 도서관'),D,{s:1.0},{s:1.08,x:(i%2?-1.5:1.5)}));
pop('#k5-walk',T('걸어서'));
""",
    sfx=[("impact", "0.4"), ("pop", "T('노스욕 중심가')+0.45"), ("whoosh", "T('지하철')"), ("pop", "T('학교에서 5분')"), ("impact", "T('대치동')+0.4"),
         ("pop", "T('큰 도서관')"), ("pop", "T('쇼핑몰')"), ("pop", "T('푸드코트')"), ("pop", "T('아트센터')")],
    thumb=dict(photo="town-04", lines=[("토론토의", "#fff"), ("대치동", "#e8b931"), ("노스욕", "#fff")], pill="지하철역 가까운 관리형 사립고 SGA"),
    upload=dict(
        title="토론토의 대치동, 노스욕 | 토론토 관리형 사립고 SGA 위치",
        first="캐나다 조기유학 토론토 관리형 사립고 SGA는 토론토 북쪽 노스욕 중심가에 있습니다.",
        body="지하철 노스욕 센터역이 가까워서 겨울 통학도 편하고, 학교에서 5분에서 10분 거리에 토론토 공립교육청과 가톨릭교육청이 모두 있습니다. 옆에는 큰 도서관과 쇼핑몰, 푸드코트, 아트센터까지 걸어서 해결돼요.",
        note="※ 자료: SGA 홈페이지(2026년 10월 확인), 2026 SGA 공식 브로셔.",
        tags="#캐나다조기유학 #토론토조기유학 #토론토사립고 #노스욕 #관리형조기유학 #StGeorgeAcademy #AACanada #shorts"),
)

# ------------------------------------------------------------------ 4. "영어가 부족해도 시작할 수 있는 이유"
bars4 = [("1교시", "9:30~12:00", "정규 수업", False), ("2교시", "12:40~3:10", "정규 수업", False), ("3교시", "3:15~4:45", "파운데이션", True)]
bh4 = "".join(f'<div class="tb{" g" if g else ""}" id="k4-b{i}" style="top:{430 + i * 130}px"><span class="p">{a}</span><span class="tm">{b}</span><span class="k">{c}</span></div>'
              for i, (a, b, c, g) in enumerate(bars4))
mini4 = "".join(f'<div class="ms" id="k4-m{i}" style="left:{150 + i * 230}px;top:{1300 - (i + 1) * 80}px;height:{(i + 1) * 80}px">{n}</div>' for i, n in enumerate(["ESL C", "ESL D", "ESL E"]))
SHORTS[4] = dict(
    slug="foundation", title="영어가 부족해도 시작할 수 있는 이유", hook=1.8,
    rows=[
        ("영어가 아직 부족하다면 어떻게 할까요?", "영어가 아직 부족하다면 어떻게 할까요?"),
        ("도착하자마자 영어로 수학, 과학 학점을 따라고 하면 버티기 어렵죠.", "도착하자마자 영어로 수학, 과학 학점을 따라고 하면 버티기 어렵죠."),
        ("그래서 SGA에는 파운데이션 프로그램이 있습니다.", "그래서 에스지에이에는 파운데이션 프로그램이 있습니다."),
        ("정규 수업 뒤 3교시에 아카데믹 라이팅과 파워 스피킹으로 쓰기와 말하기를 집중 훈련해요.",
         "정규 수업 뒤 삼 교시에 아카데믹 라이팅과 파워 스피킹으로 쓰기와 말하기를 집중 훈련해요."),
        ("학점 과목은 아니지만, 다음 영어 단계로 더 빨리 올라가는 데 도움이 됩니다.", "학점 과목은 아니지만, 다음 영어 단계로 더 빨리 올라가는 데 도움이 됩니다."),
        ("등록 조건에 따라 무료로 들을 수 있으니 상담 때 꼭 확인해 보세요.", "등록 조건에 따라 무료로 들을 수 있으니 상담 때 꼭 확인해 보세요."),
        ("카카오톡 canlog로 상담해 보세요.", "카카오톡 캔로그로 상담해 보세요."),
    ],
    keys=["파운데이션 프로그램", "3교시", "더 빨리", "무료", "canlog"],
    photos=["exchange-01"], brand=["Oly_5", "Oly_2"],
    css="""
R .full img{filter:saturate(.55)}
R #k4-q{left:0;right:0;top:300px;text-align:center;font-size:96px;color:#e8b931}
R #k4-oly{left:310px;top:500px;width:460px;height:576px}
R #k4-oly img,R #k4-oly2 img{width:100%;height:100%;object-fit:contain}
R #k4-oly2{left:700px;top:930px;width:330px;height:430px}
R #k4-t1{left:0;right:0;top:470px;text-align:center;font-size:120px;line-height:1.02}
R .tb{position:absolute;left:70px;width:940px;height:110px;border-radius:18px;background:#f5efe3;color:#14254a;display:flex;align-items:center;padding:0 30px;gap:26px;font-weight:900;font-size:38px}
R .tb.g{background:#e8b931}
R .tb .p{width:110px}
R .tb .tm{font-weight:700;font-size:34px;width:250px}
R .ms{position:absolute;width:210px;border-radius:14px 14px 0 0;background:#f5efe3;color:#14254a;font-weight:900;font-size:34px;display:flex;justify-content:center;padding-top:14px}
""",
    bg="""        <div class="full" id="k4-ph" style="opacity:0"><img src="@P/exchange-01.jpg" alt="" /></div>
        <div class="dim" style="opacity:.78"></div>""",
    body=f"""
          <div class="abs h" id="k4-q">영어가 부족하면?</div>
          <div class="abs" id="k4-oly"><img src="@B/Oly_5.png" alt="" /></div>
          <div class="chip" id="k4-c1" style="left:110px;top:1240px;font-size:34px">영어로 수학 학점</div>
          <div class="chip" id="k4-c2" style="left:560px;top:1240px;font-size:34px">영어로 과학 학점</div>
          <div class="chip red" id="k4-c3" style="left:330px;top:1100px;font-size:40px">버티기 어려움</div>
          <div class="abs l gold" id="k4-k" style="left:0;right:0;top:400px;text-align:center;font-size:36px">SGA</div>
          <div class="abs h" id="k4-t1">FOUNDATION PROGRAM</div>
          <div class="abs hd gold" id="k4-t2" style="left:0;right:0;top:760px;text-align:center;font-size:58px">파운데이션 프로그램</div>
          <div class="abs" id="k4-oly2"><img src="@B/Oly_2.png" alt="" /></div>
          <div class="abs hd" id="k4-h" style="left:70px;top:340px;font-size:42px">하루 시간표</div>{bh4}
          <div class="chip cream" id="k4-w" style="left:70px;top:830px;font-size:36px">아카데믹 라이팅</div>
          <div class="chip cream" id="k4-s" style="left:450px;top:830px;font-size:36px">파워 스피킹</div>
          <div class="chip" id="k4-nc" style="left:70px;top:940px;font-size:32px">학점 과목 아님</div>
          <div class="abs" id="k4-mini" style="inset:0">{mini4}
            <svg class="abs" style="left:250px;top:1000px;width:560px;height:220px" viewBox="0 0 560 220"><path id="k4-skip" d="M10 210 C 120 10, 420 -10, 540 140 M505 118 L542 144 L548 100" fill="none" stroke="#e8b931" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <div class="abs hd gold" id="k4-up" style="left:560px;top:1000px;font-size:36px;white-space:nowrap">더 빨리</div></div>
          <div class="pill" id="k4-free" style="left:300px;top:640px;font-size:56px;padding:20px 50px">조건에 따라 무료</div>
          <div class="abs b" id="k4-note" style="left:0;right:0;top:760px;text-align:center;font-size:30px;color:rgba(255,255,255,.8)">무료 여부는 등록 학점 등 조건에 따라 다릅니다</div>""",
    js="""
tl.fromTo('#k4-oly',{scale:1.15,rotation:-4},{scale:1,rotation:0,duration:0.5,ease:'back.out(1.6)'},0);
tl.fromTo('#k4-q',{scale:1.3},{scale:1,duration:0.4,ease:'power4.in'},0);shake(0.4);
tl.to('#k4-oly',{y:-120,scale:0.8,duration:0.6,ease:'power2.inOut'},T('도착하자마자'));
pop('#k4-c1',T('수학'));pop('#k4-c2',T('과학 학점'));stamp('#k4-c3',T('버티기 어렵죠'),-4);
tl.to(['#k4-q','#k4-oly','#k4-c1','#k4-c2','#k4-c3'].map(s=>q(s)),{opacity:0,y:-60,duration:0.4,ease:'power2.in'},T('그래서 SGA에는')-0.35);
inn('#k4-k',T('그래서 SGA에는'),{y:10});mask('#k4-t1',T('그래서 SGA에는')+0.2,0.8,'l');inn('#k4-t2',T('파운데이션 프로그램'),{y:14});
tl.fromTo('#k4-oly2',{opacity:0,y:80},{opacity:1,y:0,duration:0.6,ease:'back.out(1.8)'},T('파운데이션 프로그램')+0.3);
tl.to(['#k4-k','#k4-t1','#k4-t2'].map(s=>q(s)),{opacity:0,y:-40,duration:0.4,ease:'power2.in'},T('정규 수업 뒤')-0.35);
tl.to('#k4-oly2',{opacity:0,duration:0.3},T('정규 수업 뒤')-0.35);
tl.to('#k4-ph',{opacity:1,duration:0.8},T('정규 수업 뒤')-0.35);kb('#k4-ph img',T('정규 수업 뒤')-0.35,D,{s:1.0},{s:1.1});
inn('#k4-h',T('정규 수업 뒤'),{y:10});grow('#k4-b0',T('정규 수업 뒤'),0.5);grow('#k4-b1',T('정규 수업 뒤')+0.3,0.5);
grow('#k4-b2',T('3교시에'),0.6);tl.fromTo('#k4-b2',{scaleY:1},{scaleY:1.08,duration:0.3,yoyo:true,repeat:1,immediateRender:false},T('3교시에')+0.7);
pop('#k4-w',T('아카데믹 라이팅'));pop('#k4-s',T('파워 스피킹'));
pop('#k4-nc',T('학점 과목은'));
grow(['#k4-m0','#k4-m1','#k4-m2'].map(s=>q(s)),T('다음 영어 단계로'),0.5,'50% 100%','y');
draw('#k4-skip',T('더 빨리'),0.8);inn('#k4-up',T('더 빨리')+0.4,{y:10});
tl.to(['#k4-h','#k4-b0','#k4-b1','#k4-b2','#k4-w','#k4-s','#k4-nc','#k4-mini'].map(s=>q(s)),{opacity:0,y:-40,duration:0.4,ease:'power2.in'},T('등록 조건에')-0.35);
slam('#k4-free',T('무료로'));inn('#k4-note',T('상담 때'),{y:10});
tl.fromTo('#k4-oly2',{opacity:0,y:80},{opacity:1,y:0,duration:0.6,ease:'back.out(1.8)',immediateRender:false},T('상담 때'));
""",
    sfx=[("pop", "0.0"), ("impact", "0.4"), ("pop", "T('수학')"), ("stamp", "T('버티기 어렵죠')+0.3"), ("whoosh", "T('그래서 SGA에는')+0.2"),
         ("pop", "T('3교시에')"), ("pop", "T('아카데믹 라이팅')"), ("pop", "T('파워 스피킹')"), ("impact", "T('무료로')+0.42")],
    thumb=dict(photo="exchange-01", lines=[("영어가", "#fff"), ("부족해도", "#e8b931"), ("시작하는 법", "#fff")], pill="파운데이션 프로그램 · 토론토 SGA"),
    upload=dict(
        title="영어가 부족해도 시작할 수 있는 이유 | 토론토 사립고 SGA 파운데이션",
        first="캐나다 조기유학 토론토 관리형 사립고 SGA의 파운데이션 프로그램을 정리했습니다.",
        body="도착하자마자 영어로 수학, 과학 학점을 따기는 어렵습니다. SGA는 정규 수업 뒤 3교시에 아카데믹 라이팅과 파워 스피킹으로 쓰기와 말하기를 집중 훈련해요. 학점 과목은 아니지만 다음 영어 단계로 더 빨리 올라가는 데 도움이 되고, 등록 조건에 따라 무료로 들을 수 있습니다.",
        note="※ 무료 여부는 등록 학점 등 조건에 따라 다릅니다. 자료: 2026 SGA 공식 브로셔, AA Canada-SGA 미팅(2026년 3월).",
        tags="#캐나다조기유학 #토론토조기유학 #토론토사립고 #관리형조기유학 #ESL #StGeorgeAcademy #AACanada #shorts"),
)

# ------------------------------------------------------------------ 6. "공부만 하는 학교가 아닙니다, SGA 1년 행사"
# Only group / wide / back-view shots (face close-ups excluded until SGA confirms permissions).
ev6 = [("ev-halloween-03", "가을 · 할로윈", "가을엔 할로윈"), ("ev-christmas-01", "겨울 · 크리스마스", "겨울엔 크리스마스"), ("ev-valentine-01", "2월 · 발렌타인", "2월엔 발렌타인"),
       ("ev-easter-02", "봄 · 부활절", "봄엔 부활절"), ("ev-persian-01", "봄 · 페르시안 새해", "페르시안 새해"), ("ev-korean-01", "한국 축제", "한국 축제")]
trips6 = [("trip-island-03", "센터 아일랜드", "센터 아일랜드"), ("trip-niagara-02", "나이아가라", "나이아가라"), ("trip-rom-01", "로열 온타리오 박물관", "로열 온타리오")]
rot6 = [-4, 3, -3, 4, -2, 3, -3, 4, -2]
cards6 = "".join(f'<div class="ph frame ev" id="k6-e{i}" style="left:{120 + (i % 2) * 30}px;top:{400 + (i % 3) * 20}px"><img src="@P/{n}.jpg" alt="" style="object-position:50% {"0" if "valentine" in n else "50"}%" /></div>'
                 f'<div class="chip gold evl" id="k6-l{i}">{lab}</div>' for i, (n, lab, _) in enumerate(ev6 + trips6))
SHORTS[6] = dict(
    slug="events", title="공부만 하는 학교가 아닙니다, SGA 1년 행사", hook=2.4,
    rows=[
        ("공부만 하는 학교가 아닙니다.", "공부만 하는 학교가 아닙니다."),
        ("가을엔 할로윈, 겨울엔 크리스마스, 2월엔 발렌타인, 봄엔 부활절과 페르시안 새해, 여름 전에는 한국 축제까지.",
         "가을엔 할로윈, 겨울엔 크리스마스, 이월엔 발렌타인, 봄엔 부활절과 페르시안 새해, 여름 전에는 한국 축제까지."),
        ("센터 아일랜드와 나이아가라, 로열 온타리오 박물관 현장학습도 있어요.", "센터 아일랜드와 나이아가라, 로열 온타리오 박물관 현장학습도 있어요."),
        ("로보틱스와 과학 동아리도 있고, 노스욕에서 가장 큰 YMCA와 제휴돼 있어서 수영장과 체육관을 1년 내내 쓸 수 있어요.",
         "로보틱스와 과학 동아리도 있고, 노스욕에서 가장 큰 와이엠씨에이와 제휴돼 있어서 수영장과 체육관을 일 년 내내 쓸 수 있어요."),
        ("이런 활동 기록은 나중에 대학 에세이의 재료가 됩니다.", "이런 활동 기록은 나중에 대학 에세이의 재료가 됩니다."),
        ("카카오톡 canlog로 상담해 보세요.", "카카오톡 캔로그로 상담해 보세요."),
    ],
    keys=["공부만 하는 학교", "현장학습", "YMCA", "대학 에세이", "canlog"],
    photos=[n for n, _, _ in ev6 + trips6] + ["robotic-02", "ymca-01"], clips=["christmas-hall", "centre-island"],
    vars={"__V1__": "T('겨울엔 크리스마스')+0.5", "__V2__": "T('센터 아일랜드')"},
    css="""
R .full img{filter:saturate(.6)}
R .ev{width:840px;height:620px}
R .evl{left:120px;top:1110px;font-size:40px}
R #k6-h1{left:0;right:0;top:300px;text-align:center;font-size:84px}
R .vid{position:absolute;left:60px;top:420px;width:960px;height:540px;border-radius:24px;overflow:hidden;box-shadow:0 24px 50px rgba(0,0,0,.4);border:6px solid #f5efe3;background:#0b1630}
R .vid video{width:100%;height:100%;object-fit:cover;display:block}
R .sq{width:480px;height:480px}
""",
    bg="""        <div class="full" id="k6-bg"><img src="@P/trip-island-03.jpg" alt="" /></div>
        <div class="dim" style="opacity:.8"></div>""",
    body=f"""
          <div class="abs h" id="k6-h1">SGA의 <span class="gold">1년</span></div>
          <div class="abs hd" id="k6-h2" style="left:0;right:0;top:310px;text-align:center;font-size:64px">현장학습</div>
          <div class="vid" id="k6-v1"><video id="k6-cv1" src="assets/clips/christmas-hall.mp4" data-start="__V1__" data-duration="4.0" data-track-index="32" muted playsinline data-hf-media-start-basis="local"></video></div>
          <div class="vid" id="k6-v2"><video id="k6-cv2" src="assets/clips/centre-island.mp4" data-start="__V2__" data-duration="4.0" data-track-index="33" muted playsinline data-hf-media-start-basis="local"></video></div>
          {cards6}
          <div class="ph frame sq" id="k6-r" style="left:60px;top:430px"><img src="@P/robotic-02.jpg" alt="" /><div class="lab">로보틱스 동아리</div></div>
          <div class="ph frame sq" id="k6-y" style="left:540px;top:760px"><img src="@P/ymca-01.jpg" alt="" /><div class="lab">YMCA</div></div>
          <div class="chip gold" id="k6-yc" style="left:60px;top:1290px;font-size:40px">수영장 · 체육관 1년 내내</div>
          <div class="card" id="k6-es" style="left:110px;top:560px;width:860px;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center"><div class="hd" style="font-size:50px">활동 기록 =</div><div class="h red" style="font-size:96px;margin-top:8px;display:block">대학 에세이</div></div>""",
    js="""
kb('#k6-bg img',0,D,{s:1.0},{s:1.1});
// hook: fast stack of the year
const EV=qa('.ev'), EL=qa('.evl'), R6=[-4,3,-3,4,-2,3,-3,4,-2];
tl.fromTo('#k6-h1',{scale:1.4},{scale:1,duration:0.4,ease:'power4.in'},0);shake(0.4);
for(let i=0;i<6;i++){tl.fromTo(EV[i],{opacity:0},{opacity:1,duration:0.01},0.2+i*0.36);tl.fromTo(EV[i],{y:-260,rotation:R6[i]*2.5},{y:0,rotation:R6[i],duration:0.3,ease:'power3.out'},0.2+i*0.36);}
tl.to(EV.slice(0,6),{opacity:0,duration:0.2},T('가을엔 할로윈')-0.25);
// seasons in step with the narration
const ET=[T('가을엔 할로윈'),T('겨울엔 크리스마스'),T('2월엔 발렌타인'),T('봄엔 부활절'),T('페르시안 새해'),T('한국 축제')];
for(let i=0;i<6;i++){tl.to(EV[i],{opacity:1,duration:0.01},ET[i]);tl.fromTo(EV[i],{y:-300,rotation:R6[i]*2.4},{y:0,rotation:R6[i],duration:0.45,ease:'power3.out',immediateRender:false},ET[i]);
  pop(EL[i],ET[i]+0.15);if(i<5){tl.to(EL[i],{opacity:0,duration:0.2},ET[i+1]);}}
tl.to(['#k6-h1'].map(s=>q(s)),{opacity:0,duration:0.3},T('가을엔 할로윈')-0.3);
// christmas clip between winter and february
tl.fromTo('#k6-v1',{opacity:0,scale:0.9},{opacity:1,scale:1,duration:0.3},T('겨울엔 크리스마스')+0.5);tl.to('#k6-v1',{opacity:0,duration:0.15},T('2월엔 발렌타인')-0.15);
tl.to(EV.slice(0,6).concat([EL[5]]),{opacity:0,y:-40,duration:0.35,ease:'power2.in'},T('센터 아일랜드')-0.35);
inn('#k6-h2',T('센터 아일랜드'),{y:14});
tl.fromTo('#k6-v2',{opacity:0,scale:0.9},{opacity:1,scale:1,duration:0.35},T('센터 아일랜드'));tl.to('#k6-v2',{opacity:0,duration:0.3},T('나이아가라')-0.2);
const TT=[T('센터 아일랜드')+0.05,T('나이아가라'),T('로열 온타리오')];
for(let i=6;i<9;i++){tl.fromTo(EV[i],{opacity:0},{opacity:1,duration:0.01},TT[i-6]);tl.fromTo(EV[i],{y:-300,rotation:R6[i]*2.4},{y:0,rotation:R6[i],duration:0.45,ease:'power3.out'},TT[i-6]);pop(EL[i],TT[i-6]+0.15);if(i<8)tl.to(EL[i],{opacity:0,duration:0.2},TT[i-5]);}
tl.to(EV.slice(6).concat(EL.slice(6),[q('#k6-h2')]),{opacity:0,y:-40,duration:0.35,ease:'power2.in'},T('로보틱스')-0.35);
flip('#k6-r',T('로보틱스'));flip('#k6-y',T('YMCA'));pop('#k6-yc',T('1년 내내'));
tl.to(['#k6-r','#k6-y','#k6-yc'].map(s=>q(s)),{opacity:0,y:-40,duration:0.35,ease:'power2.in'},T('이런 활동')-0.35);
inn('#k6-es',T('이런 활동'),{y:30,s:0.92});tl.fromTo('#k6-es .h',{opacity:0,scale:1.6},{opacity:1,scale:1,duration:0.42,ease:'power4.in'},T('대학 에세이'));shake(T('대학 에세이')+0.42);
""",
    sfx=[("impact", "0.4"), ("pop", "T('가을엔 할로윈')"), ("pop", "T('겨울엔 크리스마스')"), ("pop", "T('2월엔 발렌타인')"), ("pop", "T('봄엔 부활절')"),
         ("pop", "T('페르시안 새해')"), ("pop", "T('한국 축제')"), ("whoosh", "T('센터 아일랜드')"), ("pop", "T('로보틱스')"), ("impact", "T('대학 에세이')+0.42")],
    thumb=dict(photo="trip-island-03", lines=[("공부만", "#fff"), ("하는 학교가", "#fff"), ("아닙니다", "#e8b931")], pill="토론토 사립고 SGA의 1년 행사"),
    upload=dict(
        title="공부만 하는 학교가 아닙니다 | 토론토 사립고 SGA 1년 행사",
        first="캐나다 토론토 사립고 SGA의 1년 학교 행사를 사진으로 정리했습니다.",
        body="가을 할로윈, 겨울 크리스마스, 2월 발렌타인, 봄 부활절과 페르시안 새해, 한국 축제까지. 센터 아일랜드, 나이아가라, 로열 온타리오 박물관 현장학습과 로보틱스·과학 동아리, YMCA 제휴 수영장·체육관도 있습니다. 이런 활동 기록은 대학 에세이의 재료가 됩니다. 캐나다 조기유학, 토론토 관리형 사립고를 찾고 계신다면 참고해 보세요.",
        note="※ 사진·영상: SGA 제공(2026년 10월). 행사와 현장학습은 해마다 달라질 수 있습니다.",
        tags="#캐나다조기유학 #토론토조기유학 #토론토사립고 #캐나다고등학교 #학교행사 #StGeorgeAcademy #AACanada #shorts"),
)

# ------------------------------------------------------------------ 7. "레지던스 5곳, 어디에 살까"
houses7 = "".join(f'<div class="ph frame hs" id="k7-h{i}" style="left:{70 + (i % 3) * 320}px;top:{430 + (i // 3) * 450}px"><img src="@B/res-h{i + 1}.jpg" alt="" /></div>' for i in range(5))
rooms7 = [("res104-01", "외관"), ("res248-02", "식사 공간"), ("res248-01", "방"), ("res248-03", "주방"), ("res123-01", "거실")]
SHORTS[7] = dict(
    slug="residence", title="레지던스 5곳, 어디에 살까", hook=2.0,
    rows=[
        ("아이가 지낼 레지던스, 어떤 곳일까요?", "아이가 지낼 레지던스, 어떤 곳일까요?"),
        ("SGA 레지던스는 학교에서 걸어서 다닐 수 있는 거리에 다섯 곳이 있고, 여학생 전용 하우스도 있습니다.",
         "에스지에이 레지던스는 학교에서 걸어서 다닐 수 있는 거리에 다섯 곳이 있고, 여학생 전용 하우스도 있습니다."),
        ("모든 레지던스에 사감 선생님이 상주하며 24시간 생활을 관리해요.", "모든 레지던스에 사감 선생님이 상주하며 이십사 시간 생활을 관리해요."),
        ("식사는 하루 세 끼, 한식 메뉴도 자주 나오고 알레르기가 있으면 따로 챙겨 줍니다.", "식사는 하루 세 끼, 한식 메뉴도 자주 나오고 알레르기가 있으면 따로 챙겨 줍니다."),
        ("방 타입은 신청 순서와 잔여 상황에 따라 배정됩니다.", "방 타입은 신청 순서와 잔여 상황에 따라 배정됩니다."),
        ("카카오톡 canlog로 상담해 보세요.", "카카오톡 캔로그로 상담해 보세요."),
    ],
    keys=["다섯 곳", "여학생 전용", "24시간", "하루 세 끼", "canlog"],
    photos=[n for n, _ in rooms7], brochure=["res-h1", "res-h2", "res-h3", "res-h4", "res-h5", "meals-grid"],
    css="""
R .full img{filter:saturate(.6)}
R .hs{width:300px;height:420px}
R #k7-cnt{left:0;right:0;top:300px;text-align:center}
R .rm{width:940px;height:640px;left:70px;top:420px}
R #k7-meal{left:70px;top:420px;width:940px;height:400px}
""",
    bg="""        <div class="full" id="k7-bg"><img src="@P/res104-01.jpg" alt="" /></div>
        <div class="dim" style="opacity:.8"></div>""",
    body=f"""
          <div class="abs" id="k7-cnt"><span class="num gold" style="font-size:150px" id="k7-n">5</span><span class="hd" style="font-size:64px">곳</span></div>
          {houses7}
          <div class="chip cream" id="k7-c1" style="left:120px;top:1300px;font-size:38px">도보 통학</div>
          <div class="chip cream" id="k7-c2" style="left:400px;top:1300px;font-size:38px">여학생 전용 하우스</div>
          {''.join(f'<div class="ph frame rm" id="k7-r{i}"><img src="@P/{n}.jpg" alt="" /><div class="lab">{l}</div></div>' for i, (n, l) in enumerate(rooms7[1:]))}
          <div class="pill" id="k7-24" style="left:250px;top:1120px;font-size:52px;padding:18px 44px">사감 24시간 상주</div>
          <div class="ph frame" id="k7-meal"><img src="@B/meals-grid.jpg" alt="" /></div>
          <div class="chip gold" id="k7-m1" style="left:90px;top:870px;font-size:38px">하루 3식</div>
          <div class="chip cream" id="k7-m2" style="left:330px;top:870px;font-size:38px">한식 메뉴</div>
          <div class="chip cream" id="k7-m3" style="left:610px;top:870px;font-size:38px">알레르기 맞춤</div>
          <div class="card" id="k7-room" style="left:110px;top:560px;width:860px;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center"><div class="hd" style="font-size:50px">방 타입 배정</div><div class="h" style="font-size:68px;margin-top:12px">신청 순서 · <span class="red">잔여 상황</span></div></div>""",
    js="""
kb('#k7-bg img',0,D,{s:1.0},{s:1.1});
slam('#k7-cnt',0.0,{s:1.6});odo('#k7-n',0.0,0.8);
const H=['#k7-h0','#k7-h1','#k7-h2','#k7-h3','#k7-h4'].map(s=>q(s));
tl.fromTo(H,{opacity:0,y:-140,rotation:(i)=>[-8,5,-4,7,-6][i]},{opacity:1,y:0,rotation:(i)=>[-3,2,-2,3,-2][i],duration:0.6,ease:'power3.out',stagger:0.15},0.3);
pop('#k7-c1',T('걸어서'));pop('#k7-c2',T('여학생 전용'));
tl.to(H.concat(['#k7-cnt','#k7-c1','#k7-c2'].map(s=>q(s))),{opacity:0,y:-40,duration:0.35,ease:'power2.in'},T('모든 레지던스에')-0.35);
const RT=[T('모든 레지던스에'),T('사감 선생님이')+0.2,T('24시간'),T('생활을 관리해요')];
for(let i=0;i<4;i++){if(i>0)tl.to('#k7-r'+(i-1),{opacity:0,duration:0.3},RT[i]+0.25);tl.fromTo('#k7-r'+i,{opacity:0,x:120,rotation:3},{opacity:1,x:0,rotation:(i%2?1.5:-1.5),duration:0.5,ease:'power3.out'},RT[i]);kb('#k7-r'+i+' img',RT[i],6,{s:1.0},{s:1.08});}
pop('#k7-24',T('24시간'));
tl.to(['#k7-r0','#k7-r1','#k7-r2','#k7-r3','#k7-24'].map(s=>q(s)),{opacity:0,y:-40,duration:0.35,ease:'power2.in'},T('식사는')-0.35);
mask('#k7-meal',T('식사는'),0.8,'d');kb('#k7-meal img',T('식사는'),D,{s:1.0},{s:1.06});
pop('#k7-m1',T('하루 세 끼'));pop('#k7-m2',T('한식 메뉴'));pop('#k7-m3',T('알레르기'));
tl.to(['#k7-meal','#k7-m1','#k7-m2','#k7-m3'].map(s=>q(s)),{opacity:0,y:-40,duration:0.35,ease:'power2.in'},T('방 타입은')-0.35);
inn('#k7-room',T('방 타입은'),{y:30,s:0.92});
""",
    sfx=[("impact", "0.4"), ("pop", "T('걸어서')"), ("pop", "T('여학생 전용')"), ("whoosh", "T('모든 레지던스에')"), ("pop", "T('24시간')"),
         ("pop", "T('하루 세 끼')"), ("pop", "T('한식 메뉴')"), ("pop", "T('알레르기')")],
    thumb=dict(photo="res104-01", lines=[("레지던스", "#fff"), ("5곳,", "#e8b931"), ("어디에 살까", "#fff")], pill="사감 24시간 상주 · 토론토 SGA"),
    upload=dict(
        title="레지던스 5곳, 어디에 살까 | 토론토 사립고 SGA 레지던스",
        first="캐나다 조기유학 토론토 관리형 사립고 SGA의 학생 레지던스를 정리했습니다.",
        body="SGA 레지던스는 학교에서 걸어서 다닐 수 있는 거리에 다섯 곳이 있고, 여학생 전용 하우스도 있습니다. 모든 레지던스에 사감 선생님이 상주하며 24시간 생활을 관리하고, 식사는 하루 세 끼(한식 메뉴, 알레르기 맞춤)가 나옵니다. 방 타입은 신청 순서와 잔여 상황에 따라 배정됩니다.",
        note="※ 자료: 2026 SGA 공식 브로셔(레지던스 5곳). 식사는 격주 일요일 저녁 제외. 사진은 레지던스 일부입니다.",
        tags="#캐나다조기유학 #토론토조기유학 #토론토사립고 #홈스테이 #레지던스 #StGeorgeAcademy #AACanada #shorts"),
)
