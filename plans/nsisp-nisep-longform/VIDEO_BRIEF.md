# VIDEO_BRIEF: NSISP vs NISEP 롱폼 (plans/nsisp-nisep-longform/)

Reports in Korean. Build with HyperFrames, render 1920x1080, 30 fps, 16:9. Target loudness -16 LUFS (measure after render; fix by lowering/raising the audio track).

## Inputs (this folder)
- SCRIPT.md: 장면별 대본 (NSISP_vs_NISEP_롱폼_대본_v1.md). 화면 큐는 각 장면 "- 화면:" 줄.
- audio/S1.mp3 ... S9.mp3: ElevenLabs 내레이션 (대표님 복제 음성, 장면당 1파일). 길이(초): S1 29.2, S2 35.8, S3 26.3, S4 24.9, S5 63.5, S6 46.7, S7 30.1, S8 22.2, S9 30.1. 합계 약 5분 8초.
- heygen/S1_face.mp4 (29.2s), heygen/S9_face.mp4 (30.1s), 둘 다 1920x1080 30fps로 재압축됨: 대표님 디지털 트윈, 위 S1/S9 오디오로 립싱크됨. 이 클립의 오디오를 그대로 쓰고 S1/S9 mp3는 중복 재생하지 말 것.

## Structure
- S1: HeyGen 얼굴 전체 화면, 하단 타이틀 "NSISP vs NISEP".
- S2~S8: 오디오 길이에 맞춘 HyperFrames 모션그래픽 (각 장면 "- 화면:" 큐 참고).
  - S2 대서양 캐나다 지도 (핼리팩스, 세인트존스 핀), 학교 수 카운트업 65 / 30+20.
  - S3 좌우 비교 카드 "지역 배정 / 학교 희망 요청".
  - S4 아이콘 인원 그래픽 (국가별 최대 7명 / 유학생 2.5% 이하).
  - S5 NISEP 항목 막대가 쌓여 21,950 카운트업 (학비 9,500, 홈스테이 10,850, 보험 700, 지원 400, 행정 250, 오리엔테이션 250), 2027-28 22,450 보조 표기, 마지막에 "공식 가격표 그대로 / 수속비 0원" 도장.
  - S6 홈스테이 체크리스트가 하나씩 켜짐.
  - S7 타임라인 (졸업 최소 1년 / 2년), 대학 혜택 텍스트 카드 (로고 없이).
  - S8 두 갈래 선택 그래픽.
- S9: HeyGen 얼굴, 하단 "무료 상담 aacanada.co.kr / 02-567-4345", 끝에 3초 엔드카드.
- 장면 전환 0.3~0.5초, 장면 사이 0.5초 여백.

## Rules
- 한국어 자막(대본 텍스트 기준, [calm] 태그 제외). 자막 타이밍은 무음 구간 기준으로 나눠도 됨.
- 화면에 출처 표기 넣지 않음 (출처는 유튜브 설명란에만).
- 최상급 표현("가장", "최고", "최저", "100%") 금지.
- NSISP 비용 숫자는 화면에 넣지 않음.
- 커미션 정보 절대 넣지 않음.
- NSISP를 깎아내리는 표현 금지. 사실 비교만.
- 결과물: video.mp4 (GitHub 100MB 제한 넘으면 -c copy 분할 + sha256), thumbnail.jpg (1280x720, "NSISP 알아보셨다면? 뉴펀들랜드 NISEP 비교"). 게시용 READY 파일은 만들지 말 것.

