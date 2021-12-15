import abc


class Node (abc.ABC):
    """
    The class that inherits from this one
    inherits all the attributes and methods
    needed to work as an Node of the graph
    on which the Clarke Wright Savings heuristic
    is going to be computed.
    """
    def __init__(self, id, dn_edge, nd_edge):
        """
        Initialise.

        :param id: The unique id of the node. (NOTE: There is no control
                  on the unicity of this id)
        :param dn_edge: Depot-to-node edge.
        :param nd_edge: Node-to-depot edge.
        :attr route: The cluster where the node currently is.
        """
        self.id = id
        self.dn_edge = dn_edge
        self.nd_edge = nd_edge
        self.route = None

    def __repr__(self):
        return str(self.id)
