# 2차 발행 묶음: 센테니얼 + 헤리티지 고등학교

> 1차(`../batch01/`)와 같은 형식입니다. 발행 순서와 카드 다시 만드는 방법은 [`../batch01/README.md`](../batch01/README.md)를 따릅니다.

## 들어 있는 것

| 파일 | 용도 |
|---|---|
| `cards/c1-cover.png` ~ `c5-fit.png` | 센테니얼 카드 5장: 표지, 기본 정보, 영재반 TaG, 미들스쿨·불어 단계, 추천 학생 + 상담 안내 |
| `cards/h1-cover.png` ~ `h5-fit.png` | 헤리티지 카드 5장: 표지, 하루 일과(75분 4교시), 특화반 4개, 시설, 추천 학생 + 상담 안내 |
| `homepage/high/02_centennial.html`, `homepage/high/01_heritage.html` | 홈페이지용 학교 페이지 |
| `blog_03_centennial.txt`, `blog_04_heritage.txt` | 네이버 블로그 3·4편 (학교 유튜브 영상 링크 포함) |
| `cafe_posts.txt` | 카페 게시글 ③·④ |

카드 다시 만들기: `node tools/render.mjs tools/batch02.html content/batch02/cards`

## 공개 전 확인

- **헤리티지 시간표는 2024-25 기준**입니다. 2026-27 시간표(학교 홈페이지 Bell schedule)로 바뀐 게 있는지 확인
- 헤리티지: 현재 교장, iCan과 iTEC 관계(iTEC이 새 이름인지), 특화반 비용
- 센테니얼: TaG 선발 기준·시기, 현재 교장(임시 교장 표기)
- 프레이저 점수(센테니얼 5.9, 헤리티지 5.7)는 보고서 표에서 읽은 값입니다. compareschoolrankings.org에서 한 번 더 확인
- 학교 유튜브 영상은 **링크로만** 넣었습니다. 영상을 잘라 쓰거나 자막을 넣는 것은 RISE 허락 후
