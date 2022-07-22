import pytest
from pathlib import Path

from pre_commit_hooks import commit_message_reuse


def test_msg_reuse() -> None:
    bad_path = Path('tests') / 'resources' / 'bad_commit_msg.txt'
    good_path = Path('tests') / 'resources' / 'good_commit_msg.txt'

    assert bad_path.exists()

    assert commit_message_reuse.check_commit_messages(good_path) is None

    with pytest.raises(ValueError):
        commit_message_reuse.check_commit_messages(bad_path)
