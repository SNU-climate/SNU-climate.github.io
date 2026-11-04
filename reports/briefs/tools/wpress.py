"""All-in-One WP Migration .wpress 아카이브 목록/추출 (실행 없이 바이트 파싱만)."""
import sys, os
HDR = 255 + 14 + 12 + 4096

def entries(path):
    with open(path, 'rb') as f:
        while True:
            h = f.read(HDR)
            if len(h) < HDR or h == b'\0' * HDR:
                return
            name = h[:255].rstrip(b'\0').decode('utf-8', 'replace')
            size = int(h[255:269].rstrip(b'\0') or 0)
            prefix = h[281:].rstrip(b'\0').decode('utf-8', 'replace')
            rel = name if prefix in ('', '.') else prefix + '/' + name
            pos = f.tell()
            yield rel, size, f, pos
            f.seek(pos + size)

if __name__ == '__main__':
    mode, arc = sys.argv[1], sys.argv[2]
    if mode == 'list':
        for rel, size, _, _ in entries(arc):
            print(size, rel)
    else:  # extract <arc> <outdir> <names...>
        out, want = sys.argv[3], set(sys.argv[4:])
        for rel, size, f, pos in entries(arc):
            if rel in want:
                dst = os.path.join(out, os.path.basename(rel))
                f.seek(pos)
                with open(dst, 'wb') as o:
                    left = size
                    while left:
                        chunk = f.read(min(left, 1 << 20)); o.write(chunk); left -= len(chunk)
                print('extracted', rel, size)
