---
name: aac-shorts-maker
description: AA Canada(캐나다 유학·이민 유학원)의 유튜브 쇼츠 / 인스타 릴스 영상을 아이디어 한 줄에서 완성 MP4 + 썸네일까지 만드는 전체 워크플로. 아이디어 → 팩트체크한 컨셉 제안 → 대표님 수정/컨펌 → HyperFrames(faceless-explainer)로 모션그래픽 중심 제작 → ElevenLabs "네 번째" 클론 보이스 내레이션 + 배경음악 → 한글 자막 → 렌더 → 쇼츠/유튜브 썸네일 → 업로드 문구. 사용자가 "쇼츠 만들자", "릴스 영상", "이 내용으로 영상", "영상 아이디어 있어", "유튜브에 올릴 영상", "카드뉴스를 영상으로", 캐나다 이민·영주권·유학·불어·몬트리올·자녀무상교육 주제의 영상/모션그래픽/썸네일을 언급하면, 스킬 이름을 말하지 않아도 반드시 이 스킬을 사용한다.
---

# AA Canada 쇼츠 메이커

대표님(AA Canada 운영, 몬트리올 중심 캐나다 유학·이민)이 아이디어를 주면 → 컨셉을 잡아 제안하고 → 수정/컨펌을 받은 뒤 → HyperFrames로 **모션그래픽이 풍부한** 세로 쇼츠를 만들고 → 썸네일까지 함께 낸다. 첫 작품(2026-10, "불어 NCLC 5 연방 5,000 TO")이 이 스킬의 기준 예시다: `videos/french-nclc5-federal-quota/`.

이 스킬은 **오케스트레이션 레이어**다. 실제 영상 제작 규칙은 HyperFrames 스킬들이 갖고 있으니, 각 단계에서 지정한 스킬을 반드시 읽고 따른다. 여기에는 AA Canada에 맞춘 결정(브랜드, 목소리, 사실관계 원칙)과 이 환경에서 겪은 함정의 해결책만 담는다.

## 0. 고정 설정 (매번 묻지 않는다)

| 항목 | 값 |
|---|---|
| 포맷 | 세로 1080×1920, 3분 이내(권장 60–110초), 한국어 |
| 목소리 | ElevenLabs "네 번째" (대표님 클론 보이스, `eleven_multilingual_v2`, speed 1.05) |
| 디자인 | `blue-professional` 프리셋(크림 #fdfae7 + 코발트 #1e2bfa), 폰트 Pretendard(로컬) |
| 자막 | 하단 한글 캡션 (화면 하단 17%는 자막 전용) |
| 배경음악 | ElevenLabs Music, 잔잔한 피아노/코퍼릿, 볼륨 0.14 |
| 채널 | 유튜브 "캐나다 전문 유학원 AA Canada", 인스타 `aac.montreal` |
| 마무리 | AA Canada 워드마크 + "상담 문의" CTA |

대표님이 다르게 요청하면 그 요청이 우선한다.

## 1. 컨셉 제안 (게이트 — 컨펌 전에는 제작하지 않는다)

1. **팩트체크 먼저.** 이민 정책은 자주 바뀌고, 틀린 정보는 유학원의 신뢰를 깎는다. WebSearch로 공식 출처(canada.ca, 각 주 정부 사이트)와 이민 뉴스를 교차 확인하고, 확인된 것과 추정을 구분한다. 수치·날짜·조건(NCLC 레벨, 쿼터 수, 대상 주)은 출처를 남긴다.
2. `references/concept-template.md` 형식으로 컨셉을 채팅에 제안한다: 한 줄 메시지, 후킹 문장 후보 2–3개, 장면 구성표(장면별 화면/모션그래픽/내레이션), 예상 길이, 썸네일 문구, 사실관계 주의점.
3. 모션그래픽 아이디어를 **장면마다** 구체적으로 적는다(카운트업 숫자, 막대 비교, 줄 서기 다이어그램, 취소선→단어 교체, 경로 연결 등). "텍스트만 뜨는 장면"은 만들지 않는다.
4. 대표님이 수정하면 반영해 다시 보여준다. **"컨펌/진행/좋아" 같은 명시적 승인 후에만** 2단계로 간다.

사실관계 원칙(첫 작품에서 정한 것):
- 과장 금지: "점수 경쟁과 완전 분리"처럼 단정하지 말고 조건(기본 자격 필요 등)을 한 줄 넣는다.
- 특정 주의 선발 사례는 대표님이 원할 때만. 공식 근거 없는 연결("온타리오도 연방 쿼터를 썼다")은 쓰지 않는다.
- 몬트리올을 "불어라서 어렵다"가 아니라 "불어를 배울 수 있어서 유리하다"로 프레이밍하는 것이 대표님의 핵심 마케팅 메시지다. 자연스러우면 CTA를 "몬트리올 어학연수"로 연결한다.

## 2. 제작 (HyperFrames)

컨펌된 컨셉이 곧 브리프다. `/hyperframes`를 먼저 읽고(진입점 규칙), 워크플로는 `faceless-explainer`로 라우팅한다. 컨셉 단계에서 인터뷰를 끝냈으므로 HyperFrames 인텐트 질문은 반복하지 않고 `flow: automation`, `storyboard: no`로 BRIEF.md를 쓴다. 이후 `faceless-explainer` SKILL.md의 Step 0–6을 순서대로 따르되, 아래 AA Canada 변경점을 적용한다.

```bash
SK=<이 스킬 디렉터리>            # 예: .claude/skills/aac-shorts-maker
P=videos/<kebab-주제명>           # 저장소 루트 기준
npx hyperframes skills update faceless-explainer
npx hyperframes init "$P" --non-interactive --example=blank --skill=faceless-explainer
mkdir -p $P/assets/fonts $P/assets/vendor && cp $SK/assets/fonts/*.woff2 $P/assets/fonts/ && cp $SK/assets/gsap.min.js $P/assets/vendor/
```

- **Step 1 (brief):** `tokens.json`의 `fonts`는 `["Pretendard","Pretendard"]`, `colors`는 비워 둔다.
- **Step 2:** `build-frame.mjs --preset blue-professional`.
- **Step 3 (스토리보드/스크립트):** 컨펌된 컨셉의 내레이션을 그대로(verbatim) SCRIPT.md에 넣는다. 형식은 `## Line N — 제목 (Frame N)` + 4칸 들여쓴 대사.
- **Step 3.1 (오디오):** `audio.mjs` 대신 아래를 쓴다. HeyGen/Kokoro는 한국어 클론 보이스가 없다.
  ```bash
  node $SK/scripts/el-tts.mjs $P --voice-name "네 번째"     # 단어 타이밍 포함 audio_meta.json
  node $SK/scripts/el-music.mjs $P <총길이+8초>              # 호스트 BGM 등록
  sed -i 's/^music: .*/music: none/' $P/STORYBOARD.md          # 호스트 BGM을 쓰므로 조회 BGM 끔
  node <faceless-explainer>/scripts/audio.mjs sync-durations --audio-meta $P/audio_meta.json --storyboard $P/STORYBOARD.md
  ```
- **Step 4 (비주얼 디자인) — 모션그래픽 중심:** 실제 단어 타이밍(`audio_meta.json`)을 출력해서 장면마다 "어떤 단어가 나올 때 무엇이 등장하는지"를 초 단위로 적는다. 장면마다 블루프린트를 하나씩 정하고, 영상 전체에서 최소 4종을 섞는다. 이름 있는 효과는 `npx hyperframes catalog --query "..."`로 먼저 찾는다. 단골 조합은 `references/motion-playbook.md`를 본다.
- **Step 5 (프레임 제작):** 장면당 서브에이전트 1개를 병렬로 띄운다(Agent 도구, background). 디스패치 문맥에 반드시 넣을 것:
  - 캔버스 1080×1920과 자막 금지 구역(y > 1590)
  - 한국어 문구는 그대로 사용
  - Pretendard @font-face 블록 복붙
  - GSAP은 `<script src="assets/vendor/gsap.min.js">`
  - 진행바(N/총장면)
  
  모든 프레임 파일이 생기면 `status: animated`로 바꾸고 captions → assemble을 실행한다.
- **Step 6:** `transitions inject/verify` → **`bash $SK/scripts/offline-fixups.sh $P`** → `lint` → `check` → `snapshot`(장면 중간 지점 + 끝) → 컨택트 시트를 눈으로 확인 → `render --quality high --output renders/video.mp4`. 렌더 후 `ffprobe`와 `volumedetect`로 1080×1920 해상도와 오디오 존재를 확인한다.

함정과 해결법(48KB 패킷 한도, 숫자로 시작하는 id, 의도된 겹침 등)은 `references/lessons.md`에 있다. 에러가 나면 먼저 읽는다.

## 3. 썸네일

영상과 같은 디자인 언어로 두 장을 만든다(쇼츠 커버 1080×1920, 유튜브 1280×720).

```bash
cat > $P/thumbnail/spec.json <<'EOF'
{ "badge": "2026 연방정부 발표", "strike": "주정부 점수 경쟁",
  "title": ["불어 *중하 수준*이면", "경쟁에서 빠져나온다"],
  "big": "5,000", "bigUnit": "개 TO", "sub": "불어 NCLC 5 · 주정부 쿼터와 *별도*",
  "thumbnail-shorts": { "title": ["불어 *중하 수준*이면", "점수 경쟁에서", "빠져나온다"] } }
EOF
node $SK/scripts/make-thumbnail.mjs $P/thumbnail/spec.json $P/thumbnail
```

- `*단어*`는 코발트색으로 강조된다. `strike`는 빨간 취소선(부정할 통념), `big`은 핵심 숫자다(없으면 생략).
- 세로 썸네일은 한 줄 7–9자 이하로 줄을 직접 나눈다(`thumbnail-shorts.title`).
- 렌더 후 이미지를 열어서 줄바꿈과 겹침을 확인한다.

## 4. 납품

1. 모두 커밋하고 작업 브랜치에 푸시한다(`videos/<주제>/` 전체: 소스, `renders/video.mp4`, `thumbnail/*.png`).
2. `SendUserFile`로 영상과 썸네일을 보낸다.
3. 업로드 문구를 채팅에 준다: 유튜브 제목·설명·해시태그(#Shorts 포함), 인스타 캡션. 주의 문구(기본 자격 필요 등)를 설명에 포함한다.
4. 최종 보고에 아래를 적는다:
   - 영상 길이
   - 파일 위치(브랜치와 경로)
   - 장면 목록(번호로 부분 수정 가능)
   - 대표님이 직접 확인해야 할 것(음성 발음은 들어봐야 앎)
5. 업로드 대행 요청이 오면: 클라우드 세션에서는 대표님 PC의 브라우저(Aside 등)를 조작할 수 없다. Aside에 붙여넣을 지시문(게시 직전 멈춤 포함)과 문구를 준다.

## 5. 부분 수정 요청

"3번 장면 숫자 바꿔줘", "목소리 느리게" 같은 요청이 오면:
- **장면 수정:** `compositions/frames/NN-*.html`만 고치고 → `offline-fixups` → `check` → 렌더한다.
- **대사 수정:** SCRIPT.md와 STORYBOARD.md의 voiceover를 고치고 → `el-tts.mjs` 재실행 → `sync-durations` → 해당 프레임의 타이밍을 조정 → `captions build` → `assemble` → `transitions inject` → `fixups` → `check` → 렌더한다.
