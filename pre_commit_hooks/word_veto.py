import typer
from typing import List, Optional
from pathlib import Path
import re


def check(files: List[Path], badwords: Optional[List[str]] = None):
    mdx_fence = re.compile('````.*?````', re.DOTALL)
    code_fence = re.compile('```.*?```', re.DOTALL)
    inline_fence = re.compile('`.*?`', re.DOTALL)
    ext_link = re.compile(r'(\(https?://.*\))')
    for f in files:
        text = open(f).read()
        text = mdx_fence.sub('', text)
        text = code_fence.sub('', text)
        text = inline_fence.sub('', text)
        text = ext_link.sub('', text)
        for word in badwords:
            if word in text:
                raise ValueError(
                    f"The vetoed word '{word}' has been "
                    f'found in {str(f)}')


def main():
    return typer.run(check)


if __name__ == '__main__':
    raise SystemExit(main())
