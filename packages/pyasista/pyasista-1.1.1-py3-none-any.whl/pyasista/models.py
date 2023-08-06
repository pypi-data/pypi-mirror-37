# -*- coding: utf-8 -*-
from enum import Enum

import re


# Enumeration of supported environments (DEVELOPMENT, TESTING, PRODUCTION)
class Environment(Enum):
    """A case-sensitive enumeration of supported environments.

    Supported environments are:
        - DEVELOPMENT: 'DEVELOPMENT'
        - TESTING: 'TESTING'
        - PROD: 'PRODUCTION'
    """
    DEVELOPMENT = 'DEVELOPMENT'
    TESTING = 'TESTING'
    PROD = 'PRODUCTION'

    # A static method returning the related enum for the given environment.
    # For unrecognized environments, fallbacks to DEVELOPMENT
    @staticmethod
    def get(environment):
        """A static method to parse an object to Environment instance.
        If the object is not a valid environment, fallback to
        Environment.DEVELOPMENT.

        :param environment: An object, the key for the Environment.
        :rtype: Environment

        Usage::

            >>> from pyasista import Environment
            >>> env = 'TESTING'
            >>> environment = Environment.get(env)
            <Environment.TESTING: 'TESTING'>

            ... or

            >>> from pyasista import Environment
            >>> env = 'ILLEGAL'
            >>> environment = Environment.get(env)
            <Environment.DEVELOPMENT: 'DEVELOPMENT'>
        """
        if not isinstance(environment, str):
            return Environment.DEVELOPMENT
        for env in Environment:
            if env.value == environment:
                return env
        return Environment.DEVELOPMENT


# An inner class of AsistaInput, for helping Asista handle OAUTH access and
# refresh tokens.
class AsistaToken:
    """An helper class to hold and refresh Arçelik Smart Assistant token."""

    def __init__(self, token):
        self.__access_token = None
        self.__asista_refresh_data = None
        self.__asista_refresh_token_uri = None
        self.__asista_client_key = None
        if isinstance(token, dict):
            self.__access_token = token.get('access_token', None)
            self.__asista_refresh_data = token.get('asista_refresh_data', None)
            self.__asista_refresh_token_uri = token.get(
                'asista_refresh_token_uri', None)
            self.__asista_client_key = token.get('asista_client_key', None)

    # URL regular expression pattern.
    __URL_PATTERN = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # domain
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain (cont.) or
        r'localhost|'  # localhost or
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ip
        r'(?::\d+)?'  # port (optional)
        r'(?:/?|[/?]\S+)$',  re.IGNORECASE
    )

    def is_valid(self):
        """Checks whether an ``AsistaToken`` object is in correct form.
        This method does not check whether the access token is valid or not,
        it merely validates the ``AsistaToken`` is structurally refreshable.

        :rtype: :Boolean: True if the token is valid, else False.

        Usage::

            >>> ...
            >>> token = asista_input.token
            >>> token.is_valid()
            True
        """
        if (isinstance(self.__access_token, str) and
                isinstance(self.__asista_client_key, str) and
                isinstance(self.__asista_refresh_data, str) and
                isinstance(self.__asista_refresh_token_uri, str) and
                re.match(AsistaToken.__URL_PATTERN,
                         self.__asista_refresh_token_uri) is not None):
            return True
        return False

    # Method for refreshing the refresh token
    def refresh(self):
        """An helper method to refresh an AsistaToken object.

        :rtype: :Boolean: True if the token is refreshed successfully,
        else False.

        Usage::

            >>> ...
            >>> token = asista_input.token
            >>> token.refresh()
        """
        try:
            # botocore is available in all lambda functions, check this first
            from botocore.vendored import requests
            from botocore.vendored.requests.packages import urllib3
        except ModuleNotFoundError:
            try:
                # Not in AWS lambda, check requests is available.
                import requests
                import urllib3
            except ModuleNotFoundError:
                print('requests module is required to refresh the token. Use' +
                      ' pip install requests to install.')
                return False

        if not self.is_valid():
            # TODO: raise error as the token object is not valid
            return False

        headers = {
            'Authorization': 'Token {}'.format(self.__asista_client_key)
        }

        params = {
            'data': self.__asista_refresh_data
        }

        # Disable insecure request warning than enable
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            resp = requests.post(self.__asista_refresh_token_uri,
                                 headers=headers,
                                 data=params,
                                 verify=False)
        except Exception as e:
            print('Cannot refresh token. HTTPException={}'.format(e))
            resp = None
        finally:
            urllib3.warnings.resetwarnings()

        if resp is None:
            return False

        if resp.status_code == 200:
            new_token = AsistaToken.__parse_refresh_response(resp)
            if new_token is not None:
                self.__access_token = new_token
                return True
        else:
            print('Cannot refresh access token. ' +
                  'HTTP Error: StatusCode={} '.format(resp.status_code) +
                  'Response={}'.format(resp))
        return False

    @staticmethod
    def __parse_refresh_response(resp):
        try:
            token_output = resp.json()
        except:
            print('Token refresh is unsuccessful. Response is not in ' +
                  'the correct format.')
            return None
        if 'success' not in token_output:
            print('Token refresh is unsuccessful. Response is not in ' +
                  'the correct format.')
            return None
        result = token_output['success']
        if result and 'token' in token_output:
            token = token_output['token']
            if 'access_token' in token:
                return token['access_token']
            print('Token refresh is unsuccessful. Response is not in ' +
                  'the correct format.')
        else:
            if 'error' in token_output:
                reason = token_output['error']
                print('Cannot refresh the token. {}'.format(reason))
            else:
                print('Cannot refresh the token. Error code not found.')
        return None

    # Public getter for the access token
    @property
    def access_token(self):
        """Access token to access restricted sources."""
        return self.__access_token


# A standard class for the Lambda input
class AsistaInput:
    """A wrapper class for a default lambda_handler ``event`` for Arçelik Asista.

    :param event: Event of the lambda handler to be parsed.
    :param required_parameters: List of required parameters for the lambda.

    Usage::

        >>> from pyasista import AsistaInput
        >>> def lambda_handler(event, context):
        ...     asista_input = AsistaInput(event)
        ...     # All input parameters are accessible from asista_input
        ...     print(asista_input.language)  # TR
        ...     print(asista_input.serial_number)  # 'QNUBQWERTY123'
        ...     return dict()
    """
    def __init__(self, event, required_parameters=None):
        required = []  # Default required parameters, for future use.

        # event should be a python dictionary
        if not isinstance(event, dict):
            print('Cannot parse \'event\'.' +
                  '[expected_type=dict, actual_type={}]'.format(type(event)))
            raise TypeError('Cannot parse \'event\'.[expected_type=dict, ' +
                            'actual_type={}]'.format(type(event)))

        if required_parameters is None:
            required_parameters = []
        elif not isinstance(required_parameters, list):
            print('\'required_parameters\' should be a list. [expected_type=' +
                  'list, actual_type={}]'.format(type(required_parameters)))
            required_parameters = []

        # concat required parameters with the default required parameters
        required += required_parameters

        # Get `timeout`. Default is False.
        self.__timeout = event.get('timeout', False)

        # If any one of the required parameters does not exists in the event
        # and timeout is not True, raise a KeyError
        if not self.__timeout and not all(key in event for key in required):
            # Log the error
            if 'serial_number' in event:
                print('[{}] Lambda input does'.format(event['serial_number']) +
                      ' not contain one or  more of the required parameters')
            else:
                print('Lambda input does not contain one or more of the ' +
                      'required parameters.')
            raise KeyError('Lambda input does not contain one or more of ' +
                           'the required parameters.')

        # Parse input data
        try:
            self.__environment = Environment.get(event['environment'])
        except KeyError:
            self.__environment = None
        self.__ext_node_id = event.get('ext_node_id', None)
        # Default language is Turkish
        self.__language = event.get('language', 'TR')
        self.__location = event.get('location', {
            'latitude': None,
            'longitude': None
        })
        self.__serial_number = event.get('serial_number', None)
        self.__session = event.get('session', dict())
        self.__slot_values = AsistaInput.__parse_slot_values(
            event.get('slot_values', None))
        self.__sr_text = event.get('sr_text', None)
        self.__token = AsistaToken(event.get('token', dict()))

        if 'is_customer_confirmed' in event:
            self.__customer_confirmed = event['is_customer_confirmed']

    # Public getters for the class variables
    @property
    def ext_node_id(self):
        return self.__ext_node_id

    @property
    def environment(self):
        return self.__environment

    @property
    def language(self):
        return self.__language

    @property
    def location(self):
        return self.__location

    @property
    def serial_number(self):
        return self.__serial_number

    @property
    def session(self):
        return self.__session

    @property
    def slot_values(self):
        """A ``dictionary`` of slot values."""
        return self.__slot_values

    @property
    def sr_text(self):
        return self.__sr_text

    @property
    def timeout(self):
        """User has not responded in the 10 seconds period
        when the session_continue is True.
        """
        return self.__timeout

    @property
    def token(self):
        return self.__token

    @property
    def customer_confirmed(self):
        try:
            return self.__customer_confirmed
        except AttributeError:
            return None

    @staticmethod
    def __parse_slot_values(slot_values):
        parameters = dict()
        if isinstance(slot_values, list):
            for slot_value in slot_values:
                key, value = AsistaInput.__parse_slot_value(slot_value)
                # If key is found, add to the parameter dictionary
                if key is not None:
                    try:
                        parameters[key].append(value)
                    except KeyError:
                        parameters[key] = list()
                        parameters[key].append(value)
        return parameters

    @staticmethod
    def __parse_slot_value(slot_value):
        # Slot values should be strings of format key=value
        if not isinstance(slot_value, str):
            return None, None
        if '=' in slot_value:
            try:
                key, value = slot_value.split('=')

                # Replace the keywords, odoto & ocommao
                key = key.strip().replace(
                    'odoto', '.'
                ).replace(
                    'ocommao', ','
                )

                value = value.strip().replace(
                    'odoto', '.'
                ).replace(
                    'ocommao', ','
                )

                # 'NULL' is sent when the parameter is not detected
                if value == 'NULL':
                    value = None
            # If slot_value has more than one = sign, it will give
            # ValueError (not a valid format, just ignore)
            except ValueError:
                return None, None
        # If the slot value does not have an = sign, there are no
        # parameters to be parsed.
        else:
            return None, None
        return key, value


# Enumeration of supported Commands (PLAY_SOUND, PLAY_STREAM, DO_NOTHING)
class CommandType(Enum):
    """An enumeration of valid Asista commands.

    Supported commands are:
        - PLAY_ANNOUNCE: 'PLAY_SOUND'  # Use TTS to create the announcement.
        - PLAY_STREAM: 'PLAY_STREAM'  # Use an external resource to stream.
        - STOP: 'STOP'  # Terminate.
        - NOACTION: 'NOACTION'  # Take no action.

    Usage::

        >>> from pyasista import CommandType
        >>> command_type_name = 'PLAY_SOUND'
        >>> command_type = CommandType.get(command_type_name)
        <CommandType.PLAY_ANNOUNCE: 'PLAY_SOUND'>

        ... or

        >>> from pyasista import Command
        >>> from pyasista import CommandType
        >>> command_type = CommandType.PLAY_STREAM
        >>> command = Command(command_type, 'https://stream.url/')
        {'command': 'PLAY_STREAM', 'payload': {'data': 'https://stream.url/'}}
    """
    PLAY_ANNOUNCE = 'PLAY_SOUND'
    PLAY_STREAM = 'PLAY_STREAM'
    STOP = 'STOP'
    NOACTION = 'NOACTION'

    # A static method returning the related enum for the given command type str
    # For unrecognized command types, fallbacks to NOACTION.
    @staticmethod
    def get(command_type):
        """A static method to parse an object to CommandType instance.
        If the object is not a valid command type, fallback to
        CommandType.NOACTION.

        :param command_type: An object, the key for the CommandType.
        :rtype: CommandType
        """
        if not isinstance(command_type, str):
            return CommandType.NOACTION
        for ct in CommandType:
            if ct.value == command_type:
                return ct
        return CommandType.NOACTION


# An inner class of AsistaOutput, to help Asista take the desired action.
class Command:
    """A wrapper class for a generic Asista command.

    Asista is capable of the following tasks:
        - Play an announcement using TTS.
        - Play a stream using an external resource.
        - Do nothing.

    Lambda handler for a typical Arçelik Smart Asistant lambda function
    return an ``AsistaOutput`` object which has a list of ``Command``s.

    :param command_type: Desired command type.
    :param payload: Data for the command.

    Usage::

        >>> from pyasista import AsistaOutput
        >>> from pyasista import Command
        >>> from pyasista import CommandType
        >>> output = AsistaOutput()
        >>> command = Command(CommandType.PLAY_ANNOUNCE, 'Hello from Asista.')
        >>> output.push_command(command)
    """
    def __init__(self, command_type, payload=None):
        if isinstance(command_type, str):  # Parse command
            self.__command = CommandType.get(command_type)
        elif isinstance(command_type, CommandType):
            self.__command = command_type
        else:
            raise TypeError('Cannot set \'command_type\'. [expected_types=' +
                            '[str,CommandType], actual_type={}]'.format(
                                type(command_type)))

        if (self.__command == CommandType.NOACTION or
            self.__command == CommandType.STOP or
                payload is None):
            self.__payload = dict()
        elif (self.__command == CommandType.PLAY_ANNOUNCE or
                self.__command == CommandType.PLAY_STREAM):
            self.__payload = {'data': payload}

    def __iter__(self):
        obj_dictionary = {
            'command': self.__command.value,
            'payload': self.__payload
        }
        for key, value in obj_dictionary.items():
            yield (key, value)

    def __repr__(self):
        return str(dict(self))


# A standard class for tbe Lambda output
class AsistaOutput:
    """A wrapper class for a default lambda_handler output for Arçelik Asista.

    Usage::

        >>> from pyasista import AsistaInput
        >>> from pyasista import AsistaOutput
        >>> from pyasista import Command
        >>> from pyasista import CommandType
        >>> def lambda_handler(event, context):
        ...     asista_input = AsistaInput(event)
        ...     # Implement your business logic.
        ...     asista_output = AsistaOutput()  # Initialize an instance
        ...     # Session will continue [default=False]
        ...     asista_output.session_continue(True)
        ...     # Add session data
        ...     asista_output.session({'session_data': 'my_data'})
        ...     # Create a ``Command`` for Asista
        ...     command = Command(CommandType.PLAY_ANNOUNCE,
                                  'Hello from Asista')
        ...     asista_output.push_command(command)  # Add created command
        ...     # As AsistaOutput is not serializable, ``dict(AsistaOutput)``
        ...     # should be returned.
        ...     return dict(asista_output)
    """
    def __init__(self):
        self.__session_continue = False
        self.__session = dict()
        self.__commands = []

    # obj.__dict__ should return an actual dictionary.
    # By overriding __iter__ method, we can achieve this.
    def __iter__(self):
        # Create Command dictionaries
        commands = []
        for command in self.__commands:
            commands.append(dict(command))

        # Create object dictionary
        obj_dictionary = {
            'session_continue': self.__session_continue,
            'session': self.__session,
            'commands': commands
        }

        # Yield values one by one
        for key, value in obj_dictionary.items():
            yield (key, value)

    def __repr__(self):
        return str(dict(self))

    # Public setters for the class variables with input validations.
    def session_continue(self, session_continue):
        if isinstance(session_continue, bool):
            self.__session_continue = session_continue
        else:
            raise TypeError('Cannot set \'session_continue\'. ' +
                            '[expected_type=bool, actual_type={}.'.format(
                                type(session_continue)))

    def session(self, session):
        if isinstance(session, dict):
            self.__session = session
        else:
            raise TypeError('Cannot set \'session\'. [expected_type=dict, ' +
                            'actual_type={}.'.format(type(session)))

    def push_command(self, command):
        """Add a ``Command`` instance to the output."""
        if isinstance(command, Command):
            self.__commands.append(command)
        else:
            raise TypeError('Cannot set \'command\'. [expected_type=Command,' +
                            ' actual_type={}.'.format(type(command)))

    @staticmethod
    def with_stream(data):
        """Creates an instance with PLAY_STREAM command."""
        if not isinstance(data, str):
            raise TypeError('Stream url should be a string.')
        instance = AsistaOutput()
        instance.push_command(Command(CommandType.PLAY_STREAM, data))
        return instance

    @staticmethod
    def with_announce(data):
        """Creates an instance with CommandType.PLAY_ANNOUNCE command."""
        if not isinstance(data, str):
            raise TypeError('Announcement should be a string.')
        instance = AsistaOutput()
        instance.push_command(Command(CommandType.PLAY_ANNOUNCE, data))
        return instance

    @staticmethod
    def with_stop():
        """Creates an instance with CommandType.STOP command."""
        instance = AsistaOutput()
        instance.push_command(Command(CommandType.STOP))
        return instance

    @staticmethod
    def with_noaction():
        """Creates an instance with CommandType.NOACTION command."""
        instance = AsistaOutput()
        instance.push_command(Command(CommandType.NOACTION))
        return instance
