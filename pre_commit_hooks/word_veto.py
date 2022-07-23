import typer
from typing import List, Optional
from pathlib import Path
import re


def check(files: List[Path], badwords: Optional[List[str]] = None):
    mdx_fence = re.compile('````.*?````', re.DOTALL)
    code_fence = re.compile('```.*?```', re.DOTALL)
    preamble_fence = re.compile('---.*?---', re.DOTALL)
    inline_fence = re.compile('`.*?`', re.DOTALL)
    ext_link = re.compile(r'(\[[^\]]+])\([^\)]+\)')
    found = 0
    for f in files:
        if not f.exists():
            print(f"Unable to open file '{f}'")
            found = 1
            break
        text = open(f).read()
        text = mdx_fence.sub('', text)
        text = code_fence.sub('', text)
        text = inline_fence.sub('', text)
        text = preamble_fence.sub('', text)
        text = ext_link.sub(r'\1', text)
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
