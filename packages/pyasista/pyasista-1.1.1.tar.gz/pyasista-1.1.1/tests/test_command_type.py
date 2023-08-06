# -*- coding: utf-8 -*-
from pyasista import CommandType


def test_get_command_type():
    # Play announcement
    command_type = CommandType.get('PLAY_SOUND')
    assert command_type == CommandType.PLAY_ANNOUNCE

    # Play stream
    command_type = CommandType.get('PLAY_STREAM')
    assert command_type == CommandType.PLAY_STREAM

    # Stop
    command_type = CommandType.get('STOP')
    assert command_type == CommandType.STOP

    # No action
    command_type = CommandType.get('NOACTION')
    assert command_type == CommandType.NOACTION


def test_command_type_fallback():
    # fallbacks to NOACTION
    command_type = CommandType.get('DUMMY')
    assert command_type == CommandType.NOACTION


def test_get_command_type_case():
    # command types are case-sensitive
    command_type = CommandType.get('play_stream')
    assert command_type == CommandType.NOACTION
