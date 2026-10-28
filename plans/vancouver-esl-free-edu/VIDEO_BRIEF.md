# 밴쿠버 자녀무상교육: 영어 점수 없어도 어학연수 1년 무상? (BC주 규정 원문 확인) — 롱폼 브리프

작성: Aside, 2026-10-27 (KST). 대표님 승인 대본: `NARRATION.txt` (s01~s09, 6번 장면은 대표님 수정본).

## 목표
- 16:9 롱폼 1편, 1920x1080, 30fps. 예상 길이 약 5분 30초 (TTS 길이에 맞춤).
- 얼굴 없음. 목소리 + HyperFrames 그래픽.
- 이번 단계는 **대표님 미리보기용 렌더까지만**. publish 브랜치, READY, 업로드는 하지 않는다. 쇼츠는 대표님이 미리보기를 승인한 뒤에 만든다(후보는 아래).

## 음성 (ElevenLabs)
- 목소리: ElevenLabs 계정의 **"여덟번째"** 목소리 (대표님 최종 버전, 앞으로 기본). voice_id는 API `GET /v1/voices`에서 이름으로 찾는다. 못 찾으면 멈추고 보고.
- 모델: **`eleven_v4`** (대표님 지정). v4는 Stability/Similarity만 쓰고 Style/Speed/SSML 없음. 시작값 Stability 0.5, Similarity 0.75 정도에서 시작해 자연스러운 쪽으로.
- `NARRATION.txt`의 [s01]~[s09] 블록을 장면별 파일로 생성: `audio/vanesl_s01.mp3` ~ `vanesl_s09.mp3`. 대본 문구를 바꾸지 말 것.
- 생성 후 ASR이나 귀로 확인: 숫자(5,000달러, 17,000달러, 1,400달러, 2027-28, 2011년, 2013년, 듀오링고 90, 아이엘츠 5.0), 영문 약어(EQA, BC), 학교 이름(아이엘에스씨, 캐플란, 에스지아이씨, 옥스퍼드 인터내셔널, 밴웨스트, 씨씨이엘, 브이지씨)을 제대로 읽는지. 틀리면 그 장면만 다시 생성.
- 최종 믹스 -16 LUFS (지난번 -13.3이 나와 다시 맞춘 적 있음). BGM은 기존 롱폼(Vernon/SGA/영유) BGM 재사용, 내레이션 아래로 낮게.

## 브랜드
- 색: 메이플 레드 #C8102E, 크림 배경 #FFF8F2, 진한 글자 #2B2B2B, 강조 띠 #FFD6CF, 보조 #7A1B26. 파랑·하늘색 금지(경쟁사 색).
- 글꼴: Black Han Sans(큰 제목), Noto Sans KR 700/900(나머지).
- 로고: `assets/aa-canada-logo-transparent.png`. 마지막 장면과 화면 구석에 작게.
- 하단 한국어 자막: 대본 문장 그대로(철자는 대본 기준).

## 에셋 (`assets/`)
- `cap_bc_title.png` — BC 교육부 규정 페이지 제목, 시행·개정일, Status: Current
- `cap_bc_clause.png` — 규정 조항 캡처. 초록 박스 = 기본 조건(사립은 학위), 빨간 박스 3개 = ESL 조건부 입학 조항
- `cap_vsb_ell.png` — 밴쿠버 교육청(VSB) FAQ의 ELL 부모 질문과 세 조건
- `card_thumb.png`, `card_c1.png`(사립 컬리지는 학위 과정만), `card_c2.png`(어학연수 기간도 최대 1년 인정), `card_table.png`(추천 플랜 2가지), `card_c3.png`(비자 1년 이상, 판단은 교육청) — 블로그 카드
- 캡처 화면에는 출처 자막을 작게: "출처: BC Ministry of Education and Child Care, Eligibility of Students for Operating Grant Funding (2026.10.27 확인)", "출처: Vancouver School Board, Newcomer Welcome Centre FAQ (2026.10.27 확인)"

## 장면별 연출 (HyperFrames 적극 활용: 셰이더 전환, 키네틱 타이포, 숫자 슬램, 캡처 위 하이라이트 애니메이션)
- s01 오프닝: 큰 글자 "영어 점수 없어도?" → "어학연수 1년 무상" 숫자 슬램. BC 정부 문서(cap_bc_title)가 날아와 박히는 효과.
- s02 원리: 아이콘 2줄(시민권·영주권 / 학생비자·취업비자 부모) → "거주자" 도장. cap_bc_title을 천천히 줌, "Revised March 18, 2013 / Status: Current"에 밑줄.
- s03 기본 조건: cap_bc_clause의 초록 박스 확대. 체크리스트 2줄. "사립 = 학위" 도장, "디플로마·수료증 ✕". card_c1.
- s04 핵심(가장 공들일 장면): cap_bc_clause의 빨간 박스 3개를 문장에 맞춰 하나씩 하이라이트, 화면에 ①②③ 카운트. "최대 1년" 강조. "대학 부설 제한 없음 → EQA 지정 기관" 대비. card_c2.
- s05 VSB: cap_vsb_ell, 질문 문장 하이라이트 → 세 조건 → "beyond one year … international student fees" 부분 빨간 밑줄.
- s06 알렉산더 조건부 오퍼: 흐름도 "디포짓 CAD 5,000 → 조건부 입학허가 → 협약 어학원 ESL(최대 1년) → 알렉산더 준학사". 어학원은 로고 말고 글자 카드: 지금 가능 4곳(ILSC, Kaplan, SGIC, Oxford International) + "곧 가능" 3곳(VanWest, CCEL, VGC). 마지막에 "모두 BC EQA 지정 기관" 체크 표시.
- s07 추천 플랜: 두 갈래 타임라인. 플랜 A(Duolingo 90 / IELTS 5.0 → 준학사 바로) / 플랜 B(어학연수 최대 1년 → 준학사), 아래에 "자녀 공립학교 학비 면제 대상" 바. VSB 국제학생 학비 CAD 17,000 + 의료보험 1,400 카운트업(작게 "2027-28학년도, VSB 국제교육부"). card_table.
- s08 체크 3가지: 체크리스트가 하나씩 등장, 3번에 "최종 판단 = 교육청" 도장. card_c3.
- s09 클로징: "블로그·홈페이지에 규정 원문 링크", 카카오톡 canlog, 02-567-4345, 로고.
- 화면 하단 상시 각주(s04~s08): "최종 적용 여부는 거주지 교육청이 결정합니다".

## 사실 규칙 (지킬 것)
- 대본에 없는 숫자·주장 추가 금지. "무조건", "100%", "최고" 금지.
- 사실 근거(2026-10-27 Aside 확인): BC 교육부 규정 원문, VSB FAQ, BC EQA 지정 기관 명단(Report Date 2026-10-27: ILSC-Vancouver, Kaplan International Languages, OIEG Oxford International, St. George International College(SGIC), VanWest College (Vancouver), Canadian College of English Language(CCEL), VGC International College, Alexander College 모두 등재), 알렉산더 컬리지 한국 담당자 안내 메일(2026-10-24, 10-27), VSB 국제학생 학비 페이지(2027-28: CAD 17,000 + 의료보험 1,400). "곧 밴웨스트·CCEL·VGC 가능"은 대표님 확인 내용.

## 산출물
- `renders/video.mp4` (미리보기용), `renders/thumbnail.jpg` (1280x720, 큰 글자 "밴쿠버 자녀무상교육" + "영어 점수 없어도 어학연수 1년?", 메이플 레드 템플릿, 파랑 금지).
- 장면 시작 시각 목록(유튜브 챕터용).
- 영상 파일은 세션 채팅 첨부(약 28MB 단위로 나눠서)와 작업 브랜치 둘 다.
- 숏폼 후보(승인 후 제작): ① s01 앞부분+s04 "영어 점수 없어도 밴쿠버 자녀무상?" ② s03 "사립 컬리지는 학위만" ③ s07 "플랜 A vs B" ④ s08 "신청 전 확인 3가지".
- 보고는 한국어로.
