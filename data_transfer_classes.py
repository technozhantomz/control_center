from typing import Type, ClassVar
from marshmallow import Schema
from marshmallow_dataclass import dataclass


@dataclass
class DataTransferClass:
    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class IsAliveResponse:
    is_alive: bool


@dataclass
class EmptyRequest:
    pass

