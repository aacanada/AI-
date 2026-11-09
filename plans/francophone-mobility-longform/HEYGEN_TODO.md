# HeyGen 얼굴 클립 교체 방법 (S1 오프닝 / S9 엔딩)

이번 렌더(2026-11-09)는 HeyGen API(api.heygen.com)에 접근할 수 없어 S1·S9를 타이틀/요약 그래픽 + 내레이션으로 만들었습니다.

1. HeyGen에서 대표님 디지털 트윈으로 audio/S1.mp3, audio/S9.mp3 를 립싱크해 1920x1080 30fps로 받습니다.
2. heygen/S1_face.mp4, heygen/S9_face.mp4 로 저장합니다.
3. 다시 빌드·렌더합니다:
   cd video && python3 build.py && npx hyperframes render -o ../render_raw.mp4 --quality standard
   (build.py가 얼굴 영상을 감지해 전체 화면 얼굴 + 하단 타이틀/연락처로 바꾸고, S1/S9 mp3는 빼고 클립 오디오를 씁니다.)
4. 렌더 후 -16 LUFS 맞추기:
   ffmpeg -i render_raw.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a aac -b:a 192k video.mp4
