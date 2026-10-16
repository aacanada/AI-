# Voice QC

median rate 6.24 syl/s · loudness -21.5 dB · pitch 140 Hz · takes per scene 3

## s1-hook
- chunk 0 take 0 ✅ · "부모가 어학원만 다녀도" → heard "부모가 어학원만 다녀도" · clean
- chunk 1 take 0 ✅ · "아이 학비가 0원?" → heard "아이 학비가 0원?" · clean

## s2-rule
- chunk 0 take 0 ✅ · "캐나다 노바스코샤주 핼리팩스" → heard "어, 캐나다 노바스코리아주 핼리팩스" · filler ['어,'], text: heard '어, 캐나다 노바스코리아주 핼리팩스'
  - repaired chunk 0: cut 1 filler span(s) → heard "캐나다 노바스코이아주 핼리팩스" · text: heard '캐나다 노바스코이아주 핼리팩스'
- chunk 1 take 0 ✅ · "부모님 학생비자만 있으면" → heard "부모님 학생 비자만 있으면" · clean
- chunk 2 take 0 ✅ · "자녀 공립학교가 무상이에요" → heard "자녀 공립학교가 무상이에요." · clean

## s3-school
- chunk 0 take 0 ✅ · "대학이나 컬리지에" → heard "음, 대학이나 컬리지에" · filler ['음,'], text: heard '음, 대학이나 컬리지에', ending rises +30%
  - repaired chunk 0: cut 1 filler span(s) → heard "대학이나 컬리지" · text: heard '대학이나 컬리지', ending rises +30%
- chunk 1 take 0 ✅ · "다닐 필요가 없어요" → heard "다닐 필요가 없어요." · rushed 8.61 syl/s
- chunk 2 take 0 ✅ · "사설 어학원도 OK!" → heard "사실 어학원도 오케이," · text: heard '사실 어학원도 오케이,', ending rises +22%
- chunk 3 take 0 ✅ · "학교 종류 조건이 없거든요" → heard "학교 종류 조건이 없거든요." · clean

## s4-weeks
- chunk 0 take 0 ✅ · "핵심은 40주 학비로" → heard "핵심은 40주 학비로" · clean
- chunk 1 take 0 ✅ · "50주 입학허가서!" → heard "50주 입학 허가서," · clean
- chunk 2 take 0 ✅ · "방학 10주는 학비 0원" → heard "방학 10주는 학비 0원" · clean
- chunk 3 take 0 ✅ · "이걸로 약 1년 학생비자 진행" → heard "이걸로 약 1년 학생 비자 진행" · clean

## s5-price
- chunk 0 take 0 ✅ · "학비는 40주에" → heard "이 학비는 40주에" · filler ['이'], text: heard '이 학비는 40주에', dragging 4.47 syl/s, pitch 180.0 Hz (median 139.55)
  - repaired chunk 0: cut 1 filler span(s) → heard "학비는 40주에" · dragging 4.47 syl/s, pitch 180.0 Hz (median 139.55)
- chunk 1 take 0 ✅ · "11,400 캐나다 달러" → heard "11,400 캐나다 달러" · clean
- chunk 2 take 0 ✅ · "정가에서 25% 할인된 금액" → heard "정가에서 25% 할인된 금액" · clean

## s6-parents
- chunk 0 take 0 ✅ · "아이 등교 후 9시 반 시작" → heard ""아이 등교 후 9시 반 시작" · clean
- chunk 1 take 0 ✅ · "하교 전에 수업 끝" → heard "하교 전에 수업 끝." · clean
- chunk 2 take 0 ✅ · "반 친구들도 모두 학부모" → heard "반 친구들도 모두 학부모" · clean
- chunk 3 take 0 ✅ · "대학 부설 과정보다 저렴하고 편해요" → heard "대학 부설 과정보다 저렴하고 편해요."" · ending rises +36%

## s7-cta
- chunk 0 take 0 ✅ · "핼리팩스 자녀무상교육" → heard "헬리팩스 자녀 무상 교육" · text: heard '헬리팩스 자녀 무상 교육'
- chunk 1 take 0 ✅ · "AA Canada와 상담하세요" → heard "AA 캐나다와 상담하세요." · clean

## Result
Still flagged after choosing the best take:
- s2-rule chunk 0: text: heard '캐나다 노바스코이아주 핼리팩스'
- s3-school chunk 0: text: heard '대학이나 컬리지', ending rises +30%
- s3-school chunk 1: rushed 8.61 syl/s
- s3-school chunk 2: text: heard '사실 어학원도 오케이,', ending rises +22%
- s5-price chunk 0: dragging 4.47 syl/s, pitch 180.0 Hz (median 139.55)
- s6-parents chunk 3: ending rises +36%
- s7-cta chunk 0: text: heard '헬리팩스 자녀 무상 교육'
