import random




class ClarkeWrightSavings (object):
    """
    An instance of this class represents the
    Clarke & Wright Savings heuristic implementation.
    """
    def __init__(self, nodes, edges):
        """
        Initialise.

        :param nodes: The nodes to visit.
        :param edges: The edges connecting the nodes.
        """
        self.nodes = nodes
        self.edges = edges

    @staticmethod
    def _biased_randomisation (array, beta=0.3):
        """
        This method carry out a biased-randomised selection over a certain list.
        The selection is based on a quasi-geometric function:

                        f(x) = (1 - beta) ^ x

        and it therefore prioritise the first elements in list.

        :param array: The set of options already sorted from the best to the worst.
        :param beta: The parameter of the quasi-geometric distribution.
        :return: The element picked at each iteration.
        """
        L = len(array)
        options = list(array)
        for _ in range(L):
            idx = int(log(random.random(), 1.0 - beta)) % len(options)
            yield options.pop(idx)


    def __call__(self, biased = False):
        """
        This method representes the main function of the algorithm.

        :param biased: If True a biased randmisation on the savings list is
                     carried out, otherwise not.
        """
        pass
