"""S07-S10 (elementary, cost & dates, director's take, wrap-up)."""
import geo
from clips import dur as clip_dur
from mapkit import cam_html, cam_set_js, clock, icon, label, pin, reel, seq

S = {}

# ---------------------------------------------------------------- S07 elementary
V_EL = geo.view(45.545, -73.445, 50, cx=860, cy=470)
_EL_OFF = {"goodshepherd": (30, -10), "napper": (30, 34), "stlambertel": (-250, -40), "gpi": (-330, 20),
           "cpi": (-200, -76), "boucherville": (30, -30)}
_el = "".join(pin(f"ep-{k}", la, lo, V_EL, 46) + label(f"el-{k}", n, la, lo, V_EL, 26, dot=False, dx=_EL_OFF[k][0], dy=_EL_OFF[k][1], kind="mtag")
              for k, n, la, lo in geo.ELEM)
KW = [("kw1", "굿셰퍼드", "영어 84%", "T('브로사드의 굿셰퍼드')"),
      ("kw2", "해롤드 내퍼", "2026 증축", "T('해롤드 내퍼는')"),
      ("kw3", "생랑베르 초등", "영어 70 : 불어 30", "T('생랑베르 초등학교는')"),
      ("kw4", "그린필드파크 · 코틀랜드파크", "IB 초등(PYP)", "T('그린필드파크와 생브루노에는')")]
S["s07"] = dict(
    css="""
R .elt{left:120px;top:150px;font-size:58px;z-index:5}
R .kws{position:absolute;left:1330px;top:150px;width:480px;display:flex;flex-direction:column;gap:18px}
R .kws .card{position:relative;padding:20px 28px}
R .kws .a{font-weight:900;font-size:30px;color:#7A1B26}
R .kws .b{font-family:'Black Han Sans',sans-serif;font-size:50px;color:#C8102E;margin-top:4px}
R .clk{position:absolute;top:220px;width:560px;display:flex;flex-direction:column;align-items:center}
R .clk .t{font-size:96px;margin-top:20px}
R .clk .n{font-weight:900;font-size:36px;color:#7A1B26;margin-top:6px}
R .ck1{left:260px}.ck2{left:1100px}
R .diff{left:780px;top:330px;font-size:44px}
R .more{left:0;right:0;top:700px;text-align:center;font-size:40px}
""",
    body=f"""
<div class="tag"><i></i>6 · 초등학교</div>
<div class="ph p1">
  {cam_html(_el)}
  <div class="abs bhs elt">초등학교는 <span class="red">선택지가 더 많아요</span></div>
  <div class="kws">{"".join(f'<div class="card {k}"><div class="a">{a}</div><div class="b">{b}</div></div>' for k, a, b, _ in KW)}</div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="clk ck1">{clock(7, 50, 260)}<div class="t num">7:50</div><div class="n">굿셰퍼드 수업 시작</div></div>
  <div class="stamp diff">1시간 15분 차이</div>
  <div class="clk ck2">{clock(9, 5, 260, "#7A1B26")}<div class="t num red">9:05</div><div class="n">생랑베르 초등 수업 시작</div></div>
  <div class="abs more"><span class="chip solid" style="position:relative">학교별 정리 → 블로그 · 홈페이지</span></div>
</div>
""",
    js=f"""
{cam_set_js(V_EL)}
inn('.elt',T('초등학생이라면'),{{y:20}});
tl.fromTo(qa('.pin'),{{opacity:0,y:-50}},{{opacity:1,y:0,duration:0.5,ease:'bounce.out',stagger:0.18}},T('몇 곳만'));
pop('.mtag',T('몇 곳만')+0.4,0.18);
{"".join(f"inn('.{k}',{cue},{{x:60,y:0}});" for k, _, _, cue in KW)}
phase('.p2',T('학교마다 시작 시간이'),'.p1');inn('.ck1',T('학교마다 시작 시간이'),{{x:-50,y:0}});inn('.ck2',T('학교마다 시작 시간이')+0.4,{{x:50,y:0}});
stamp('.diff',T('한 시간 넘게'),-5);pop('.more',T('블로그와 홈페이지에'));
""",
    sfx=[("pop", "T('몇 곳만')"), ("pop", "T('브로사드의 굿셰퍼드')"), ("pop", "T('생랑베르 초등학교는')"),
         ("whoosh", "T('학교마다 시작 시간이')-0.3"), ("stamp", "T('한 시간 넘게')+0.3"), ("pop", "T('블로그와 홈페이지에')")],
)

# ---------------------------------------------------------------- S08 cost & dates
S["s08"] = dict(
    css="""
R .ct{left:120px;top:150px;font-size:58px}
R .ct small{font-size:32px;color:#7A1B26;font-family:'Noto Sans KR',sans-serif;font-weight:700;margin-left:16px}
R .cost{position:absolute;top:260px;width:800px;height:420px;padding:40px 50px}
R .cost .k{font-weight:900;font-size:42px}
R .cost .v{font-size:132px;margin-top:22px;white-space:nowrap}
R .cost .v small{font-size:52px}
R .cost .row{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}
R .cost .row span{padding:6px 18px;border-radius:99px;background:#FFD6CF;color:#7A1B26;font-weight:700;font-size:26px}
R .co1{left:120px}.co2{left:1000px}
R .note{left:120px;top:700px;font-size:26px;color:#7A1B26;font-weight:700}
R .inc{position:absolute;top:230px;width:800px;height:460px;padding:40px 46px}
R .inc .h{font-weight:900;font-size:44px;margin-bottom:30px}
R .inc .ics{display:flex;gap:40px}
R .inc .it{display:flex;flex-direction:column;align-items:center;gap:12px;font-weight:900;font-size:32px}
R .in1{left:120px}.in2{left:1000px}
R .tline{position:absolute;left:180px;top:470px;width:1560px;height:8px;border-radius:4px;background:#C8102E}
R .tp{position:absolute;top:300px;width:620px;text-align:center}
R .tp .d{font-size:84px;color:#C8102E}
R .tp .l{font-weight:900;font-size:40px;margin-top:70px}
R .tp .s{font-weight:700;font-size:30px;color:#7A1B26;margin-top:8px}
R .tp i{position:absolute;left:290px;top:154px;width:40px;height:40px;border-radius:50%;background:#fff;border:8px solid #C8102E}
R .tp1{left:220px}.tp2{left:1080px}
R .early{left:0;right:0;top:720px;text-align:center}
""",
    body=f"""
<div class="tag"><i></i>7 · 비용과 일정</div>
<div class="ph p1">
  <div class="abs bhs ct">조기유학 비용 <small>리버사이드 학생·가족용 학비표 · 2027-28</small></div>
  <div class="card cost co1"><div class="k">1년 과정 (10개월)</div><div class="v num">약 <span class="red">CAD 32,000</span></div>
    <div class="row"><span>수업료</span><span>홈스테이</span><span>행정비</span><span>CAQ</span></div></div>
  <div class="card cost co2"><div class="k">한 학기 (5개월)</div><div class="v num">약 <span class="red">CAD 18,800</span></div>
    <div class="row"><span>학교 예시 금액</span></div></div>
  <div class="abs note">* 학교 예시(CAQ 포함) · 캐나다 달러 · 변경될 수 있음</div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="card inc in1"><div class="h">행정비에 포함</div><div class="ics">
    <div class="it">{icon("shield", 110)}의료보험</div><div class="it">{icon("bus", 110)}통학</div><div class="it">{icon("ball", 110)}교내 활동</div></div></div>
  <div class="card pink inc in2"><div class="h">홈스테이에 포함</div><div class="ics">
    <div class="it">{icon("meal", 110, "#7A1B26")}하루 세 끼</div><div class="it">{icon("plane", 110, "#7A1B26")}공항 픽업</div></div></div>
</div>
<div class="ph p3" style="opacity:0">
  <div class="tline"></div>
  <div class="tp tp1"><div class="d num">2027.02.02</div><i></i><div class="l">겨울 학기 개강</div><div class="s">한 학기 5개월</div></div>
  <div class="tp tp2"><div class="d num">2027.09.08</div><i></i><div class="l">1년 과정 개강</div><div class="s">2027-28학년도</div></div>
  <div class="abs early"><span class="chip solid" style="position:relative">홈스테이 학생은 빨리 지원할수록 유리 (교육청 안내)</span></div>
</div>
""",
    js="""
inn('.ct',T('비용도 궁금하시죠'),{y:20});
inn('.co1',T('1년 과정은'),{x:-60,y:0});pulse('.co1 .v',T('약 3만 2천')+0.4);pop('.co1 .row span',T('수업료,'),0.12);
inn('.co2',T('한 학기 5개월은'),{x:60,y:0});pulse('.co2 .v',T('1만 8,800달러'));inn('.note',T('한 학기 5개월은')+1.0,{y:10});
phase('.p2',T('행정비 안에'),'.p1');inn('.in1',T('행정비 안에'),{x:-60,y:0});pop('.in1 .it',T('의료보험과'),0.25);
inn('.in2',T('홈스테이에는'),{x:60,y:0});pop('.in2 .it',T('하루 세 끼'),0.35);
phase('.p3',T('일정은 두 가지'),'.p2');grow('.tline',T('일정은 두 가지'),1.0);
inn('.tp1',T('2027년 2월 2일'),{y:30});inn('.tp2',T('2027년 9월 8일'),{y:30});pop('.early',T('홈스테이 학생은'));
""",
    sfx=[("pop", "T('1년 과정은')"), ("pop", "T('한 학기 5개월은')"), ("whoosh", "T('행정비 안에')-0.3"),
         ("whoosh", "T('일정은 두 가지')-0.3"), ("pop", "T('2027년 2월 2일')"), ("pop", "T('2027년 9월 8일')")],
)

# ---------------------------------------------------------------- S09 director's take
_bg, _ = seq(["sli-garden", "stj-entrance", "cen-sign", "her-bus", "sli-sign"], "T('제가 사우스쇼어를')", 2.4, clip_dur)
S["s09"] = dict(
    css="""
R .bgr{position:absolute;left:0;top:0;width:1920px;height:1080px;border-radius:0}
R .veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,248,242,.55) 0%,rgba(255,248,242,.92) 46%,rgba(255,248,242,.96) 100%)}
R .ln1{top:300px;font-size:92px}
R .ln2{top:450px;font-size:92px}
R .steps{position:absolute;left:120px;top:250px;width:1680px;display:flex;align-items:center;gap:30px}
R .steps .card{position:relative;flex:1;height:360px;padding:40px;display:flex;flex-direction:column;justify-content:center}
R .steps .k{font-weight:900;font-size:34px;color:#7A1B26}
R .steps .v{font-family:'Black Han Sans',sans-serif;font-size:66px;margin-top:16px;line-height:1.15}
R .steps .ar{font-size:70px;color:#C8102E;font-family:'Black Han Sans',sans-serif}
""",
    body=f"""
<div class="ph p1">
  {reel("s09", "bgr", 0, 0, 1920, 1080, _bg)}
  <div class="veil"></div>
  <div class="abs center bhs ln1">생활은 <span class="red">조용한 영어권 교외</span>에서,</div>
  <div class="abs center bhs ln2">경험은 <span class="red">18분 거리의 대도시</span>에서.</div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="steps">
    <div class="card s1"><div class="k">처음 몇 달</div><div class="v">조금 힘들 수 있어요</div></div>
    <div class="ar">→</div>
    <div class="card red s2"><div class="k" style="color:#FFD6CF">그 시간이 지나면</div><div class="v">영어가 <span style="color:#FFD6CF">생활</span>이 됩니다</div></div>
    <div class="ar">+</div>
    <div class="card pink s3"><div class="k">덤으로</div><div class="v">불어까지</div></div>
  </div>
</div>
""",
    js="""
inn('.bgr',0.2,{s:1.04,y:0,d:1.2});
kin('.ln1',T('생활은 조용한'),0.03);kin('.ln2',T('경험은 18분'),0.03);
phase('.p2',T('한국 친구들끼리'),'.p1');inn('.s1',T('처음 몇 달은'),{y:30});pop('.steps .ar',T('그 시간이 지나면'),0.6);
inn('.s2',T('그 시간이 지나면'),{y:30});pulse('.s2',T('생활이 됩니다'));inn('.s3',T('불어까지 덤으로'),{y:30});
""",
    sfx=[("whoosh", "T('생활은 조용한')-0.2"), ("whoosh", "T('한국 친구들끼리')-0.3"), ("pop", "T('그 시간이 지나면')"), ("pop", "T('불어까지 덤으로')")],
)

# ---------------------------------------------------------------- S10 wrap-up + end card
S["s10"] = dict(
    css="""
R .sum{left:120px;top:150px;font-size:64px}
R .ck{position:absolute;left:180px;width:1560px;height:130px;display:flex;align-items:center;gap:34px;padding:0 44px}
R .ck .t{font-weight:900;font-size:50px}
R .ck1{top:270px}.ck2{top:430px}.ck3{top:590px}
R .end{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;padding-bottom:180px}
R .end img{width:200px;height:194px}
R .end .brand{font-family:'Black Han Sans',sans-serif;font-size:110px;color:#2B2B2B}
R .end .sub{font-weight:700;font-size:40px;color:#7A1B26}
R .end .kakao{display:flex;align-items:center;gap:20px;background:#C8102E;color:#fff;border-radius:28px;padding:22px 50px;font-weight:900;font-size:54px}
R .end .ph2{font-weight:900;font-size:40px}
R .end .blog{font-weight:700;font-size:34px;color:#2B2B2B;background:#FFD6CF;border-radius:16px;padding:10px 28px}
""",
    body=f"""
<div class="ph p1">
  <div class="abs bhs sum">오늘 내용 <span class="red">정리</span></div>
  <div class="card ck ck1"><span class="check">1</span><span class="t">다운타운까지 <span class="red">REM 18분</span></span></div>
  <div class="card ck ck2"><span class="check">2</span><span class="t"><span class="red">한국 사람이 거의 없는</span> 영어 공립학교 생활권</span></div>
  <div class="card ck ck3"><span class="check">3</span><span class="t">리버사이드 초등 19 · 고등 4 중에서 <span class="red">아이에게 맞는 학교</span></span></div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="end">
    <img class="lg" src="@I/aa-canada-logo-transparent.png" alt="" />
    <div class="brand">AA CANADA</div>
    <div class="sub">아이 학년·성향 보내 주시면 동네·학교 + 학교 영상을 골라 드려요</div>
    <div class="kakao">{icon("chat", 70, "#fff")}카카오톡 canlog</div>
    <div class="ph2">02-567-4345</div>
    <div class="blog">학교별 자세한 정보 → 설명란 블로그 링크</div>
  </div>
</div>
""",
    js="""
inn('.sum',T('오늘 내용'),{y:20});
inn('.ck1',T('첫째'),{x:-60,y:0});inn('.ck2',T('둘째'),{x:-60,y:0});inn('.ck3',T('셋째'),{x:-60,y:0});
phase('.p2',T('아이 학년과 성향을'),'.p1');pop('.lg',T('아이 학년과 성향을'));kin('.brand',T('아이 학년과 성향을')+0.2,0.05);
inn('.sub',T('카카오톡으로'),{y:16});pop('.kakao',T('카카오톡으로')+0.3);pulse('.kakao',T('학교 영상과 함께'),3);
inn('.ph2',T('학교 영상과 함께')+0.5,{y:10});inn('.blog',T('설명란의 블로그'),{y:16});
""",
    sfx=[("pop", "T('첫째')"), ("pop", "T('둘째')"), ("pop", "T('셋째')"), ("whoosh", "T('아이 학년과 성향을')-0.3"),
         ("pop", "T('카카오톡으로')+0.3")],
)
