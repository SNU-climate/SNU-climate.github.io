"""미리보기 두 벌을 비교해 다시 게시할 파일 목록을 낸다(바뀐 것만 올리기 위해).
사용: python diff_preview.py <이전 미리보기 폴더> <새 미리보기 폴더> [--json]
- 이전 폴더: 마지막으로 게시한 커밋의 스냅숏으로 만든 미리보기
- 새 폴더:   GitHub 최신 커밋의 스냅숏으로 만든 미리보기
출력: changed(내용이 바뀐 파일), added(새 파일), removed(없어진 파일 — 게시할 때 null로 지운다).
"최종 수정" 날짜만 다른 HTML은 바뀐 것으로 치지 않는다(빌드 날짜가 달라 모든 페이지가 다르게 보이는 것을 막음)."""
import filecmp
import json
import re
import sys
from pathlib import Path

DATE = re.compile(rb'(datetime="|Last updated |\xec\xb5\x9c\xec\xa2\x85 \xec\x88\x98\xec\xa0\x95 )[^<"]*')  # 날짜 표시 부분


def files(root):
    return {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}


def same(a, b):
    if filecmp.cmp(a, b, shallow=False):
        return True
    if a.suffix != '.html':
        return False
    return DATE.sub(b'', a.read_bytes()) == DATE.sub(b'', b.read_bytes())


def main():
    old, new = Path(sys.argv[1]), Path(sys.argv[2])
    fo, fn = files(old), files(new)
    out = {
        'changed': sorted(p for p in fo & fn if not same(old / p, new / p)),
        'added': sorted(fn - fo),
        'removed': sorted(fo - fn),
    }
    if '--json' in sys.argv:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        for k, v in out.items():
            print(f'{k}: {len(v)}')
            for p in v:
                print(f'  {p}')


if __name__ == '__main__':
    main()
