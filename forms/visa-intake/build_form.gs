/**
 * AA Canada – "비자 신청정보" 구글 폼 자동 구성 스크립트
 *
 * IMM1294(해외 학생비자) · IMM5709(캐나다 내 학생비자 연장) · IMM5708(방문자 체류연장)
 * 세 신청서에 필요한 정보를 하나의 폼으로 받습니다.
 *  - 첫 페이지의 "신청 유형"에 따라 해당 신청서 전용 페이지만 보이고,
 *    개인정보·여권·연락처·학력·경력·배경질문은 모두 공통으로 받습니다.
 *  - 응답은 스프레드시트 하나에 모이고, 같은 파일의 "IMM 매핑" 탭에
 *    각 질문이 어느 신청서의 몇 번 문항에 들어가는지 정리됩니다.
 *
 * 실행 방법: 폼 편집 화면 → 점 3개(⋮) → 스크립트 편집기 → 이 코드 붙여넣기
 *           → 함수 buildVisaForm 선택 → 실행 → 권한 허용
 * 기존 질문이 있으면 폼을 "(백업)" 사본으로 복사한 뒤 지우고 새로 만듭니다.
 */

const FORM_ID = '1Dy2Us_rszliO0o7boayI7ePoZDGBmJtQLXgpM01AhM4';
const DATE_RE = '\\d{4}-\\d{2}-\\d{2}';

const TYPE_1294 = '해외(한국 등)에서 캐나다 학생비자 신규 신청 (IMM1294)';
const TYPE_5709 = '캐나다 안에서 학생비자 연장·변경·복원 (IMM5709)';
const TYPE_5708 = '캐나다 안에서 방문자 체류 연장·복원 – 동반 부모 등 (IMM5708)';

// map: [IMM1294, IMM5708, IMM5709] 문항 위치. '—' = 해당 신청서에 없음
const ENTRY = [
  { type: 'date', title: '캐나다 최초 입국일', help: 'YYYY-MM-DD', map: ['—', '입국 Q1', '입국 Q1'] },
  { type: 'text', title: '최초 입국 장소 (도시/공항)', help: '예: Montréal', map: ['—', '입국 Q1', '입국 Q1'] },
  { type: 'mc', title: '최초 입국 목적', choices: ['학업', '방문(관광·가족 동반)', '취업'], other: true, map: ['—', '입국 Q2A-B', '입국 Q2A-B'] },
  { type: 'text', title: '가장 최근 입국일 및 장소 (최초 입국과 다를 때만)', help: '미국 여행 후 재입국 등 포함. 예: 2026-01-05, Lacolle', map: ['—', '입국 Q3', '입국 Q3'] },
  { type: 'text', title: '가장 최근에 받은 Study Permit / Work Permit / Visitor Record 문서번호', help: '문서 오른쪽 위의 번호 (예: F123456789). 없으면 비워두세요.', map: ['—', '입국 Q4', '입국 Q4'] },
];

const PAGES = [
  {
    key: 'start',
    items: [
      { type: 'mc', key: 'appType', title: '어떤 신청인가요?', req: true,
        help: '잘 모르시면 AA Canada에 문의해 주세요. 가족이 함께 신청하면 가족 1명당 1번씩 제출해 주세요.',
        choices: [TYPE_1294, TYPE_5709, TYPE_5708], map: ['(신청서 선택)', '(신청서 선택)', '(신청서 선택)'] },
    ],
  },
  {
    key: 'p1294', title: '학생비자 신규 신청 (해외)', goToAfter: 'study',
    items: [
      { type: 'mc', title: '현재 살고 있는 나라에서 신청하시나요?', choices: ['예', '아니오'], req: true, map: ['개인 Q9A', '—', '—'] },
      { type: 'para', title: '"아니오"인 경우: 신청하는 나라 / 그 나라에서의 신분 / 기간', help: '예: USA / Visitor / 2026-05-01 ~ 2026-11-01', map: ['개인 Q9B', '—', '—'] },
    ],
  },
  {
    key: 'p5709', title: '캐나다 내 학생비자 연장·변경',
    items: [
      { type: 'mc', title: '신청 종류', req: true, map: ['—', '—', '상단 신청 종류'],
        choices: ['학생비자 연장 (현재 신분 유효)', '학생 신분 복원 (만료 후 90일 이내)', 'TRP(임시거주허가) – 해당자만'] },
      ...ENTRY,
      { type: 'mc', title: '학생비자와 함께 Co-op 워크퍼밋도 신청하나요?', choices: ['예', '아니오', '잘 모름'], map: ['—', '—', '학업 Q6A-B'] },
    ],
  },
  {
    key: 'study', title: '학교 및 학업 정보', desc: '입학허가서(LOA)·CAQ에 적힌 그대로 영문으로 적어주세요. 금액은 캐나다 달러(CAD)로 적어주세요.', goToAfter: 'personal',
    items: [
      { type: 'text', title: '학교명 (영문)', req: true, map: ['학업 Q1A', '—', '학업 Q1A'] },
      { type: 'text', title: '과정 레벨', help: '예: 초등학교, 중·고등학교, 컬리지 AEC/DEC/Diploma, 대학교 학사, 어학연수', map: ['학업 Q1B', '—', '학업 Q1A'] },
      { type: 'text', title: '전공 / 과정명', map: ['학업 Q1C', '—', '학업 Q1A'] },
      { type: 'text', title: '학교 주소 (번지, 거리, 도시, 주)', map: ['학업 Q1D', '—', '학업 Q1B'] },
      { type: 'text', title: 'DLI 번호', help: '입학허가서에 있는 O로 시작하는 번호', map: ['학업 Q2A', '—', '학업 Q2'] },
      { type: 'text', title: '학생 ID 번호 (있으면)', map: ['학업 Q2B', '—', '학업 Q2'] },
      { type: 'date', title: '학업 시작일', help: 'YYYY-MM-DD', map: ['학업 Q3', '—', '학업 Q3'] },
      { type: 'date', title: '학업 종료일', help: 'YYYY-MM-DD', map: ['학업 Q3', '—', '학업 Q3'] },
      { type: 'text', title: '학비 (CAD)', map: ['학업 Q4', '—', '학업 Q4'] },
      { type: 'text', title: '숙식비 – Room & board (CAD)', map: ['학업 Q4', '—', '학업 Q4'] },
      { type: 'text', title: '기타 비용 (CAD)', map: ['학업 Q4', '—', '학업 Q4'] },
      { type: 'text', title: '체류 기간 동안 사용 가능한 자금 (CAD)', req: true, map: ['학업 Q5', '—', '학업 Q5A'] },
      { type: 'mc', title: '경비 부담자', choices: ['본인', '부모'], other: true, req: true, map: ['학업 Q6A-B', '—', '학업 Q5B-C'] },
      { type: 'text', title: 'CAQ 번호 / 만료일 (퀘벡 학교)', help: '예: 1234567 / 2027-08-31', map: ['학업 Q8', '—', '학업 Q7'] },
      { type: 'text', title: 'PAL(TAL) 번호 / 만료일 (퀘벡 외 지역, 해당 시)', map: ['학업 Q7', '—', '학업 Q8'] },
    ],
  },
  {
    key: 'p5708', title: '방문자 체류 연장', goToAfter: 'personal',
    items: [
      { type: 'mc', title: '신청 종류', req: true, map: ['—', '상단 신청 종류', '—'],
        choices: ['체류 연장 (현재 신분 유효)', '체류자격 복원 (만료 후 90일 이내)', 'TRP(임시거주허가) – 해당자만'] },
      ...ENTRY,
      { type: 'text', title: '연장 목적', req: true, help: '예: 몬트리올에서 학교에 다니는 자녀 OOO 동반 보호', map: ['—', '방문 Q1A-B', '—'] },
      { type: 'date', title: '원하는 체류 시작일', help: 'YYYY-MM-DD', map: ['—', '방문 Q2', '—'] },
      { type: 'date', title: '원하는 체류 종료일', help: 'YYYY-MM-DD', map: ['—', '방문 Q2', '—'] },
      { type: 'text', title: '체류 기간 동안 사용 가능한 자금 (CAD)', req: true, map: ['—', '방문 Q3A', '—'] },
      { type: 'mc', title: '경비 부담자', choices: ['본인', '부모'], other: true, req: true, map: ['—', '방문 Q3B-C', '—'] },
      { type: 'para', title: '캐나다에서 함께 지내거나 방문하는 사람/기관 ①: 이름 / 나와의 관계 / 주소', help: '예: Minji Kim / Daughter / 123 Rue X, Montréal, QC H3A 1A1', map: ['—', '방문 Q4', '—'] },
      { type: 'para', title: '캐나다에서 함께 지내거나 방문하는 사람/기관 ②: 이름 / 나와의 관계 / 주소 (있으면)', map: ['—', '방문 Q4', '—'] },
    ],
  },
  {
    key: 'personal', title: '개인 정보', desc: '이름·주소는 영문으로, 날짜는 YYYY-MM-DD 형식으로 적어주세요.',
    items: [
      { type: 'text', title: 'UCI 번호 (있으면)', help: '기존 비자·퍼밋 위쪽의 8~10자리 숫자', map: ['상단 UCI', '상단 UCI', '상단 UCI'] },
      { type: 'text', title: '영문 성 (여권과 동일)', req: true, map: ['개인 Q1', '개인 Q1', '개인 Q1'] },
      { type: 'text', title: '영문 이름 (여권과 동일)', req: true, map: ['개인 Q1', '개인 Q1', '개인 Q1'] },
      { type: 'text', title: '다른 이름을 쓴 적이 있다면 그 이름 (개명 전 이름, 예전 영문 이름 등)', help: '없으면 비워두세요.', map: ['개인 Q2A-B', '개인 Q2A-B', '개인 Q2A-B'] },
      { type: 'mc', title: '성별', choices: ['남성', '여성', '기타(X)'], req: true, map: ['개인 Q3', '개인 Q3', '개인 Q3'] },
      { type: 'date', title: '생년월일', help: 'YYYY-MM-DD', req: true, map: ['개인 Q4', '개인 Q4', '개인 Q4'] },
      { type: 'text', title: '출생 도시 / 국가', help: '예: Seoul, Korea', req: true, map: ['개인 Q5A-B', '개인 Q5A-B', '개인 Q5A-B'] },
      { type: 'text', title: '국적', help: '예: Korea', req: true, map: ['개인 Q6', '개인 Q6', '개인 Q6'] },
      { type: 'text', title: '현재 거주 국가', help: '예: Korea 또는 Canada', req: true, map: ['개인 Q7A', '개인 Q7A', '개인 Q7A'] },
      { type: 'mc', title: '현재 거주 국가에서의 신분', choices: ['시민권자', '영주권자', '방문자', '학생', '근로자'], other: true, req: true, map: ['개인 Q7B-C', '개인 Q7B-C', '개인 Q7B-C'] },
      { type: 'text', title: '현재 신분 기간 (시작일 ~ 만료일)', help: '시민권자는 비워두세요. 예: 2025-08-20 ~ 2026-08-31', map: ['개인 Q7D-E', '개인 Q7D-E', '개인 Q7D-E'] },
      { type: 'para', title: '최근 5년간 (현재 거주국 외에) 6개월 이상 산 나라: 국가 / 신분 / 기간', help: '없으면 "없음"', req: true, map: ['개인 Q8A-B', '개인 Q8A-B', '개인 Q8A-B'] },
      { type: 'mc', title: '현재 혼인 상태', choices: ['미혼', '기혼', '사실혼', '별거', '이혼', '사별', '혼인 무효'], req: true, map: ['개인 Q10A', '개인 Q9A', '개인 Q9A'] },
      { type: 'text', title: '(기혼·사실혼) 결혼일(사실혼 시작일) / 배우자 영문 성명', help: '예: 2010-05-01 / KIM, Minsu', map: ['개인 Q10B-C', '개인 Q9B-C', '개인 Q9B-C'] },
      { type: 'mc', title: '(기혼·사실혼) 배우자가 캐나다 시민권자 또는 영주권자인가요?', choices: ['아니오', '예', '해당 없음'], map: ['—', '개인 Q9D', '개인 Q9D'] },
      { type: 'para', title: '이전 결혼/사실혼 경험: 전 배우자 영문 성명 / 생년월일 / 관계(결혼·사실혼) / 기간', help: '없으면 "없음"', req: true, map: ['개인 Q11A-C', '개인 Q10A-E', '개인 Q10A-D'] },
    ],
  },
  {
    key: 'lang', title: '언어 · 여권 · 신분증',
    items: [
      { type: 'text', title: '모국어', help: '예: Korean', req: true, map: ['언어 Q1A', '언어 Q1A', '언어 Q1A'] },
      { type: 'mc', title: '영어/불어로 의사소통이 가능한가요?', choices: ['영어', '불어', '둘 다', '둘 다 불가'], req: true, map: ['언어 Q1B', '언어 Q1B', '언어 Q1B'] },
      { type: 'mc', title: '(둘 다 가능한 경우) 더 편한 언어', choices: ['영어', '불어'], map: ['언어 Q1C', '언어 Q1C', '언어 Q1C'] },
      { type: 'text', title: '영어/불어 공인시험을 본 적이 있다면 시험명', help: '예: IELTS, CELPIP, TEF, TCF. 없으면 비워두세요.', map: ['언어 Q1D', '언어 Q3', '언어 Q3'] },
      { type: 'text', title: '여권번호', req: true, map: ['여권 Q1', '여권 Q1', '여권 Q1'] },
      { type: 'text', title: '여권 발급 국가', help: '예: Korea', req: true, map: ['여권 Q2', '여권 Q2', '여권 Q2'] },
      { type: 'date', title: '여권 발급일', help: 'YYYY-MM-DD', req: true, map: ['여권 Q3', '여권 Q3', '여권 Q3'] },
      { type: 'date', title: '여권 만료일', help: 'YYYY-MM-DD', req: true, map: ['여권 Q4', '여권 Q4', '여권 Q4'] },
      { type: 'date', title: '주민등록증 발급일', help: 'YYYY-MM-DD. 주민등록번호는 여기 적지 마세요. 필요하면 따로 여쭤봅니다.', map: ['신분증 Q1-4', '신분증 Q1-4', '신분증 Q1-4'] },
      { type: 'text', title: '미국 영주권(그린카드)이 있다면 번호 / 만료일', help: '없으면 비워두세요.', map: ['미국PR Q1-3', '미국PR Q1-4', '미국PR Q1-4'] },
    ],
  },
  {
    key: 'contact', title: '연락처',
    items: [
      { type: 'para', title: '우편 주소 (Apt/Unit, 번지, 거리명, 도시, 주/도, 우편번호, 국가)', req: true, map: ['연락처 Q1', '연락처 Q1', '연락처 Q1'] },
      { type: 'para', title: '실제 거주지 주소가 우편 주소와 다르면 거주지 주소', help: '같으면 "같음"', req: true, map: ['연락처 Q2', '연락처 Q2', '연락처 Q2'] },
      { type: 'text', title: '휴대폰 번호 (국가번호 포함)', help: '예: +1 514 123 4567', req: true, map: ['연락처 Q3', '연락처 Q3', '연락처 Q3'] },
      { type: 'text', title: '보조 전화번호 (한국 번호 등)', map: ['연락처 Q4', '연락처 Q4', '연락처 Q4'] },
      { type: 'email', title: '이메일 주소', req: true, map: ['연락처 Q6', '연락처 Q6', '연락처 Q6'] },
    ],
  },
  {
    key: 'edu', title: '학력 · 경력',
    items: [
      { type: 'para', title: '고등학교 이후 최종 학력: 학교명(영문) / 전공·학위 / 입학 년월 ~ 졸업 년월 / 도시·국가', help: '대학·전문대 등이 없으면 "없음"', req: true, map: ['학력 Q1', '학력 Q1', '학력 Q1'] },
      { type: 'section', title: '경력 (최근 10년, 현재부터 역순)', help: '직장뿐 아니라 주부(Homemaker), 무직, 학생, 캐나다 체류(자녀 동반) 등도 기간이 비지 않게 이어서 적어주세요. 형식: 기간(YYYY-MM ~ YYYY-MM) / 직업·활동(영문) / 회사·기관명 / 도시·국가' },
      { type: 'para', title: '경력 ① 현재', help: '예: 2024-03 ~ 현재 / Homemaker / - / Montréal, Canada', req: true, map: ['경력 1', '경력 1', '경력 1'] },
      { type: 'para', title: '경력 ②', map: ['경력 2', '경력 2', '경력 2'] },
      { type: 'para', title: '경력 ③', map: ['경력 3', '경력 3', '경력 3'] },
      { type: 'para', title: '그 이전 경력 (10년이 다 채워지지 않았다면)', map: ['별지', '별지', '별지'] },
    ],
  },
  {
    key: 'bg', title: '배경 질문', desc: '반드시 본인이 직접 확인 후 답해 주세요. 사실과 다른 기재는 신청 거절과 최대 5년 입국 금지 사유(misrepresentation)가 될 수 있습니다.',
    items: [
      { type: 'yn', title: '최근 2년 내 본인 또는 가족이 결핵에 걸렸거나 결핵 환자와 밀접 접촉한 적이 있나요?', map: ['배경 Q1A', '배경 Q1A', '배경 Q1A'] },
      { type: 'yn', title: '캐나다 체류 중 사회·의료 서비스가 필요한 신체적/정신적 질환이 있나요? (약 복용으로 관리되는 경우 제외)', map: ['배경 Q1B', '배경 Q1B', '배경 Q1B'] },
      { type: 'yn', title: '체류기간 초과, 허가 없는 학업 또는 취업을 한 적이 있나요?', map: ['배경 Q2A', '배경 Q2A', '배경 Q2A'] },
      { type: 'yn', title: '캐나다나 다른 나라에서 비자/퍼밋 거절, 입국 거부, 출국 명령을 받은 적이 있나요?', map: ['배경 Q2B-C', '배경 Q2B', '배경 Q2B'] },
      { type: 'yn', title: '이전에 캐나다 입국 또는 체류를 신청한 적이 있나요? (eTA, 비자, 퍼밋 모두 포함)', map: ['—', '배경 Q2C', '배경 Q2C'] },
      { type: 'para', title: '위 질문 중 "예"가 있다면 상세 내용 (종류, 시기, 결과)', map: ['배경 Q1C·Q2D', '배경 Q1C·Q2D', '배경 Q1C·Q2D'] },
      { type: 'yn', title: '어느 나라에서든 범죄를 저지르거나 체포·기소·유죄판결을 받은 적이 있나요? (음주운전 포함)', map: ['배경 Q3A', '배경 Q3A', '배경 Q3A'] },
      { type: 'para', title: '"예"인 경우 상세 내용', map: ['배경 Q3B', '배경 Q3B', '배경 Q3B'] },
      { type: 'yn', title: '군대, 민방위, 경찰 등 보안기관에서 복무한 적이 있나요? (한국 병역 포함)', map: ['배경 Q4A', '배경 Q4A', '배경 Q4A'] },
      { type: 'para', title: '"예"인 경우 복무 기간 / 군별 / 계급 / 근무지', help: '예: 2005-03 ~ 2007-02 / Army / Sergeant / Korea', map: ['배경 Q4B', '배경 Q4B', '배경 Q4B'] },
      { type: 'yn', title: '폭력을 사용하거나 옹호한 정당·단체에 소속되거나 관련된 적이 있나요?', map: ['배경 Q5', '배경 Q5', '배경 Q5'] },
      { type: 'yn', title: '포로·민간인 학대, 약탈, 종교시설 훼손을 목격하거나 가담한 적이 있나요?', map: ['배경 Q6', '배경 Q6', '배경 Q6'] },
      { type: 'mc', title: '향후 IRCC 또는 IRCC 의뢰 기관의 연락(설문 등)에 동의하시나요?', choices: ['예', '아니오'], req: true, map: ['동의', '동의', '동의'] },
    ],
  },
];

function buildVisaForm() {
  const form = FormApp.openById(FORM_ID);

  if (form.getItems().length) {
    const stamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd HH:mm');
    DriveApp.getFileById(FORM_ID).makeCopy('비자 신청정보 (백업 ' + stamp + ')');
    form.getItems().forEach(item => form.deleteItem(item));
  }

  form.setTitle('비자 신청정보')
    .setDescription('AA Canada 비자 신청서 작성을 위한 정보 요청서입니다.\n' +
      '· 이름·주소는 영문(여권과 동일), 날짜는 YYYY-MM-DD(예: 2026-03-15)로 적어주세요.\n' +
      '· 잘 모르는 항목은 비워두시면 저희가 확인 후 연락드립니다.\n' +
      '· 여권·비자 사본 등 서류는 이메일이나 카카오톡으로 따로 보내주세요.')
    .setProgressBar(true)
    .setAllowResponseEdits(true)
    .setConfirmationMessage('제출해 주셔서 감사합니다. 확인 후 AA Canada에서 연락드리겠습니다.');

  const breaks = {};
  const mapping = [];
  let appTypeItem;

  PAGES.forEach(page => {
    if (page.key !== 'start') {
      breaks[page.key] = form.addPageBreakItem().setTitle(page.title).setHelpText(page.desc || '');
    }
    page.items.forEach(q => {
      const item = addItem(form, q);
      if (q.key === 'appType') appTypeItem = item;
      if (q.map) mapping.push([page.title || '신청 유형', q.title].concat(q.map));
    });
  });

  // 신청 유형별로 해당 페이지로 이동, 각 전용 페이지가 끝나면 다음 단계로 건너뜀
  appTypeItem.setChoices([
    appTypeItem.createChoice(TYPE_1294, breaks.p1294),
    appTypeItem.createChoice(TYPE_5709, breaks.p5709),
    appTypeItem.createChoice(TYPE_5708, breaks.p5708),
  ]);
  const order = PAGES.map(p => p.key);
  PAGES.forEach((page, i) => {
    if (page.goToAfter) breaks[order[i + 1]].setGoToPage(breaks[page.goToAfter]);
  });

  const ss = SpreadsheetApp.create('비자 신청정보 (응답)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  writeMapping(ss, mapping);

  Logger.log('폼: ' + form.getPublishedUrl());
  Logger.log('응답 시트: ' + ss.getUrl());
}

function addItem(form, q) {
  let item;
  switch (q.type) {
    case 'section':
      return form.addSectionHeaderItem().setTitle(q.title).setHelpText(q.help || '');
    case 'mc':
    case 'yn':
      item = form.addMultipleChoiceItem().setChoiceValues(q.choices || ['아니오', '예']);
      if (q.other) item.showOtherOption(true);
      if (q.type === 'yn') q.req = true;
      break;
    case 'para':
      item = form.addParagraphTextItem();
      break;
    case 'date':
      item = form.addTextItem().setValidation(FormApp.createTextValidation()
        .setHelpText('YYYY-MM-DD 형식으로 적어주세요 (예: 2026-03-15)')
        .requireTextMatchesPattern(DATE_RE).build());
      break;
    case 'email':
      item = form.addTextItem().setValidation(FormApp.createTextValidation()
        .setHelpText('이메일 주소를 확인해 주세요').requireTextIsEmail().build());
      break;
    default:
      item = form.addTextItem();
  }
  return item.setTitle(q.title).setHelpText(q.help || '').setRequired(!!q.req);
}

function writeMapping(ss, rows) {
  const sheet = ss.insertSheet('IMM 매핑');
  const header = ['섹션', '폼 질문', 'IMM1294 (해외 학생비자)', 'IMM5708 (방문자 연장)', 'IMM5709 (학생비자 연장)'];
  sheet.getRange(1, 1, 1, header.length).setValues([header]).setFontWeight('bold');
  sheet.getRange(2, 1, rows.length, header.length).setValues(rows);
  sheet.setFrozenRows(1);
  sheet.autoResizeColumns(1, header.length);
}
