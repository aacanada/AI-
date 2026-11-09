# VIDEO_BRIEF: 프랑코폰 모빌리티 롱폼 (plans/francophone-mobility-longform/)

Reports in Korean. Build with HyperFrames, render 1920x1080, 30 fps, 16:9. Target loudness -16 LUFS.

## Inputs (this folder)
- SCRIPT.md: 장면별 대본. 화면 큐는 각 장면 "- 화면:" 줄.
- audio/S1.mp3 ... S9.mp3: ElevenLabs 내레이션 (대표님 복제 음성, stability 0.8, 장면당 1파일).
- heygen/S1_face.mp4, heygen/S9_face.mp4: HeyGen 디지털 트윈 (아직 없음, api.heygen.com 접근 불가). 들어오면 composition의 얼굴 자리(placeholder)를 교체. 이 클립 오디오를 쓰면 S1/S9 mp3는 중복 재생하지 말 것.
- BGM: 잔잔한 피아노/앰비언트, 내레이션 아래 덕킹.

## Structure
- S1 / S9: 얼굴 전체 화면 (placeholder: 대표님 이름 카드), S1 하단 타이틀 "컬리지 없이 캐나다 취업비자?", S9 하단 "무료 상담 aacanada.co.kr / 02-567-4345", 끝 3초 엔드카드.
- S2~S8: SCRIPT.md "- 화면:" 큐대로 모션그래픽.

## Rules
- 한국어 자막(대본 텍스트, [calm] 제외).
- 화면에 출처 표기 넣지 않음.
- 최상급 표현("가장", "최고", "100%") 금지. 커미션 정보 금지.
- 결과물: video.mp4 (100MB 넘으면 분할 + sha256), thumbnail.jpg 1280x720 ("컬리지 없이 캐나다 취업비자? 불어 NCLC 5로 LMIA 면제").
