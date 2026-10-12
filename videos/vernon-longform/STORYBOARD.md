---
format: 1920x1080
duration: 8m11s
message: "유럽 부모들이 고르는 캐나다의 휴양 도시. 한국 아이는 적게, 관리는 촘촘하게."
arc: 훅 → 공감(두 마음) → 기준(대학) → 지역 공개 → 셀링포인트 6 → 증거(사례) → 비용 → CTA
audience: 중3~고1 자녀를 둔 한국 학부모
mode: collaborative
photo_rule: "A등급(01·01c·02·03·04·15·40)만 풀스크린. 나머지는 화면 40% 이하 카드. 자세한 내용은 ASSETS.md"
---

# 버논 관리형 조기유학 — 롱폼 v1

## Decisions

- **Message:** 유럽 부모들이 고르는 캐나다의 휴양 도시에서, 한국 아이는 적게, 관리는 촘촘하게.
- **Audience · arc:** 중3~고1 학부모 · 불안(고교학점제) → 공감(두 마음) → 기준(대학) → 공개(버논) → 셀링포인트 6 → 증거(사례) → 비용 → 상담
- **Format:** 1920×1080, 약 15분 40초, 한국어 내레이션 있음, 잔잔한 어쿠스틱 BGM, 하단 180px 자막 영역 비움
- **Spine:** ① 버논 핀(지도 장면마다 같은 핀) ② 폴라로이드 스택(사진은 늘 기울어진 카드로 떨어져 쌓임) ③ SELLING POINT 스티커 6장(Frame 14에서 한데 모이는 콜백)
- **Brand:** frame.md (Okanagan Postcard) — paper #FAF6EF · ink #16324F · lake #1F8A99 · sunset #E8572B · vine #7FB236 · Pretendard 900/800/500 · Yellowtail 스크립트
- **Bans:** 그라데이션 텍스트, 네온, 빨간 경고 자막, 가짜 UI, 인종 표현, 기술 과목, 졸업률 수치, 커미션. 모션 실패 2가지 금지: 슬라이드쇼(매 장면 새 카드만 넘기기), 스크린세이버(의미 없는 움직임)
- **Held frame:** Frame 11 마지막 "평범한 일상이 만든 결과" — 3초간 아무것도 움직이지 않고 문장만 남김
- **Long-form note:** 각 Frame은 1~1.7분 챕터. 챕터 안에서는 내레이션 문장마다 2~4초 비트로 요소가 바뀐다(정지 화면 금지). 시안 시트는 챕터마다 대표 순간 1컷.

## Frame 1 — 훅: 고교학점제, 그리고 아는 사람만 아는 도시

- src: compositions/01-hook.html
- motion_ref: blueprint kinetic-type-beats → titlecard-reveal · rules kinetic-beat-slam, multi-phase-camera
- scene: 어두운 화면에서 "5등급 내신" 타이포에 금이 감 → 밴쿠버·토론토 핀 사이로 물음표 핀이 떨어짐 → 흰 플래시와 함께 호수 점프 사진 풀스크린
- duration: 40s
- transition_in: cut
- voiceover: "캐나다 사람들이 정작 살고 싶어 하는 도시는 따로 있습니다."
- photos: assets/photos/01c-hero-lake-jump-notext.jpg
- motion: 0~28s 다크 타이포(등급표가 흔들리며 금 감) / 28s 화이트 플래시(0.2s)로 01c 리빌 → 1.08배 슬로 줌인 + 위로 틸트 / 34s 타이틀 "버논, 아는 사람만 아는 캐나다"가 손글씨 스트로크로 그려짐
- status: animated

## Frame 2 — 부모의 두 마음

- src: compositions/02-two-minds.html
- motion_ref: blueprint comparison-split · rules split-tilt-cards, scale-swap-transition
- scene: 좌우 분할. 왼쪽 "캐나다 아이처럼", 오른쪽 "좋은 대학"이 가운데로 모여 하나의 화살표가 됨
- duration: 50s
- transition_in: crossfade
- voiceover: "부모님의 마음은 늘 두 가지입니다. 이 두 마음은 사실 같은 방향을 가리킵니다."
- photos: assets/photos/18-students-lockers.jpg (왼쪽 카드), assets/photos/17-classroom-writing.jpg (오른쪽 카드)
- motion: 두 사진이 폴라로이드로 양쪽에서 기울어져 떨어짐(-6°, +5°) → 텍스트 라벨 타이핑 → 두 카드가 중앙으로 슬라이드되며 겹치고 화살표 하나로 모핑
- status: animated

## Frame 3 — 대학 큰 그림 먼저

- src: compositions/03-university.html
- motion_ref: blueprint grid-card-assemble · rules waterfall-entry, css-marker-patterns
- scene: 캐나다·미국·한국 대학 3열 카드에 공통 키워드 '영어·내신·비교과'가 하이라이트됨
- duration: 1m30s
- transition_in: wipe
- voiceover: "캐나다에는 수능이 없습니다. 탄탄한 영어, 믿을 수 있는 내신, 진짜 경험에서 나온 비교과."
- photos: assets/photos/17-classroom-writing.jpg (배경 블러 20px, 불투명도 25%)
- motion: 3열 카드가 순서대로 업슬라이드(0.15s 간격) → 공통 키워드 3개가 각 카드에서 빠져나와 하단 한 줄로 정렬 → "입학보다 버티는 힘" 카드가 스탬프처럼 찍힘 → 질문 카드 "이 세 가지를 가장 자연스럽게 만드는 곳은?"
- status: animated

졸업률 수치는 쓰지 않는다.

## Frame 4 — 버논은 어디인가

- src: compositions/04-where.html
- motion_ref: blueprint camera-journey (B) · rules viewport-change, svg-path-draw, spring-pop-entrance
- scene: 캐나다 전도 → BC주 → 오카나간 줌인, 버논 핀 낙하 → 파노라마 → 사계절 4분할
- duration: 1m10s
- transition_in: cut
- voiceover: "밴쿠버에서 비행기로 45분, 켈로나 공항에서 차로 30분. 캐나다의 캘리포니아, 버논입니다."
- photos: assets/photos/02-okanagan-panorama.jpg, assets/photos/40-map-playground.jpg, 사계절: 11-kayak-lake(여름) · 07-park-autumn(가을) · 05-silverstar-ski-powder(겨울) · 04-students-canada-flag(봄·호수)
- motion: SVG 벡터 지도 줌(밴쿠버 → 켈로나 → 버논, 점선 비행 경로 드로잉) → 버논 핀 바운스 → 02 파노라마로 크로스 디졸브, 8초간 좌→우 패닝 + 인포 칩(인구 5.8만 / 오카나간 밸리 45만 / 켈로나 40~50분) 순차 팝 → 40 일러스트 지도로 전환, 칼라말카·오카나간 호수에 틸 글로우 → 2×2 사계절 그리드가 한 칸씩 플립 + 기온 라벨(여름 30~35°C / 겨울 0~5°C)
- status: animated

## Frame 5 — SELLING POINT 01: 영어만 쓰는 교실

- src: compositions/05-sp1-english.html
- motion_ref: blueprint dataviz-countup · rules counting-dynamic-scale, stat-bars-and-fills, multi-phase-camera
- scene: 교실 사진 위 100칸 도트 그리드(95칸 틸 / 5칸 오렌지) → 학교 아이콘에 '한국 학생 정원' 자물쇠
- duration: 1m20s
- transition_in: wipe
- voiceover: "학생의 95%가 캐나다 현지 학생. 그리고 학교마다 한국 학생 수에 상한이 있습니다."
- photos: assets/photos/15-classroom-teacher.jpg (풀스크린), assets/photos/16-classroom-overhead.jpg (원형 마스크), assets/photos/18-students-lockers.jpg
- motion: 15를 풀스크린 1.06배 슬로 줌, 좌측 40%에 반투명 네이비 패널 → 패널 위 도트 그리드가 웨이브로 채워짐 + "95%" 카운트업 → 숫자 3단 카운트업(SD22 약 8,600명 → 국제학생 300여 명 → 20여 개국) → 좌석 아이콘 5개 중 하나가 비었다가(졸업) 다시 채워지는 루프 + 자물쇠 아이콘. 16이 원형 마스크로 확대되며 "교실·복도·클럽 모두 영어" 라벨
- status: animated

학교별 상한 수치는 확인 전까지 표기하지 않는다.

## Frame 6 — SELLING POINT 02: 유럽 부모들이 고르는 곳

- src: compositions/06-sp2-europe.html
- motion_ref: rules svg-path-draw, spring-pop-entrance, center-outward-expansion
- scene: 세계 지도에서 유럽 → 버논으로 굵은 곡선 화살표가 여러 개 날아오고, 도착점에서 단체 사진 카드가 펼쳐짐
- duration: 1m10s
- transition_in: crossfade
- voiceover: "버논의 국제학생은 독일을 비롯한 유럽 출신이 가장 많습니다. 유럽 부모들이 고르는 캐나다죠."
- photos: assets/photos/13-group-photo-lake.jpg, assets/photos/12-dock-group.jpg, assets/photos/04-students-canada-flag.jpg
- motion: 미니멀 세계 지도(도트 스타일), 유럽에서 출발하는 곡선 4~5개가 스태거로 드로잉(굵기 3px, 오렌지) → 도착 순간 버논 핀이 펄스 → 13이 카드로 펼쳐짐(스케일 0.6→1, 회전 -3°) → 12가 옆에 겹쳐 떨어짐 → 키워드 칩 "스위스 같은 분위기" / "대도시 대신 버논" → 마지막에 04 스플릿(좌 50%) + 우측 문구 "같은 교실, 다른 나라 친구들"
- status: animated

국가별 비율 수치를 교육청에서 받으면 원형 차트 1개 추가.

## Frame 7 — SELLING POINT 03: 생활 수준이 높은 동네

- src: compositions/07-sp3-living.html
- motion_ref: blueprint grid-card-assemble · rules multi-phase-camera, spring-pop-entrance, waterfall-entry
- scene: 세로 사진 틸트 → 리조트·와이너리·호숫가 라이프 콜라주 → 홈스테이 가정 카드
- duration: 1m30s
- transition_in: wipe
- voiceover: "캐나다 사람들이 은퇴 후 살고 싶어 하는 휴양 도시. 아이가 머무는 홈스테이 가정도 이 동네 사람들입니다."
- photos: assets/photos/03-magical-hillside.jpg (풀스크린 틸트), assets/photos/02-okanagan-panorama.jpg, 액티비티: 08-pumpkin-patch · 09-zipline-forest · 10-pond-hockey · 11-kayak-lake · 19-school-bus-trip, 홈스테이: 21-homestay-house · 20-host-family · 22-homestay-kitchen
- motion: 03을 아래→위 6초 틸트 패닝(손가락 끝에서 멈춤) → 리조트 이름 3개가 라인 아이콘과 함께 타이핑(Predator Ridge 골프 / Silver Star 스키 / Sparkling Hill 스파) → 폴라로이드 5장이 테이블 위에 던져지듯 스택(각각 무작위 회전 ±8°, 0.25s 간격) → 화면이 정리되며 홈스테이 3장이 가로 정렬 + 라벨("1인 1실", "엄선된 캐나다 가정", "24시간 담당자")
- status: animated

와이너리·골프장 사진이 없음 → 스톡 영상 2~3컷으로 보완(ASSETS.md 참고). 생활 수준 통계를 확보하면 그래픽 1장 추가.

## Frame 8 — SELLING POINT 04: 캐나다 공교육 + 학교 안의 비교과

- src: compositions/08-sp4-school.html
- motion_ref: blueprint spatial-pan-stations → grid-card-assemble · rules viewport-change, spring-pop-entrance
- scene: 선택과목 태그 → 고등학교 5곳 캐러셀 → 아카데미 표지 → 아카데미 9종 아이콘 그리드 → 클럽·봉사 레이어가 '대학 지원서' 아이콘으로 합쳐짐
- duration: 1m40s
- transition_in: crossfade
- voiceover: "국제학교가 아니라 캐나다 학생과 같은 교실. 비교과는 따로 만드는 게 아니라 생활이 됩니다."
- photos: assets/photos/30~34 (학교 5곳), assets/photos/41-academies-cover.jpg, assets/photos/06-ski-student.jpg, assets/photos/14-soccer.jpg, assets/photos/16-classroom-overhead.jpg, assets/photos/40-map-playground.jpg
- motion: 선택과목 태그(드라마·밴드·오케스트라·로보틱스·컴퓨터·비즈니스·법·사진·프랑스어·스페인어)가 칩 형태로 위에서 떨어져 쌓임 → 40 지도 위에서 학교 핀 5개가 순서대로 점등되고, 핀마다 학교 카드(사진+인원+특징)가 옆으로 슬라이드되는 캐러셀 → 41이 기울어진 문서로 들어왔다 넘어가며 아이콘 그리드(축구·하키·알파인·프리스타일·노르딕·골프·야구·배구·댄스·어스퀘스트)로 전환, 06·14를 큰 카드로 → 방과후 클럽·봉사 아이콘이 아래에서 올라와 '지원서' 문서 아이콘에 흡수
- status: animated

학교 카드: Vernon Secondary(1,075명, 최대 종합) / W.L. Seaton(1,000명, 예술·프랑스어 몰입) / Kalamalka(650명, 높은 학업 기준) / Clarence Fulton(775명, 운동·예술) / Charles Bloom(375명, 작은 마을 분위기). 목공·재봉·자동차 정비 등 기술 과목은 넣지 않는다.

## Frame 9 — SELLING POINT 05: 빠른 졸업

- src: compositions/09-sp5-graduation.html
- motion_ref: blueprint dataviz-countup · rules stat-bars-and-fills, counting-dynamic-scale, physics-press-reaction
- scene: 80칸 학점 게이지가 계산 순서대로 채워짐
- duration: 1m
- transition_in: cut
- voiceover: "고1을 마치고 오면 약 40학점 인정. 계산상 세 학기면 졸업 요건을 채울 수 있습니다."
- motion: 가로 게이지(80칸) → "한국 고1 성적 + 한국어 12학점" 블록이 40칸에 한 번에 꽂힘(스냅 + 바운스) → 학기 1·2·3 블록(16학점씩)이 차례로 채워지며 카운트 56→72→80(3학기에는 나머지 8학점만 필요) → 80 도달 시 졸업모 아이콘 팝 → 하단 각주 페이드
- status: animated

각주: "영어 수준·ESL 이수에 따라 기간이 달라집니다"

## Frame 10 — SELLING POINT 06: 현지 한국인 선생님의 관리

- src: compositions/10-sp6-care.html
- motion_ref: blueprint grid-card-assemble · rules stat-bars-and-fills, svg-path-draw, waterfall-entry
- scene: 주간 시간표 셀이 순서대로 채워짐 → 관리 체크리스트 → 관리 옵션 계단
- duration: 1m40s
- transition_in: crossfade
- voiceover: "버논에서 16년을 산 한국인 선생님이 출결·성적·홈스테이까지 살피고 부모님께 보고합니다."
- photos: assets/photos/20-host-family.jpg, assets/photos/22-homestay-kitchen.jpg, assets/photos/18-students-lockers.jpg
- motion: 7×4 시간표 그리드가 선으로 그려진 뒤 셀이 요일별로 채워짐(학교 수업 = 틸, 클럽 = 그린, 튜터링·첨삭 = 오렌지) → '저녁' 행이 채워질 때 22가 셀 옆으로 미니 카드로 팝 → 체크리스트 6개가 체크마크 드로잉과 함께 등장 → 정착 → 가디언 케어 → 에듀 가이드 3단 계단 카드가 아래에서 쌓임, 단계마다 포함 항목 아이콘 증가
- status: animated

체크리스트: 주1회 2시간 1:1 튜터링 / 주1회 에세이 첨삭 / 정기 카운셀링 / 학교 방문·부모 보고 / 월 1회 이상 한식 / 휴대폰 사용 지도

## Frame 11 — 진학 사례

- src: compositions/11-case.html
- motion_ref: blueprint spatial-pan-stations · rules svg-path-draw, viewport-change
- scene: 좌→우 타임라인. 2020 VSS 입학 → 2022 U of T 조건부 → 최종 합격
- duration: 1m
- transition_in: wipe
- voiceover: "화려한 스펙 공장이 아니라, 버논의 평범한 일상이 만든 결과입니다."
- photos: assets/photos/32-school-vernon-secondary.jpg (출발점 카드)
- motion: 타임라인 선이 좌→우로 드로잉, 노드마다 카드 팝(입학·클럽 → 저널 → 봉사 → 수학경시 입선 → 조건부 입학 → 최종 합격). 마지막 노드에서 컨페티 대신 은은한 글로우 + "Computer Science" 라벨
- status: animated

## Frame 12 — 비용은 투명하게

- src: compositions/12-cost.html
- motion_ref: blueprint grid-card-assemble · rules counting-dynamic-scale, waterfall-entry
- scene: 4열 가격 카드가 순서대로 등장, 포함 항목 체크
- duration: 50s
- transition_in: crossfade
- voiceover: "학비·홈스테이·보험을 모두 포함한 기본형이 두 학기 약 2만 9,900 캐나다달러입니다."
- motion: 카드 4장이 스태거 업슬라이드, 금액 카운트업(29,900 / 33,900 / 37,500 / 44,150) → 포함 항목 체크 → 하단 고지 페이드
- status: animated

CAD 2026.9~2027.6 두 학기 기준. 포함: 입학신청비·학비·홈스테이·가디언 지정·의료보험·교육청 활동비. 별도: 항공료·용돈. 고지: "2026.10 기준, 변동 가능". 가격표 이미지(PDF 25p)는 쓰지 않는다.

## Frame 13 — (선택) 여름 준비과정

- src: compositions/13-summer-prep.html
- motion_ref: blueprint titlecard-reveal · rules stat-bars-and-fills
- scene: 6~8월 캘린더 바, 오전 '영어' / 오후 '과목 용어' 2단 분할 → 9월 버논 입학 화살표
- duration: 30s
- transition_in: cut
- voiceover: "첫 한 달의 적응기를, 입학 전에 미리 지나고 오는 셈이죠."
- status: animated

PLAN.md 6장 확인 전에는 빼고 렌더한다(총 15m10s).

## Frame 14 — 정리 + 상담 CTA

- src: compositions/14-cta.html
- motion_ref: blueprint logo-assemble-lockup · rules center-outward-expansion, multi-phase-camera
- scene: 셀링포인트 스티커 6개가 한 화면에 모임 → 호수 점프 사진 + AA캐나다 상담 안내
- duration: 50s
- transition_in: crossfade
- voiceover: "학교별 한국 학생 자리는 한정돼 있습니다. 지금 현황부터 확인해 보세요."
- photos: assets/photos/01-hero-lake-jump.jpg, assets/photos/04-students-canada-flag.jpg
- motion: 스티커 6개가 각 챕터 위치에서 날아와 3×2 그리드로 붙음(약간씩 기울어짐) → 그리드가 축소되며 01이 풀스크린(원본 "Take Flight!" 문구 그대로 사용) → 하단 1/3에 네이비 바 + AA캐나다 로고 + "학교별 잔여석 · 맞는 학교·관리 옵션 · 대학 로드맵" + 연락처
- status: animated
