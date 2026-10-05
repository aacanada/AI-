---
format: 1080x1920
duration: 68s
message: "자녀무상교육은 '공짜'가 아니라 '학비면제' — 부모 학생비자 종류와 지역에 따라 조건이 다르다"
arc: Hook → 개념 뒤집기 → 분류 → 거주자 구조 → 전환 → 3가지 유형 → 퀘벡 강조 → CTA
audience: 캐나다 자녀 동반 유학을 고민하는 한국 학부모
mode: autonomous
music: none
---

## Video direction

- **palette system** — frame.md(bold-poster): white `#FFFFFF` 기본 바탕, ink `#1C1410` 본문·선, red `#D8000F` 유일한 액센트(핵심 단어, 숫자, 진행바, 레드 패널), off-white `#F5F2EF` 보조 띠. 다섯 번째 색 없음. 캐나다 레드와 겹치는 것이 의도.
- **type** — Noto Sans KR 900(디스플레이, 기울임 −4°~−6°), 700(카드 제목), 400(보조). 영어 용어(Tuition exemption 등)는 같은 패밀리.
- **narrated short** — ElevenLabs 클론 음성(네 번째) 내레이션, 자막 트랙 없음(화면 타이포가 핵심 단어를 보여줌). 각 공개는 해당 단어 발화 시점에 맞춤. 화면 텍스트가 곧 메시지이므로, 일반 규칙의 "화면 텍스트 짧게"는 "한 번에 한 메시지, 읽을 시간 확보"로 적용. 각 텍스트 블록은 등장 후 최소 1.2초 이상 정지해 읽히게 한다.
- **motion grammar** — power3/expo.out 계열의 빠르고 단단한 진입, 바운스 없음. 각 프레임은 박자(약 0.6–1.0s 간격)에 맞춰 순차 공개, 뒤쪽 50%에도 공개가 이어진다. 홀드 중에는 정지(호흡 애니메이션 금지).
- **rhythm** — Frame 5("3가지")는 짧은 브레이크/전환 박자, Frame 7(퀘벡)은 클라이맥스 후 홀드.
- **chrome** — 매 프레임 하단 레드 진행바(0.83 높이 위, 프레임 번호에 비례) + 상단 작은 라벨 "AA CANADA · 자녀무상교육".
- **negative list** — 원본 docx 이미지 사용 금지, 스톡 사진·이모지·그라디언트·둥근 카드·박스섀도 금지. 슬라이드쇼(앞에서 다 보여주고 멈춤) 금지, 스크린세이버(제각각 둥둥 떠다님) 금지.

## Frame 1 — Hook

- scene: "캐나다 / 자녀무상교육 조건," 위로 거대한 레드 기울임 "지역별 차이" + "알고 가시나요?"
- voiceover: "캐나다 자녀무상교육 조건, 지역별 차이 알고 가시나요?"
- duration: 4.46s
- poster: 3s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- blueprint: compose
- focal: "공짜일까?" 레드 hero-title-red(−5°)
- roles: 상단 라벨(supporting), "캐나다" "자녀무상교육" ink 스택(foreground), 레드 물음표 대형(foreground), 흰 바탕(background)

Scene 1 (0.0–1.0s): 상단 라벨 + "캐나다" → "자녀무상교육" 두 줄이 아래에서 빠르게 슬라이드 업(kinetic type, 줄별 stagger). hero stack 중앙 상단 0.25h. → Scene 2 (1.0–2.2s): "진짜" 작게 → "공짜일까?" 레드 대형이 −5° 기울어 스케일 펀치인(1.3→1). → Scene 3 (2.2–4.0s): 레드 밑줄 바가 왼→오 그려짐, 하단에 "1분 정리" 작은 태그 등장 후 홀드.

## Frame 2 — 공짜가 아니라 학비면제

- scene: "Free education"에 취소선 → "Tuition exemption = 학비면제"
- voiceover: "흔히 무상교육이라고 부르지만, 정확한 개념은 학비면제, 튜이션 익젬션입니다."
- duration: 7.1s
- poster: 5s
- transition_in: cut
- status: animated
- src: compositions/frames/02-concept.html
- blueprint: compose
- focal: "학비면제" 레드 대형 단어
- roles: "Free education / 무상교육" 회색 취소(foreground), "Tuition exemption / 학비면제"(foreground focal), 정확한 개념 라벨(supporting)

Scene 1 (0.0–1.4s): 라벨 "정확한 개념은?" + "Free education" "(무상교육)" ink 등장. → Scene 2 (1.4–2.4s): 레드 취소선이 단어 위로 그어지고 텍스트 30% 디밍. → Scene 3 (2.4–4.2s): 아래쪽에 "Tuition exemption" 슬라이드 업, 이어서 "학비면제" 레드 대형 −4° 펀치인. → Scene 4 (4.2–6.0s): 보조 한 줄 "학비를 '면제'받는 제도" 페이드 업, 홀드.

## Frame 3 — 교육청의 두 가지 분류

- scene: 학생을 두 갈래로 나누는 분기 다이어그램 — International students(학비 납부) vs Residents(학비 면제)
- voiceover: "교육청은 학생을 두 가지로 나눕니다. 학비를 내는 국제학생, 그리고 학비가 면제되는 거주자죠."
- duration: 7.1s
- poster: 5s
- transition_in: cut
- status: animated
- src: compositions/frames/03-split.html
- blueprint: compose
- focal: 두 갈래 분기 다이어그램
- roles: 상단 "교육청은 학생을 이렇게 나눠요" 헤더(supporting), 분기 선(supporting), 왼쪽 카드 International students / 학비 납부 ₩(foreground), 오른쪽 카드 Residents / 학비 면제 0(foreground, 레드)

Scene 1 (0.0–1.2s): 헤더 등장, 중앙 노드 "학생" 박스 팝. → Scene 2 (1.2–2.4s): 노드에서 두 갈래 선이 아래로 그려짐(draw). → Scene 3 (2.4–3.8s): 왼쪽 카드 "International students" + "국제학생" + "학비 납부" (ink 테두리) 등장. → Scene 4 (3.8–6.0s): 오른쪽 카드 "Residents" + "거주자" + "학비 면제" (레드 패널, 흰 글씨) 등장, 레드 카드가 살짝 스케일 1.04로 강조 후 홀드.

## Frame 4 — 학생비자 부모의 자녀 = Resident

- scene: Residents 아래 두 가지(영구거주자 / 임시거주자) 트리, Study permit이 강조되며 "동반자녀 학비 0"
- voiceover: "거주자에는 시민권자, 영주권자 같은 영구거주자와, 부모가 워크퍼밋이나 스터디퍼밋을 가진 임시거주자가 있어요. 그래서 부모가 학생비자를 받으면, 동반 자녀도 거주자로 학비가 면제됩니다."
- duration: 14.44s
- poster: 6s
- transition_in: cut
- status: animated
- src: compositions/frames/04-resident.html
- blueprint: compose
- focal: "Study permit" 하이라이트 → "동반자녀 = Resident"
- roles: "Residents 거주자" 상단 헤더 레드(foreground), 왼쪽 red-leftbar 카드 "영구거주자 — 시민권자·영주권자"(supporting), 오른쪽 카드 "임시거주자 — 부모 Work permit / Study permit"(foreground), 결과 배너(foreground)

Scene 1 (0.0–1.2s): "Residents (거주자)" 헤더 슬라이드. → Scene 2 (1.2–2.4s): 영구거주자 카드(시민권자 · 영주권자) 레드 레프트바와 함께 등장. → Scene 3 (2.4–3.8s): 임시거주자 카드 등장, 내부 "Work permit" "Study permit" 두 칩. → Scene 4 (3.8–5.0s): "Study permit" 칩이 레드로 반전 + 마커 하이라이트. → Scene 5 (5.0–7.0s): 하단 레드 배너 "부모 학생비자 → 동반자녀 학비면제" 와이프 인, 홀드.

## Frame 5 — 그런데, 조건은 3가지

- scene: 레드 풀 패널 위 거대한 흰색 "3" (−6°) + "공부 종류에 따라 조건이 달라요"
- voiceover: "단, 부모가 어떤 공부를 하느냐에 따라, 지역별 조건이 세 가지로 갈립니다."
- duration: 5.75s
- poster: 3s
- transition_in: cut
- status: animated
- src: compositions/frames/05-three.html
- blueprint: compose
- focal: stat-big "3" 흰색 + stacked shadow
- roles: 레드 풀 패널(background), "3가지" stat(foreground), 위 라벨 "단," / 아래 서브(supporting)

Scene 1 (0.0–0.8s): 라벨 "단, 부모가 어떤 공부를 하느냐에 따라" 등장. → Scene 2 (0.8–2.0s): 흰 "3" 스케일 펀치인(−6°) + "가지" → Scene 3 (2.0–4.0s): 서브 "지역별 학비면제 조건이 달라요" 페이드 업, 홀드.

## Frame 6 — 학생비자 3가지 유형

- scene: 더블 보더 그리드 3행 — 01 정규과정 / 02 조건부입학 영어과정 / 03 사설어학원, 각 행 오른쪽에 적용 지역
- voiceover: "첫째, 컬리지나 대학 학위과정 같은 정규과정은 캐나다 모든 지역에서 인정돼요. 둘째, 정규과정 입학을 위한 조건부 영어과정은 온타리오와 매니토바 일부에서 인정됩니다. 셋째, 사설어학원은 퀘벡과 노바스코샤에서 인정돼요."
- duration: 15.79s
- poster: 9s
- transition_in: cut
- status: animated
- src: compositions/frames/06-grid.html
- blueprint: compose
- focal: fin-grid 3행
- roles: 헤더(supporting), 행 1/2/3(foreground), 레드 숫자(supporting accent)

Scene 1 (0.0–1.0s): 헤더 "학생비자, 무슨 공부?" + 그리드 외곽선 그려짐. → Scene 2 (1.0–3.6s): 01 행 — "정규과정" "컬리지·대학 학위과정" → 지역 "캐나다 전 지역 ✓" (AB·SK·NB는 정규과정만). → Scene 3 (3.6–6.2s): 02 행 — "조건부입학 영어과정" "정규과정 입학 조건의 어학" → "온타리오 · 매니토바 일부" (+BC 일부 사설도 최대 1년). → Scene 4 (6.2–10.0s): 03 행 — "사설어학원" "목적 상관없이 학생비자만 있으면" → "퀘벡 · 노바스코샤" 레드 강조 박스가 스탬프처럼 찍힘, 홀드.

## Frame 7 — 몬트리올이 있는 퀘벡

- scene: 레드 패널, "사설어학원 학생비자만 있어도" → "퀘벡·노바스코샤" → "조건 없이 무상교육" + MONTRÉAL 태그
- voiceover: "즉, 몬트리올이 있는 퀘벡에서는 사설어학원 학생비자만 있어도, 조건 없이 자녀 무상교육이 가능합니다."
- duration: 7.47s
- poster: 4s
- transition_in: cut
- status: animated
- src: compositions/frames/07-quebec.html
- blueprint: compose
- focal: "조건 없이" 흰색 대형 −5°
- roles: 레드 풀 패널(background), "퀘벡 · 노바스코샤"(foreground), "조건 없이 무상교육"(focal), 작은 태그 "몬트리올 MONTRÉAL"(supporting)

Scene 1 (0.0–1.0s): 상단 "사설어학원 학생비자만 있어도" 등장. → Scene 2 (1.0–2.2s): "퀘벡 · 노바스코샤" 흰 박스 와이프. → Scene 3 (2.2–3.4s): "조건 없이" 대형 펀치인 + "무상교육". → Scene 4 (3.4–5.0s): 하단 "몬트리올 MONTRÉAL" 핀 태그 팝, 홀드(클라이맥스).

## Frame 8 — AA Canada CTA

- scene: 흰 바탕, "우리 아이에게 맞는 지역은?" + 레드 −5° "AA Canada" + "캐나다 전문 유학원 · 무료 상담"
- voiceover: "우리 아이에게 맞는 지역, 캐나다 전문 유학원 에이에이 캐나다와 상담해 보세요."
- duration: 6.18s
- poster: 3.5s
- transition_in: cut
- status: animated
- src: compositions/frames/08-cta.html
- blueprint: compose
- focal: "AA Canada" close-big 레드 −5°
- roles: 질문 헤더(foreground), AA Canada 워드마크 타이포(focal), 서브 + 키워드 칩 "자녀무상교육 · 유학후이민 · 영주권"(supporting)

Scene 1 (0.0–1.0s): "우리 아이에게 맞는 지역은?" 등장. → Scene 2 (1.0–2.0s): "AA Canada" 대형 레드 −5° 펀치인. → Scene 3 (2.0–3.2s): "캐나다 전문 유학원" + 세 칩 stagger. → Scene 4 (3.2–4.0s): 진행바 100% 채움 + 최종 프레임이므로 조용한 settle.
