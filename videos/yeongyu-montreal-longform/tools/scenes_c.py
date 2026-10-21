"""S09-S11."""
from common import adult, kid, maple

S = {}

# ---------------------------------------------------------------- S09 배우는 영어 vs 몸에 밴 영어
S["s09"] = dict(
    css="""
R .half{position:absolute;top:150px;width:800px;height:640px;border-radius:30px;overflow:hidden}
R .lft{left:120px;background:#fff;box-shadow:0 14px 30px rgba(122,27,38,.10)}
R .rgt{left:1000px;background:#C8102E;color:#fff}
R .half .h{position:absolute;left:0;right:0;top:40px;text-align:center;font-family:'Black Han Sans',sans-serif;font-size:58px}
R .half .s{position:absolute;left:0;right:0;top:120px;text-align:center;font-weight:700;font-size:32px;opacity:.8}
R .book{position:absolute;left:250px;top:230px;width:300px;height:220px}
R .lt{position:absolute;left:0;right:0;top:500px;text-align:center;font-family:'Black Han Sans',sans-serif;font-size:64px}
R .sit{position:absolute;left:40px;width:720px;height:120px;border-radius:22px;background:#fff;color:#2B2B2B;display:flex;align-items:center;gap:18px;padding:0 24px}
R .sit .w{font-weight:900;font-size:28px;width:160px;flex:none;color:#7A1B26}
R .sit .e{font-weight:900;font-size:31px;color:#C8102E;white-space:nowrap}
R .s1{top:180px}.s2{top:310px}.s3{top:440px}
R .rt{position:absolute;left:0;right:0;top:572px;text-align:center;font-family:'Black Han Sans',sans-serif;font-size:0}
R .vs{position:absolute;left:880px;top:420px;width:160px;height:160px;border-radius:50%;background:#2B2B2B;color:#fff;display:flex;align-items:center;justify-content:center;font-size:64px;z-index:5}
R .young{left:120px;top:150px;font-size:80px}
R .mt{position:absolute;left:160px;width:1600px;height:130px;display:flex;align-items:center;gap:40px}
R .mt .l{width:440px;flex:none;font-family:'Black Han Sans',sans-serif;font-size:54px;white-space:nowrap}
R .mt .bars{flex:1;display:flex;flex-direction:column;gap:14px}
R .mt .bars div{height:30px;border-radius:15px;position:relative}
R .mt .a{background:#E3D5D2}
R .mt .b{background:#C8102E}
R .m1{top:300px}.m2{top:460px}.m3{top:620px}
R .lg{position:absolute;left:1090px;top:250px;display:flex;gap:30px;font-weight:700;font-size:28px}
R .lg i{display:inline-block;width:26px;height:16px;border-radius:8px;margin-right:10px;vertical-align:middle}
R .son{left:260px;top:300px;width:1400px;height:300px;display:flex;align-items:center;gap:50px;padding:0 70px}
R .son .t{font-family:'Black Han Sans',sans-serif;font-size:66px;line-height:1.25}
R .nx{top:340px;font-size:100px}
R .nx2{top:500px;font-size:62px;color:#7A1B26}
""",
    body=f"""
<div class="tag"><i></i>6장 · 배우는 영어 vs 몸에 밴 영어</div>
<div class="ph p1">
  <div class="half lft"><div class="h">영어유치원</div><div class="s">수업 시간에 배우는 영어</div>
    <svg class="book" viewBox="0 0 300 220"><path d="M150 40 C 110 10, 40 10, 10 30 L10 200 C 40 180, 110 180, 150 210 Z" fill="#FFD6CF" stroke="#7A1B26" stroke-width="6"/><path d="M150 40 C 190 10, 260 10, 290 30 L290 200 C 260 180, 190 180, 150 210 Z" fill="#FFD6CF" stroke="#7A1B26" stroke-width="6"/><text x="80" y="120" font-family="Black Han Sans" font-size="44" fill="#7A1B26" text-anchor="middle">ABC</text></svg>
    <div class="lt">= 하나의 <span class="red">과목</span></div></div>
  <div class="half rgt"><div class="h">캐나다 영어학교</div><div class="s">필요해서 꺼내 쓰는 영어</div>
    <div class="sit s1"><span class="w">친구와 놀 때</span><span class="e">"Can I play too?"</span></div>
    <div class="sit s2"><span class="w">놀이터 순서</span><span class="e">"Is it my turn?"</span></div>
    <div class="sit s3"><span class="w">선생님께</span><span class="e">"May I go to the bathroom?"</span></div>
    <div class="rt" style="font-size:46px">외운 영어 ✕ · 생활 영어 ○</div></div>
  <div class="vs bhs">VS</div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="abs bhs young">어릴수록 차이가 <span class="red">크게</span></div>
  <div class="lg"><span><i style="background:#E3D5D2"></i>공부로 만든 영어</span><span><i style="background:#C8102E"></i>몸에 밴 영어</span></div>
  <div class="mt m1"><div class="l">발음</div><div class="bars"><div class="a" style="width:55%"></div><div class="b" style="width:92%"></div></div></div>
  <div class="mt m2"><div class="l">억양</div><div class="bars"><div class="a" style="width:50%"></div><div class="b" style="width:90%"></div></div></div>
  <div class="mt m3"><div class="l">말이 나오는 속도</div><div class="bars"><div class="a" style="width:45%"></div><div class="b" style="width:94%"></div></div></div>
</div>
<div class="ph p3" style="opacity:0">
  <div class="card son">{maple("", 150)}<div class="t"><div>원장님이 아들을 키우며</div><div class="red">가장 크게 느낀 부분</div></div></div>
</div>
<div class="ph p4" style="opacity:0">
  <div class="abs center bhs nx">학교는 꼭 <span class="red">영어학교</span>로만?</div>
  <div class="abs center bhs nx2">여기서 부모님의 선택지가 생깁니다</div>
</div>
""",
    js="""
inn('.tag',0.2,{x:-30,y:0});inn('.lft',0.4,{x:-80,y:0});inn('.rgt',0.7,{x:80,y:0});slam('.vs',T('몸에 익히는'));
inn('.book',T('수업 시간에'),{y:30});pop('.lt',T('과목이에요'));
dim('.lft',T('하지만 캐나다에서'),0.45);inn('.s1',T('친구와 놀 때'),{x:40,y:0});inn('.s2',T('놀이터에서'),{x:40,y:0});inn('.s3',T('선생님께'),{x:40,y:0});
pop('.rt',T('외워서 쓰는'));tl.to(q('.lft'),{opacity:1,duration:0.3},T('외워서 쓰는'));
phase('.p2',T('어린 나이일수록'),'.p1');kin('.young',T('어린 나이일수록'));inn('.lg',T('어린 나이일수록')+0.6,{y:10});
inn('.m1',T('발음과'),{x:-40,y:0});grow('.m1 .bars div',T('발음과')+0.2,0.9,'x');
inn('.m2',T('억양'),{x:-40,y:0});grow('.m2 .bars div',T('억양')+0.2,0.9,'x');
inn('.m3',T('말이 입에서'),{x:-40,y:0});grow('.m3 .bars div',T('말이 입에서')+0.2,0.9,'x');
phase('.p3',T('제 아들을'),'.p2');inn('.son',T('제 아들을'),{s:0.9});
phase('.p4',T('그럼 학교는'),'.p3');kin('.nx',T('그럼 학교는'));kin('.nx2',T('여기서 부모님의'));
""",
    sfx=[("impact", "T('몸에 익히는')+0.38"), ("pop", "T('친구와 놀 때')"), ("pop", "T('놀이터에서')"), ("pop", "T('선생님께')"),
         ("whoosh", "T('어린 나이일수록')-0.3"), ("whoosh", "T('제 아들을')-0.3"), ("whoosh", "T('그럼 학교는')-0.3")],
)

# ---------------------------------------------------------------- S10 영어학교? 불어학교?
S["s10"] = dict(
    css="""
R .ttl{left:120px;top:140px;font-size:80px}
R .bd{position:absolute;top:290px;width:740px;height:280px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px}
R .bd .t{font-family:'Black Han Sans',sans-serif;font-size:76px}
R .bd .s{font-weight:700;font-size:32px}
R .b1{left:160px}.b2{left:1020px}
R .elig{left:160px;top:620px;width:1600px;height:170px;display:flex;align-items:center;gap:40px;padding:0 50px}
R .elig .t{font-weight:900;font-size:44px}
R .elig .t small{display:block;font-weight:700;font-size:30px;color:#7A1B26}
R .lim{left:1300px;top:600px;font-size:58px}
R .plan{position:absolute;top:300px;width:520px;height:420px;display:flex;flex-direction:column;align-items:center;padding-top:44px;gap:20px;text-align:center}
R .plan .y{font-family:'Black Han Sans',sans-serif;font-size:64px}
R .plan .d{font-weight:900;font-size:40px;line-height:1.35}
R .plan .flags{display:flex;gap:12px}
R .plan .flags span{padding:8px 20px;border-radius:99px;background:#FFD6CF;color:#7A1B26;font-weight:900;font-size:28px}
R .pl1{left:120px}.pl2{left:700px}.pl3{left:1280px}
R .sonc{left:1280px;top:740px;font-size:32px}
R .seoul{left:120px;top:150px;font-size:76px}
R .fr{left:240px;top:330px;width:1440px;height:240px;display:flex;align-items:center;gap:40px;padding:0 60px}
R .fr .t{font-family:'Black Han Sans',sans-serif;font-size:62px}
R .fr .s{font-weight:700;font-size:32px;color:#7A1B26}
R .any{top:640px;font-size:64px}
""",
    body=f"""
<div class="tag"><i></i>7장 · 영어학교? 불어학교? 부모님이 고릅니다</div>
<div class="ph p1">
  <div class="abs bhs ttl">퀘벡 공립학교 <span class="red">교육청</span>은 두 가지</div>
  <div class="card bd b1"><div class="t">영어 교육청</div><div class="s">English School Board</div></div>
  <div class="card dark bd b2"><div class="t">불어 교육청</div><div class="s">Centre de services scolaire</div></div>
  <div class="card elig"><span class="check">✓</span><div class="t">학생비자 부모의 자녀 = 영어학교 임시 자격<small>Eligibility(일리저빌리티) · 어느 쪽이든 부모님이 선택</small></div></div>
  <div class="stamp lim">최대 3년 · 1회만</div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="abs bhs ttl">체류 기간별 <span class="red">언어 플랜</span></div>
  <div class="card plan pl1"><div class="y">1~2년</div><div class="d"><div>영어학교에서</div><div>영어 집중</div></div><div class="flags"><span>영어</span></div></div>
  <div class="card plan pl2"><div class="y">3년 이상</div><div class="d"><div>영어 + 불어</div><div>모두 하는 아이로</div></div><div class="flags"><span>영어</span><span>불어</span></div></div>
  <div class="card red plan pl3"><div class="y">장기</div><div class="d"><div>영어 · 불어</div><div>+ 독일어까지</div></div><div class="flags"><span>영어</span><span>불어</span><span>독일어</span></div></div>
  <div class="chip dark sonc">원장님 아들의 실제 이야기</div>
</div>
<div class="ph p3" style="opacity:0">
  <div class="abs bhs seoul">귀국 후 선택지도 <span class="red">넓어집니다</span></div>
  <div class="card fr">{maple("", 120)}<div><div class="t">서울프랑스학교 (서래마을)</div><div class="s">오래 지낸 가족 중 이런 학교로 보내는 경우도 많아요</div></div></div>
  <div class="abs center bhs any">영어만 원해도, 그 이상을 원해도 <span class="red">플랜은 맞춤</span></div>
</div>
""",
    js="""
inn('.tag',0.2,{x:-30,y:0});kin('.ttl',0.4);inn('.b1',T('영어 교육청'),{y:40});inn('.b2',T('불어 교육청'),{y:40});
inn('.elig',T('학생비자 부모의'),{y:40});pop('.elig .check',T('임시 자격'));pulse('.elig',T('부모님이 고르실'));
stamp('.lim',T('최대 3년'),-6);
phase('.p2',T('그래서 체류'),'.p1');kin('.p2 .ttl',T('그래서 체류'));
inn('.pl1',T('1~2년'),{y:50});inn('.pl2',T('3년 이상'),{y:50});
inn('.pl3',T('제 아들도'),{y:50});pop('.sonc',T('제 아들도')+0.4);pop('.pl3 .flags span',T('독일어까지')-0.6,0.25);
phase('.p3',T('이렇게 오래'),'.p2');kin('.seoul',T('이렇게 오래'));inn('.fr',T('서래마을'),{s:0.9});
kin('.any',T('영어만 원하셔도'));
""",
    sfx=[("pop", "T('영어 교육청')"), ("pop", "T('불어 교육청')"), ("stamp", "T('최대 3년')+0.3"), ("whoosh", "T('그래서 체류')-0.3"),
         ("pop", "T('1~2년')"), ("pop", "T('3년 이상')"), ("impact", "T('제 아들도')"), ("whoosh", "T('이렇게 오래')-0.3")],
)

# ---------------------------------------------------------------- S11 마무리
S["s11"] = dict(
    css="""
R .ttl{left:120px;top:140px;font-size:80px}
R .sum{position:absolute;left:120px;width:1680px;height:150px;display:flex;align-items:center;gap:36px;padding:0 44px}
R .sum .n{width:90px;height:90px;border-radius:50%;background:#C8102E;color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Black Han Sans',sans-serif;font-size:50px;flex:none}
R .sum .t{font-weight:900;font-size:40px;white-space:nowrap}
R .sum .t b{color:#C8102E}
R .u1{top:290px}.u2{top:470px}.u3{top:650px}
R .ab{position:absolute;top:260px;width:780px;height:420px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;text-align:center}
R .ab .k{font-family:'Black Han Sans',sans-serif;font-size:140px;line-height:1}
R .ab .t{font-weight:900;font-size:48px;line-height:1.35}
R .A{left:120px}.B{left:1020px}
R .cm{top:720px;font-size:50px;color:#7A1B26}
R .end{position:absolute;left:260px;top:170px;width:1400px;height:600px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:28px}
R .end img{width:180px;height:174px}
R .end .t{font-family:'Black Han Sans',sans-serif;font-size:70px}
R .end .row{display:flex;gap:26px}
R .end .row span{padding:16px 36px;border-radius:99px;font-weight:900;font-size:40px;background:#FFD6CF;color:#7A1B26}
R .end .row span.k{background:#C8102E;color:#fff}
R .end .s{font-weight:700;font-size:32px;color:#7A1B26}
R .nextv{left:560px;top:792px;font-size:32px}
""",
    body=f"""
<div class="tag"><i></i>마무리 · 세 줄 정리</div>
<div class="ph p1">
  <div class="abs bhs ttl">오늘 내용 <span class="red">세 줄</span> 정리</div>
  <div class="card sum u1"><span class="n">1</span><span class="t">영어유치원, 아이 둘이면 1년 <b>약 3,580만원</b></span></div>
  <div class="card sum u2"><span class="n">2</span><span class="t">몬트리올은 부모가 어학원만 다녀도 <b>아이 학비 0원</b> · 부모 학비 연 1,200만원 정도</span></div>
  <div class="card sum u3"><span class="n">3</span><span class="t">유치원부터 <b>하루 종일 영어</b>로 생활 · 학교 언어는 부모님이 선택</span></div>
</div>
<div class="ph p2" style="opacity:0">
  <div class="card dark ab A"><div class="k">A</div><div class="t"><div>한국에서</div><div>영어유치원 3년</div></div></div>
  <div class="card red ab B"><div class="k">B</div><div class="t"><div>캐나다에서</div><div>영어로 생활하는 3년</div></div></div>
  <div class="abs center bhs cm">댓글로 A 또는 B만 남겨 주세요</div>
</div>
<div class="ph p3" style="opacity:0">
  <div class="card end"><img src="@I/aa-canada-logo-transparent.png" alt="" /><div class="t">우리 집 예상 비용, 궁금하시면</div>
    <div class="row"><span class="k">카카오톡 canlog</span><span>02-567-4345</span></div>
    <div class="s">블로그 글 링크는 영상 설명란에 있어요</div></div>
  <div class="chip solid nextv">다음 영상 · 영어 노출 시간, 숫자로 계산해 봅니다</div>
</div>
""",
    js="""
inn('.tag',0.2,{x:-30,y:0});kin('.ttl',0.4);
inn('.u1',T('첫 번째'),{x:-60,y:0});inn('.u2',T('둘째'),{x:-60,y:0});inn('.u3',T('셋째'),{x:-60,y:0});
phase('.p2',T('여러분이라면'),'.p1');inn('.A',T('A, 한국에서'),{x:-80,y:0});inn('.B',T('B, 캐나다에서'),{x:80,y:0});kin('.cm',T('댓글로'));
phase('.p3',T('우리 집 예상'),'.p2');inn('.end',T('우리 집 예상'),{s:0.9});pop('.end .row span',T('canlog'),0.3);
pop('.nextv',T('다음 영상에서는'));
""",
    sfx=[("pop", "T('첫 번째')"), ("pop", "T('둘째')"), ("pop", "T('셋째')"), ("whoosh", "T('여러분이라면')-0.3"), ("impact", "T('A, 한국에서')+0.3"),
         ("impact", "T('B, 캐나다에서')+0.3"), ("whoosh", "T('우리 집 예상')-0.3"), ("pop", "T('canlog')")],
)
