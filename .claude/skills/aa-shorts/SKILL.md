---
name: aa-shorts
description: AA Canada 숏폼 자동 제작 — 원장님이 주제만 주면 대본 작성 → (확인) → ElevenLabs 원장님 목소리 음성 → 9:16 유튜브 쇼츠/릴스 영상까지. "주제: ○○ 숏폼 만들어줘", "이 주제로 쇼츠", "대본 만들어줘", "일레븐랩스에서 만든 음성으로 영상 만들어줘", "방금 만든 음성 가져와서 영상" 같은 요청에 사용. 기존 videos/<slug> 프로젝트의 대본 수정·재녹음·재렌더에도 사용.
---

# AA Canada 숏폼 파이프라인

주제 → **대본** → ⏸ 원장님 확인 → **음성** (A: API 생성 / B: 원장님이 사이트에서 생성한 것 가져오기) → **프레임** → **완성·렌더** → MP4 전달.
기준 작품: `videos/montreal-english/` (대본 `SCRIPT.md`, 프레임 `compositions/frames/`). 새 영상의 톤·구성·코드 모두 이것을 출발점으로 삼는다.

`$SK` = `.claude/skills/aa-shorts/scripts`, `$P` = `videos/<slug>` (주제를 영어 kebab-case로, 예: `montreal-free-education`).

## 0. 원장님 / 브랜드 사실 (대본·화면에 그대로 사용)

- AA Canada: 캐나다 전문 유학원. 주력 = 캐나다 자녀무상교육, 유학 후 이민, 영주권. 지역 = 몬트리올(최우선), 밴쿠버, 토론토, 온타리오 런던.
- 현재 핵심 메시지: 몬트리올 사립컬리지 + 자녀무상교육, 퀘벡 정부 불어수업 → Francophone mobility(LMIA 면제 취업비자) → 영주권 루트. "불어권이라 영어가 안 는다"는 오해 해소.
- 연락처(CTA 화면): 카카오톡 **canlog** · **02-567-4345** · 필요 시 하단 작은 글씨 "학비 프로모션·학생비자 접수는 선착순으로 제한될 수 있어요".
- 음성: ElevenLabs 원장님 클론 `$ELEVENLABS_VOICE_ID`(환경변수, 원장님이 바꾸면 그 값을 따른다) · `eleven_multilingual_v2`.

## 1. 대본 (항상 여기서 멈추고 확인받기)

1. `python3 $SK/new_project.py <slug> --title "<제목>"` 로 프로젝트 생성.
2. `$P/SCRIPT.md` 작성 — 형식은 `videos/montreal-english/SCRIPT.md` 그대로: 헤더(형식/대상/핵심 메시지/Voice/Voice direction/숫자 근거) + `## Line N — <라벨> (Frame N)` 마다 `**화면:**`, `**Delivery:**`, 4칸 들여쓴 낭독 텍스트.
   - 50–60초, 6–8줄. 훅(학부모 걱정/질문) → 반전 → 근거 2–4개(숫자·실물 근거) → CTA("AA캐나다가 함께하겠습니다").
   - 차분하고 신뢰감 있는 상담 선생님 말투, 학부모 대상 존댓말.
   - **숫자는 지어내지 않는다.** 학비·비용·비율은 원장님이 준 값만. 없으면 대본에 `[확인 필요: …]`로 표시하고 물어본다. 계산(차액, 튜터 비용 등)은 직접 검산하고 헤더 `**숫자 근거:**`에 식을 적는다. 계산이 원장님 주장과 맞지 않으면(예: 차액 < 비용) 숫자를 조정한 안을 제시하고 그 이유를 말한다.
3. 원장님께 **자막용 대본**과 **ElevenLabs 붙여넣기용 발음 버전**(숫자 한글 풀어쓰기, 불어꿘, 퍼센트, 에이에이 캐나다, 필러 유발 쉼표 제거)을 채팅으로 보여주고, 아래 둘 중 어떻게 녹음할지 묻는다. **승인 전에는 음성을 만들지 않는다.**
   - A. "이대로 녹음해줘" → 2A
   - B. 원장님이 ElevenLabs 사이트에서 직접 생성 → "만들었어" 하면 2B
4. 커밋·푸시(대본만).

## 2A. 음성 — API로 생성

`python3 $SK/tts.py --project $P` — 줄마다 생성 → STT로 검증 → "어,/뭐/음" 필러나 대본 이탈이 있으면 자동 재녹음(최대 6회). 특정 줄만: `--only 3,5`.
- 오독이 반복되면 `voicelib.py`의 `SAY` 표에 발음 규칙을 추가(음성에만 적용, 자막은 대본 표기 유지)하고 그 줄만 다시.
- 출력 로그의 `heard:` 문장을 원장님께 보여줄 필요는 없지만 직접 읽고 이상하면 재녹음.

## 2B. 음성 — 원장님이 사이트에서 만든 것 가져오기

`python3 $SK/import_audio.py --project $P --dry-run` 으로 어떤 생성 기록이 잡히는지 확인 후, 같은 명령에서 `--dry-run` 빼고 실행.
- 줄별로 생성했든 전체를 한 번에 생성했든 자동 판별(가장 최근 것 우선). 전체 녹음은 문장 사이 쉼에서 줄별로 자른다.
- 특정 기록 지정: `--ids <id>` (전체 1개) 또는 줄 수만큼 `--ids a,b,c…`. 파일로 받은 경우(구글 드라이브 등): `--file x.mp3`.
- 타이밍은 STT로 뽑아 대본 표기에 맞춘다 → 원장님이 애드리브해도 자막은 대본 표기. 로그의 `heard:`가 대본과 크게 다르면 원장님께 알린다.

## 3. 스토리보드 + 프레임

1. `$P/STORYBOARD.md` — `videos/montreal-english/STORYBOARD.md` 형식(frontmatter `format: 1080x1920`, `music: none`, `mode: autonomous` + `## Video direction` + `## Frame N` 블록: scene/duration/transition_in/status: animated/voiceover/src/blueprint/focal/roles + Scene 줄). duration은 아무 값이나 — 4단계가 실제 음성 길이로 덮어쓴다. transition_in: 1번 `cut`, 이후 `crossfade` / `push-slide UP|LEFT` 교대.
2. `$P/scripts/build_frames.py` 작성 후 실행 — `framekit.Kit` 사용(사용법은 `$SK/framekit.py` 상단). 참고 구현: `videos/montreal-english` 프레임들(훅 타이포, 막대 비교, 카운트업, 계산식, 교실 다이어그램, CTA).
   - 모든 등장은 `k.W(frame, "단어")`로 그 단어가 들릴 때 큐. 처음에 다 띄우지 말 것.
   - 화면 글씨는 짧은 키워드/숫자만(낭독 문장을 화면에 반복하지 않는다 — 자막이 따로 있음).
   - 콘텐츠는 stage 좌표 y≈250–1580 안. **자막은 항상 화면 위쪽**(finish.py가 처리) — 하단은 쇼츠 UI 영역이라 비워둔다.
   - 한글 폰트는 Pretendard(템플릿 포함)만. 외부 이미지·폰트 URL 금지(렌더 환경 차단). 원장님 제공 이미지는 `$P/assets/`에 두고 `assets/<파일>`로 참조.
   - CTA는 마지막 프레임, 연락처는 0번 섹션 그대로.

## 4. 완성·검수·렌더

`python3 $SK/finish.py --project $P --snapshot` → `snapshots/contact-sheet.jpg`를 **직접 열어 확인**(글자 겹침, 잘림, 빈 화면, 숫자 오타). 고칠 게 있으면 build_frames.py 수정 → 재실행 → finish 다시.
문제없으면 `python3 $SK/finish.py --project $P --render` → `renders/video.mp4`.
- lint/check 실패 시 메시지가 가리키는 프레임 요소를 고친다(무시하지 말 것).

## 5. 전달

- SendUserFile로 MP4 전달 + 짧은 요약(장면 구성, 재녹음/발음 처리한 것, 원장님이 판단할 것).
- `$P/BRIEF.md`에 결정사항(음성 ID, 숫자 근거, 발음 처리) 기록, 커밋·푸시(작업 브랜치). `snapshots/`는 gitignore.

## 원장님 선호 (누적 — 새로 알게 되면 여기에 추가)

- 유튜브 쇼츠 자막은 **항상 위쪽**.
- "불어권"은 **불어꿘**, "%"는 **퍼센트**로 읽기.
- 영어 실력 주제에서는 "수업 중 친구들과의 소통이 100% 영어"가 핵심(쉬는 시간보다 수업 시간 강조).
- 몬트리올 영어 영상에서는 "불어는 덤" 내용을 뺐다 — 비슷한 주제에서 쓰기 전에 확인.
- BGM 없음(업로드 시 플랫폼 음원 사용).
