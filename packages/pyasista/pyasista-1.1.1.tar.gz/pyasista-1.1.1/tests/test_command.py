# -*- coding: utf-8 -*-
from pyasista import Command
from pyasista import CommandType


def test_create_noaction_command():
    command = Command(CommandType.NOACTION)
    command_dict = dict(command)

    assert 'command' in command_dict
    assert command_dict['command'] == 'NOACTION'


def test_create_noaction_with_data_command():
    command = Command(CommandType.NOACTION, 'dummy_data')
    command_dict = dict(command)

    # Type is NOACTION, payload will be ignored
    assert 'payload' in command_dict
    assert 'data' not in command_dict['payload']


def test_create_stop_command():
    command = Command(CommandType.STOP)
    command_dict = dict(command)

    assert 'command' in command_dict
    assert command_dict['command'] == 'STOP'


def test_create_stop_with_data_command():
    command = Command(CommandType.STOP, 'dummy_data')
    command_dict = dict(command)

    # Type is NOACTION, payload will be ignored
    assert 'payload' in command_dict
    assert 'data' not in command_dict['payload']


def test_create_stream_command():
    stream_uri = 'https://dummy.co/dummy.mp3'
    command = Command(CommandType.PLAY_STREAM, stream_uri)
    command_dict = dict(command)

    assert 'command' in command_dict
    assert command_dict['command'] == 'PLAY_STREAM'
    assert 'payload' in command_dict
    assert 'data' in command_dict['payload']
    assert command_dict['payload']['data'] == stream_uri


def test_create_announce_command():
    announcement = 'Hello, my name is Asista.'
    command = Command(CommandType.PLAY_ANNOUNCE, announcement)
    command_dict = dict(command)

    assert 'command' in command_dict
    assert command_dict['command'] == 'PLAY_SOUND'
    assert 'payload' in command_dict
    assert 'data' in command_dict['payload']
    assert command_dict['payload']['data'] == announcement
