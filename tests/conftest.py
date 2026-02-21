import pytest
from agents.shared.global_state import GlobalState


@pytest.fixture
def base_state() -> GlobalState:
    return GlobalState(
        messages=[],
        task="test task",
        final_output=None,
    )
