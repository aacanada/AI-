# 이 샌드박스에서 막히는 것과 우회책 (2026-10-03 검증)

| 문제 | 증상 | 우회 |
|---|---|---|
| CDN 차단 (cdn.jsdelivr.net, unpkg) | GSAP·폰트 로드 실패, 403 | `setup_project.sh`가 npm 레지스트리(허용)에서 `npm pack`으로 GSAP·Pretendard를 받아 `assets/`에 넣음. `post_assemble.sh`가 index의 CDN 스크립트를 로컬로 교체 |
| 자막 폰트 충돌 | `hyperframes check` → Runtime "Maximum call stack size exceeded" | captions.html의 Pretendard @font-face(800→Black)가 장면 쪽(800→ExtraBold)과 달라서 생김. `post_assemble.sh`가 장면의 @font-face로 통일 |
| HeyGen 미로그인 | 기본 TTS/BGM/SFX 불가 | 음성은 `tts_elevenlabs.py`. BGM은 현재 없음 — 사용자에게 "쇼츠 앱에서 음악 추가" 또는 음악 파일 제공을 안내 |
| Whisper 모델 다운로드 403 | `hyperframes transcribe` 실패 → 단어 0개 | 일레븐랩스 `/with-timestamps` 응답의 글자 타이밍으로 단어 타이밍 생성 (스크립트에 내장) |
| 일레븐랩스 forced-alignment 권한 없음 | 401 missing_permissions | 사용하지 않음 (위 방식) |
| 일레븐랩스 동시 요청 제한 | 병렬 생성 시 일부 줄 실패 | 스크립트가 순차 호출 + 429 재시도 |
| 일레븐랩스 엔진 기본 출력 | `.wav` 이름에 mp3 내용 | 스크립트가 ffmpeg로 PCM wav 변환 |
| 스냅샷 비교 시 HTML 여러 개 | 프로젝트 폴더에 다른 .html이 있으면 check가 엉뚱한 파일을 볼 수 있음 | 실험용 index 사본은 프로젝트 밖에 둔다 |

## 이미지 좌표 확인 (줌·하이라이트 전에 필수)

이미지 위 박스/줌은 원본 픽셀 좌표로 계산한다. 먼저 상자를 그려서 눈으로 확인:
```bash
ffmpeg -y -loglevel error -i assets/images/x.jpg -vf "drawbox=x=550:y=700:w=200:h=124:color=red@0.9:t=4" /tmp/chk.png
```
줌 계산 (템플릿 방식): 창(window) W×H 안의 stage에 원본 크기 이미지를 두고 `transform-origin:0 0`. 원본 점 (cx,cy)를 배율 s로 창 중앙에 두려면 `x = W/2 − cx·s`, `y = H/2 − cy·s`, 그다음 `x ∈ [W − imgW·s, 0]`, `y ∈ [H − imgH·s, 0]`로 클램프. 하이라이트 rect/SVG는 stage 안에 넣어 함께 확대되게 한다. 한 행 전체(라벨+막대+값)가 보여야 하면 배율을 `0.95·W / 행너비` 이하로.

## 검증 루틴

`npx hyperframes check` 통과(Runtime·Layout·Contrast) → `npx hyperframes snapshot --at <장면별 끝>` 후 contact-sheet를 직접 본다. 대비 경고는 `text-light`를 한 단계 진하게 하면 대개 해결. "overlapping_gsap_tweens" 경고는 같은 요소의 입장 트윈이 다음 이동 트윈 시작 전에 끝나도록 duration을 줄인다.
