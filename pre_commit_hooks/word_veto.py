import typer
from typing import List, Optional
from pathlib import Path
from functools import reduce
import re


def check(files: List[Path], badwords: Optional[str] = None):
    badwords = badwords.split(',') if badwords else []
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

        for word in badwords:
            matcher = re.compile(fr'(.{{0,15}}{word}.{{0,15}})')
            for match in matcher.finditer(text):
                found = 1
                print(f"Vetoed word '{word}' found in {str(f)}): "
                      f"'{match.groups()[0]}'")

    raise typer.Exit(code=found)


def main():
    return typer.run(check)


if __name__ == '__main__':
    raise SystemExit(main())
