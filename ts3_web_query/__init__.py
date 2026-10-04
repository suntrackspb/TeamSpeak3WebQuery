"""Asynchronous Python wrapper for the TeamSpeak 3 HTTP WebQuery API."""

from .client import Client
from .exceptions import TeamSpeakConnectionError
from .types import TeamSpeakError

__version__ = '0.1.0'

__all__ = ['Client', 'TeamSpeakError', 'TeamSpeakConnectionError', '__version__']
