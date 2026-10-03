---
name: aacanada-shorts
description: AA Canada 유튜브 쇼츠/릴스(9:16) 자동 제작 — 주제만 주면 대본 작성 → 일레븐랩스 "네 번째"(대표 본인 클론 보이스)로 음성 자동 생성 → 색 시안 이미지 먼저 보여주기 → HyperFrames로 영상 렌더까지 진행한다. 첨부 이미지(통계청 캡처, 차트, 학교 사진 등)는 영상 안에서 줌·하이라이트 모션으로 직접 활용하고, 매 영상마다 색 팔레트를 바꾸며, 자막은 화면 위쪽, 글자는 크게, 말 속도는 약간 빠르게 만든다. "쇼츠 만들자", "릴스 영상", "이 내용으로 영상", "몬트리올/캐나다 유학·무상교육·영주권 주제로 짧은 영상", "숏폼", "음성 넣어서 영상" 같은 요청이면 사용자가 스킬 이름을 말하지 않아도 이 스킬을 쓴다. 가로(16:9) 일반 영상이나 기존 영상에 자막만 다는 작업은 해당하지 않는다.
---

# AA Canada 쇼츠 자동 제작

대표(AA Canada, 캐나다 전문 유학원)는 주제만 던지고 나머지는 맡기길 원한다. 그래서 이 스킬의 핵심은 **묻지 않고 진행하는 것**이다. 사용자가 확인해야 하는 지점은 딱 두 번: ① 색 시안 이미지(대본 요약과 함께), ② 완성 영상. 일레븐랩스 음성은 절대 사용자에게 만들어 달라고 하지 않는다 — API 키(`ELEVENLABS_API_KEY`)가 환경에 있고 `scripts/tts_elevenlabs.py`가 "네 번째" 보이스로 직접 만든다.

HyperFrames(`/hyperframes` → `/faceless-explainer` 워크플로)를 뼈대로 쓴다. 이 스킬은 그 위에 AA Canada의 고정 선호와, 이 샌드박스에서 검증된 우회책을 얹은 것이다.

## 고정 선호 (매번 적용, 다시 묻지 않음)

| 항목 | 값 | 이유 |
|---|---|---|
| 비율 | 1080×1920 (9:16) | 쇼츠/릴스 |
| 음성 | 일레븐랩스 "네 번째" 클론, `eleven_multilingual_v2`, speed 1.1 | 대표 본인 목소리, 일상 대화보다 약간 빠르게 |
| 길이 | 40–55초 | 쇼츠 최적 구간 |
| 자막 | 화면 위쪽 밴드(y 180–330), 큰 글씨 | 하단은 쇼츠 UI(제목·버튼)가 가림 |
| 글자 | 헤드라인 100px+, 본문 56–64px, 숫자 120px+ | 폰에서 가독성 |
| 폰트 | Pretendard (woff2 동봉) | 한글 렌더 보장 |
| 색 | 영상마다 다른 팔레트 (`scripts/pick_palette.py`) | 연속 영상이 비슷해 보이지 않게 |
| 첨부 이미지 | 영상에 직접 넣고 줌·하이라이트 모션 | 실제 자료가 신뢰를 준다 |
| 마무리 | "AA Canada" 워드마크 + "프로필 링크에서 상담 신청" CTA | 상담 유입 |

## 워크플로

경로 기준: 저장소 루트. `SK=.claude/skills/aacanada-shorts`, `FX=.claude/skills/faceless-explainer/scripts`, 프로젝트 `P=videos/<slug>` (slug는 주제의 영문 kebab-case).

### 1. 대본 작성 (자동)

`references/script-guide.md`를 읽고 주제(+사용자가 준 메모·이미지)로 대본을 쓴다. 요점: 첫 2초 훅 질문 → 2번째 장면에 결론 → 근거 3가지(첨부 이미지가 있으면 근거 장면에 배치) → 한 줄 정리 → CTA. 숫자는 나레이션엔 한글("삼천삼십 달러"), 화면·자막엔 숫자("$3,030"). 근거 없는 수치나 과장("캐나다에서 가장 저렴")은 쓰지 않는다 — 자료가 말하는 범위까지만.

### 2. 프로젝트 준비 + 음성 (자동, 병렬로 진행 가능)

```bash
python3 $SK/scripts/pick_palette.py suggest --n 3            # 최근에 안 쓴 팔레트 3개
bash $SK/scripts/setup_project.sh <slug> <첫번째-추천-팔레트> <첨부이미지 경로...>
```

그다음 `$P`에 쓴다 (형식은 faceless-explainer와 동일 — `../hyperframes/references/storyboard-format.md`, `script-format.md`):
- `BRIEF.md` — workflow: faceless-explainer, flow: automation, storyboard: no, aspect 1080x1920, language ko, message 한 줄
- `STORYBOARD.md` — 장면별 `## Frame N — 제목` + scene/voiceover/duration/transition_in/src/type/blueprint, 첨부 이미지는 `asset_candidates: assets/images/<파일>`
- `SCRIPT.md` — `## Line N — 라벨 (Frame N)` + 4칸 들여쓴 나레이션
- `caption_map.json` — 나레이션 한글 숫자 → 자막 표기 (예: `{"삼천삼십":"$3,030","에이에이":"AA","캐나다와":"Canada와"}`)

```bash
python3 $SK/scripts/tts_elevenlabs.py --project $P --caption-map $P/caption_map.json
node $FX/audio.mjs sync-durations --audio-meta $P/audio_meta.json --storyboard $P/STORYBOARD.md
```
음성은 순차 호출(스타터 요금제 동시 3건 제한), 단어 타이밍은 with-timestamps 응답에서 바로 얻는다. 특정 문장만 다시: `--only 03,05`.

### 3. 장면 제작 + 색 시안 (자동 → 사용자 확인 1회)

`$P/scripts/build_frames.py`(템플릿 복사본)를 이번 주제에 맞게 고쳐 쓴다. 템플릿에는 오늘 검증된 패턴이 다 있다: 키네틱 훅(취소선 반전), 대비 카드 + 배지, 번호 리스트 스테이지 + 카드 스태거, **사용자 이미지 줌·스포트라이트**(04: 차트 행 확대 + 나머지 흐리게), **이미지 위 카메라 팬**(05: 도시별 순서대로 이동 + 박스 그리기 + 전체로 복귀), 카운트업, 동심원 정리, 워드마크 CTA. 레이아웃 밴드(파일 머리 주석)를 지키고, 문장 단어 타이밍(`audio_meta.json`)에 맞춰 요소를 등장시킨다. 이미지 좌표는 원본 픽셀 기준으로 ffmpeg drawbox로 먼저 확인한다(`references/gotchas.md`).

```bash
cd $P && python3 scripts/build_frames.py && sed -i 's/^- status: outline$/- status: animated/' STORYBOARD.md
node $FX/captions.mjs build --storyboard ./STORYBOARD.md --audio-meta ./audio_meta.json --hyperframes . --out ./caption_groups.json
node $FX/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes .
node $FX/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes .
bash scripts/post_assemble.sh .          # GSAP 로컬화, 폰트 충돌 해결, 자막 상단 이동 — 위 3개 명령 뒤엔 항상 다시 실행
npx hyperframes check                    # 실패하면 고치고 다시
bash $SK/scripts/theme_samples.sh . "<훅 끝,결론 끝,이미지 장면 끝 시각>" <추천1> <추천2> <추천3>
```

사용자에게 `design-samples/option-*.jpg` 3장 + 나레이션 미리듣기(`narration-preview.mp3`) + 대본 요약 표를 보내고 **한 번만** 묻는다: "어느 색으로 갈까요? (수정할 문구가 있으면 같이 알려주세요)". 이 시점에 대본·음성 수정 요청을 받으면 `--only`로 해당 줄만 재생성한다.

### 4. 확정 색 적용 + 렌더 (자동)

```bash
python3 $SK/scripts/pick_palette.py apply <선택> $P && python3 $SK/scripts/pick_palette.py use <선택> $P
cd $P && THEME="$(python3 ../../$SK/scripts/pick_palette.py theme-json <선택>)" python3 scripts/build_frames.py
# 템플릿 C 기본값도 선택 팔레트로 바꿔 두면 이후 재빌드에 THEME 없이도 유지된다
node $FX/captions.mjs build ... && node $FX/assemble-index.mjs ... && node $FX/transitions.mjs inject ... && bash scripts/post_assemble.sh .
npx hyperframes check && npx hyperframes snapshot --at <장면별 끝 시각>   # contact-sheet 눈으로 확인
npx hyperframes render --skill=faceless-explainer --quality high --output renders/video.mp4
```
(`captions.mjs`는 frame.md 색을 읽으므로 자막 색도 자동으로 따라온다.)

완성본을 SendUserFile로 보내고, 장면 번호·시간 표를 함께 준다 — 수정 요청을 장면 번호로 받기 위해서다. 작업 브랜치에 커밋·푸시한다.

## 보고 형식

- 시안 단계: 대본 요약 표(장면 | 화면 | 나레이션) + 색 시안 3장 + 미리듣기, 질문은 하나.
- 완성 단계: 파일 경로·길이, 장면 표, 원문과 달라진 점(과장 문구 조정 등), 안 된 것(예: 배경음악)을 솔직하게.

## 참고 파일

- `references/script-guide.md` — 대본 구조, 훅 예시, AA Canada 사업 맥락, 표현 주의점
- `references/gotchas.md` — 이 샌드박스에서 막히는 것과 우회책 (CDN 차단, 폰트 충돌, 일레븐랩스 제한, 이미지 좌표 확인법 등)
- `assets/build_frames_template.py` — 장면 생성기 템플릿 (오늘 만든 몬트리올 무상교육 쇼츠 기반)
- 완성 예시 프로젝트: `videos/montreal-free-education-shorts/`
