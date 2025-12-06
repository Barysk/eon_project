class Route:
    def __init__(self, source : int, destination : int, edges : list[int], distance : int) -> None:
        self.source = source
        self.destination = destination
        self.edges = edges
        self.distance = distance