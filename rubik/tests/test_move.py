from rubik.move import MOVE_MAP


def test_move_magic_str() -> None:
    for move_str, move in MOVE_MAP.items():
        assert move_str == move.__str__()
