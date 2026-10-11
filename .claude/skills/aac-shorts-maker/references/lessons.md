# 함정과 해결 (첫 작품 제작 로그에서)

| 증상 | 원인 | 해결 |
|---|---|---|
| 웹 폰트/GSAP 로딩 실패, `CONNECT tunnel failed 403` | 클라우드 컨테이너가 `cdn.jsdelivr.net` 차단 | 폰트와 GSAP은 이 스킬의 `assets/`에서 프로젝트로 복사. `captions.mjs`와 `assemble-index.mjs`는 CDN 주소를 다시 쓰므로 **lint/check/render 직전에 `offline-fixups.sh` 실행** |
| npm 패키지 파일이 필요함 | jsdelivr 차단, npm 레지스트리는 열림 | `npm pack <pkg>@<ver>` 후 tgz에서 추출 |
| HeyGen 미로그인 → Kokoro 의존성 없음 | 한국어 클론 보이스 없음 | `el-tts.mjs`(ElevenLabs `/with-timestamps`)로 대체. 글자 단위 정렬을 공백 기준으로 묶어 단어 타이밍을 만든다 |
| `frame packet is 50233 bytes (limit 48000)` | 한 장면에서 인용한 규칙 레시피가 너무 많음 | Scene 라인에서 덜 중요한 규칙 id 하나를 지우고 말로만 묘사 |
| 블루프린트가 패킷에 안 들어감 | `- blueprint/focal/roles` 줄을 프로즈(narrativeRole 아래)에 둠 | 반드시 프레임 메타데이터 bullet 목록 안(`- beat:` 다음)에 둔다 |
| lint `id_requires_css_escape` 경고 다수 | 프레임 id가 숫자로 시작(`09-caveat-…`) | 워커가 클래스/속성 셀렉터를 쓰면 동작에는 문제 없음. 디스패치 문맥에 "id/class는 영문자로 시작하는 접두사 사용(예: f09-)"을 넣으면 깔끔해짐 |
| check `content_overlap` 에러 | 의도된 롤링 숫자(5,000→4,999)가 겹침 | 두 요소에 `data-layout-allow-overlap` 추가 |
| check 대비(contrast) 경고 | 일부러 흐리게 처리한 회색 카드 | 의도된 것이면 그대로 둔다. 핵심 텍스트라면 #6b6b6b 이상으로 진하게 |
| 화면 숫자와 서사가 어긋남 | 장면 설계에서 계산 실수 | 컨셉 단계에서 숫자 일관성 점검(예: 커트라인 84, 첫 탈락자 81이면 "-3점") |
| 스톱 훅 "untracked files" | 저장소 규칙 | 단계마다 커밋하고 작업 브랜치에 푸시 |
| 총 길이가 예상보다 짧음 | 실제 음성 길이가 우선함 | 정상. `sync-durations`가 프레임 길이를 음성에 맞춘다. 손으로 고치지 않는다 |

## 렌더 성능 참고
1분 43초 영상, 소프트웨어 GPU 기준 렌더에 약 6분, 결과 파일은 약 23MB였다. 장면 10개를 병렬로 빌드하는 데 약 2–3분 걸렸다.
