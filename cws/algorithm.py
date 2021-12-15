import random
import operator
import collections
import functools
import dataclasses
import typing


class Route (object):
    """
    An instance of this class represents a route made by a sequence
    of edges.
    """
    def __init__ (self, edges = None):
        """
        Initialise.

        :param edges: The edges that currently constitute the route.
        :attr cost: The overall cost of the route.
        """
        self.edges = edges or collections.deque()
        self.cost = sum(edge.cost for edge in self.edges)

    def extend (self, edges):
        """
        This method is preferable for extending the route with new
        edges because it automatically updates the cost too.

        :param edges: The new edges to add to the route.
        """
        self.edges.extend(edges)
        self.cost += sum(edge.cost for edge in self.edges)

    def __repr__(self):
        return "->".join([edge for edge in self.edges])


def biased_randomisation (array, beta=0.3):
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



@dataclasses.dataclass(repr=True, frozen=True)
class CWSConfiguration:
    """
    An instance of this class represents a configuration of the parameters
    used during the execution of the algorithm.
    It can be passed to the heuristic method as well as to the __call__ method.

    :param biased: If True a biased randomisation is used, otherwise not.
                    In case of active biased randomisation the callable method
                    passed as biasedfunc is used.
    :param biasedfunc: The function to use in case of biased randomisation
                        required.
    :param reverse: If True every time a merging is tried, the possibility
                    to reverse the routes we are going to merge is considered.
    :param metaheuristic: If True more solutions are generated doing a sort
                        of iterated local search, otherwise a single solution
                        is returned using the classic heuristic.
    :param start: The starting solution generated with a different method or
                 parameters, we want the metaheuristic to start from.
    :param maxiter: The maximum number of solutions explored in case of a
                    metaheuristic.
    :param maxnoimp: The maximum number of
    :param maxcost: The maximum cost of a route that makes it feasible.
    :param minroutes: The minimum number of routes allowed.
    """
    biased : bool = False
    biasedfunc : typing.Callable = biased_randomisation,
    reverse : bool = True,
    metaheuristic : bool = False,
    start : typing.Tuple[typing.List[Route], int] = None,
    maxiter : int = 1000,
    maxnoimp : int = 500,
    maxcost : float = float('inf'),
    minroutes : float = float('inf')



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
    def savings_list (edges):
        """
        Given the set of edges, this method generates the savings list
        by simply sorting them for decreasing saving value.

        :param edges: The edges list.
        """
        return sorted(edges, key=operator.attrgetter("saving"), reverse=True)

    @staticmethod
    def _reversed (route):
        """
        This method is used to reverse a route.
        It instantiate and return a new Route.

        :param route: The route to reverse.
        """
        pass

    def heuristic (self, biased, biasedfunc, reverse, maxcost, minroutes):
        """
        This method is the core of the algorithm. Here is where the well-known
        Clarke & Wright Savings algorithm is implemented.

        It is indirectly used by the mainmethod __call__, or it can be used
        alone for generating a single solution using different berameters or
        behaviour.

        :param config: The configuration used during the execution of the heuristic
                        (see CWSConfiguration class).
        """
        edges, nodes = self.edges, self.nodes
        biased, biasedfunc, reverse = config.biased, config.biasedfunc, config.reverse
        maxcost, minroutes = config.maxcost, config.minroutes
        routes = list()

        # Generates the dummy solution
        for node in nodes:
            r = Route(collections.deque([node.dn_edge, node.nd_edge]))
            node.route = r
            routes.append(r)

        # Generates the savings list with eventual biased randomisation
        savings_list = self.savings_list(edges)
        savings_iterator = savings_list if not biased else biasedfunc(savings_list)

        # Starts the iterative merging process...
        for edge in savings_iterator:
            # Check if the minimum number of routes has been reached
            if len(routes) <= minroutes:
                return routes, sum(r.cost for r in routes)

        # Returns the solution found
        return routes, sum(r.cost for r in routes)


    def _metaheuristic (self, starting_sol, config):
        """
        This method represents an Iterated Local Search in which
        the Clarke Wright Savings heuristic is incorporated.
        In order to generate a ifferent solution at each iteration,
        the biased randomisation in the configuration should be activated
        and a biasedfunc should be provided.

        :param starting_sol: The starting solution.
        :param config: The configurations of parameters defined.
        """
        # Initialise the behaviour we want to use to generate new solutions
        heuristic = functools.partial(self.heuristic, config)
        # Initialise the current best solution
        best, cost = sarting_sol
        missed_improvements = 0
        # Starts the iterated local search
        for _ in range(maxiter):
            # Generates a new solution
            newsol, newcost = heuristic()
            missed_improvements += 1
            # Eventually updates the best
            if newcost < cost:
                best, cost = newsol, newcost
                missed_improvements = 0
            # If the maximum number of iterations with no improvement is exceeded
            # returns the current best
            if missed_improvements > maxnoimp:
                return best, cost
        # Return the best solution found at the end of the process
        return best, cost



    def __call__(self, config):
        """
        This method representes the main function of the algorithm.

        :param config: The configuration of parameters used for the
                        execution of the algorithm (see CWSConfiguration class).
        """
        best, cost = self.heuristic(config)
        if metaheuristic:
            starting_sol = start or self.heuristic(config)
            best, cost = self._metaheuristic(starting_sol, config)
        return best, cost
