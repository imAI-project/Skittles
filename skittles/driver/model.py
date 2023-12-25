import abc


class AbsDriver(metaclass=abc.ABCMeta):

    handler: callable

    @abc.abstractmethod
    async def run(self) -> int:
        pass
