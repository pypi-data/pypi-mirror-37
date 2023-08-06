from docgui import usage_parser
import pytest
import docopt


# @pytest.mark.skip
def test_multiple_commands():
    usage = """
    Usage:
        foo
        foo bar <a>
        foo baz
    """

    commands = usage_parser.get_commands(usage)
    names = set(c.name for c in commands)

    assert names == {'', 'bar', 'baz'}


# @pytest.mark.skip
def test_usage_with_args():
    usage = """
    Usage:
        foo <bar> <baz>
    """

    commands = usage_parser.get_commands(usage)

    assert len(commands) == 1
    assert commands[0].name == ''
    assert len(commands[0].args) == 2
    assert commands[0].args[0].name == '<bar>'
    assert commands[0].args[1].name == '<baz>'
