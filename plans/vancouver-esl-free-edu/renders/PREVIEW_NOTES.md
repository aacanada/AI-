# 밴쿠버 자녀무상교육 롱폼 — 대표님 미리보기 (2026-10-27)

- 파일: `renders/video.mp4` (1920x1080, 30fps, H.264 + AAC 192k), 길이 5:14.16, 통합 음량 -16.0 LUFS, 트루피크 -1.4 dBFS
- 음성: ElevenLabs "여덟번째"(voice_id cbVXtFGe9VfUKWtbYIty) + eleven_multilingual_v2, Stability 0.5 / Similarity 0.75 (`audio_v2/`)
- 상태: 미리보기 전용. publish 브랜치·READY·업로드·쇼츠 없음.

## 장면 시작 시각 (유튜브 챕터용)
0:00 오프닝: 영어 점수 없어도?
0:24 원리: 아이가 거주자로 인정되는 조건
0:54 부모가 학생일 때 기본 조건 (사립은 학위)
1:24 핵심 조항: 어학연수 최대 1년 인정
2:16 밴쿠버 교육청(VSB) FAQ도 똑같이
2:41 알렉산더 컬리지 조건부 입학허가
3:33 AA Canada 추천 플랜 A / B
4:22 신청 전 꼭 확인할 3가지
4:52 마무리 · 상담 안내

## 분할 파일 합치기 (채팅 첨부본)
- Mac/Linux: `cat video.mp4.part_00 video.mp4.part_01 > video.mp4`
- Windows(cmd): `copy /b video.mp4.part_00 + video.mp4.part_01 video.mp4`
- 확인(SHA-256): 509261dd4e0f4d9faad777645efe8aafcbd7c6f84d80efb8ca4fab9bc1ad2d94

## 발음 확인 (ElevenLabs Scribe 음성인식으로 대조)
- 숫자 5,000달러 / 17,000달러 / 1,400달러 / 2027-28 / 2011년 / 2013년 / 듀오링고 90 / 아이엘츠 5.0, 약어 EQA·BC, 학교 이름 ILSC·Kaplan·SGIC·Oxford International·CCEL·VGC: 정상
- s06 "밴웨스트": 원문 입력 시 'VANEST/Vawest'로 읽혀 TTS 입력만 "밴 웨스트"로 바꿔 재생성 → 정상
- s09 "AA Canada": 일부 'A카나다'로 읽혀 TTS 입력만 "에이에이 캐나다"로 재생성 → 정상
- s09 "canlog": 원문 입력 시 '찰롱'. TTS 입력 "캔로그"/"캔 로그"로 4회 재생성, 인식 결과 '캣로그'·'캔록' 사이 → 가장 '로그'가 분명한 버전 사용. 대표님 귀로 최종 확인 필요.
- 화면 자막은 모두 대본 원문 그대로.

## 재생성 방법
- 시간표: `python3 video/tools/timing.py video/asr_v2 audio_v2` → `video/timing.json`
- 화면: `python3 video/tools/build.py` → `hf/index.html`, 렌더: `cd hf && npx hyperframes render -o ../renders/video_silent.mp4 --fps 30 --page-side-compositing`
- 오디오: `python3 video/tools/mix.py audio_v2 video/bgm_vanesl.mp3 renders/mix_v2.m4a` (BGM은 ElevenLabs Music으로 새로 생성 — 기존 롱폼 BGM 파일이 저장소에 없음)
- 합치기: `ffmpeg -i renders/video_silent.mp4 -i renders/mix_v2.m4a -map 0:v -map 1:a -c copy -movflags +faststart renders/video.mp4`
