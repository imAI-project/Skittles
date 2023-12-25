import abc


class AbsPlatformAdapter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def run(self):
        pass