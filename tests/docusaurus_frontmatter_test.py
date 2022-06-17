import pytest

from pre_commit_hooks import check_docusaurus_frontmatter


def test_draftskip() -> None:

    test_txt = """---
id: 123
draft: true
---
    """

    assert check_docusaurus_frontmatter.check(test_txt, required_keys=['foo'])

    with pytest.raises(KeyError, match="missing 'foo'"):
        check_docusaurus_frontmatter.check(
            test_txt, required_keys=['foo'], include_drafts=True)
