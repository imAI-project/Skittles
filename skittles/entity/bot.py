import typing

import pydantic

from . import connection


class Bot(pydantic.BaseModel):
    """
    机器人实体信息
    """

    account_id: str
    """账号ID"""

    nickname: str
    """昵称"""

    connection_types: typing.List[connection.ConnectionType]
    """连接类型"""
