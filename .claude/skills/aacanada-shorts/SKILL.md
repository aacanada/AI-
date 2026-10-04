---
name: aacanada-shorts
description: AA Canada 쇼츠(9:16 세로) 교육용 영상 제작. 사용자가 준 내용(유학·이민·자녀무상교육 안내 원고, 메모, 핵심 포인트)으로 일레븐랩스 "네 번째" 클론 목소리 내레이션(약간 빠른 템포)을 만들고, HyperFrames로 고급스러운 색감(미드나잇 네이비 + 샴페인 골드 + 아이보리)의 교육용 쇼츠 MP4를 렌더링한다. 사용자가 캡처해서 첨부한 이미지(학교 홈페이지, 학비표, 정부 공지, 상담 카톡, 서류 등)는 영상 장면에 직접 넣는다(정보 카드 + 스포트라이트/줌/스크롤, 개인정보 모자이크). "쇼츠 만들어줘", "릴스/틱톡 영상", "이 내용으로 영상", "숏폼", "유튜브 쇼츠", "네 번째 목소리", "일레븐랩스로 음성 만들어서 영상" 같은 요청이면 영상 길이나 주제가 달라도 반드시 이 스킬을 쓸 것. Use for any AA Canada short-form vertical video request built from pasted text, with ElevenLabs voice + HyperFrames.
---

# AA Canada 교육용 쇼츠 제작

사용자가 붙여넣은 원고/메모 → **9:16 쇼츠 MP4** (1080×1920, 보통 45–90초).

고정 스펙 (사용자가 따로 말하지 않으면 그대로):

| 항목 | 값 |
| --- | --- |
| 목소리 | 일레븐랩스 클론 **"네 번째"** (이름으로 조회, 없으면 `$ELEVENLABS_VOICE_ID`) |
| 템포 | `speed: 1.12` (약간 빠르게, 일레븐랩스 최대 1.2) · 모델 `eleven_multilingual_v2` |
| 톤 | 교육용 — 레슨 카운터(01/09), 키커("POINT · 학비"), 카드/표/로드맵으로 구조화 |
| 색감 | 고급 — 미드나잇 네이비 `#070a12`, 샴페인 골드 `#c9a96e`/`#e6cf9f`, 아이보리 `#f4efe6`, 와인 포인트 `#c95a55` |
| 폰트 | 한글 Pretendard, 숫자·영문 워드마크 Playfair Display |
| 음악 | 일레븐랩스 Music 인스트루멘털(피아노+스트링), 볼륨 0.12 |
| 자막 | 문장 단위 캡션, 음성 글자 타이밍에 동기화 |
| 첨부 이미지 | **반드시 영상에 직접 사용** — 해당 내용을 말하는 장면의 주인공으로 (§ 1.5) |

HyperFrames 규칙은 `/hyperframes-core`가 기준이다. 이 스킬은 그 계약을 지키는 완성된 템플릿과 스크립트를 제공하므로, 처음부터 컴포지션을 설계하지 말고 템플릿을 고쳐서 쓴다. 질문 없이 바로 진행하되(사용자는 내용만 주고 결과를 원한다), 원문이 모호하거나 사실관계가 불확실한 곳만 마지막 보고에 적는다.

## 0. 준비

```bash
SKILL=<this skill dir>            # 예: .claude/skills/aacanada-shorts
P=videos/<kebab-case-topic>       # 예: videos/montreal-free-education-premium
bash $SKILL/scripts/setup_project.sh $P
```

`hyperframes init` + 폰트(Pretendard, Playfair) + 로컬 GSAP + 템플릿(`src/index.template.txt`) + `scenes.json` 예시 + 스크립트를 복사한다. CDN은 렌더 브라우저에서 막히므로 폰트/GSAP는 항상 로컬 파일을 쓴다. `ELEVENLABS_API_KEY`가 없으면 멈추고 사용자에게 알린다.

## 1. 원고 → `scenes.json`

`references/script-writing.md`를 읽고 작성한다. 핵심:

- 6–10개 장면. 교육용 흐름: **질문/오해(훅) → 정답 → 포인트들(장점·조건·숫자) → 장기 플랜/로드맵 → CTA**. 원문 순서를 그대로 따를 필요는 없다.
- `tts`는 **귀로 듣는 문장**: 숫자·단위·약어를 한글로 풀어 쓴다 (`$17,075` → "만 칠천칠십오 달러", `LMIA` → "엘엠아이에이", `AA Canada` → "에이에이 캐나다", `09:00` → "오전 아홉 시").
- `captions`는 `[화면 표시 문구, tts 안의 앵커 문자열]`. 표시는 숫자/영문 그대로, 앵커는 tts에 실제로 있는 문자열이어야 한다. 앵커가 그 자막의 시작 시점이 된다.
- 애니메이션 타이밍에 쓸 추가 앵커는 `cues`에.
- 오타·맞춤법은 조용히 고치되(예: "서설어학원"→"사설어학원") 의미가 바뀌는 수정은 보고한다.

## 1.5 첨부 이미지(캡처) — 있으면 반드시 직접 사용

사용자가 이미지를 첨부했다면 그 이미지는 장식이 아니라 **증거 자료**다. 모든 첨부 이미지를 최소 한 번씩, 그 내용을 내레이션이 말하는 장면의 중심에 넣는다. 이미지를 빼거나 비슷하게 다시 그리지 않는다.

**1) 파일 찾기.** 메시지에 적힌 경로 → `/mnt/user-data/uploads/` → 저장소에 올린 파일(예: `videos/<project>/inputs/`) 순서로 찾는다. 채팅 화면에서 이미지가 보이기만 하고 디스크에 파일이 없으면 픽셀을 꺼낼 수 없으므로, 사용자에게 파일로 업로드(또는 저장소 `inputs/`에 추가)해 달라고 한 번만 요청하고 나머지 작업은 계속한다.

**2) 가져오기 + 개인정보 처리.**
```bash
cd $P && python3 prep_images.py <파일들 또는 폴더> \
   [--crop "img-01:0,0,100,72"]  [--redact "img-01:2,89,60,7"]
```
- 순서대로 `public/images/img-01.jpg …`, `images.json`(크기·비율·kind: wide/square/tall/xtall) 생성.
- **각 이미지를 Read로 직접 보고** 무엇이 찍혔는지, 어느 부분을 강조할지 정한다.
- 고객 이름, 여권·비자·UCI 번호, 이메일, 전화번호, 주소, 일반인 얼굴, 카톡 프로필은 `--redact`(이미지 대비 % 좌표)로 모자이크한다. 처리 후 다시 Read로 확인하고, 무엇을 가렸는지 최종 보고에 적는다.
- 빈 여백·상태바는 `--crop`으로 잘라낸다(redact 좌표는 자른 뒤 이미지 기준).

**3) 장면 배치** (`templates/image-scenes.example.txt`에 검증된 예시):

| 이미지 종류 | 컴포넌트 | 모션 |
| --- | --- | --- |
| wide (웹페이지, 표, 공지) | `.shot` 카드(폭 940) + 위 `.shot-tag`/`.title`, 아래 `.shot-cap` | `shotIn` → 말하는 시점에 `spot`(스포트라이트 박스). 작은 영역이면 `focusShot`으로 확대 |
| tall/xtall (휴대폰 캡처, 긴 페이지) | `.shot.phone`(휴대폰 프레임) 또는 `.shot.window` | `shotIn` → `scrollShot`으로 위→아래 천천히, 필요하면 `focusShot` |
| square / 서류 | `.shot` 카드 또는 `.shot.window` | `spot` / `focusShot` |

- 강조 위치는 이미지 대비 % 좌표 `{x, y, w, h}`. 같은 값을 `.hl-box`의 `left/top/width/height`와 `focusShot`에 쓴다.
- 이미지 장면 내레이션은 "실제 ○○ 화면을 보시면…"처럼 화면을 가리키게 쓰고, 스포트라이트는 그 숫자/문구를 말하는 앵커에 맞춘다.
- 한 장면에 이미지 1장. 이미지가 많으면 장면을 늘리거나 짧은 연속 장면(각 3–5초)으로 나눈다.
- 이미지 영역은 y 1300px 위에서 끝나야 자막과 겹치지 않는다(카드 높이가 넘치면 `.shot.window`로 높이를 고정).

## 2. 음성 (일레븐랩스)

```bash
cd $P && python3 gen_tts.py && python3 gen_bgm.py
```

`gen_tts.py`는 장면별 MP3 + 글자 단위 타임스탬프(`voice_alignment.json`)를 만든다. 문장이 바뀐 장면만 다시 생성하므로 수정 후 재실행해도 비용이 적다. 음악 생성이 실패하면(요금제/한도) 음악 없이 진행하고 `<audio id="bgm">`를 템플릿에서 지운 뒤 보고한다.

## 3. 장면 디자인 → `src/index.template.txt`

`references/design-system.md`를 읽는다. 템플릿의 `SCENES START/END` 사이 `<section>`과 `SCENE TIMELINE START/END` 사이 JS만 이번 내용으로 바꾼다. 디자인 토큰·크롬·자막·헬퍼는 건드리지 않는다.

- 장면마다 `<section id="s-…" class="clip" %%S_<scene-id>%% data-track-index="1">` + 안에 `.stage`.
- 컴포넌트 카탈로그(오해 카드+스탬프, 판정 슬랩, 방정식 카드, 배지, 체크 행, 2×2 타일, 영수증+카운트업, 버블, 로드맵, 체인, CTA)에서 내용에 맞는 것을 고른다. 필요하면 같은 토큰으로 새 컴포넌트를 만든다.
- 등장 타이밍은 `c("<scene-id>", "<앵커>")`로 음성에 맞춘다. 장면 시작에 모든 걸 띄우지 말고 말하는 순서대로 하나씩 등장시킨다. 장면 끝에는 `exit()`.
- 화면 텍스트는 짧게(카드 1줄 핵심어 + 회색 보조 1줄). 자막이 문장을 맡는다.

## 4. 빌드 · 검사 · 확인

```bash
cd $P && python3 build.py && npx hyperframes check
npx hyperframes snapshot --at <각 장면의 마지막 무렵 시각들>
```

- `check`의 `nested_structure_needs_subcomposition`, `timeline_track_too_dense`, `composition_file_too_large` 경고는 이 단일 파일 구조에서 예상되는 것이므로 무시한다. **에러**와 Layout/Contrast 문제는 고친다(애니메이션 중간 순간의 대비 경고는 무시 가능).
- `snapshots/contact-sheet-*.jpg`를 직접 열어 겹침·잘림·빈 화면이 없는지 본다. 하단 1540px 아래는 쇼츠 UI가 덮으므로 비워 둔다.

## 5. 렌더 · 전달

```bash
cd $P && npx hyperframes render --quality high --output renders/video.mp4
```

90초 영상 기준 약 6–7분 걸린다(타임아웃을 넉넉히). 끝나면:

1. `ffprobe`로 길이/해상도 확인, `ffmpeg -af volumedetect`로 무음이 아닌지 확인.
2. MP4와 컨택트 시트를 사용자에게 보낸다(SendUserFile 등).
3. 커밋·푸시하라고 했다면 `videos/<project>` 전체를 커밋.
4. 보고: 경로, 길이, 장면 구성 요약, 원문과 달라진 부분(오타 수정, 추가한 설명 문구), 다시 만들 때 고칠 파일(`scenes.json` → `gen_tts.py` → `build.py` → render).

## 수정 요청이 올 때

- 문구/내레이션 변경 → `scenes.json` 수정 → `gen_tts.py`(바뀐 장면만 재생성) → `build.py` → render.
- 디자인 변경 → `src/index.template.txt`만 → `build.py` → render.
- 더 빠르게/느리게 → `settings.speed` (0.7–1.2) 변경 후 전 장면 재생성.
- 다른 목소리 → `settings.voice_name`.
- 이미지 교체/추가 → `prep_images.py` 다시 실행(같은 순서면 id 유지) → 장면 수정 → `build.py` → render.
