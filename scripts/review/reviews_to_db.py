"""REVIEW_LOG.md(비공개 리뷰 기록)의 "1. 리뷰 기록"과 "2. 반영 현황"을 미리보기 db reviews 컬렉션 행(JSON 파일)으로 만든다.
미리보기의 편집자 전용 "리뷰 정리" 버튼이 이 행을 보여 준다. 파일은 Claude가 ArtifactData batch(file_path)로 넣는다.
사용: python reviews_to_db.py <REVIEW_LOG.md> <출력 폴더>
행: {time, author, page, text, thread, status, commit}. 갱신 시각은 _meta.json {updated: "YYYY.MM.DD.HH:MM"(KST), count}. 문서 id = <스레드 앞 8자>-<YYYYMMDDHHMM>(같은 리뷰는 같은 id라 다시 넣으면 덮어씀)."""
import json
import re
import sys
from pathlib import Path

log, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
t = log.read_text(encoding='utf-8')
sec1 = t.split('## 1.', 1)[1].split('### 보낸 사진', 1)[0]
sec2 = t.split('## 2.', 1)[1].split('## 3.', 1)[0]


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


status = {}
for line in sec2.splitlines():
    if not line.startswith('| ') or line.startswith('| 스레드') or line.startswith('|---'):
        continue
    c = cells(line)
    if len(c) < 5:
        continue
    st = c[3]
    st = next((k for k in ('일부 반영', '해당 없음', '미반영', '보류', '반영') if st.startswith(k)), st.split(' ')[0])
    m = re.match(r'([0-9a-f]{7,})', c[4])
    for th in re.findall(r'[0-9a-f]{8}', c[0]):
        status[th] = (st, m.group(1) if m else '')

n = 0
for line in sec1.splitlines():
    if not re.match(r'\| \d{4}-\d{2}-\d{2} ', line):
        continue
    time, author, page, text, th = cells(line)[:5]
    st, commit = status.get(th, ('미반영', ''))
    doc = re.sub(r'\D', '', time)
    row = {'time': time, 'author': author, 'page': page, 'text': text, 'thread': th, 'status': st, 'commit': commit}
    (out / f'{th}-{doc}.json').write_text(json.dumps(row, ensure_ascii=False), encoding='utf-8')
    n += 1
from datetime import datetime, timedelta, timezone
now = datetime.now(timezone(timedelta(hours=9))).strftime('%Y.%m.%d.%H:%M')
(out / '_meta.json').write_text(json.dumps({'updated': now, 'count': n}, ensure_ascii=False), encoding='utf-8')
print(f'reviews {n} + _meta(updated {now}) → {out}')
