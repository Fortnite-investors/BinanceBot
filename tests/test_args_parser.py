from unittest import result
from parsers import command_args

import pytest

@pytest.mark.parametrize('args, is_ok', [
    (' 699 TRY            ZIRAAT RUB TINKOFF', True),
    (' aaa TRY            ZIRAAT RUB TINKOFF', False),
    ('', False),
    ('699 TRY', False),
])
def test_cost_parser(args, is_ok):
    if is_ok:
        res = command_args.CostArgs(args)
        assert res
    else:
        with pytest.raises(command_args.ParseError):
            res = command_args.CostArgs(args)

@pytest.mark.parametrize('args, out', [
    (' 699 TRY            ZIRAAT RUB TINKOFF', ['699', 'TRY', 'ZIRAAT', 'RUB', 'TINKOFF'])
])
def test_simple_parser(args, out):
    assert command_args.parse_line(args) == out
