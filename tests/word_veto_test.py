import pytest
from pathlib import Path

from pre_commit_hooks import word_veto


def test_veto() -> None:

    bad_doc = Path('.') / 'tests' / 'resources' / 'bad_doc.md'

    with pytest.raises(ValueError, match="The vetoed word 'dataframe' "
                       'has been found in'):
        word_veto.check([bad_doc], badwords=['dataframe'])
