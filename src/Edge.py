class Edge:
    """ The Edge class is used to store information about a connection in an EON

    Attributes:
    source : int - The source node

    dest : int - The destination node

    bands : list[bool] - A list representing the availability of optical slots along the connection
    """

    def __init__(self, source : int, destination : int):
        self.source = source
        self.destination = destination
        self.bands : list[bool] = [False] * 320 # stores info about the availability of slots

    def is_spectrum_free(self, start:int, length:int) -> bool:
        """ Return True if the connection is free, False otherwise

        :param start:int - The first slot of the connection
        :param length:int - The length of the connection
        :return: True if the connection is free, False otherwise
        """
        for i in range(start, length):
            if self.bands[i]:
                return False
        return True


if __name__ == "__main__":
    e = Edge(1, 2)
    e.bands[1] = True
    print(e.is_spectrum_free(3, 2))