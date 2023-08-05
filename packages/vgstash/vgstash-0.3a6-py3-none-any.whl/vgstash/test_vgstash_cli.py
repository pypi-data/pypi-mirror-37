import click
import os
import pytest
import vgstash
import vgstash_cli

from click.testing import CliRunner

verbose = False
interactive = False

# Change this to suit your testing environment
if not interactive:
    os.environ['EDITOR'] = "cat"
else:
    if not os.getenv("EDITOR"):
        os.environ['EDITOR'] = "vim"

def test_init():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['init'])
    if verbose:
        print(result.output)
    assert result.exit_code == 0
    assert result.output == "Initializing the database...\nSchema created.\n"


def test_add_minimum():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['add', 'Super Mario Bros.', 'NES'])
    if verbose:
        print(result.output)
    assert result.exit_code == 0
    assert result.output == "Added Super Mario Bros. for NES. You physically own it and are playing it.\n"


def test_add_ownership():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['add', 'The Legend of Zelda', 'NES', 'd'])
    if verbose:
        print(result.output)
    assert result.exit_code == 0
    assert result.output == "Added The Legend of Zelda for NES. You digitally own it and are playing it.\n"


def test_add_typical():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['add', 'Sonic the Hedgehog 2', 'Genesis', '0', '3'])
    if verbose:
        print(result.output)
    assert result.exit_code == 0
    assert result.output == "Added Sonic the Hedgehog 2 for Genesis. You do not own it and have beaten it.\n"


def test_add_full():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['add', 'Vectorman', 'Genesis', 'u', 'b', 'beep'])
    if verbose:
        print(result.output)
    assert result.exit_code == 0
    assert result.output == "Added Vectorman for Genesis. You do not own it and have beaten it. It also has notes.\n"


def test_add_full_note_with_newline():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['add', 'Vectorman 2', 'Genesis', 'p', 'p', 'beep\nboop'])
    if verbose:
        print(result.output)
    assert result.exit_code == 0
    assert result.output == "Added Vectorman 2 for Genesis. You physically own it and are playing it. It also has notes.\n"


def test_list():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.list_games, ['--raw'])
    if verbose:
        print(result.output)
    assert result.exit_code == 0
    assert result.output == '\n'.join((
        'Sonic the Hedgehog 2|Genesis|0|3|',
        'Vectorman|Genesis|0|3|beep',
        'Vectorman 2|Genesis|1|2|beep\\nboop',
        'Super Mario Bros.|NES|1|2|',
        'The Legend of Zelda|NES|2|2|\n',
    ))


def test_list_filter():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['list', '-r', 'playlog'])
    if verbose:
        print(result.output)
    assert result.exit_code == 0
    assert result.output == '\n'.join((
        'Vectorman 2|Genesis|1|2|beep\\nboop',
        'Super Mario Bros.|NES|1|2|',
        'The Legend of Zelda|NES|2|2|\n',
    ))


def test_list_pretty():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['list', '-w', '80'])
    if verbose:
        print()
        print(result.output)
    assert result.exit_code == 0
    assert result.output == '\n'.join((
        'Title                                               | System   | Own | Progress',
        '--------------------------------------------------------------------------------',
        'Sonic the Hedgehog 2                                | Genesis  |     |     B',
        'Vectorman                                           | Genesis  |     |     B',
        'Vectorman 2                                         | Genesis  | P   |   P',
        'Super Mario Bros.                                   |   NES    | P   |   P',
        'The Legend of Zelda                                 |   NES    |   D |   P\n',
    ))


def test_list_pretty_smaller():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['list', '-w', '60'])
    if verbose:
        print()
        print(result.output)
    assert result.exit_code == 0
    assert result.output == '\n'.join((
        'Title                           | System   | Own | Progress',
        '------------------------------------------------------------',
        'Sonic the Hedgehog 2            | Genesis  |     |     B',
        'Vectorman                       | Genesis  |     |     B',
        'Vectorman 2                     | Genesis  | P   |   P',
        'Super Mario Bros.               |   NES    | P   |   P',
        'The Legend of Zelda             |   NES    |   D |   P\n'
    ))


def test_list_pretty_tiny():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['list', '-w', '50'])
    if verbose:
        print()
        print(result.output)
    assert result.exit_code == 0
    assert result.output == '\n'.join((
        'Title                 | System   | Own | Progress',
        '--------------------------------------------------',
        'Sonic the Hedgehog 2  | Genesis  |     |     B',
        'Vectorman             | Genesis  |     |     B',
        'Vectorman 2           | Genesis  | P   |   P',
        'Super Mario Bros.     |   NES    | P   |   P',
        'The Legend of Zelda   |   NES    |   D |   P\n'
    ))


def test_delete():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['delete', 'Vectorman', 'Genesis'])
    if verbose:
        print(result.output)
    assert result.exit_code == 0
    assert result.output == "Removed Vectorman for Genesis from your collection.\n"


def test_update():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['update', 'Super Mario Bros.', 'NES', 'progress', 'c'])
    if verbose:
        print(result.output)
    assert result.exit_code == 0
    assert result.output == 'Updated Super Mario Bros. for NES. Its progress is now complete.\n'

    list_result = runner.invoke(vgstash_cli.cli, ['list', '-w', '40'])
    if verbose:
        print(list_result.output)
    assert list_result.exit_code == 0
    assert list_result.output == "\n".join((
        'Title       | System   | Own | Progress',
        '----------------------------------------',
        'Sonic the H | Genesis  |     |     B',
        'Vectorman 2 | Genesis  | P   |   P',
        'Super Mario |   NES    | P   |       C',
        'The Legend  |   NES    |   D |   P\n'
    ))

def test_notes():
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['notes', 'Vectorman 2', 'Genesis'])
    if verbose:
        print(result.output)
    assert result.exit_code == 0
    assert result.output == "\n".join((
        'Notes for Vectorman 2 on Genesis:',
        '',
        'beep',
        'boop\n'
    ))

def test_notes_edit():
    if not interactive:
        return
    runner = CliRunner()
    result = runner.invoke(vgstash_cli.cli, ['notes', 'Vectorman 2', 'Genesis', '-e'])
    if verbose:
        print(result.output)
    assert result.exit_code == 0
    assert result.output == "Notes for Vectorman 2 on Genesis have been updated!\n"

    # List the results to make sure they match what the editor has.
    list_runner = CliRunner()
    list_result = runner.invoke(vgstash_cli.cli, ['list', '-r'])
    if verbose:
        print(list_result.output)
    assert list_result.exit_code == 0
