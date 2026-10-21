"""S01-S04. Cues: T('phrase') = when that phrase is spoken (resolved by build.py)."""
from common import adult, kid, maple

S = {}

# ---------------------------------------------------------------- S01 opening
S["s01"] = dict(
    css="""
R .q1{top:150px;font-size:92px}
R .q2{top:270px;font-size:150px}
R .kids{position:absolute;left:1430px;top:150px;display:flex;gap:24px}
R .avg{left:760px;top:500px}
R .amt{top:570px;font-size:230px;color:#C8102E}
R .amt small{font-size:120px}
R .intro{left:0;right:0;top:0;bottom:0}
R .logo{position:absolute;left:250px;top:250px;width:420px;height:406px}
R .who1{left:780px;top:280px;font-size:44px;color:#7A1B26;font-weight:700}
R .who2{left:780px;top:350px;font-size:120px}
R .son{left:780px;top:540px;width:900px;height:130px;display:flex;align-items:center;gap:22px;padding:0 40px;font-size:46px;font-weight:700}
R .vsl{left:170px;top:250px;width:680px;height:300px;display:flex;align-items:center;justify-content:center;font-size:110px}
R .vsr{left:1070px;top:250px;width:680px;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:96px;line-height:1.05}
R .vsr small{font-size:58px;opacity:.9}
R .vs{position:absolute;left:880px;top:320px;width:160px;height:160px;border-radius:50%;background:#2B2B2B;color:#fff;display:flex;align-items:center;justify-content:center;font-size:72px}
R .c1{left:640px;top:590px}
R .c2{left:820px;top:590px}
R .st{left:1010px;top:578px;font-size:50px}
R .which{top:730px;font-size:64px;color:#7A1B26}
""",
    body=f"""
<div class="ph p1">
  <div class="abs center bhs q1">영어유치원에 아이 둘,</div>
  <div class="abs center bhs q2 red">1년에 얼마?</div>
  <div class="kids">{kid("#7A1B26", 80)}{kid("#C8102E", 64)}</div>
  <div class="chip pink avg">서울 평균으로 계산하면</div>
  <div class="abs center num amt">약 <span class="n">3,580</span><small>만원</small></div>
</div>
<div class="ph p2" style="opacity:0">
  <img class="logo" src="@I/aa-canada-logo-transparent.png" alt="" />
  <div class="abs who1">캐나다 전문 유학원</div>
  <div class="abs bhs who2">AA Canada 원장</div>
  <div class="card son">{maple("", 70)}<span>아들을 <b class="red">몬트리올</b>에서 키운 부모</span></div>
</div>
<div class="ph p3" style="opacity:0">
  <div class="card dark bhs vsl">영어유치원</div>
  <div class="card red bhs vsr"><span>캐나다</span><span>몬트리올</span></div>
  <div class="vs bhs">VS</div>
  <div class="chip solid c1">비용</div>
  <div class="chip solid c2">영어</div>
  <div class="stamp st">숫자로 비교</div>
  <div class="abs center bhs which">우리 집은 어느 쪽?</div>
</div>
""",
    js="""
kin('.q1',0.6);kin('.q2',T('1년에 얼마'));pop('.kids svg',T('아이 둘'),0.15);
inn('.avg',T('서울 평균'),{y:20});inn('.amt',T('1년에 약'),{s:0.8});odo('.n',T('1년에 약'),1.6);pulse('.amt',T('3,580만')+1.0);
phase('.p2',T('안녕하세요'),'.p1');pop('.logo',T('안녕하세요')+0.1);inn('.who1',T('캐나다 전문'),{x:-40,y:0});kin('.who2',T('AA Canada입니다'));
inn('.son',T('저는 아들을'),{x:60,y:0});
phase('.p3',T('오늘은'),'.p2');inn('.vsl',T('영어유치원에 다니는'),{x:-80,y:0});inn('.vsr',T('캐나다 몬트리올에서'),{x:80,y:0});slam('.vs',T('캐나다 몬트리올에서')+0.5);
pop('.c1',T('비용과'));pop('.c2',T('영어가'));stamp('.st',T('숫자로'));
kin('.which',T('우리 집은'));
""",
    sfx=[("pop", "T('아이 둘')"), ("impact", "T('1년에 약')+1.4"), ("whoosh", "T('안녕하세요')-0.3"), ("whoosh", "T('오늘은')-0.3"),
         ("impact", "T('캐나다 몬트리올에서')+0.88"), ("stamp", "T('숫자로')+0.3")],
)

# ---------------------------------------------------------------- S02 영유 비용
S["s02"] = dict(
    css="""
R .ttl{left:120px;top:150px;font-size:84px}
R .sub{left:120px;top:262px;font-size:36px;color:#7A1B26;font-weight:700}
R .axis{position:absolute;left:150px;top:760px;width:820px;height:4px;background:#2B2B2B}
R .bar{width:250px;background:#2B2B2B}
R .b21{left:230px;top:430px;height:330px;background:#D9B9B5}
R .b25{left:620px;top:375px;height:385px;background:#C8102E}
R .yl{position:absolute;top:780px;width:250px;text-align:center;font-weight:700;font-size:36px}
R .v{position:absolute;width:250px;text-align:center;font-size:62px}
R .v21{left:230px;top:362px}
R .v25{left:620px;top:305px;color:#C8102E}
R .up{left:440px;top:220px;font-size:44px}
R .inc{left:1090px;top:330px;width:700px;padding:34px 40px}
R .inc .t{font-weight:900;font-size:40px;margin-bottom:22px}
R .inc .row{display:flex;flex-wrap:wrap;gap:16px}
R .inc .row span{display:inline-block;padding:10px 26px;border-radius:99px;background:#FFD6CF;color:#7A1B26;font-weight:700;font-size:34px}
R .gn{left:1120px;top:640px;font-size:58px}
R .yr{position:absolute;left:150px;width:1620px;height:150px;display:flex;align-items:center;padding:0 50px;gap:40px}
R .yr .k{display:flex;gap:10px;width:300px}
R .yr .l{font-weight:900;font-size:50px;width:260px}
R .yr .m{margin-left:auto;font-size:96px}
R .yr .m small{font-size:56px}
R .y1{top:250px}.y2{top:430px}.y3{top:610px}
R .plus{position:absolute;left:150px;top:300px;width:1620px;height:420px;display:flex;align-items:center;justify-content:center;gap:40px}
R .plus .base{font-size:84px}
R .plus .op{font-size:90px;color:#C8102E}
R .plus .add{display:flex;flex-direction:column;gap:18px}
R .plus .arrow{font-size:76px;color:#C8102E}
""",
    body=f"""
<div class="tag"><i></i>1장 · 영유 비용의 현실</div>
<div class="ph p1">
  <div class="abs bhs ttl">서울 영어유치원 <span class="red">월평균</span> 교습비</div>
  <div class="abs sub">교육부 자료 · 서울 기준</div>
  <div class="bar b21"></div><div class="bar b25"></div><div class="axis"></div>
  <div class="yl" style="left:230px">2021년</div><div class="yl" style="left:620px">2025년</div>
  <div class="v num v21">127.8만</div><div class="v num v25">149만</div>
  <div class="chip solid up">4년 새 +약 17%</div>
  <div class="card inc"><div class="t">월 149만원에 포함</div><div class="row"><span>교습비</span><span>재료비</span><span>급식비</span><span>차량비</span></div></div>
  <div class="stamp gn">학군지 월 200만원대</div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="abs bhs ttl">1년으로 계산하면</div>
  <div class="card yr y1"><div class="k">{kid("#C8102E", 60)}</div><div class="l">아이 1명</div><div class="m num">약 <span class="n1">1,790</span><small>만원</small></div></div>
  <div class="card yr y2"><div class="k">{kid("#C8102E", 60)}{kid("#C8102E", 60)}</div><div class="l">아이 2명</div><div class="m num red"><span class="n2">3,580</span><small>만원</small></div></div>
  <div class="card yr y3"><div class="k">{kid("#C8102E", 60)}{kid("#C8102E", 60)}{kid("#C8102E", 60)}</div><div class="l">아이 3명</div><div class="m num red"><span class="n3">5,360</span><small>만원</small></div></div>
</div>
<div class="ph p3" style="opacity:0">
  <div class="abs bhs ttl">실제 지출은 <span class="red">더 커집니다</span></div>
  <div class="plus"><div class="card base bhs" style="position:relative;padding:40px 50px">영유 학비</div><div class="op bhs">+</div>
    <div class="add"><div class="chip pink" style="position:relative">방과후 프로그램</div><div class="chip pink" style="position:relative">다른 학원</div></div>
    <div class="arrow bhs">= ↑↑</div></div>
</div>
""",
    js="""
inn('.tag',0.2,{x:-30,y:0});kin('.ttl',0.5);inn('.sub',1.2,{y:10});
grow('.b25',T('149만'),0.9,'y');inn('.v25',T('149만')+0.5,{y:20});
inn('.inc',T('교습비에'),{x:60,y:0});pop('.inc .row span',T('재료비'),0.25);
grow('.b21',T('2021년에는'),0.9,'y');inn('.v21',T('127만')+0.2,{y:20});pop('.up',T('17%'));
stamp('.gn',T('200만'),-6);
phase('.p2',T('1년으로'),'.p1');kin('.p2 .ttl',T('1년으로'));
inn('.y1',T('아이 한 명에'),{x:-60,y:0});odo('.n1',T('아이 한 명에')+0.3,1.2);
inn('.y2',T('아이가 둘이면'),{x:-60,y:0});odo('.n2',T('아이가 둘이면')+0.3,1.2);
inn('.y3',T('셋이면'),{x:-60,y:0});odo('.n3',T('셋이면')+0.3,1.2);pulse('.y3 .m',T('셋이면')+1.6);
phase('.p3',T('여기에 방과후'),'.p2');kin('.p3 .ttl',T('여기에 방과후'));inn('.plus .base',T('여기에 방과후')+0.3,{s:0.8});
pop('.plus .op',T('방과후 프로그램'));pop('.plus .chip',T('방과후 프로그램')+0.3,0.4);pop('.plus .arrow',T('실제 지출'));
""",
    sfx=[("pop", "T('149만')+0.5"), ("pop", "T('17%')"), ("stamp", "T('200만')+0.3"), ("whoosh", "T('1년으로')-0.3"),
         ("pop", "T('아이 한 명에')"), ("pop", "T('아이가 둘이면')"), ("impact", "T('셋이면')+0.3"), ("whoosh", "T('여기에 방과후')-0.3")],
)

# ---------------------------------------------------------------- S03 원 문을 나서면
S["s03"] = dict(
    css="""
R .ask{top:300px;font-size:70px;color:#7A1B26}
R .ask2{top:420px;font-size:120px}
R .room{left:140px;top:170px;width:760px;height:560px;padding:0;overflow:hidden}
R .room .board{position:absolute;left:60px;top:60px;width:640px;height:230px;border-radius:18px;background:#2B2B2B;color:#fff;display:flex;align-items:center;justify-content:center;font-size:110px;font-family:'Black Han Sans',sans-serif;letter-spacing:.08em}
R .room .lab,.out .lab{position:absolute;left:0;right:0;bottom:36px;text-align:center;font-weight:900;font-size:44px}
R .door{position:absolute;left:910px;top:250px;width:100px;height:400px}
R .out{left:1020px;top:170px;width:760px;height:560px;overflow:hidden}
R .bub1{left:1080px;top:250px}.bub2{left:1380px;top:380px}.bub3{left:1120px;top:510px}
R .en1{left:190px;top:470px}.en2{left:560px;top:530px}
R .day{left:140px;top:770px;width:1640px;height:44px;border-radius:22px;overflow:hidden;display:flex;background:#fff}
R .day .e{width:24%;background:#C8102E}
R .day .k{flex:1;background:#2B2B2B}
R .dl{position:absolute;top:722px;font-weight:700;font-size:30px}
R .big1{top:270px;font-size:110px}
R .big2{top:440px;font-size:150px;color:#C8102E}
R .strike{position:absolute;left:470px;top:330px;width:0;height:12px;background:#C8102E}
R .go{top:300px;font-size:110px}
R .plane{position:absolute;left:330px;top:520px;width:1260px;height:220px}
""",
    body=f"""
<div class="ph p1">
  <div class="abs center bhs ask">상담에서 더 아쉬워하시는 건</div>
  <div class="abs center bhs ask2">비용보다 <span class="hl">이 부분</span></div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="card room"><div class="board">ABC</div><div class="lab">원 안: <span class="red">영어 수업</span></div></div>
  <div class="bubble red en1">Good morning!</div><div class="bubble red en2">Apple!</div>
  <svg class="door" viewBox="0 0 100 400"><rect x="10" y="10" width="80" height="380" rx="8" fill="#7A1B26"/><circle cx="72" cy="210" r="7" fill="#FFD6CF"/></svg>
  <div class="card out" style="background:#fff"><div class="lab">문 밖: <span>다시 한국어</span></div></div>
  <div class="bubble bub1">같이 놀자!</div><div class="bubble pink bub2">엄마, 배고파</div><div class="bubble bub3">집에 가자~</div>
  <div class="dl" style="left:150px">하루 몇 시간 영어</div><div class="dl" style="left:1540px">나머지는 한국어</div>
  <div class="abs day"><div class="e"></div><div class="k"></div></div>
</div>
<div class="ph p3" style="opacity:0">
  <div class="abs center bhs big1">영어가 <span class="red">생활</span>이 아니라</div>
  <div class="abs center bhs big2">하나의 '과목'</div>
</div>
<div class="ph p4" style="opacity:0">
  <div class="abs center bhs go">같은 돈으로 <span class="red">캐나다</span>에 가면?</div>
  <svg class="plane" viewBox="0 0 1260 220"><path class="pl" d="M20 200 C 300 20, 900 20, 1180 120" fill="none" stroke="#C8102E" stroke-width="8" stroke-dasharray="1 0" stroke-linecap="round"/>
    <g transform="translate(1130 60)">{maple("", 110).replace('<svg ', '<svg x="0" y="0" ')}</g></svg>
</div>
""",
    js="""
kin('.ask',0.3);kin('.ask2',T('비용보다'));
phase('.p2',T('하루 몇 시간'),'.p1');inn('.room',T('하루 몇 시간'),{x:-60,y:0});pop('.en1,.en2',T('영어로 수업')+0.2,0.3);
grow('.day',T('하루 몇 시간'),1.0,'x');
inn('.door',T('원 문을'),{s:0.6});inn('.out',T('나서는 순간'),{x:60,y:0});dim('.en1,.en2',T('다시 한국어'),0.3);
pop('.bub1',T('친구와 노는'));pop('.bub2',T('집에 오는'));pop('.bub3',T('한국어죠'));
phase('.p3',T('영어가 생활이'),'.p2');kin('.big1',T('영어가 생활이'));slam('.big2',T('하나의 과목'));
phase('.p4',T('그럼 같은 돈으로'),'.p3');kin('.go',T('그럼 같은 돈으로'));draw('.pl',T('캐나다에 가면'),1.2);pop('.plane g',T('캐나다에 가면')+1.0);
""",
    sfx=[("whoosh", "T('하루 몇 시간')-0.3"), ("pop", "T('친구와 노는')"), ("pop", "T('집에 오는')"), ("impact", "T('하나의 과목')+0.38"),
         ("whoosh", "T('캐나다에 가면')")],
)

# ---------------------------------------------------------------- S04 자녀무상교육 구조
S["s04"] = dict(
    css="""
R .ttl{left:120px;top:150px;font-size:84px}
R .par{left:180px;top:300px;width:560px;height:400px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px}
R .par .t{font-weight:900;font-size:46px}
R .par .s{font-weight:700;font-size:36px;color:#7A1B26}
R .arr{position:absolute;left:770px;top:450px;width:380px;height:100px}
R .kidc{left:1180px;top:300px;width:560px;height:400px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px}
R .kidc .t{font-weight:900;font-size:46px}
R .zero{font-size:120px;color:#C8102E}
R .qc{left:740px;top:720px;font-size:40px}
R .qc2{left:1120px;top:620px;font-size:62px}
R .one{left:120px;top:270px;font-size:100px}
R .ladder{position:absolute;left:120px;top:470px;width:1680px;height:300px}
R .stp{position:absolute;bottom:0;width:390px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:26px;border-radius:22px 22px 0 0;font-weight:900;font-size:44px;color:#fff;background:#C8102E}
R .more{top:250px;font-size:96px}
R .kidrow{position:absolute;left:0;right:0;top:450px;display:flex;justify-content:center;gap:40px}
R .diff{top:700px;font-size:60px;color:#7A1B26}
""",
    body=f"""
<div class="tag"><i></i>2장 · 캐나다 자녀무상교육</div>
<div class="ph p1">
  <div class="abs bhs ttl">캐나다 <span class="red">자녀무상교육</span>이란?</div>
  <div class="card par">{adult("#2B2B2B", 90)}<div class="t">부모</div><div class="s">학생비자로 공부</div></div>
  <svg class="arr" viewBox="0 0 380 100"><path class="ar" d="M10 50 L340 50 M300 14 L350 50 L300 86" fill="none" stroke="#C8102E" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <div class="card kidc">{kid("#C8102E", 80)}<div class="t">동반 자녀 · 현지 공립학교</div><div class="num zero">학비 0원</div></div>
  <div class="chip pink qc">퀘벡주(몬트리올)도 동일</div>
  <div class="stamp qc2">학비 면제</div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="abs bhs one">학비는 <span class="hl">부모 1명분</span>만</div>
  <div class="ladder">
    <div class="stp s1" style="left:0;height:110px">유치원</div>
    <div class="stp s2" style="left:430px;height:170px">초등학교</div>
    <div class="stp s3" style="left:860px;height:230px">중학교</div>
    <div class="stp s4" style="left:1290px;height:290px">고등학교</div>
  </div>
</div>
<div class="ph p3" style="opacity:0">
  <div class="abs center bhs more">아이가 <span class="red">둘, 셋</span>이 되면?</div>
  <div class="kidrow">{kid("#C8102E", 110, "k k1")}{kid("#C8102E", 110, "k k2")}{kid("#C8102E", 110, "k k3")}</div>
  <div class="abs center bhs diff">차이가 더 커집니다</div>
</div>
""",
    js="""
inn('.tag',0.2,{x:-30,y:0});kin('.ttl',0.4);
inn('.par',T('부모가 학생비자로'),{x:-60,y:0});draw('.ar',T('함께 간 자녀')-0.3,0.7);inn('.kidc',T('함께 간 자녀'),{x:60,y:0});slam('.zero',T('학비 없이'));
pop('.qc',T('퀘벡주도'));stamp('.qc2',T('면제됩니다')-0.3,-6);
phase('.p2',T('그래서 학비는'),'.p1');kin('.one',T('그래서 학비는'));
grow('.s1',T('유치원부터'),0.6,'y');grow('.s2',T('초등학교'),0.6,'y');grow('.s3',T('중학교'),0.6,'y');grow('.s4',T('고등학교까지'),0.6,'y');
phase('.p3',T('그리고 이 구조는'),'.p2');kin('.more',T('그리고 이 구조는'));pop('.k1',T('아이가 둘'));pop('.k2',T('아이가 둘')+0.3);pop('.k3',T('셋이 되면'));
kin('.diff',T('더 큰 차이'));
""",
    sfx=[("impact", "T('학비 없이')+0.38"), ("stamp", "T('면제됩니다')"), ("whoosh", "T('그래서 학비는')-0.3"), ("whoosh", "T('그리고 이 구조는')-0.3"),
         ("pop", "T('아이가 둘')"), ("pop", "T('셋이 되면')")],
)
