import abc
import typing
import asyncio


class AbsDriver(metaclass=abc.ABCMeta):

    handler: typing.Callable

    loop: asyncio.AbstractEventLoop

    @abc.abstractmethod
    async def run(self, **kwargs):
        pass

    @abc.abstractmethod
    async def kill(self):
        pass