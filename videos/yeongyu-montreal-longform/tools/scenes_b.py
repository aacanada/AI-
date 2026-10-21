"""S05-S08."""
import json
import os

from common import adult, kid, maple

S = {}
_MAP = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "canada_map.json")))


def canada_svg(cls, hi="qc"):
    paths = "".join(f'<path class="pv pv-{k}" d="{p}" fill="{"#C8102E" if k == hi else "#E9CFCB"}" stroke="#FFF8F2" stroke-width="2"/>'
                    for k, p in _MAP["paths"].items())
    return f'<svg class="{cls}" viewBox="{_MAP["viewBox"]}">{paths}</svg>'


# ---------------------------------------------------------------- S05 아이 수별 비교표
S["s05"] = dict(
    css="""
R .ttl{left:120px;top:140px;font-size:80px}
R .ttl small{font-size:40px;color:#7A1B26;font-family:'Noto Sans KR',sans-serif;font-weight:700;margin-left:24px}
R .hdr{position:absolute;top:268px;font-weight:900;font-size:40px;width:520px;text-align:center}
R .h1{left:640px;color:#2B2B2B}.h2{left:1240px;color:#C8102E}
R .row{position:absolute;left:120px;width:1680px;height:150px;border-radius:24px;background:#fff;box-shadow:0 14px 30px rgba(122,27,38,.10);border-left:14px solid #C8102E}
R .row .k{position:absolute;left:46px;top:0;height:150px;display:flex;align-items:center;gap:8px}
R .row .lb{position:absolute;left:250px;top:0;height:150px;display:flex;align-items:center;font-weight:900;font-size:46px}
R .row .a{position:absolute;left:520px;width:520px;top:0;height:150px;display:flex;align-items:center;justify-content:center;font-size:84px}
R .row .b{position:absolute;left:1120px;width:520px;top:0;height:150px;display:flex;align-items:center;justify-content:center;font-size:84px;color:#C8102E}
R .row small{font-size:46px}
R .r1{top:330px}.r2{top:500px}.r3{top:670px}
R .mul{left:600px;top:190px;font-size:40px}
R .zero{left:1230px;top:190px;font-size:40px}
R .lv1{top:200px;font-size:96px}
R .lv2{top:340px;font-size:54px;color:#7A1B26}
R .eq{left:220px;top:470px;width:1480px;height:250px;display:flex;align-items:center;justify-content:center;gap:40px;font-size:64px}
R .q{top:500px;font-size:84px}
R .meter{position:absolute;left:360px;top:660px;width:1200px;height:60px;border-radius:30px;background:#FFD6CF;overflow:hidden}
R .meter i{position:absolute;left:0;top:0;bottom:0;width:100%;background:#C8102E;border-radius:30px}
R .ml{position:absolute;top:735px;font-weight:700;font-size:32px}
""",
    body=f"""
<div class="tag"><i></i>2장 · 1년 학비 나란히</div>
<div class="ph p1">
  <div class="abs bhs ttl">아이 수별 1년 학비<small>1달러 = 약 1,000원</small></div>
  <div class="hdr h1">영어유치원</div><div class="hdr h2">몬트리올 자녀무상교육</div>
  <div class="row r1"><div class="k">{kid("#C8102E", 46)}</div><div class="lb">아이 1명</div><div class="a num">약 1,790<small>만원</small></div><div class="b num">약 1,200<small>만원</small></div></div>
  <div class="row r2"><div class="k">{kid("#C8102E", 46)}{kid("#C8102E", 46)}</div><div class="lb">아이 2명</div><div class="a num">3,580<small>만원</small></div><div class="b num">1,200<small>만원</small></div></div>
  <div class="row r3"><div class="k">{kid("#C8102E", 46)}{kid("#C8102E", 46)}{kid("#C8102E", 46)}</div><div class="lb">아이 3명</div><div class="a num">5,360<small>만원</small></div><div class="b num">1,200<small>만원</small></div></div>
  <div class="chip dark mul">× 아이 수만큼</div>
  <div class="chip solid zero">아이 학비 0원 · 부모 학비만</div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="abs center bhs lv1">가족 생활비는 <span class="red">따로</span></div>
  <div class="abs center lv2" style="font-weight:700">하지만 한국에서도 원래 드는 돈</div>
  <div class="card eq"><span class="bhs">비교할 건</span><span class="bhs red">"추가로 얼마가 더 드느냐"</span></div>
</div>
<div class="ph p3" style="opacity:0">
  <div class="abs center bhs lv1">아이가 <span class="red">둘 이상</span>이라면</div>
  <div class="abs center bhs q">차이를 꽤 줄이거나, <span class="hl">오히려 절약</span>도</div>
  <div class="meter"><i></i></div>
  <div class="ml" style="left:360px">추가 비용</div><div class="ml" style="left:1400px">줄어듦</div>
</div>
""",
    js="""
inn('.tag',0.2,{x:-30,y:0});kin('.ttl',0.4);inn('.hdr',T('나란히')-0.4,{y:-20,st:0.2});
inn('.r1',T('아이가 한 명이면'),{x:-60,y:0});inn('.r1 .a',T('약 1,790'),{s:0.6});inn('.r1 .b',T('부모 학비 약'),{s:0.6});
inn('.r2',T('아이가 둘이면'),{x:-60,y:0});inn('.r2 .a',T('3,580만'),{s:0.6});inn('.r2 .b',T('그대로 1,200'),{s:0.6});pulse('.r2 .b',T('그대로 1,200')+0.6);
inn('.r3',T('아이가 셋이면'),{x:-60,y:0});inn('.r3 .a',T('5,360만'),{s:0.6});inn('.r3 .b',T('여전히 1,200'),{s:0.6});pulse('.r3 .b',T('여전히 1,200')+0.6);
pop('.mul',T('아이 수만큼'));pop('.zero',T('아이 학비가 0원'));pulse('.zero',T('0원이기')+0.3,2);
phase('.p2',T('물론 솔직하게'),'.p1');kin('.p2 .lv1',T('가족 생활비'));inn('.lv2',T('다만 한국에서도'),{y:20});inn('.eq',T('그래서 실제로'),{s:0.85});pulse('.eq',T('추가로 얼마가')+0.8);
phase('.p3',T('아이가 둘 이상이라면'),'.p2');kin('.p3 .lv1',T('아이가 둘 이상이라면'));kin('.q',T('이 차이를'));inn('.meter',T('이 차이를'),{y:20});inn('.ml',T('이 차이를'),{y:10});
tl.fromTo(q('.meter i'),{width:'100%'},{width:'28%',duration:2.2,ease:'power2.inOut'},T('꽤 줄이거나'));
""",
    sfx=[("pop", "T('약 1,790')"), ("pop", "T('부모 학비 약')"), ("pop", "T('3,580만')"), ("impact", "T('그대로 1,200')"),
         ("pop", "T('5,360만')"), ("impact", "T('여전히 1,200')"), ("stamp", "T('아이 학비가 0원')"), ("whoosh", "T('물론 솔직하게')-0.3"),
         ("whoosh", "T('아이가 둘 이상이라면')-0.3")],
)

# ---------------------------------------------------------------- S06 부모는 어학원만 다녀도
S["s06"] = dict(
    css="""
R .worry{left:300px;top:250px;width:1320px;padding:50px 70px;font-size:62px;line-height:1.35}
R .worry:after{content:'';position:absolute;left:160px;bottom:-40px;border:22px solid transparent;border-top:28px solid #fff}
R .who{left:300px;top:560px;font-weight:700;font-size:36px;color:#7A1B26}
R .faq{left:1340px;top:560px;font-size:42px}
R .opt{position:absolute;top:240px;width:460px;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px}
R .opt .t{font-family:'Black Han Sans',sans-serif;font-size:66px}
R .opt .s{font-weight:700;font-size:30px;color:#7A1B26}
R .o1{left:120px}.o2{left:700px}
R .or{position:absolute;left:598px;top:360px;font-weight:900;font-size:40px;color:#7A1B26}
R .ok{left:1290px;top:240px;width:500px;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;font-family:'Black Han Sans',sans-serif;font-size:56px;text-align:center}
R .arr2{position:absolute;left:1200px;top:370px;font-size:60px;color:#C8102E}
R .when{left:160px;top:600px;width:1620px;height:190px}
R .tline{position:absolute;left:300px;right:60px;height:46px;border-radius:12px}
R .tl1{top:36px;background:#FFD6CF}.tl2{top:106px;background:transparent}
R .tl2 i{position:absolute;top:0;bottom:0;border-radius:12px;background:#C8102E}
R .tlab{position:absolute;left:40px;font-weight:900;font-size:32px}
R .hrs{position:absolute;top:-6px;font-weight:700;font-size:22px;color:#7A1B26}
R .col{left:160px;top:250px;width:1620px;height:420px;display:flex;align-items:center;justify-content:space-around}
R .feat{display:flex;flex-direction:column;align-items:center;gap:24px;width:600px;text-align:center}
R .feat .ic{width:150px;height:150px;border-radius:50%;background:#FFD6CF;display:flex;align-items:center;justify-content:center;font-size:80px;font-family:'Black Han Sans',sans-serif;color:#C8102E}
R .feat .t{font-family:'Black Han Sans',sans-serif;font-size:60px}
R .feat .s{font-weight:700;font-size:34px;color:#7A1B26}
R .big{top:290px;font-size:96px}
R .big2{top:460px;font-size:72px;color:#7A1B26}
R .fam{position:absolute;left:0;right:0;top:600px;display:flex;justify-content:center;align-items:flex-end;gap:20px}
""",
    body=f"""
<div class="tag"><i></i>3장 · 부모는 어학원만 다녀도</div>
<div class="ph p1">
  <div class="card worry hd"><div>"제가 영어를 잘 못하는데,</div><div>공부를 할 수 있을까요?"</div></div>
  <div class="abs who">상담에서 정말 많이 듣는 질문</div>
  <div class="chip solid faq">FAQ No.1</div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="card opt o1"><div class="t">사설 어학원</div><div class="s">평일 오전 수업</div></div>
  <div class="or">또는</div>
  <div class="card opt o2"><div class="t">사립 칼리지</div><div class="s">시간표 자유 · 공인 점수 없이 입학</div></div>
  <div class="arr2 bhs">→</div>
  <div class="card red ok">{maple("", 70, "#fff")}<span style="display:block">동반 자녀</span><span style="display:block">무상교육 ✓</span></div>
  <div class="card when">
    <div class="tlab" style="top:38px">아이 학교</div><div class="tline tl1"></div>
    <div class="tlab" style="top:108px">부모 수업</div><div class="tline tl2"><i class="mi" style="left:6%;width:38%"></i></div>
    <div class="hrs" style="left:300px">8시</div><div class="hrs" style="left:860px">12시</div><div class="hrs" style="left:1500px">15시</div>
  </div>
</div>
<div class="ph p3" style="opacity:0">
  <div class="card col">
    <div class="feat"><div class="ic">⏰</div><div class="t">시간표 자유</div><div class="s">저희가 진행하는 칼리지 과정</div></div>
    <div class="feat"><div class="ic">0</div><div class="t">공인 영어 점수</div><div class="s">없어도 입학 가능</div></div>
  </div>
</div>
<div class="ph p4" style="opacity:0">
  <div class="abs center bhs big">부모 학업 부담 <span class="red">최소</span></div>
  <div class="abs center bhs big2">공부 때문에 아이를 못 챙기는 일 ↓</div>
  <div class="fam">{adult("#2B2B2B", 90)}{kid("#C8102E", 70)}{kid("#C8102E", 56)}</div>
</div>
""",
    js="""
inn('.tag',0.2,{x:-30,y:0});inn('.worry',T('제가 영어를'),{s:0.85});inn('.who',T('상담에서'),{y:20});pop('.faq',T('정말 많이'));
phase('.p2',T('몬트리올은 부모가'),'.p1');inn('.o1',T('사설 어학원'),{y:40});inn('.or',T('이나'),{y:0});inn('.o2',T('사립 칼리지'),{y:40});
inn('.arr2',T('다녀도')-0.2,{x:-30,y:0});slam('.ok',T('동반 자녀'));
inn('.when',T('어학원은 평일'),{y:40});grow('.tl1',T('평일 오전')-0.2,0.8,'x');grow('.mi',T('평일 오전')+0.4,0.8,'x');pulse('.mi',T('잘 맞아요'));
phase('.p3',T('저희가 진행하는'),'.p2');inn('.col',T('저희가 진행하는'),{s:0.9});pop('.feat:nth-child(1) .ic',T('시간표를'));pop('.feat:nth-child(2) .ic',T('공인 영어'));
phase('.p4',T('부모의 학업 부담이'),'.p3');kin('.big',T('부모의 학업 부담이'));kin('.big2',T('공부 때문에'));pop('.fam svg',T('가장 큰 장점'),0.15);
""",
    sfx=[("pop", "T('정말 많이')"), ("whoosh", "T('몬트리올은 부모가')-0.3"), ("impact", "T('동반 자녀')+0.38"), ("whoosh", "T('저희가 진행하는')-0.3"),
         ("pop", "T('공인 영어')"), ("whoosh", "T('부모의 학업 부담이')-0.3")],
)

# ---------------------------------------------------------------- S07 왜 몬트리올
S["s07"] = dict(
    css=f"""
R .map{{position:absolute;left:150px;top:120px;width:560px;height:729px}}
R .pin{{position:absolute;left:{150 + 585 * 560 / 793 - 22:.0f}px;top:{120 + 905 * 729 / 1032 - 60:.0f}px;width:44px;height:60px}}
R .pinl{{position:absolute;left:{150 + 585 * 560 / 793 + 34:.0f}px;top:{120 + 905 * 729 / 1032 - 66:.0f}px;font-family:'Black Han Sans',sans-serif;font-size:42px;color:#C8102E;white-space:nowrap;background:#fff;border:4px solid #C8102E;border-radius:16px;padding:4px 18px}}
R .tor{{position:absolute;left:{150 + 548 * 560 / 793 - 9:.0f}px;top:{120 + 930 * 729 / 1032 - 9:.0f}px;width:18px;height:18px;border-radius:50%;background:#2B2B2B}}
R .torl{{position:absolute;left:{150 + 548 * 560 / 793 - 130:.0f}px;top:{120 + 930 * 729 / 1032 + 12:.0f}px;font-weight:700;font-size:28px}}
R .ttl{{left:820px;top:150px;font-size:76px}}
R .list{{position:absolute;left:820px;top:280px;width:980px;display:flex;flex-direction:column;gap:16px}}
R .it{{display:flex;align-items:center;gap:26px;background:#fff;border-radius:22px;padding:14px 30px;box-shadow:0 10px 24px rgba(122,27,38,.10)}}
R .it .t{{font-weight:900;font-size:38px}}
R .it .t b{{color:#C8102E}}
""",
    body=f"""
<div class="tag"><i></i>4장 · 왜 하필 몬트리올인가</div>
<div class="ph p1">
  {canada_svg("map")}
  <div class="tor"></div><div class="torl">토론토</div>
  <svg class="pin" viewBox="0 0 44 60"><path d="M22 58 C 8 38, 2 30, 2 22 A20 20 0 0 1 42 22 C 42 30, 36 38, 22 58 Z" fill="#7A1B26"/><circle cx="22" cy="22" r="8" fill="#fff"/></svg>
  <div class="pinl">몬트리올</div>
  <div class="abs bhs ttl">캐나다 <span class="red">2위</span> 대도시인데</div>
  <div class="list">
    <div class="it i1"><span class="check">✓</span><span class="t">토론토 다음, <b>캐나다 두 번째 대도시</b></span></div>
    <div class="it i2"><span class="check">✓</span><span class="t">자녀 동반 시 <b>가장 저렴하게</b> 갈 수 있는 도시</span></div>
    <div class="it i3"><span class="check">✓</span><span class="t">부모 학비 <b>연 1,200만원</b> 정도</span></div>
    <div class="it i4"><span class="check">✓</span><span class="t">렌트비는 <b>중소도시 수준</b></span></div>
    <div class="it i5"><span class="check">✓</span><span class="t">지하철·버스로 <b>차 없이</b> 생활</span></div>
  </div>
</div>
""",
    js="""
inn('.tag',0.2,{x:-30,y:0});tl.fromTo(qa('.pv'),{opacity:0},{opacity:1,duration:0.8,stagger:0.03,ease:'power2.out'},0.2);
pop('.tor,.torl',T('토론토'),0.1);tl.fromTo(q('.pin'),{opacity:0,y:-80},{opacity:1,y:0,duration:0.6,ease:'bounce.out'},T('두 번째'));inn('.pinl',T('두 번째')+0.3,{x:-20,y:0});
kin('.ttl',T('두 번째')+0.2);inn('.i1',T('대도시입니다'),{x:60,y:0});
inn('.i2',T('가장 저렴하게'),{x:60,y:0});inn('.i3',T('1년에 1,200'),{x:60,y:0});pulse('.i3 .t b',T('1년에 1,200')+0.6);
inn('.i4',T('렌트비는'),{x:60,y:0});inn('.i5',T('지하철과 버스'),{x:60,y:0});
pulse('.pin',T('그럼 아이는'),2);
""",
    sfx=[("pop", "T('두 번째')+0.3"), ("pop", "T('가장 저렴하게')"), ("pop", "T('1년에 1,200')"), ("pop", "T('렌트비는')"), ("pop", "T('지하철과 버스')")],
)

# ---------------------------------------------------------------- S08 유치원 건물이 없다
BUS = """<svg class="bus" viewBox="0 0 600 260"><rect x="10" y="30" width="560" height="170" rx="26" fill="#F2B705"/>
<rect x="10" y="150" width="560" height="14" fill="#2B2B2B"/><rect x="520" y="60" width="60" height="70" rx="10" fill="#2B2B2B" opacity=".85"/>
<g fill="#FFF8F2"><rect x="40" y="56" width="80" height="62" rx="8"/><rect x="140" y="56" width="80" height="62" rx="8"/><rect x="240" y="56" width="80" height="62" rx="8"/><rect x="340" y="56" width="80" height="62" rx="8"/><rect x="440" y="56" width="62" height="62" rx="8"/></g>
<text x="250" y="190" font-family="Noto Sans KR" font-weight="900" font-size="34" fill="#2B2B2B" text-anchor="middle">SCHOOL BUS</text>
<circle cx="120" cy="208" r="40" fill="#2B2B2B"/><circle cx="120" cy="208" r="16" fill="#ccc"/><circle cx="460" cy="208" r="40" fill="#2B2B2B"/><circle cx="460" cy="208" r="16" fill="#ccc"/></svg>"""

S["s08"] = dict(
    css="""
R .q1{top:240px;font-size:76px;color:#7A1B26}
R .q2{top:350px;font-size:140px}
R .school{position:absolute;left:150px;top:150px;width:900px;height:640px}
R .k1{left:1120px;top:170px;width:680px;padding:24px 40px;font-size:44px}
R .k2{left:1120px;top:355px;width:680px;padding:30px 40px;display:flex;align-items:center;gap:26px}
R .k2 .t{font-family:'Black Han Sans',sans-serif;font-size:64px}
R .clock{width:110px;height:110px}
R .k3{left:1120px;top:545px;width:680px;padding:22px 40px}
R .k3 .s{font-weight:700;font-size:34px;color:#7A1B26}
R .k3 .t{font-family:'Black Han Sans',sans-serif;font-size:70px}
R .road{position:absolute;left:0;right:0;top:640px;height:16px;background:#2B2B2B;opacity:.85}
R .bus{position:absolute;left:640px;top:400px;width:640px;height:277px}
R .sib{position:absolute;left:200px;top:458px;display:flex;align-items:flex-end;gap:24px}
R .sibl{position:absolute;font-weight:900;font-size:30px;color:#7A1B26}
R .bt{left:120px;top:150px;font-size:72px}
R .conv{left:1150px;top:250px;font-size:44px}
R .ft{top:720px;font-size:66px}
R .allday{top:300px;font-size:150px}
R .allday2{top:500px;font-size:70px;color:#7A1B26}
""",
    body=f"""
<div class="tag"><i></i>5장 · 캐나다엔 유치원 건물이 없다</div>
<div class="ph p1">
  <div class="abs center bhs q1">한국과 가장 다른 점</div>
  <div class="abs center bhs q2">유치원 '건물'이 <span class="red">없다</span></div>
</div>
<div class="ph p2" style="opacity:0">
  <svg class="school" viewBox="0 0 900 640">
    <path class="roof" d="M40 200 L450 40 L860 200 Z" fill="#7A1B26"/>
    <rect class="bld" x="80" y="200" width="740" height="420" fill="#fff" stroke="#7A1B26" stroke-width="6"/>
    <text x="450" y="160" font-family="Black Han Sans" font-size="54" fill="#fff" text-anchor="middle">초등학교</text>
    <g fill="#FFD6CF"><rect x="130" y="250" width="140" height="110" rx="10"/><rect x="380" y="250" width="140" height="110" rx="10"/><rect x="630" y="250" width="140" height="110" rx="10"/><rect x="380" y="420" width="140" height="110" rx="10"/><rect x="630" y="420" width="140" height="110" rx="10"/></g>
    <g class="kroom"><rect x="110" y="400" width="200" height="150" rx="14" fill="#C8102E"/><text x="210" y="488" font-family="Black Han Sans" font-size="42" fill="#fff" text-anchor="middle">유치원반</text></g>
    <rect x="400" y="540" width="100" height="80" fill="#7A1B26"/>
  </svg>
  <div class="card k1 hd"><div>유치원 과정은</div><div class="red">모두 초등학교 안에</div></div>
  <div class="card k2"><svg class="clock" viewBox="0 0 110 110"><circle cx="55" cy="55" r="50" fill="#FFD6CF" stroke="#C8102E" stroke-width="6"/><path class="hand" d="M55 55 L55 20" stroke="#2B2B2B" stroke-width="7" stroke-linecap="round"/><path d="M55 55 L80 62" stroke="#2B2B2B" stroke-width="7" stroke-linecap="round"/></svg><div><div class="t">하루 종일</div><div class="b" style="font-weight:700;font-size:32px">초등학생과 같은 시간표 · 풀타임</div></div></div>
  <div class="card red k3"><div class="s" style="color:#FFD6CF">입학 나이</div><div class="t">그해 9월 30일 기준</div><div class="t" style="font-size:96px">만 4세</div></div>
</div>
<div class="ph p3" style="opacity:0">
  <div class="abs bhs bt">형·누나와 <span class="red">같은 학교, 같은 스쿨버스</span></div>
  <div class="road"></div>
  {BUS}
  <div class="sib">{kid("#7A1B26", 130)}{kid("#C8102E", 92)}</div>
  <div class="sibl" style="left:210px;top:672px">형·누나</div><div class="sibl" style="left:360px;top:672px">유치원생</div>
  <div class="chip solid conv">둘째·셋째 있는 집엔 정말 편해요</div>
</div>
<div class="ph p4" style="opacity:0">
  <div class="abs center bhs allday">이 <span class="red">'하루 종일'</span>이</div>
  <div class="abs center bhs allday2">영어 실력의 큰 차이를 만듭니다</div>
</div>
""",
    js="""
inn('.tag',0.2,{x:-30,y:0});kin('.q1',0.4);slam('.q2',T('시설이 따로'));
phase('.p2',T('퀘벡은 유치원'),'.p1');inn('.school',T('퀘벡은 유치원'),{y:40});pop('.kroom',T('초등학교 안에'));pulse('.kroom',T('초등학교 안에')+0.6,2);inn('.k1',T('초등학교 안에'),{x:60,y:0});
inn('.k2',T('초등학생과 같은'),{x:60,y:0});tl.fromTo(q('.hand'),{rotation:0,svgOrigin:'55 55'},{rotation:720,svgOrigin:'55 55',duration:2.4,ease:'power2.inOut'},T('하루 종일'));
slam('.k3',T('9월 30일'));
phase('.p3',T('4학년이나'),'.p2');kin('.bt',T('4학년이나'));inn('.sib svg',T('형, 누나')-0.3,{y:30,st:0.2});inn('.sibl',T('형, 누나'),{y:10,st:0.2});
tl.fromTo(q('.bus'),{x:1400},{x:0,duration:1.6,ease:'power3.out'},T('같은 스쿨버스')-0.4);pop('.conv',T('둘째, 셋째'));
phase('.p4',T('그리고 바로'),'.p3');kin('.allday',T('그리고 바로'));kin('.allday2',T('영어 실력에서'));
""",
    sfx=[("impact", "T('시설이 따로')+0.38"), ("whoosh", "T('퀘벡은 유치원')-0.3"), ("pop", "T('초등학교 안에')"), ("impact", "T('9월 30일')+0.38"),
         ("whoosh", "T('같은 스쿨버스')-0.4"), ("pop", "T('둘째, 셋째')"), ("whoosh", "T('그리고 바로')-0.3")],
)
