import abc
import typing

from ..entity import bot, connection


class AbsPlatformAdapter(metaclass=abc.ABCMeta):

    _action_handler: typing.Callable[
        [bot.Bot, connection.ConnectionType, str],
        typing.Coroutine[typing.Any, typing.Any, typing.Any]
    ]
    """动作处理器"""

    def action_handler(self, handler: typing.Callable[
        [bot.Bot, connection.ConnectionType, str],
        typing.Coroutine[typing.Any, typing.Any, typing.Any]
    ]):
        """
        设置 API 调用处理器
        当客户端发起一个动作（调用API）时，平台服务端实现将接收到的数据直接发给这个处理器
        """
        self._action_handler = handler
    
    @abc.abstractmethod
    async def emit_event(self, bots: typing.List[bot.Bot], event: dict):
        """
        发送事件
        通过这个方法，调用平台服务端，将事件数据dict发送给客户端
        """
        pass

    @abc.abstractmethod
    async def run(self, bots: typing.List[bot.Bot], **kwargs):
        pass

    @abc.abstractmethod
    async def kill(self):
        pass