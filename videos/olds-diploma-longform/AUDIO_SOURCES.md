# 오디오 출처·라이선스 (Olds EP2 롱폼, 음성 교체판 2026-11-01)

| 용도 | 파일 | 출처 | 라이선스 |
|---|---|---|---|
| 내레이션 | `../../plans/olds-diploma-longform/audio/oldsdip_s01.mp3` ~ `s09.mp3` → `assets/voice/sNN.wav` | ElevenLabs TTS, AA Canada 계정의 "여덟번째" 목소리(voice_id `cbVXtFGe9VfUKWtbYIty`), 모델 `eleven_multilingual_v2`. 요청 기록 `plans/olds-diploma-longform/audio/tts_log.json` | AA Canada 계정 생성물(ElevenLabs 유료 플랜 상업 이용). 유튜브 설명란에 AI 음성 표기 유지 |
| 배경음악 | `assets/music/bgm_vanesl.mp3` (150초, 3초 크로스페이드로 반복) | 밴쿠버 롱폼 때 ElevenLabs Music으로 생성한 곡 재사용 (브랜치 `claude/beautiful-ptolemy-4l997y`, `plans/vancouver-esl-free-edu/video/bgm_vanesl.mp3`, 커밋 d8a2e9c). 몬트리올 롱폼(2026-10-31)과 같은 곡 | AA Canada 계정 생성물(ElevenLabs Music 상업 이용) |
| 효과음: 장면 전환 whoosh | `assets/sfx/soft-whoosh.wav` | `tools/sfx_synth.py`로 직접 합성(노이즈 + 밴드패스 스윕, 샘플 사용 없음) | 자체 제작, CC0 1.0으로 공개 |
| 효과음: 장면 시작 클릭 | `assets/sfx/soft-click.wav` | `tools/sfx_synth.py`로 직접 합성(사인파 버스트) | 자체 제작, CC0 1.0으로 공개 |

## 이번 판에서 쓰지 않은 기존 오디오
- `assets/music/bgm-a.mp3`, `bgm-b.mp3` (기존 4:09 영상의 BGM): "royalty-free"라고만 적혀 있고 원 출처·라이선스 기록이 저장소에 없어 이번 판에서는 쓰지 않았습니다. 파일은 그대로 둡니다.
- `assets/sfx/impact.mp3`, `pop.mp3`, `stamp.mp3`, `whoosh.mp3` (HyperFrames 번들, Pixabay Content License, `assets/sfx/CREDITS.md`): 효과음을 전환부 whoosh/클릭으로 줄이기로 해서 장면 안 효과음은 껐습니다(`SCENE_SFX=1`로 다시 켤 수 있음).
