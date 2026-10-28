# Writes upload-text.txt + meta.txt into publish-staging/<folder>/ (run after finish.py for final.json)
import json, sys

ROOT = '/home/user/AI-'
S = ROOT + '/plans/vancouver-esl-free-edu/shorts'
LONG = 'https://youtu.be/a6GSAfwZMjo'
CONTACT = '📞 AA Canada 무료 상담: 카카오톡 canlog · 02-567-4345\n🌐 www.aacanada.co.kr'
SRC_BC = 'BC 교육부 「Eligibility of Students for Operating Grant Funding」 (2011 시행, 2013 개정, Status: Current), 2026-10-27 확인'
SRC_VSB = '밴쿠버 교육청(VSB) Newcomer Welcome Centre FAQ, 2026-10-27 확인'
SRC_FEE = 'VSB 국제교육부 국제학생 학비 페이지 (2027-28학년도: CAD 17,000 + 의료보험 CAD 1,400), 2026-10-27 확인'
SRC_AC = '알렉산더 컬리지 한국 담당자 안내 메일 (2026-10-24, 10-27)'
TAGS = '#밴쿠버자녀무상교육 #자녀무상교육 #밴쿠버 #캐나다조기유학 #부모동반유학 #AACanada'

SH = {
 'a': dict(folder='2026-10-29-vancouver-esl-short-a', order=1, date='2026-10-29',
   title='영어 점수 없어도 밴쿠버 자녀무상?',
   summary='영어 점수가 없어도, 사설 어학원 어학연수로 시작해서 최대 1년까지 아이 학비 면제를 받을 수 있는 길이 있습니다. BC주 교육부 규정: 1년 이상 학업이 허가된 부모가 ① EQA 인증 기관에서 최대 1년 영어 과정 ② 학위 과정 입학허가 ③ 영어 과정 수료 조건부 입학, 세 가지를 모두 충족하면 어학연수 기간에도 최대 1년까지 거주자로 봅니다.',
   clip='영어 점수 없어도 밴쿠버 자녀무상? BC주 규정: EQA 인증 기관 영어 과정(최대 1년) + 학위 과정 조건부 입학이면 어학연수 중에도 최대 1년 거주자 인정. 최종 판단은 교육청.',
   srcs=[SRC_BC], src_note='세 가지 조건·최대 1년: BC 교육부 규정 원문'),
 'b': dict(folder='2026-10-31-vancouver-esl-short-b', order=2, date='2026-10-31',
   title='밴쿠버 자녀무상교육, 사립 컬리지는 학위만',
   summary='부모가 학생일 때 기본 조건은 두 가지: 1년 이상 학업이 허가된 학생비자, 그리고 BC주 공립 대학·컬리지의 학위·디플로마 과정 또는 사립이라면 학위 과정. 사립 컬리지의 디플로마나 수료증 과정은 해당이 안 됩니다. 그래서 사립 컬리지의 준학사(Associate Degree)를 주목합니다.',
   clip='밴쿠버 자녀무상교육, 부모가 학생이면 학생비자 1년 이상 + 공립은 학위·디플로마, 사립은 학위 과정만. 사립 디플로마·수료증은 해당 안 됨. 그래서 준학사(Associate Degree).',
   srcs=[SRC_BC], src_note='기본 조건(사립은 학위): BC 교육부 규정 원문'),
 'c': dict(folder='2026-11-02-vancouver-esl-short-c', order=3, date='2026-11-02',
   title='밴쿠버 자녀무상교육 플랜 A vs B',
   summary='플랜 A: 영어 점수가 있다면 듀오링고 90이나 아이엘츠 5.0부터 알렉산더 준학사로 바로 입학, 처음부터 자녀 학비 면제 조건. 플랜 B: 영어 점수가 없다면 알렉산더 조건부 입학허가를 받고 협약 어학원에서 어학연수로 시작, 최대 1년 동안 자녀 무상교육, 그다음 준학사로 올라가서 계속 무상교육. 참고: 밴쿠버 교육청 국제학생 학비 2027-28학년도 기준 1년 CAD 17,000 + 의료보험 CAD 1,400.',
   clip='밴쿠버 자녀무상교육 플랜 A: 듀오링고 90·아이엘츠 5.0부터 알렉산더 준학사 바로 입학. 플랜 B: 조건부 입학허가 + 어학연수 최대 1년 후 준학사. 국제학생 학비 CAD 17,000+의료보험 1,400(2027-28).',
   srcs=[SRC_AC, SRC_FEE, SRC_BC], src_note='영어 점수 기준·조건부 입학: 알렉산더 컬리지 안내 메일 / 학비·의료보험: VSB 국제교육부 2027-28'),
 'd': dict(folder='2026-11-04-vancouver-esl-short-d', order=4, date='2026-11-04',
   title='밴쿠버 자녀무상교육 신청 전 확인 3가지',
   summary='첫째, 부모 학생비자가 1년 이상이어야 합니다. 둘째, 어학연수만 따로 하는 건 안 되고 반드시 학위 과정 조건부 입학이 붙어 있어야 해요. 어학연수가 1년을 넘으면 국제학생 학비 대상이 될 수 있습니다. 셋째, 최종 판단은 교육청이 합니다. 등록 서류를 처음부터 제대로 준비하는 게 중요합니다.',
   clip='밴쿠버 자녀무상교육 신청 전 3가지: ① 부모 학생비자 1년 이상 ② 어학연수만 단독 불가, 학위 과정 조건부 입학 필수(1년 초과 시 국제학생 학비 가능) ③ 최종 판단은 교육청.',
   srcs=[SRC_BC, SRC_VSB], src_note='세 가지 확인 사항: BC 교육부 규정 원문 + VSB FAQ'),
}

for sid in sys.argv[1:]:
    d = SH[sid]
    f = json.load(open(f'{S}/{sid}/final.json'))
    out = f"{ROOT}/publish-staging/{d['folder']}"
    clip = d['clip'] + ' ' + TAGS
    assert len(clip) <= 300, (sid, len(clip))
    m, s = divmod(round(f['duration']), 60)
    txt = f"""[유튜브 제목]
{d['title']} #shorts

[유튜브 설명]
{d['summary']}

▶ 본편(규정 원문 화면으로 확인): {LONG}

📌 출처·기준일 (2026-10-27 확인)
""" + '\n'.join('- ' + x for x in d['srcs']) + f"""
※ 최종 적용 여부는 거주지 교육청이 결정합니다.
🎙 AI 음성(ElevenLabs) 사용
{CONTACT}

{TAGS} #shorts

[인스타 캡션]
{d['title']}

{d['summary']}

▶ 본편: 유튜브 'AA Canada' 채널 ({LONG})
📞 무료 상담: 카카오톡 canlog · 02-567-4345
(출처: BC 교육부 규정·VSB 자료 등, 2026-10-27 확인 · 최종 판단은 교육청)

{TAGS} #캐나다유학

[클립 설명]
{clip}

[출처·기준일] (숫자별, 게시 루틴 확인용)
- {d['src_note']} (2026-10-27 확인)
""" + '\n'.join('- ' + x for x in d['srcs']) + '\n'
    open(out + '/upload-text.txt', 'w', encoding='utf-8').write(txt)
    meta = f"""type: short
title: {d['title']}
channels: youtube_shorts, reels, threads, clip, blog, homepage
visibility: public
publish_order: {d['order']}
publish_after: {d['date']}
linked_to: 2026-10-28-vancouver-esl-longform
files: video.mp4 (1080x1920, {m}:{s:02d}, {f['size_mb']} MB), video.mp4.sha256, thumbnail.jpg (1080x1920 cover), upload-text.txt
voice: 여덟번째 cbVXtFGe9VfUKWtbYIty eleven_multilingual_v2
loudness: {f['lufs']} LUFS, true peak {f['peak']} dBFS
source: aacanada/AI- branch claude/beautiful-ptolemy-4l997y, plans/vancouver-esl-free-edu/shorts/ (본편 https://youtu.be/a6GSAfwZMjo)
notes: 밴쿠버 자녀무상교육 숏폼({sid}). 블로그는 기존 글 https://blog.naver.com/allthatcan/224455993779 수정해 링크 추가, 홈페이지는 ab-1704-11 수정해 링크 추가(새 글 금지). 쇼츠 '관련 동영상'에 본편(https://youtu.be/a6GSAfwZMjo) 연결. 숫자별 출처·기준일은 upload-text.txt [출처·기준일].
"""
    open(out + '/meta.txt', 'w', encoding='utf-8').write(meta)
    print(sid, 'texts ok; clip len', len(clip))
