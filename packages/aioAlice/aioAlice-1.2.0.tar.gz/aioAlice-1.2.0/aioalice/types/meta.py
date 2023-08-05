from attr import attrs, attrib
from aioalice.utils import safe_kwargs
from . import AliceObject


@safe_kwargs
@attrs
class Meta(AliceObject):
    """Meta object"""
    locale = attrib(type=str)
    timezone = attrib(type=str)
    client_id = attrib(type=str)
    flags = attrib(factory=list)
