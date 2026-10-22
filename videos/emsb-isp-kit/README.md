# EMSB 국제학생 프로그램 2027-28 영상 키트

롱폼 1편(16:9)과 숏폼 12편(9:16)을 **같은 컴포넌트**로 생성하는 HyperFrames 생성기입니다.
브리프: `plans/emsb-isp-2027/VIDEO_BRIEF.md` · 대본: `SCRIPT.txt`, `SHORTS_SCRIPT.txt`

| 파일 | 역할 |
|---|---|
| `timing.json` | **장면 길이 설정 (유일한 곳)**. 롱폼 s01~s11, 숏폼 12편의 `duration`(초). 선택: `cues`(문장별 시작 초) |
| `content/longform.mjs` | 롱폼 11장면 화면 구성 + 유튜브 썸네일 |
| `content/shorts.mjs` | 숏폼 12편 화면 구성 + 커버 |
| `lib/components.mjs` | 공용 컴포넌트(카드·칩·학비표·사진 Ken Burns·체크리스트·흐름도·CTA 등) |
| `lib/script.mjs` | 대본 파서 — 하단 자막은 항상 대본 원문 그대로 |
| `runtime/` | 브랜드 CSS(메이플 레드), GSAP, 런타임(폰트 `document.fonts.load` → `check` 후 타임라인 등록) |
| `fonts/` | Black Han Sans, Noto Sans KR (한글 KS X 1001 + 대본 문자로 서브셋) |
| `build.mjs` | 위 내용을 각 프로젝트 `index.html`로 생성 (+ 업로드 문구 사본, 롱폼 챕터 시간) |
| `sync-audio.mjs` | 녹음 트림(앞뒤 무음 0.3s) → `timing.json`에 길이 기록 |

화면 요소는 초가 아니라 **대본 문장 큐**(`c3`, `c3@0.5`, `end-3`)에 걸려 있어서, 장면 길이가 바뀌면 자막과 화면이 함께 따라갑니다.

## 다시 만들기

```bash
cd videos/emsb-isp-kit
node build.mjs                 # 전체 (롱폼 + 숏폼 12편)
node build.mjs longform        # 롱폼만
node build.mjs shorts fee free # 숏폼 일부만
```

각 프로젝트의 `_kit/`(폰트·사진 사본)은 빌드 때 생성되며 git에 넣지 않습니다. 렌더 전에 반드시 `build.mjs`를 먼저 실행하세요.

## 녹음이 올라오면 (audio/emsb_s01~s11.m4a, audio/emsb_sh_*.m4a)

```bash
cd videos/emsb-isp-kit
node sync-audio.mjs            # 트림 → audio-trimmed/, timing.json 갱신 (duration = 녹음 + 0.4s)
node build.mjs                 # HTML 재생성 (자막 타이밍 = 녹음 길이 기준 문장 글자 수 비율)
cd ../emsb-isp-longform && npx hyperframes check && npx hyperframes render --quality looks --output emsb-isp-longform.mp4
```

- 자막을 더 정확히 맞추려면 `timing.json`의 해당 장면에 `"cues": [0.3, 4.1, ...]`(문장 수만큼, 장면 기준 초)를 넣고 다시 빌드합니다.
- 대본과 다르게 읽은 줄은 렌더 전에 원장님께 보고합니다(자막은 대본 원문 기준).
- 숏폼: `cd ../emsb-isp-shorts/<이름> && npx hyperframes render --quality looks --output <이름>.mp4`

## 썸네일 / 커버

`thumbnail-src/`(1280x720), 숏폼 `cover-src/`(1080x1920)는 정지 화면 컴포지션입니다.

```bash
npx hyperframes snapshot thumbnail-src --at 0.5 --no-end -o /tmp/thumb   # PNG → thumbnail.jpg로 변환
```

## 표현 규칙 (브리프 §2) — 수정할 때 꼭 확인
- "공식 에이전트/공식 파트너/독점", "최고", "100%", "북미 최고의 학생 도시" 금지. 졸업률은 "퀘벡 영어 공립 교육청 중 졸업률 1위 92.1% (2024-25학년도, EMSB 2026.09 발표)" 형태로만.
- 금액은 CAD만(원화 환산 금지), 각주 "출처: EMSB 2027-28 International Student Program 자료 (2026.10 기준)".
- 학비 면제 장면(S10, 숏폼 free)에는 "퀘벡 교육부 면제 규정, 부모 학교·체류 조건에 따라 다름 · 상담 필요" 각주 필수.
- EMSB 원본 이미지 중 `isp_montreal_skyline.jpg`, `ad_halfpage.jpg`(World's best North American city…), `gb_cover.jpg` 하단(Top Education…)은 금지 문구가 박혀 있어 크롭해서만 사용합니다.
- 어떤 채널에도 게시하지 않으며, publish 큐에 READY 파일을 만들지 않습니다. 업로드 문구는 각 영상 폴더의 `upload-text.txt`(사본)에만 둡니다.
