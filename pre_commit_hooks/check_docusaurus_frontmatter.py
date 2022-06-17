import argparse
import markdown
from typing import Sequence, Optional, Text


def check(input_str: Text, required_keys: Sequence[Text],
          include_drafts=False) -> bool:
    md = markdown.Markdown(extensions=['full_yaml_metadata'])
    md.convert(input_str)
    if not md.Meta:
        raise KeyError(f'missing frontmatter, got {md.Meta}')
    if 'draft' in md.Meta and not include_drafts:
        return True
    for k in required_keys:
        if k not in md.Meta:
            raise KeyError(f"missing '{k}'")

    True


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument('-r', '--require', action='append',
                        help='mandatory keys (multiple allowed)')
    parser.add_argument('-d', '--include_drafts', action='store_true',
                        help='Include pages marked as drafts in the check')
    args = parser.parse_args(argv)
    retval = 0
    required_keys = args.require if args.require else (
        'title', 'id', 'description', 'sidebar_position', 'tags')
    for filename in args.filenames:
        with open(filename, 'r') as f:
            try:
                check(
                    f.read(), required_keys, args.include_drafts)
            except KeyError as exc:
                print(f'{filename}: {exc}')
                retval = 1

    return retval


if __name__ == '__main__':
    raise SystemExit(main())
