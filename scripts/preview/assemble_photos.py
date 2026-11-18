"""미리보기 "사진 보내기"로 기여자가 db에 나눠 보낸 사진을 파일로 되살린다.
Claude가 ArtifactData list(out_dir=<dump>)로 uploads와 photos 컬렉션을 내려받은 뒤 실행한다.
  <dump>/uploads/*.json            : {via:"db", photoId, chunks, contentType, filename, note, uploader, ...}
  <dump>/photos/*.json             : {p, i, n, d(base64 조각)}
사용: python assemble_photos.py <dump> <출력 폴더>
조각이 모자라면(보내는 중 끊김) 건너뛰고 알린다. assets로 올라온 사진(via 없음/assets)은 여기서 다루지 않는다."""
import base64
import json
import re
import sys
from pathlib import Path


def load(d):
    out = []
    for f in sorted(Path(d).glob('*.json')):
        x = json.loads(f.read_text(encoding='utf-8'))
        if isinstance(x.get('data'), dict):  # 문서 본문이 data 아래에 담긴 형식도 받는다
            x = x['data']
        out.append(x)
    return out


dump, dst = Path(sys.argv[1]), Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)
parts = {}
for c in load(dump / 'photos'):
    parts.setdefault(c['p'], {})[int(c['i'])] = c['d']
ext = {'image/jpeg': '.jpg', 'image/png': '.png', 'image/gif': '.gif', 'image/webp': '.webp'}
for u in load(dump / 'uploads'):
    if u.get('via') != 'db':
        continue
    pid, n = u['photoId'], int(u['chunks'])
    got = parts.get(pid, {})
    if len(got) != n:
        print(f'건너뜀 {pid} {u.get("filename")}: 조각 {len(got)}/{n}')
        continue
    raw = base64.b64decode(''.join(got[i] for i in range(n)))
    stem = re.sub(r'[^\w.-]+', '_', Path(u.get('filename') or pid).stem)[:60]
    f = dst / f'{pid}_{stem}{ext.get(u.get("contentType"), ".bin")}'
    f.write_bytes(raw)
    print(f'{f}  {len(raw)} bytes  | {u.get("note", "")}')
