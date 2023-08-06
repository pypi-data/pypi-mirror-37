import abc

from ._pool import Pool


class Controller(metaclass=abc.ABCMeta):
    """
    Controller adjusting the demand in a :py:class:`~.Pool`

    :param target: the resource pool for which demand is adjusted
    """
    def __init__(self, target: Pool):
        self.target = target

    @abc.abstractmethod
    def regulate(self, interval: float):
        """Regulate demand for the ``pool`` in the past ``interval`` seconds"""
