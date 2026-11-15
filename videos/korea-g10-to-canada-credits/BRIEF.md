---
workflow: general-video
flow: companion
storyboard: yes
message: "한국 고1 수료 후 캐나다 11학년 편입 — BC는 인정 범위가 좁아 핵심 과목을 현지에서 보통 2년, 온타리오는 교장 재량(PLAR) 인정 후 최소 14학점"
destination: youtube
aspect: 1920x1080
language: ko
audience: 캐나다 자녀 유학·편입을 검토하는 한국 학부모
length: 약 3분 30초 (실제 내레이션 기준 209초)
angle: 비교 설명 (한 학생 사례: 졸업 요건 → 한국 학점 인정 → 캐나다 학점 취득)
voice: ElevenLabs S2nra0Bd5UeFVzGK3oaH (아홉번째 자연톤, eleven_v4, stability 0.8, similarity 0.75, 문단마다 [calm])
---

## Intent

AA Canada(에이에이캐나다) 유튜브·홈페이지용 설명 영상. 한국에서 고1을 마치고 캐나다 Grade 11로 들어가는 학생(가명 민준)이
졸업장을 받기까지를 BC주와 온타리오주로 나눠 비교한다. 순서: 졸업 요건 설명 → 한국 학점 인정 → 캐나다에서 학점 취득.
스토리라인 A "민준이의 학점 블록 쌓기"(BC 4학점×20칸, 온타리오 1학점×30칸 블록 틀이 채워지는 분할 화면) 확정.

## Assets

- assets/heygen/intro.mp4 — 대표님 HeyGen 얼굴 영상(5~10초), 어사이드로 대표님이 직접 제작해 업로드 예정. 화면 1/3 크기 둥근 창, 영상 맨 앞.
- assets/heygen/outro.mp4 — 같은 방식, 영상 맨 뒤.
- assets/fonts/Pretendard-*.woff2 — 한글 폰트(오픈 라이선스, npm pretendard@1.3.9).

## Customizations

- 본문 장면에는 얼굴 없이 그래픽만.
- HeyGen API 키 입력창은 띄우지 않는다(대표님 지시).
- 최종 렌더·게시는 대표님 스토리보드 검토 후에만.

## Notes

- BC Literacy 10: "11·12학년 편입생은 면제 신청 가능"(Numeracy 10, Literacy 12는 필수)로 표기.
- 온타리오 금융문해: "2년 이수 편입생은 면제"만 짧게.
- 공식 원문 미확인 수치(PLAR 16학점 상한 등)는 넣지 않음. 필요하면 "학교별 확인 필요".
- 주의 문구: 최종 인정 학점은 학교와 교육청의 평가에 따라 달라짐.
- 출처: BC Graduation Requirements · BC International Student Graduation Credit Policy · Ontario: Earning your high school diploma · Ontario Schools K-12: Student records and transfers
- 대표님 얼굴(HeyGen)은 **항상 작게**: 둥근 창 지름 520px, 원본을 0.5배로 넣어 머리~어깨와 배경 국기가 보이게. 이보다 크게 하지 않는다.
