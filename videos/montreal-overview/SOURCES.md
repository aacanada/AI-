# SOURCES — 몬트리올 개요 상담 영상

## 데이터
| 화면 | 내용 | 출처 |
|---|---|---|
| 1:05 도시권 인구 | 원장님 제공 그래프(`city-population.png`), 단위 천 명. 몬트리올 4,597.84 강조, 화면 문구 "약 460만 명" | 캐나다 통계청 Table 17-10-0148-01, 2025년 7월 1일 인구 추정(CMA). 값 대조: Toronto 7,108,874 / Montréal 4,597,837 / Vancouver 3,088,036 (요청자 확인) |
| 1:16 렌트비 인포그래픽 | 원장님 제공 통계청 공식 인포그래픽(`statcan-rent-2026q2.jpg`). 도시 라벨 순차 팝업, 몬트리올 $1,820 카운트업. 기존 막대그래프는 뺐다 | 캐나다 통계청 Table 46-10-0092-01, 2026년 2분기 (2026.09.09 발표) |
| 1:36 수학 점수 | 원장님 제공 PCAP 그래프(`pcap2023-math.png`). 퀘벡 537 · 캐나다 평균 510 카운트업 | CMEC PCAP 2023. 화면 문구는 "10개 주 중 최고"(그래프상 퀘벡 537이 최고점). 그래프 원문이 "세 주가 평균 이상"이라 "퀘벡만 평균 이상" 문구는 뺐다 |
| 2:05 교육청 | 영어교육청 자격 최대 3년 | 원장님 확인 2026-10-25 (브리프) |
| 2:59 영어 수업 비중 | 불어교육청 학교 영어 수업 최대 40% 수준, 학교·시기별로 다름 | 내레이션 / 브리프 |

- 웰컴클래스 진행 바: 브리프 메모의 "1~2년"은 내레이션에 없고 출처가 없어 화면에 넣지 않았다("기초 레벨 → 일정 레벨 도달 → 정규반"). 필요하면 `tools/scenes_b.py`의 s18에 한 줄 추가.

## 지도
- Natural Earth admin-1 (public domain), github.com/nvkelso/natural-earth-vector
  - 캐나다 주 경계: `ne_50m_admin_1_states_provinces.geojson` (Lambert 정각원추도법으로 투영)
  - 몬트리올 섬·라발: `ne_10m_admin_1_states_provinces.geojson` 퀘벡 폴리곤 중 해당 섬
  - 다운타운 마커: Ville-Marie(몬트리올 다운타운) 실제 좌표 45.5017N, 73.5673W
- 지역 장면(3:24): 원장님 제공 지도 `region-map-abcd.png` 그대로 사용. A~D 배지는 원장님이 지정한 파란 원 위치(A 다운타운 남서, B Pointe-Claire·Dorval, C 바이오돔 주변, D Longueuil·Brossard)에 표시.
- 원장님 이미지는 `tools/owner_img.py`가 라벨·범례 조각을 원본에서 잘라 같은 픽셀 위치에 다시 얹는다(팝업용). 모든 조각이 올라온 상태는 원본과 같다. 통계청 인포그래픽의 바탕만 라벨 자리를 인페인팅해서 비워 두었다.
- `timetable-real.png`는 쓰지 않음(원장님 결정).

## 이미지·폰트·음악
- 사진: 원장님 제공 이미지 4장 외에는 사용하지 않음. 이 환경에서 Pexels/Unsplash/Wikimedia 접속이 막혀 있어 내려받을 수 없었다. 오프닝·썸네일의 몬트리올 스카이라인(몽루아얄과 십자가, 다운타운 빌딩, 올림픽 경기장 탑, 자크카르티에 다리)은 SVG로 직접 그린 일러스트다.
- 로고: `plans/yeongyu-montreal-longform/assets/aa-canada-logo-transparent.png`
- 폰트: Black Han Sans, Noto Sans KR (SIL Open Font License, github.com/google/fonts). 영상에 쓰인 글자만 남겨 woff2로 서브셋.
- BGM: 버논 롱폼 BGM 재사용 (`claude/festive-ramanujan-rswtcw` 브랜치 `videos/vernon-longform/assets/music/bgm-a.mp3`, `bgm-b.mp3`).
- 셰이더 전환: `@hyperframes/shader-transitions@0.8.197` (MIT), GSAP 3.14.2.
