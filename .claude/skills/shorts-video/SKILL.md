---
name: shorts-video
description: AA Canada 유튜브 쇼츠(9:16) 영상 제작 스킬. "쇼츠 영상 제작해줘", "쇼츠 만들어줘", "숏폼 영상", "릴스 영상 만들어줘" 같은 요청에 사용. 사용자가 준 홍보 내용(캐나다 자녀무상교육, 몬트리올, 불어 루트, LMIA 면제, 유학 후 이민, 영주권 등)을 HyperFrames로 나레이션 영상으로 만들고, 일레븐랩스 "네 번째" 목소리로 음성을 생성하고, 자막은 화면 상단에 배치하며, 후크 있는 썸네일까지 만든 뒤 깃허브에 저장하고 위치를 알려준다.
---

# AA Canada 쇼츠 영상 제작

사용자가 "쇼츠 영상 제작해줘" + 홍보 내용을 주면 아래 순서를 그대로 따른다. 질문은 최소화하고(내용이 비어 있을 때만 묻기) 끝까지 만든다.

## 고정 규칙 (매번 지킨다)

1. **HyperFrames 스킬 사용** — `/hyperframes` 를 먼저 로드하고, `/hyperframes-core` 규칙(타이밍 `data-*`, `class="clip"`, 단일 paused 타임라인, `<br>` 금지, 결정적 코드)을 지킨다. 프로젝트는 `npx hyperframes init "videos/<kebab-주제>" --non-interactive --example=blank --skill=faceless-explainer` 로 만든다.
2. **음성: 일레븐랩스 "네 번째" 목소리** — 클론 보이스 `voice_id = 9qtE9eIaqHMUAfRp4QTW` (env `ELEVENLABS_VOICE_ID` 와 동일), 모델 `eleven_multilingual_v2`. HeyGen/Kokoro 등 다른 TTS로 대체하지 않는다. 키(`ELEVENLABS_API_KEY`)가 없거나 호출이 실패하면 멈추고 알린다. 이름으로 확인하려면 `GET /v1/voices` 에서 name == "네 번째".
3. **목소리 자동 점검·조정 (매번, 사용자에게 묻지 않고)** — 음성은 들을 수 없으므로 측정으로 점검한다. `scripts/voice_qc.py` 가 장면마다 여러 테이크를 만들고, 자막 청크마다 아래를 검사해 가장 깨끗한 테이크를 고르고 고칠 수 있는 것은 직접 고친다.
   - **"어~", "음", "이" 같은 추임새·군소리는 절대 남기지 않는다.** STT로 찾아서 잘라내고, 잘라낸 결과를 STT로 다시 확인한다.
   - 대본과 다르게 읽은 단어(STT 대조), 늘어진 음절, 문장 중간의 이상한 쉼, 너무 빠르거나 느린 구간, 갑자기 커지거나 작아지는 소리, 튀는 음높이, 평서문인데 끝이 올라가는 억양, 클리핑, 말 앞뒤 잡음.
   - 최종 결과에 플래그가 남아 있으면 해당 청크만 다시 생성한다. 크레딧 부족 등으로 못 고치면 남은 문제를 보고에 명시하고, 게시 대기함에는 올리지 않는다.
   - **나레이션을 문장 단위로 잘라 사이에 쉼을 끼워 넣지 않는다.** 영상 길이를 맞추려고 문장 사이에 0.5~1초씩 넣었더니 "너무 끊긴다"는 피드백을 받았다(핼리팩스 쇼츠). 길이가 모자라면 대본이나 화면 연출(장면 끝 여유)로 맞추고, 목소리는 한 번에 자연스럽게 이어지게 둔다.
   - STT로 못 잡는 추임새도 남을 수 있으므로, 측정 결과가 깨끗해도 "확인 완료"라고 단정하지 않는다. 사용자가 직접 녹음한 파일을 주면 그 음성을 우선 사용한다.
   - 결과는 프로젝트의 `voice_qc.md` 에 남기고, 최종 보고에 "목소리 점검 결과"(고친 것 / 남은 것)를 짧게 적는다.
4. **자막은 상단** — 쇼츠 하단은 제목/채널/버튼 UI에 가려지므로 자막 박스는 y≈215px부터(상단 UI 아래) 시작하는 상단 밴드에 둔다. 핵심 비주얼은 y≈560–1440 구간, 하단 ~480px에는 중요한 정보를 두지 않는다. 자막: Pretendard Black 76px, 흰 글자 + 핵심 키워드 노란색(#ffd23f), 어두운 반투명 박스.
5. **썸네일 생성** — 1080×1920, 큰 글씨 3~4줄, 숫자/대비/이득을 담은 후크 문구(예: "부모 학비 내지 말고 / 월급 받으며 / 버티는 법"), 상단 카테고리 pill, 하단 루트 칩, AA CANADA 표기. 가독성 확인을 위해 렌더된 PNG를 직접 열어 본다(줄바꿈 어색함, 의미를 뒤집는 장식 금지).
6. **깃허브 저장 후 위치 안내** — 지정된 작업 브랜치에 커밋·푸시하고, 최종 답변에 MP4/썸네일/프로젝트 경로와 깃허브 링크(`https://github.com/<owner>/<repo>/blob/<branch>/<path>`)를 알려준다.

## 제작 순서

1. **환경 확인**: `node -v`, `npx hyperframes --version`, `ffmpeg`, `ELEVENLABS_API_KEY`. CDN(jsdelivr/unpkg)이 막혀 있을 수 있으니 폰트와 GSAP는 npm으로 받아 로컬에 둔다:
   ```bash
   npm pack pretendard@1.3.9 gsap@3.14.2   # 압축 해제 후
   # pretendard: dist/web/static/woff2/Pretendard-{Medium,Bold,ExtraBold,Black}.woff2 → assets/fonts/
   # gsap: dist/gsap.min.js → assets/vendor/
   ```
2. **대본 (`script.json`)**: 60~75초, 장면 6~8개. 구조 = 후크(3초 안에 이득/질문) → 핵심 주장 → 단계/근거 → 비교 → CTA("AA Canada와 상담하세요"). 각 장면은 `chunks: [[자막표시문구, TTS발음문구], ...]`. 자막은 한 줄 13~16자 이내로 짧게. 약어·숫자는 TTS 문구에서 한글 발음으로 풀어 쓴다(LMIA→엘엠아이에이, PGWP→피지더블유피, AA Canada→에이에이 캐나다, 1~2년→일이 년, 3년→삼 년). 사실관계는 사용자가 준 내용 범위 안에서만 쓰고 과장하지 않는다(확실치 않은 숫자는 넣지 않기).
   ```json
   {"voice_id":"9qtE9eIaqHMUAfRp4QTW","voice_name":"네 번째","model_id":"eleven_multilingual_v2",
    "scenes":[{"id":"s1-hook","chunks":[["캐나다 자녀무상교육,","캐나다 자녀무상교육,"]]}]}
   ```
3. **음성 생성 + 자동 점검**: `python3 .claude/skills/shorts-video/scripts/voice_qc.py videos/<project> --takes 3` — 장면별 3테이크 생성(시드 고정) → STT·음향 측정으로 청크별 채점 → 추임새 제거 → 최선 청크를 `assets/audio/chunks/` 에 저장 → `voice_qc.md` 보고서. "Still flagged"가 남으면 대본 발음 표기(TTS 문구)를 바꾸거나 `--takes` 를 늘려 다시 돌린다. 그다음 `tools/retime.py`(청크 배치·쉼) → `tools/make.sh`(build + BGM carve). (구버전) `python3 .claude/skills/shorts-video/scripts/tts.py videos/<project>` — 장면별로 일레븐랩스 `/with-timestamps` 를 호출해 `assets/audio/<scene>.mp3`, 글자 단위 정렬을 받아 `assets/audio/narration.wav`(장면 사이 0.35초 간격)와 `timing.json`(장면 구간 + 자막 청크 시작/끝)을 만든다. 대본만 바꿨으면 `--force` 로 재생성.
4. **컴포지션**: `videos/<project>/tools/build.py` + `tools/template.html` 패턴을 사용한다(참고 예시: `videos/montreal-french-lmia-shorts/tools/`). `build.py` 가 `timing.json` 을 읽어 장면 `<section class="clip scene">` 과 자막 `<div class="clip cap">` 을 정확한 시간으로 생성하고, 템플릿의 GSAP 타임라인은 `C(장면, 청크)` 시간에 맞춰 각 비주얼을 등장시킨다(나레이션과 싱크). 장면 비주얼은 타이포·도식·비교 막대·체크리스트·타임라인 등으로 직접 디자인한다. 루트 1080×1920, `<audio id="narration">` 필수.
5. **검증**: `npx hyperframes lint` (error 0), `npx hyperframes check`, `npx hyperframes snapshot --at <각 장면 중간 시점>` 후 contact sheet를 직접 보고 겹침/잘림/빈 화면(특히 첫 1초 후크 화면)을 고친다. `nested_structure_needs_subcomposition`, `timeline_track_too_dense` 경고는 Studio 정리용이라 렌더에 영향 없음.
6. **렌더**: `npx hyperframes render --skill=faceless-explainer --quality high --output renders/video.mp4` (백그라운드 실행). 끝나면 `ffprobe` 로 길이·해상도·오디오 스트림 확인.
7. **썸네일**: `videos/<project>/thumbnail/thumbnail.html` 작성 → `bash .claude/skills/shorts-video/scripts/thumbnail.sh videos/<project>` → `thumbnail.png/.jpg`. 결과 이미지를 열어 확인.
8. **저장/보고**: `.gitignore` 에 `node_modules/`, `snapshots/`, `.hyperframes/` 등 임시물만 제외하고 렌더 MP4·썸네일·소스는 커밋. 푸시 후 아래 형식으로 보고:
   - 영상: `videos/<project>/renders/video.mp4` (길이, 해상도)
   - 썸네일: `videos/<project>/thumbnail/thumbnail.png`
   - 깃허브 링크, 사용한 목소리(네 번째), 대본 요약, 수정 가능한 포인트

## 디자인 기본값 (AA Canada)

- 배경: 네이비 그라디언트(#0b1730→#132a52) + 옅은 그리드, 포인트 색: 캐나다 레드 #e63946, 블루 #2f6bff, 골드 #ffd23f, 그린 #2ec27e.
- 상단 브랜드 라인 `AA CANADA · <주제>` (y≈150px, 작게).
- 마지막 장면 CTA: 큰 "AA CANADA" + "캐나다 자녀무상교육 · 유학 후 이민 · 영주권" + "몬트리올 · 밴쿠버 · 토론토 · 런던" + 빨간 상담 버튼.
- 몬트리올 관련 영상은 "불어권이라 망설여진다 → 오히려 불어가 무기" 프레이밍을 적극 활용한다.
