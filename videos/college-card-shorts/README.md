# 몬트리올 사립컬리지 카드뉴스 → 숏폼 2편

브리프: `plans/college-card-shorts/VIDEO_BRIEF.md` · 대본: `SCRIPT.txt` (문장 수정 없음)

| 경로 | 내용 |
|---|---|
| `tools/tts.py` | ElevenLabs "일곱번째"(vxpRrQegUpenYtez6hz1, eleven_multilingual_v2) 내레이션 + 문자 정렬 → `college_x/assets/voice.m4a`, `timing.json`. 숫자/영문은 TTS 입력만 한글 표기(화면·자막은 대본 원문). 속도: A 1.2, B 1.1 (A는 1.0에서 59.6초라 40~50초에 맞춤). 대체 TTS 없음 |
| `build.mjs` + `style.css` | HyperFrames 컴포지션 생성. 장면 전환은 대본 줄 큐, 숫자 슬램은 해당 단어가 발음되는 시점(정렬 데이터)에 맞춤 |
| `_shared/` | Black Han Sans, Pretendard(KS X 1001 서브셋), GSAP, card4 지도 크롭, BGM(South Shore 브랜치 bgm-a/b), SFX(Pixabay) |
| `thumbs/thumb.mjs` | 썸네일 1080×1920 → `college_x/thumbnail.jpg` |
| `college_a/`, `college_b/` | 프로젝트, `college_x.mp4`, `thumbnail.jpg`, `upload-text.txt` |

```bash
python3 tools/tts.py a --force   # 내레이션 다시 (API 키 필요)
node build.mjs                   # index.html 재생성 (+ assets/kit 복사, git 제외)
cd college_a && npx --yes hyperframes@0.8.185 render --quality looks --output college_a.mp4
node thumbs/thumb.mjs
```

규칙: 환율 문구 금지, 학비 근거 "2년 총 CAD 22,250", 출처는 화면 각주·설명란에만, "압도적으로"는 A 표지 제목에만.
publish 브랜치에는 올리지 않음(게시는 Aside).
