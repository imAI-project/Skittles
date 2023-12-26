import abc
import typing


class AbsDriver(metaclass=abc.ABCMeta):

    handler: typing.Callable

    @abc.abstractmethod
    async def run(self, **kwargs):
        pass
