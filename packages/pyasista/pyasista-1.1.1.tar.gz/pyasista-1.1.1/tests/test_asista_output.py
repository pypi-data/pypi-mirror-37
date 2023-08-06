# -*- coding: utf-8 -*-
from pyasista import AsistaOutput
from pyasista import Command
from pyasista import CommandType

import pytest


def test_defaults():
    asista_output = AsistaOutput()
    output_dict = dict(asista_output)

    assert 'session_continue' in output_dict
    assert isinstance(output_dict['session_continue'], bool)
    assert not output_dict['session_continue']

    assert 'session' in output_dict
    assert isinstance(output_dict['session'], dict)
    assert len(output_dict['session']) == 0

    assert 'commands' in output_dict
    assert isinstance(output_dict['commands'], list)
    assert len(output_dict['commands']) == 0


def test_push_command():
    command = Command(CommandType.NOACTION)
    asista_output = AsistaOutput()
    asista_output.push_command(command)
    output_dict = dict(asista_output)

    assert 'commands' in output_dict
    assert isinstance(output_dict['commands'], list)
    assert len(output_dict['commands']) == 1

    output_command = output_dict['commands'][0]
    assert 'command' in output_command
    assert output_command['command'] == 'NOACTION'

    with pytest.raises(TypeError):
        asista_output.push_command('Invalid')


def test_set_session_continue():
    asista_output = AsistaOutput()
    asista_output.session_continue(True)
    output_dict = dict(asista_output)

    assert 'session_continue' in output_dict
    assert isinstance(output_dict['session_continue'], bool)
    assert output_dict['session_continue']

    with pytest.raises(TypeError):
        asista_output.session_continue('Invalid')


def test_set_session():
    asista_output = AsistaOutput()
    asista_output.session({'key': 'value', 'param': 'obj'})
    output_dict = dict(asista_output)

    assert 'session' in output_dict

    session_data = output_dict['session']
    assert isinstance(session_data, dict)
    assert len(session_data) == 2
    assert 'key' in session_data
    assert 'param' in session_data
    assert session_data['key'] == 'value'
    assert session_data['param'] == 'obj'

    with pytest.raises(TypeError):
        asista_output.session('Invalid')
