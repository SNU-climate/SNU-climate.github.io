"""All-in-One WP Migration SQL 덤프(한 줄 = INSERT 1행) → 테이블별 JSONL. 민감 테이블·컬럼은 제외.
사용: python -I sql2jsonl.py <database.sql> <outdir>"""
import sys, os, re, json
KEEP = {'posts', 'postmeta', 'terms', 'term_taxonomy', 'term_relationships', 'kboard_board_content',
        'kboard_board_attached', 'kboard_board_meta', 'kboard_board_setting', 'kboard_board_option',
        'kboard_meida', 'kboard_meida_relationships'}
DROP_COLS = {'password', 'post_password'}
TOK = re.compile(r"'((?:[^'\\]|\\.)*)'|(NULL)|(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)|([(),;])", re.S)
ESC = {'0': '\0', 'n': '\n', 'r': '\r', 't': '\t', 'Z': '\x1a', 'b': '\b'}
def unesc(s):
    return re.sub(r'\\(.)', lambda m: ESC.get(m.group(1), m.group(1)), s, flags=re.S)
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
cols, cur, files, counts = {}, None, {}, {}
with open(src, encoding='utf-8', errors='replace') as f:
    for line in f:
        if line.startswith('CREATE TABLE'):
            cur = line.split('`')[1].replace('SERVMASK_PREFIX_', ''); cols[cur] = []; continue
        if cur and line.startswith('  `'):
            cols[cur].append(line.split('`')[1]); continue
        if not line.startswith('INSERT INTO'):
            continue
        t = line.split('`')[1].replace('SERVMASK_PREFIX_', '')
        if t not in KEEP:
            continue
        body = line[line.index(' VALUES ') + 8:]
        vals = []
        for m in TOK.finditer(body):
            if m.group(1) is not None: vals.append(unesc(m.group(1)))
            elif m.group(2): vals.append(None)
            elif m.group(3) is not None: vals.append(m.group(3))
            elif m.group(4) in ');': break
        row = {c: v for c, v in zip(cols[t], vals) if c not in DROP_COLS}
        if t not in files: files[t] = open(os.path.join(out, t + '.jsonl'), 'w')
        files[t].write(json.dumps(row, ensure_ascii=False) + '\n'); counts[t] = counts.get(t, 0) + 1
for t, n in sorted(counts.items()): print(t, n)
