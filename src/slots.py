import warnings
from itertools import count


class Slots:
    """ Stores data about the EON connection slots for use in the graphX library"""

    def __init__(self):
        self.__slots : list[bool] = [False] * 320 # stores info about the availability of slots

    def __repr__(self) -> str:
        return f"[Taken: {self.__slots.count(True)}; Free: {self.__slots.count(False)}]"

    def is_spectrum_free(self, start:int, length:int) -> bool:
        """
        Checks weather the specified slots are free
        :param start: The first slot of the connection
        :param length: The length of the connection
        :return: True if the connection is free, False otherwise
        """
        for i in range(start, length):
            if self.__slots[i]:
                return False
        return True

    def reserve_slots(self, start: int, length: int) -> None:
        """
        Reserve slots along the connection.
        :param start: The first slot of the connection
        :param length: The length of the connection
        :return: None
        """
        if not self.is_spectrum_free(start, length):
            raise ValueError("Slots not free!") # safety
        for i in range(start, length):
            self.__slots[i] = True

    def free_slots(self, start: int, length: int) -> None:
        """
        Free used slots along the connection.
        :param start: The first slot of the connection
        :param length: The length of the connection
        :return: None
        """
        for i in range(start, length):
            if not self.__slots[i]:
                warnings.warn("Freed up an already free slot!", RuntimeWarning) # safety
            self.__slots[i] = False
