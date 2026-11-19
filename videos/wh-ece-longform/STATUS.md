# STATUS — 워홀 + 유아교육(ECE) 공립 vs 사립 8라운드 롱폼 (2026-11-19)

상태: **렌더 완료 (renders/video.mp4), 대표님 미리보기 대기** — publish 브랜치 게시 안 함

## 품질 점검 4줄
① 모션그래픽 장면 **13/13** (정지 슬라이드 0, 정지 이미지+확대만 있는 장면 0, 얼굴·인물·HeyGen 0) — 달력 24칸 채움, 블록 낙하 ECE 조립, BC 지도 데이캐어 핀 확산 + 153 카운트업, 기간 막대 레이스·결승 깃발, 학비 49,009 / 20,282 카운트업 + 생활비 적층, 주당 근무시간 게이지(24시간 제한선 vs ∞), 캐나다 개념도 노트북 이동·자격 카드 뒤집힘·46주→38+8주 분할·주간 시간표, 시급 카운트업·월수입 범위 막대, 이력서 References 하이라이트·추천 말풍선·0→500시간·자격 계단·+$6 배지, PGWP 카드 vs 워홀 카드 비행, 자격 복제 연결선, 4년 타임라인, 체크리스트 도장, 최종 1:7 집계·비교표 행 순차 등장. **상단 스코어보드(ROUND 1~8)** 가 s03~s10 내내 떠 있고 라운드 끝마다 빨간 도장(사립 7, 공립 1 — 라운드 7만 공립)
② 배경음악 **ElevenLabs 음악 생성 신곡 2곡** `audio/bgm/el_ece_acoustic_A.mp3`(우쿨렐레·어쿠스틱 기타·피아노, 96BPM) · `el_ece_acoustic_B.mp3`(피아노·핑거피킹 기타·우쿨렐레·글로켄, 98BPM), 가사 없음, 약 3분씩 A→B→A 4초 크로스페이드 · 내레이션을 키로 한 **sidechaincompress 덕킹**(내레이션 구간 BGM이 내레이션보다 약 23.5dB 낮음) · 시작 1.5초 페이드인, 끝 3초 페이드아웃
③ 효과음 **56개** (transition_ding 14 · tick 17 · ding 14 · stamp 11) — 어느 60초 구간이든 4~8개(자동 점검 `tools/sfx_density.py`), 위치는 HyperFrames 애니메이션 시작 시각, 내레이션보다 약 12~13dB 낮게, whoosh(거친 스우시) 미사용
④ 최종 오디오 **-16.1 LUFS / 트루피크 -3.3 dBTP** (최종 MP4에서 디코딩해 측정) (목표 -16±0.5 / -1.5 이하) · 내레이션은 장면별 -16 LUFS로 맞춘 뒤 마스터 투패스 loudnorm, BGM이 말소리 아래 약 23.5dB라 내레이션 또렷함 · ElevenLabs 음성인식으로 13개 장면을 다시 받아 적어 누락·오독 없음 확인(`audio/vo/stt/`)

## 산출물
- `renders/video.mp4` — 1920×1080, 30fps, **9분 02초** (44MB → 90MB 미만이라 분할 커밋하지 않음 · sha256 b5d0f8f2…bb5cf · 채팅 전송용 재생 가능 분할본 renders/chat/part0·part1)
- `thumbnail.jpg` / `thumbnail.png` (1280×720, 좌우 대결 구도, 인물 없음)
- `upload-text.txt` (제목·설명·챕터·출처·태그·AI 사용 공개 메모)
- HyperFrames 프로젝트: `index.html` + `compositions/s01~s13.html` (원본은 `src/`, `tools/build.py` 로 생성)

## 진행하며 내린 판단 (대표님 확인용)
1. **영상 길이 9분 02초** — 브리프 예상(11~12분)보다 짧습니다. NARRATION.txt 문장을 고치지 말라는 지시대로 ElevenLabs 음성 길이에 그래픽을 맞춘 결과입니다(음성 합계 약 8분 39초).
2. **라운드 4 학비 차이 표기**: SCRIPT 표에는 "약 2만 9천 불", 내레이션은 "약 3만 불"이라 화면은 내레이션과 같은 **"차이 약 3만 불"** 로 했습니다(자막과 일치).
3. **라운드 3(입학·공부)**: 숫자가 없는 비교라 "공부 부담" 게이지(높음/가벼움)를 개념 표시로 넣었습니다(수치 없음).
4. **캐나다 지도**는 주를 블록으로 단순화한 개념도이며 화면에 "지도는 개념도입니다" 표기를 넣었습니다.
5. **s13 비교표**는 SCRIPT.md 4장 문구 그대로 11행을 순서대로 띄웠습니다. 화면이 빽빽해 글자 크기가 25px라 휴대폰에서는 작게 보일 수 있습니다(요약 카드 3장은 크게).
6. 대본에 없던 짧은 보조 문구: "이 중 딱 1과목만 마치면", "먼저 졸업!", "공부 부담 높음/가벼움", "FINAL" — 모두 내레이션 내용 범위 안의 표시입니다. 사립 학교 이름·커미션 관련 내용은 어디에도 없습니다.
7. 자막은 SCRIPT.md 3장 표기(ECE, BC, PGWP, One Year, Five Year, AA Canada, 아라비아 숫자)를 내레이션 타임스탬프에 맞춰 자동 분할했습니다. 하단 각주는 s02~s12에 상시 표시.
8. 무손실 마스터 `audio/mix_master.wav` 는 용량 때문에 커밋하지 않고(`tools/mix.py` 로 재생성), 컴포지션에는 AAC 사본 `audio/mix.m4a` 를 연결했습니다.

## 다시 만들기
```bash
python3 tools/tts.py            # (필요 시) 내레이션 재생성
python3 tools/music.py          # (필요 시) 배경음악 재생성
python3 tools/build.py          # 타이밍·자막·효과음 큐 → compositions/, index.html
python3 tools/sfx_density.py    # 효과음 분당 개수 점검
python3 tools/mix.py            # 오디오 믹스 → audio/mix_master.wav, audio/mix.m4a
npx hyperframes render --crf 20 --output renders/render_raw.mp4
bash tools/finalize.sh          # 마스터 오디오 합본 + 라우드니스 확인 + (90MB 초과 시) 분할
```
