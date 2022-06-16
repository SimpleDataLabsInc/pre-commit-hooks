import argparse
import markdown
from typing import Sequence, Optional


def check_docusaurus_frontmatter(input_str) -> bool:
    md = markdown.Markdown(extensions=['full_yaml_metadata'])
    md.convert(input_str)
    if not md.Meta:
        raise KeyError(f"missing frontmatter, got {md.Meta}")
    mandatory_keys = ("title", "id", "description", "sidebar_position", "tags")
    for k in mandatory_keys:
        if k not in md.Meta:
            raise KeyError(f"missing '{k}'")

    True

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check")

    args = parser.parse_args(argv)
    retval = 0
    for filename in args.filenames:
        with open(filename, 'rb') as f:
            try:
                check_docusaurus_frontmatter(f.read())
            except KeyError as exc:
                print(f"{filename}: {exc}")
                retval = 1
    
    return retval

if __name__ == "__main__":
    raise SystemExit(main())