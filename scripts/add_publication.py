#!/usr/bin/env python
"""DOI로 논문을 publications.yaml에 추가한다.

사용: python scripts/add_publication.py 10.1038/s41558-024-01928-0 [DOI ...] [--corresponding] [--featured]
- Crossref에서 메타데이터를 받아 정규화해서 넣는다. 이미 있는 DOI는 건너뛴다.
- 추가 후 build.py와 validate.py를 실행해 확인한다.
"""
import argparse
import sys

import pubtools as P


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('dois', nargs='+')
    ap.add_argument('--corresponding', action='store_true', help='교신저자 논문으로 표시')
    ap.add_argument('--featured', action='store_true', help='주요 논문으로 표시')
    args = ap.parse_args()

    meta, pubs = P.load_pubs()
    have = {P.norm_doi(p['doi']) for p in pubs if p.get('doi')}
    added = 0
    for doi in args.dois:
        doi = P.norm_doi(doi)
        if doi in have:
            print(f'[skip] 이미 있음: {doi}')
            continue
        try:
            entry = P.crossref_to_entry(P.crossref_work(doi))
        except Exception as e:  # noqa: BLE001
            print(f'[error] Crossref 조회 실패: {doi} ({e})', file=sys.stderr)
            continue
        if args.corresponding:
            entry['corresponding'] = True
        if args.featured:
            entry['featured'] = True
        pubs.append(entry)
        have.add(doi)
        added += 1
        print(f"[add] {entry.get('year')} {entry.get('journal')} — {entry.get('title')[:80]}")
    if added:
        P.save_pubs(meta, pubs)
    print(f'추가 {added}건, 전체 {len(pubs)}건')


if __name__ == '__main__':
    main()
