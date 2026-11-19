# STATUS — "영어도 못하는데 불어를?" 롱폼 (2026-11-19)

상태: **렌더 완료, 대표님 미리보기 대기** (publish 브랜치 게시 안 함)

## 품질 점검 4줄
① 모션그래픽 장면 **14/14** (정지 슬라이드 0, 정지 이미지+확대만 있는 장면 0 · 얼굴/HeyGen 0) — 숫자 카운트업·막대/도표 성장·계단·갈림길·지도 화살표·달력 타임라인·하이라이트·체크리스트·카드 뒤집기·저울·문 열림, 캡처는 휴대폰 프레임 안에서 노란 강조로 이동·확대 + 빨간 테두리
② 배경음악 **ElevenLabs 음악 생성 신곡 2곡** `audio/bgm/el_bright_acoustic_A.mp3`·`el_bright_acoustic_B.mp3`(밝은 어쿠스틱·피아노, 약 95BPM, 가사 없음)을 A→B→A… 4초 크로스페이드로 이어 깔고, 내레이션을 키로 한 **sidechaincompress 덕킹**(내레이션 대비 __DUCK__ dB 낮음), 시작 1.5초 페이드인·끝 3초 페이드아웃
③ 효과음 **59개** (transition_ding 13 · tick 19 · ding 12 · stamp 15) — 어느 60초 구간이든 4~8개, 위치는 HyperFrames 애니메이션 큐 시각과 동일, 내레이션보다 약 12~13dB 낮게, whoosh(거친 스우시) 미사용
④ 최종 MP4 오디오 **__LUFS__ LUFS / 트루피크 __TP__ dBTP** (목표 -16±0.5 / -1.5 이하), 내레이션은 장면별 -16 LUFS로 맞춘 뒤 마스터 투패스 loudnorm — BGM이 내레이션 아래 약 23dB라 말소리 또렷함

## 산출물
- `renders/video.mp4` (1920×1080, 30fps, __DUR__) — 90MB 초과 시 `video.mp4.part-00…` + `video.mp4.sha256` 로 분할 커밋 (합치기: `cat video.mp4.part-* > video.mp4 && sha256sum -c video.mp4.sha256`)
- `thumbnail.jpg` / `thumbnail.png` (1280×720, 빨간 스타일, 인물·얼굴 없음)
- `upload-text.txt` (제목·설명·챕터·태그·AI 사용 공개 메모)
- HyperFrames 프로젝트: `index.html` + `compositions/s01~s14.html` (원본은 `src/`, `tools/build.py` 로 생성)

## 진행하며 내린 판단 (대표님 확인용)
1. **영상 길이 약 9분 56초** — 브리프 예상(12~13분)보다 짧습니다. NARRATION.txt 문장을 고치지 말라는 지시에 따라 ElevenLabs 음성 길이(내레이션 합계 9분 32초)에 그래픽을 맞췄기 때문입니다. 늘리려면 문장 추가나 말 속도 조정이 필요합니다.
2. **워크플로**: hyperframes 진입 스킬의 라우팅 기준(3분 초과 장편 → general-video)을 따르고, faceless-explainer·motion-graphics 의 장면 설계 방식(장면별 서브컴포지션, 음성 타임스탬프에 맞춘 큐)을 차용했습니다.
3. **SCRIPT_v2.md 의 "얼굴" 장면(S1, S14)** 은 모두 모션그래픽으로 대체했습니다(말풍선·질문 카드·타이틀 / 요약·벽→문·카카오톡·로고).
4. **"[대표님 확인 필요]" 줄은 화면에 넣지 않았습니다.** 해당 내용은 내레이션대로 나갑니다 — 확인 부탁드립니다: s04 금액(약 6,000만 / 1,700만~2,500만 원) 기준일·산정 범위, s05 프렌치 이머전 중간 편입·자녀 대학 학비 적용 조건, s12 "저희 가족" 표현.
5. **대본에 없던 보조 문구**(오해 방지용 짧은 표기)를 몇 곳 넣었습니다: s04 "학비 기준 약식 비교 · 개인별 차이 있음", s09 그래프 "개념도", s13 지도 "주 위치는 개념도입니다", s11 플랜 카드 "예시 양식", s10 B1/B2 카드 "대략적 기준"(브리프 지시). 빼길 원하시면 바로 수정 가능합니다.
6. **s02 "10명 중 4명"**: 화면 메모대로 표기했고(내레이션은 "초청장 10장 중 4장"), 아이콘은 초청장(봉투) 모양으로 했습니다.
7. **s10 캡처**: 브리프 표를 우선했습니다(03은 `_01`만 사용; SCRIPT_v2 의 `03_..._03` 파일은 captures/ 에 없음).
8. **자막**: SCRIPT_v2 표기(AA Canada, LMIA, TCF, canlog, 아라비아 숫자)를 내레이션 타임스탬프에 맞춰 자동 분할했습니다(한 줄 최대 33자).
9. **오디오 파일 관리**: 무손실 마스터 `audio/mix_master.wav`(약 170MB)는 저장소 용량 제한으로 커밋하지 않고(`tools/mix.py` 로 재생성), 컴포지션에는 AAC 256k 사본 `audio/mix.m4a` 를 연결했습니다. 최종 MP4 오디오는 마스터 WAV 에서 직접 인코딩했습니다.
10. 내레이션 검수: ElevenLabs 음성인식으로 14개 장면 전체를 다시 받아 적어 누락·오독이 없는지 확인했습니다(`audio/vo/stt/`).

## 다시 만들기
```bash
python3 tools/tts.py            # (필요 시) 내레이션 재생성
python3 tools/build.py          # 타이밍·자막·효과음 큐 → compositions/, index.html
python3 tools/mix.py            # 오디오 믹스 → audio/mix_master.wav, audio/mix.m4a
npx hyperframes render --crf 20 --output renders/render_raw.mp4
bash tools/finalize.sh          # 마스터 오디오 합본 + 라우드니스 확인 + 분할
```
