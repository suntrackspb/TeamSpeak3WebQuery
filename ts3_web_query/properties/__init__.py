"""TypedDict property sets for create/edit commands (give IDE completion for the keys)."""

from .channel_create import ChannelCreateProperties, ChannelEditProperties
from .client_edit import ClientEditProperties
from .server_create import (
    InstanceEditProperties, ServerCreateProperties, ServerCreateResponse, ServerEditProperties,
)

__all__ = [
    'ChannelCreateProperties',
    'ChannelEditProperties',
    'ClientEditProperties',
    'InstanceEditProperties',
    'ServerCreateProperties',
    'ServerCreateResponse',
    'ServerEditProperties',
]
