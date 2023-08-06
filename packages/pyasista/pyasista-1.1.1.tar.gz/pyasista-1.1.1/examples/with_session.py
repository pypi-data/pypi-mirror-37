# -*- coding utf-8 -*-
"""An example of pyasista usage with session"""
from pyasista import AsistaInput
from pyasista import AsistaOutput


def lambda_handler(event, context):
    """Pass custom session variables to the Asista."""
    asista_input = AsistaInput(event)

    # Create parameters to pass to the session
    session_parameters = {
        'key1': 'value1',
        'key2': 1,
        'key3': 1.231
    }

    # Create output with PLAY_ANNOUNCE command.
    asista_output = AsistaOutput.with_announce('Merhaba.')

    asista_output.session_continue(True)
    asista_output.session(session_parameters)
    return dict(asista_output)
