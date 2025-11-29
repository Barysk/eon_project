class Connection:
    """Represents a connection from one point in the network to another. Stores the time variable traffic."""
    def __init__(self, src : int, dest : int, rates : list[float]) -> None:
        """
        Constructor
        :param src: source node
        :param dest: destination node
        :param rates: a list of time-variable traffic rates
        """
        self.source = src
        self.destination = dest
        self.rates = rates

    def __repr__(self) -> str:
        return f"[Connection from {self.source} to {self.destination}]"