# -*- coding: utf-8 -*-
from pyasista import Environment


def test_get_environment():
    # Development
    environment = Environment.get('DEVELOPMENT')
    assert environment == Environment.DEVELOPMENT

    # Testing
    environment = Environment.get('TESTING')
    assert environment == Environment.TESTING

    # Prod
    environment = Environment.get('PRODUCTION')
    assert environment == Environment.PROD


def test_environment_fallback():
    # fallbacks to Development
    environment = Environment.get('DUMMY')
    assert environment == Environment.DEVELOPMENT


def test_get_environment_case():
    # environments are case-sensitive
    environment = Environment.get('testing')
    assert environment == Environment.DEVELOPMENT
