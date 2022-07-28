import random
import operator
import collections
import functools
import itertools
import math
import dataclasses
import typing



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
        idx = int(math.log(random.random(), 1.0 - beta)) % len(options)
        yield options.pop(idx)



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

    @property
    def first_node (self):
        """
        The first node of the route visited after the origin.
        """
        return self.edges[0].dest

    @property
    def last_node (self):
        """
        The last node of the route visited before returning to the
        origin.
        """
        return  self.edges[-1].origin

    def popleft (self):
        """
        This method removes the first edge from the route and takes care
        of updating the overall cost too.
        """
        removed = self.edges.popleft()
        self.cost -= removed.cost

    def popright (self):
        """
        This method removes the last edge from the route and takes care
        of updating the overall cost too.
        """
        removed = self.edges.pop()
        self.cost -= removed.cost

    def extend (self, edges):
        """
        This method is preferable for extending the route with new
        edges because it automatically updates the cost too.

        :param edges: The new edges to add to the route.
        """
        self.edges.extend(edges)
        self.cost += sum(edge.cost for edge in edges)

    def append (self, edge):
        """
        This method is preferable for adding a new edge to the route
        because it automatically updates the cost too.

        :param edge: The new edge to add to the route.
        """
        self.edges.append(edge)
        self.cost += edge.cost

    def __repr__(self):
        return str(list(self.edges))



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
                    Usually this parameter is False when the reverse of an edge
                    is different by the edge itself.
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
    biased : bool = True
    biasedfunc : typing.Callable = biased_randomisation
    reverse : bool = True
    metaheuristic : bool = False
    start : typing.Tuple[typing.List[Route], int] = None
    maxiter : int = 1000
    maxnoimp : int = 500
    maxcost : float = float('inf')
    minroutes : float = float('-inf')



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
        return Route(collections.deque(reversed([e.inverse for e in route.edges])))

    def heuristic (self, config):
        """
        This method is the core of the algorithm. Here is where the well-known
        Clarke & Wright Savings algorithm is implemented.

        It is indirectly used by the main method __call__, or it can be used
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

            # Get the routes connected by the currently considered edge
            origin, dest = edge.origin, edge.dest
            iroute, jroute = edge.origin.route, edge.dest.route

            # If the routes are the same, next edge is considered
            if iroute == jroute:
                continue

            # Check if extremes of edge are internal. In this case,
            # next edge is considered.
            if (origin != iroute.first_node and origin != iroute.last_node) or \
                (dest != jroute.first_node and dest != jroute.last_node):
                continue

            # If the merging is possible with no reversions...
            if origin == iroute.last_node and dest == jroute.first_node:
                # If the maxcost of a route is not exceeded...
                if iroute.cost + jroute.cost - edge.saving <= maxcost:
                    # Remove the edges to the origin in the merged routes
                    iroute.popright(); jroute.popleft()
                    # Build the new route
                    iroute.append(edge)
                    iroute.extend(jroute.edges)
                    # Update the reference to the route in the nodes
                    edge.dest.route = iroute
                    for e in itertools.islice(jroute.edges, 0, len(jroute.edges) - 1):
                        e.dest.route = iroute
                    # Update the list of routes
                    routes.remove(jroute)
                # Next edge is considered
                continue
            
            # Control not needed?
            # If it is not possible to reverse the routes and the edge
            #if not reverse and (origin != iroute.last_node or dest != jroute.first_node):
            #    continue

            # If the reversion of routes is possible
            if reverse:
                # Initialise the reversed edge and routes before eventual
                # reversing process.
                redge, riroute, rjroute = edge, iroute, jroute

                # If both routes should be reversed, reverse the edge
                if origin == iroute.first_node and dest == jroute.last_node:
                    redge = edge.inverse
                # Reverse the first route
                elif origin != iroute.last_node and dest == jroute.first_node:
                    routes.remove(iroute)
                    riroute = self._reversed(iroute)
                    routes.append(riroute)
                # Reverse the second route
                elif origin == iroute.last_node and dest != jroute.first_node:
                    routes.remove(jroute)
                    rjroute = self._reversed(jroute)
                    routes.append(rjroute)

                # Once routes and edge are ready for merging, check the cost
                # If the cost of the new route does not exceed the maximum allowed...
                if riroute.cost + rjroute.cost - redge.saving <= maxcost:
                    # Remove the edges to the origin in the merged routes
                    riroute.popright(); rjroute.popleft()
                    # Build the new route
                    riroute.append(redge)
                    riroute.extend(rjroute.edges)
                    # Update the reference to the route in the nodes
                    for e in itertools.islice(riroute.edges, 0, len(riroute.edges) - 1):
                        e.dest.route = riroute
                    # Update the list of routes
                    routes.remove(rjroute)

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
        best, cost = starting_sol
        maxiter, maxnoimp = config.maxiter, config.maxnoimp
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
        if config.metaheuristic:
            starting_sol = config.start or self.heuristic(config)
            best, cost = self._metaheuristic(starting_sol, config)
        return best, cost
