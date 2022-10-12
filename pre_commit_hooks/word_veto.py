import typer
from typing import Dict, List, Optional
from pathlib import Path
from functools import reduce
import re

# Badwords should be defined as --badwords "foo:bar,baz:bin"
# Where it's a mapping of {bad word}:{replacement}


def check(files: List[Path], badwords: Optional[str] = None):
    badwords: List[str] = badwords.split(',') if badwords else []
    badwords: Dict[str, str] = dict(
        (k, v) for k, v in [bw.split(':') for bw in badwords])
    # These are defined as (regex, replace_str)
    mdx_fence = re.compile('````.*?````', re.DOTALL), ''
    code_fence = re.compile('```.*?```', re.DOTALL), ''
    preamble_fence = re.compile('---.*?---', re.DOTALL), ''
    inline_fence = re.compile('`.*?`', re.DOTALL), ''
    doc_links = re.compile(r'(\[[^\]]+])\([^\)]+\)'), '\1'

    ignore_urls = re.compile(
        'https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)', re.DOTALL), ''  # noqa: E501
    ignore_divs = re.compile('<div.*?>', re.DOTALL), ''
    rules = [mdx_fence, code_fence, preamble_fence,
             inline_fence, ignore_urls, doc_links, ignore_divs]

    found = 0
    for f in files:
        if not f.exists():
            print(f"Unable to open file '{f}'")
            found = 1
            break
        text = open(f).read()
        text = reduce(lambda t, r: r[0].sub(r[1], t), rules, text)

        for (word, replacement) in badwords.items():
            matcher = re.compile(fr'[\s\W]({word})[\s\W]')
            for match in matcher.finditer(text):
                start = max(match.start(0) - 15, 0)
                end = min(match.end(0) + 15, len(text))
                before = text[start:match.start(0)]
                after = text[match.end(0):end]
                context = before + match.group(0) + after
                found = 1
                print(f"Veto: {str(f)}: '{context}' "
                      f"'{word}' -> '{replacement}'")

    raise typer.Exit(code=found)


def main():
    return typer.run(check)


if __name__ == '__main__':
    raise SystemExit(main())
