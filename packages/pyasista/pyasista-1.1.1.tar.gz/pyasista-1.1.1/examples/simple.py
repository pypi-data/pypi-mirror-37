# -*- coding utf-8 -*-
"""Simple pyasista script"""
from pyasista import AsistaInput
from pyasista import AsistaOutput
from pyasista import Command
from pyasista import CommandType


def lambda_handler(event, context):
    """Simple function replies with 'Merhaba, benim adım Asista.'
    """
    asista_input = AsistaInput(event)
    command = Command(CommandType.PLAY_ANNOUNCE,
                      'Merhaba, benim adım Asista.')

    # Create output and add the command
    asista_output = AsistaOutput()
    asista_output.push_command(command)
    return dict(asista_output)
