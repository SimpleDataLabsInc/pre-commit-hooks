import argparse
import markdown
from typing import Sequence, Optional, Text


def check_docusaurus_frontmatter(input_str:Text, required_keys:Sequence[Text]) -> bool:
    md = markdown.Markdown(extensions=['full_yaml_metadata'])
    md.convert(input_str)
    if not md.Meta:
        raise KeyError(f"missing frontmatter, got {md.Meta}")
    for k in required_keys:
        if k not in md.Meta:
            raise KeyError(f"missing '{k}'")

    True

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check")
    parser.add_argument("-r", "--require", action="append", help="mandatory keys (multiple allowed)")
    args = parser.parse_args(argv)
    retval = 0
    required_keys = args.require if args.require else ("title", "id", "description", "sidebar_position", "tags")
    for filename in args.filenames:
        with open(filename, 'r') as f:
            try:
                check_docusaurus_frontmatter(f.read(), required_keys)
            except KeyError as exc:
                print(f"{filename}: {exc}")
                retval = 1
    
    return retval

if __name__ == "__main__":
    raise SystemExit(main())