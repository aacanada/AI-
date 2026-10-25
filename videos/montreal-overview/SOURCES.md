# SOURCES — 몬트리올 개요 상담 영상

## 데이터
| 화면 | 내용 | 출처 |
|---|---|---|
| 1:16 렌트비 차트 | 방 2개 아파트 평균 호가 월세(CAD): 밴쿠버 3,030 / 토론토 2,650 / 빅토리아 2,640 / 핼리팩스 2,400 / 캘거리 1,890 / 몬트리올 1,820 / 전국 CMA 평균 2,130 | 캐나다 통계청 Table 46-10-0092-01, 2026년 2분기 (2026.09.09 발표) — 브리프 수치 그대로 |
| 1:36 수학 점수 | "10개 주 중 퀘벡만 캐나다 평균(510점)보다 높음, 앨버타·온타리오는 평균 수준, 나머지 주는 평균 아래" | CMEC PCAP 2023 공개 보고서 — 브리프 요약 그대로. 주별 점수는 넣지 않음(아래 참고) |
| 2:05 교육청 | 영어교육청 자격 최대 3년 | 원장님 확인 2026-10-25 (브리프) |
| 2:59 영어 수업 비중 | 불어교육청 학교 영어 수업 최대 40% 수준, 학교·시기별로 다름 | 내레이션 / 브리프 |

- PCAP 주별 점수(Figure 3.2)는 이 작업 환경에서 cmec.ca 접속이 막혀 직접 확인하지 못했다. 그래서 브리프 지시대로 숫자 없이 "퀘벡만 평균 이상" 도식으로 처리했다.
- 웰컴클래스 진행 바: 브리프 메모의 "1~2년"은 내레이션에 없고 출처가 없어 화면에 넣지 않았다("기초 레벨 → 일정 레벨 도달 → 정규반"). 필요하면 `tools/scenes_b.py`의 s18에 한 줄 추가.

## 지도
- Natural Earth admin-1 (public domain), github.com/nvkelso/natural-earth-vector
  - 캐나다 주 경계: `ne_50m_admin_1_states_provinces.geojson` (Lambert 정각원추도법으로 투영)
  - 몬트리올 섬·라발: `ne_10m_admin_1_states_provinces.geojson` 퀘벡 폴리곤 중 해당 섬
  - 다운타운 마커: Ville-Marie(몬트리올 다운타운) 실제 좌표 45.5017N, 73.5673W
- A~D 지역은 원장님 원본 지도가 없어서 지도 위에 배치하지 않았다(카드로만 표시).

## 이미지·폰트·음악
- 사진: 사용하지 않음. 이 환경에서 Pexels/Unsplash/Wikimedia 접속이 막혀 있어 내려받을 수 없었다. 오프닝·썸네일의 몬트리올 스카이라인(몽루아얄과 십자가, 다운타운 빌딩, 올림픽 경기장 탑, 자크카르티에 다리)은 SVG로 직접 그린 일러스트다.
- 로고: `plans/yeongyu-montreal-longform/assets/aa-canada-logo-transparent.png`
- 폰트: Black Han Sans, Noto Sans KR (SIL Open Font License, github.com/google/fonts). 영상에 쓰인 글자만 남겨 woff2로 서브셋.
- BGM: 버논 롱폼 BGM 재사용 (`claude/festive-ramanujan-rswtcw` 브랜치 `videos/vernon-longform/assets/music/bgm-a.mp3`, `bgm-b.mp3`).
- 셰이더 전환: `@hyperframes/shader-transitions@0.8.197` (MIT), GSAP 3.14.2.
