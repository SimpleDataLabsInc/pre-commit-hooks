import pytest
from pathlib import Path
import typer

from pre_commit_hooks import word_veto


def test_veto() -> None:

    bad_doc = Path('.') / 'tests' / 'resources' / 'bad_doc.md'

    with pytest.raises(typer.Exit) as e:
        word_veto.check([bad_doc], 'spark:Spark,dataframe:Dataframe')

    assert e.value.exit_code == 1


def test_veto_link() -> None:
    bad_doc = Path('.') / 'tests' / 'resources' / 'bad_link.md'
    with pytest.raises(typer.Exit) as e:
        word_veto.check([bad_doc], 'spark:Spark')

    assert e.value.exit_code == 0


def test_veto_iframe() -> None:
    # Ignore external URLs
    bad_doc = Path('.') / 'tests' / 'resources' / 'embeddedhtml.md'
    with pytest.raises(typer.Exit) as e:
        word_veto.check([bad_doc], 'git:Git,gem:Gem')

    assert e.value.exit_code == 0


def test_veto_ampersand() -> None:
    bad_doc = Path('.') / 'tests' / 'resources' / 'ampersand_doc.md'
    with pytest.raises(typer.Exit) as e:
        word_veto.check([bad_doc], '&:and')

    assert e.value.exit_code == 1


def test_veto_not_in_the_middle_of_another_word() -> None:
    bad_doc = Path('.') / 'tests' / 'resources' / 'management.md'
    with pytest.raises(typer.Exit) as e:
        word_veto.check([bad_doc], 'gem:Gem')

    assert e.value.exit_code == 0
