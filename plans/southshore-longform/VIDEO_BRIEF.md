# 몬트리올 사우스쇼어 지도 롱폼 (원장님 음성, 얼굴 없음)

작성: 2026-10-22 · 요청: AA Canada 원장님 · 형식: 원장님 직접 녹음 내레이션 + 전 화면 그래픽(지도 모션그래픽 중심) + 학교 영상 B-roll

관련 작업: 퀘벡 조기유학(Riverside) 마케팅 플랜, 브랜치 `claude/fervent-allen-gq37dp`의 `plans/riverside-marketing/`, `plans/riverside-schools/` (학교 문서 14개, 카드 이미지). 숫자와 표현 규칙은 그쪽 문서를 따른다.

## 1. 목적과 핵심 메시지
- 타깃: 초3~고2 자녀를 둔 한국 부모. 밴쿠버·토론토만 보다가 "몬트리올은 불어라서" 제외한 사람.
- 한 줄: **"다운타운까지 REM으로 18분, 한국 사람이 거의 없는 몬트리올 남쪽 영어 공립학교 생활권"**
- 이 영상은 Riverside 학교 시리즈(블로그·홈페이지, 매주 목요일 발행)의 "입구" 역할. 지역 → 동네 → 학교 순서.

## 2. 오디오 (원장님 녹음 예정, 장면당 1파일)
`plans/southshore-longform/audio/ss_s01.m4a` ~ `ss_s10.m4a` (아직 없음. 녹음되면 Aside가 올림)
- 대본: 같은 폴더 `SCRIPT.txt`. 예상 길이 10~11분.
- **녹음 전에는 무음(가짜 타이밍)으로 먼저 전체를 만들어 둘 것.** 녹음이 오면 ASR로 타이밍을 맞추고, 대본과 다르게 읽은 줄이 있으면 렌더 전에 보고.
- 앞뒤 무음 0.3s만 남기고 트림, 장면 사이 0.4s 여백. 내레이션 -16 LUFS, BGM은 그 아래 (Olds·영유 롱폼과 같은 방식, 같은 BGM 재사용 가능).

## 3. 화면 구성 (16:9 1920x1080 30fps)
- 브랜드: 영유 롱폼과 같은 "메이플 레드" 템플릿 (배경 크림 #FFF8F2, 레드 #C8102E, 본문 #2B2B2B, 하이라이트 #FFD6CF, 서브 #7A1B26, Black Han Sans + Noto Sans KR). 지도에서 강(물)만 옅은 청회색 허용, 그 외 파란색 계열 금지.
- 로고: `plans/yeongyu-montreal-longform/assets/aa-canada-logo-transparent.png` (우하단 작게 상시).
- 하단 자막: 내레이션 전체 한국어 자막 (2줄 이내, 숫자는 레드 강조).
- 한 화면을 25초 넘게 정지 상태로 두지 말 것. 숫자는 내레이션 타이밍에 맞춰 등장.
- 숫자 화면에는 작은 출처 표기를 붙인다 (아래 6장).

### 3-1. 지도 (이 영상의 주인공)
- 스타일: 단순한 벡터 지도. 몬트리올 섬, 세인트로렌스 강, 남쪽 강변 도시들, 다리, REM 노선, 학교 핀. 실사 위성사진 불필요.
- 지도 데이터: OpenStreetMap(Overpass/Geofabrik) 또는 Natural Earth 등 오픈 데이터를 쓸 수 있으면 쓰고, OSM을 쓰면 화면 구석에 "지도 데이터 © OpenStreetMap contributors" 표기. 네트워크가 막히면 아래 좌표로 **양식화된(스키매틱) 지도**를 직접 그려도 된다. 정확한 해안선보다 "섬 / 강 / 남쪽 강변"이 한눈에 보이는 게 중요.
- 주요 좌표 (OSM Nominatim, 2026-10-22 조회, 위도,경도):

| 지점 | 좌표 |
|---|---|
| REM 브로사드역 (종점) | 45.4374,-73.4325 |
| REM 뒤 카르티에(Du Quartier)역 | 45.4467,-73.4333 |
| REM 파나마(Panama)역 | 45.4650,-73.4704 |
| REM 일데쇠르(Île-des-Sœurs)역 | 45.4703,-73.5389 |
| REM 중앙역(Gare Centrale) | 45.5000,-73.5666 |
| Heritage Regional HS (Saint-Hubert) | 45.4913,-73.3914 |
| Centennial Regional HS (Greenfield Park) | 45.4917,-73.4465 |
| Saint-Lambert International HS | 45.5102,-73.5045 |
| St. Johns School (Saint-Jean-sur-Richelieu) | 45.3151,-73.2725 |
| Good Shepherd (Brossard) | 45.4729,-73.4539 |
| Harold Napper (Brossard) | 45.4637,-73.4454 |
| St. Lambert Elementary | 45.5023,-73.5099 |
| Greenfield Park Primary International | 45.4825,-73.4714 |
| Courtland Park International (Saint-Bruno) | 45.5326,-73.3568 |
| Boucherville Elementary | 45.6205,-73.4463 |

- St. Johns는 다른 학교보다 남동쪽으로 멀다(약 30km). 지도 확대 범위 밖이면 화살표로 "생장쉬르리슐리외 →" 처리.

### 3-2. 학교 영상 B-roll (원장님 OK, 재사용 허락 받음)
`plans/southshore-longform/assets/school-videos/` (RSB 공식 유튜브 영상, 1080p, 원본 소리 포함)

| 파일 | 학교 | 길이 | 원본 |
|---|---|---|---|
| heritage.mp4 | Heritage Regional High School | 71s | https://www.youtube.com/watch?v=gzy96ug2B78 |
| centennial.mp4 | Centennial Regional High School | 78s | https://www.youtube.com/watch?v=8XS1q64VHfg |
| sli.mp4 | Saint-Lambert International High School | 65s | https://www.youtube.com/watch?v=iM-vcEJFJ2E |
| stjohns.mp4 | St. Johns School | 75s | https://www.youtube.com/watch?v=U39O3cAoE00 |

- 원본 소리는 끄고 원장님 내레이션 + BGM만. 클립 구석에 "영상: Riverside School Board" 작게 표기.
- 학생 얼굴 클로즈업 장면은 피하고, 건물·교실·체육관·운동장·복도 위주로 고를 것. 썸네일에는 학생 얼굴 쓰지 않기.

### 3-3. 장면별 화면 메모
- S01 오프닝: 큰 질문 "몬트리올 = 불어?" → 몬트리올 섬에서 강 남쪽으로 카메라 이동 → 타이틀 "몬트리올 사우스쇼어, 지도로 보는 영어 공립학교 동네". 학교 영상 2~3초 컷으로 훅.
- S02 위치: 캐나다 전체 → 퀘벡 → 몬트리올 섬 줌인. 강 이름 "세인트로렌스 강", "사우스쇼어(Rive-Sud)" 라벨. 도시 이름 7개가 강을 따라 차례로 팝업.
- S03 REM: 브로사드역에서 중앙역까지 노선이 그려지고 열차 점이 이동, 역 5개 라벨 순서대로, "16.6km", "18분" 카운터, 샹플랭 다리 강조. "2023.07.31 개통" 배지. "출퇴근 3분 45초 간격 (개통 당시)". 마지막에 다운타운 아이콘(박물관·공연장).
- S04 사람: 가로 막대그래프 "한국계 인구 (2021 인구조사)": 코퀴틀람 11,900 / 브로사드 590 / 롱게일 425 / 생랑베르 50 / 생브루노 35 / 부셔빌 30. 코퀴틀람 막대가 먼저 길게, 나머지는 거의 안 보이게 대비. 이어서 "아시아계 비율" 지도 색칠: 브로사드 약 20%, 롱게일 약 3%, 생랑베르 약 3%, 부셔빌 약 2%, 생브루노 약 2%. 마지막 두 갈래 카드: "영어만 쓰는 환경 → 생랑베르·부셔빌" / "생활 편의도 → 브로사드".
- S05 교육청: Riverside 관할(사우스쇼어 넓은 범위) 음영. 숫자 카드 "초등 19 · 고등 4", "졸업·자격 취득률 88.5% · 몬테레지 1위 (브로슈어 기준)". 슬로건 타이포 "Success in both languages". 불어 3단계 계단 그래픽.
- S06 고등학교 4곳: 지도 핀이 하나씩 뜨고 → 화면 분할(왼쪽 학교 영상 B-roll, 오른쪽 학교 카드: 지역, 학생 수, 특징 키워드 2~3개). 학교당 15~25초.
  - Heritage: 생위베르 · 1,600명+ · IB MYP · 예술 · 스포츠 · IT
  - Centennial: 그린필드파크 · 약 1,100명 · 영재반 TaG · "Fraser 2025 리버사이드 4개교 중 1위"
  - Saint-Lambert International: 생랑베르 · 약 400명 · IB · 교복 · 휴대폰 보관
  - St. Johns: 생장쉬르리슐리외 · K4~고등 한 학교 · 형제·남매
- S07 초등: 지도에 초등 핀 6개(Good Shepherd, Harold Napper, St. Lambert Elementary, Greenfield Park Intl, Courtland Park Intl, Boucherville Elementary). 키워드 카드: 굿셰퍼드 "영어 84%", 생랑베르 "영어 70 : 불어 30", GPI·CPI "IB 초등(PYP)". 마지막에 벨타임 차이 시각화(7:50 vs 9:05 시계 두 개) → "학교별 정리는 블로그·홈페이지에".
- S08 비용·일정: 비용 카드 "1년 약 CAD 32,000 / 한 학기(5개월) 약 CAD 18,800", 각주 "RSB 학생·가족용 학비표 2027-28, 학교 예시(CAQ 포함), 변경될 수 있음". 포함 항목 아이콘(의료보험, 통학, 교내활동, 홈스테이 3식, 공항 픽업). 타임라인 "2027.02.02 겨울 학기 개강" / "2027.09.08 1년 과정 개강".
- S09 원장 코멘트: 큰 문장 타이포 "생활은 조용한 영어권 교외에서, 경험은 18분 거리의 대도시에서". 교외 주택가·공원 장면(학교 영상 외부 컷 또는 무료 이미지).
- S10 마무리: 3줄 정리 체크리스트 → 엔드카드: 카카오톡 canlog · 02-567-4345 · "학교별 정보는 설명란 블로그 링크".

## 4. 산출물
1. `videos/southshore-longform/renders/video.mp4` (16:9, 약 10~11분). 100MB 넘으면 기존처럼 part 파일로 나누고 parts.txt.
2. 유튜브 썸네일 1280x720: 큰 문구 "다운타운 18분인데 한국인이 없다?" 또는 "몬트리올 영어 공립학교 동네" 계열 + 지도/REM 이미지. 학생 얼굴 금지.
3. 숏폼 5개 (9:16, 각 30~60초, 같은 오디오에서 컷) `videos/southshore-shorts/`:
   - A "다운타운 18분, REM 타고 학교 동네로" (S03)
   - B "코퀴틀람 한국계 11,900명 vs 생랑베르 50명" (S04 앞부분)
   - C "브로사드 vs 생랑베르, 솔직 비교" (S04 뒷부분)
   - D "몬트리올 영어 공립 고등학교 4곳" (S06, 학교 영상 B-roll)
   - E "캐나다 공립 조기유학 1년, 얼마일까?" (S08)
4. upload-text.txt (제목, 설명, 챕터 타임스탬프, 태그). 설명란 출처 블록 포함(6장).
5. publish 큐 폴더는 만들되 **READY 파일은 만들지 말 것** (게시일은 원장님이 정함).

## 5. 표현 규칙 (반드시)
- 커미션 정보 절대 노출 금지. "무상", "무료 교육" 표현 금지(조기유학생은 학비를 냄).
- 학비에는 항상 "2027-28 기준, 캐나다 달러, 변경될 수 있음".
- 통학 시간은 REM 공식 "브로사드→중앙역 18분"만. 학교에서 역까지 시간 같은 숫자는 만들지 말 것.
- PGWP·영주권 보장, "100%", "최고" 같은 표현 금지. "몬테레지 1위", "88.5%"는 "브로슈어 기준" 출처를 붙인다.
- 인구 숫자는 "2021 캐나다 인구조사" 출처를 화면에 표기. "아시아계"는 중국·한국·일본·필리핀·동남아계 합계(남아시아·서아시아 제외)로 계산함.
- 학교 공식 홍보물처럼 보이지 않게 "AA Canada 정리" 톤. RSB 로고는 쓰지 않거나 아주 작게.

## 6. 숫자 출처 (설명란에도 넣기)
- REM: rem.info 보도자료 "The REM ready to welcome first passengers" (2023-07-28): 브로사드–중앙역 16.6km, 18분, 역 5개, 하루 20시간 운행, 출퇴근 3분 45초 간격, 정규 운행 2023-07-31 시작.
- 인구: Statistics Canada, 2021 Census (Focus on Geography, 가시적 소수자 집단 수, 25% 표본):

| 도시 | 2021 인구 | 한국계 | 중국계 | 동·동남아계 합계(중·한·일·필리핀·동남아) | 비율 |
|---|---|---|---|---|---|
| Coquitlam (BC) | 148,625 | 11,900 | 32,770 | – | 한국계 약 8.0% |
| Brossard | 91,525 | 590 | 14,400 | 18,400 | 약 20% |
| Longueuil | 254,483 | 425 | 4,300 | 8,425 | 약 3.3% |
| Saint-Lambert | 22,761 | 50 | 360 | 645 | 약 2.8% |
| Boucherville | 41,743 | 30 | 480 | 845 | 약 2.0% |
| Saint-Bruno-de-Montarville | 26,273 | 35 | 320 | 505 | 약 1.9% |
| Saint-Jean-sur-Richelieu | 97,873 | 50 | 245 | 705 | 약 0.7% |

- 교육청·학교: RSB 2026-27 브로슈어(초등 19, 고등 4, 88.5%, 몬테레지 1위), 학교 홈페이지, Fraser Institute 2025 Quebec secondary report card, 각 학교 문서(`claude/fervent-allen-gq37dp` 브랜치 `plans/riverside-schools/`).
- 비용·일정: RSB "Youth Students fees (Student & families) 2027-28" PDF, "start date and end date Feb 2027 to Jun 2028" PDF. **에이전트용 PDF는 쓰지 말 것.**

## 7. 작업 순서 제안
1. 기존 롱폼 도구 재사용 (SGA `claude/busy-fermat-uhhvcr` videos/sga-longform/tools, Olds·영유 롱폼 파이프라인, HyperFrames 스킬).
2. 지도 베이스 먼저 만들고 스틸 3장(S02 전체 지도, S03 REM 노선, S06 학교 핀)을 렌더해서 세션에 첨부(보고만 하고 기다리지 말고 계속 진행).
3. 녹음 없이 전체 무음 빌드 → 녹음 도착 시 타이밍 맞추고 최종 렌더.
