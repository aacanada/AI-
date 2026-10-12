# publish/ — 게시 대기함

Claude Code가 완성한 영상을 올리고, 어사이드가 예약 확인으로 읽어서 게시합니다.
이 폴더는 `publish` 브랜치에서만 관리합니다.

## 폴더 하나 = 게시 묶음 하나

```
publish/YYYY-MM-DD-<이름>/
  video.mp4         최종 영상 (100MB 초과 시 영상 대신 meta.txt 에 드라이브 링크)
  thumbnail.jpg     썸네일
  upload-text.txt   [유튜브 제목] / [유튜브 설명] / [인스타 캡션]
  meta.txt          채널, 공개 범위, 게시 순서, 연결할 본편 폴더
  READY             Claude Code가 모든 파일을 올린 뒤 마지막 커밋으로 만듦
  published.md      어사이드가 게시 후 채널별 링크를 적음
```

## 규칙

1. `READY` 가 없는 폴더는 아직 준비 중입니다. 게시하지 않습니다.
2. `published.md` 가 있는 폴더는 이미 게시된 것입니다. 건너뜁니다.
3. 게시 전에 각 채널에 같은 글이 이미 있는지 확인합니다 (중복 게시 방지).
4. `meta.txt` 의 `linked_to` 가 있으면, 그 폴더의 `published.md` 에 본편 주소가 생긴 뒤에 게시하고 관련 동영상으로 연결합니다.
5. `visibility: public` 은 바로 공개 게시입니다.
