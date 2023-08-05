# -*- coding: utf-8 -*-

"""Top-level package for Anybot API Automation."""

__author__ = """Djordje Pepic"""
__email__ = 'djordje.m.pepic@gmail.com'
__version__ = '0.1.1'

from .action import Action, QueuedActions, CandidateActions
from .bot import Bot


__all__ = [
    'Bot',
    'Action', 'QueuedActions', 'CandidateActions',
]
