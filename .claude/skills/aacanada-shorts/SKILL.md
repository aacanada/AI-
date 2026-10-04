---
name: aacanada-shorts
description: AA Canada 쇼츠(9:16 세로) 교육용 영상 제작. 사용자가 준 내용(유학·이민·자녀무상교육 안내 원고, 메모, 핵심 포인트)으로 일레븐랩스 "네 번째" 클론 목소리 내레이션(약간 빠른 템포)을 만들고, HyperFrames로 고급스러운 색감(미드나잇 네이비 + 샴페인 골드 + 아이보리)의 교육용 쇼츠 MP4를 렌더링한다. "쇼츠 만들어줘", "릴스/틱톡 영상", "이 내용으로 영상", "숏폼", "유튜브 쇼츠", "네 번째 목소리", "일레븐랩스로 음성 만들어서 영상" 같은 요청이면 영상 길이나 주제가 달라도 반드시 이 스킬을 쓸 것. Use for any AA Canada short-form vertical video request built from pasted text, with ElevenLabs voice + HyperFrames.
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
