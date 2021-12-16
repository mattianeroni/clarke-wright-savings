## Clarke & Wright Savings 
*A small Python package that provides all the instruments to quickly implement your own Clarke &amp; Wright Savings heuristic algorithm*

-----------------------------------------------------------------

#### End users
This repository is supposed to be useful for people who have to quickly implement the Clarke &amp; Wright Savings (CWS) algorithm or a similar procedure inspired by it.

#### Structure 
The main elements are:
- the main `ClarkeWrightSavings` class representing the algorithm instance;
- the `CWSConfiguration` class representing a particular configuration of parameters;
- the `Edge` and `Node` classes from which the respective new implementations have to inherit.

#### Usage 
Let's suppose we want to implement the CWS to a classsic Vehicle Routing Problem (VRP). In this case, our nodes will be the customers to visit, and the edges will be the streets connecting customers to each other.

So, first, let's go to import the CWS package.
``` python
import cws
```

Then, let's create our own classes representing the customers and the streets.
``` python
class Street (cws.Edge):
    pass
    
    
class Customer (cws.Node):
    def __init__(self, id, city):
        self.city = city
        dn_edge = Street("depot", self, 0, cost=distance(depot, city))
        nd_edge = Street(self, "depot", 0, cost=distance(city, depot))
        dn_edge.inverse = nd_edge
        nd_edge.inverse = dn_edge
        super(Customer, self).__init__(id, dn_edge, nd_edge)

```
As you can see, both classes inherits from the relative `Edge` and `Node` class implemented into the CWS package. In thi way, they inherits method and attributes that will be used by the algorithm to carry out its computations.

In case of the `Street`, we don't need to include any additional aspect. Each street will therefore be instantiated as
``` python
newstreet = Street(origin, dest, saving, cost)
```
where *origin* is the `Customer` of origin, *dest* the `Customer` of destination, *saving* the respective saving value, and *cost* the respective cost value.

Concerning the customers, additional attributes are in this case considered, such as a reference to the *city* where the customer is located.
You can see from the `__init__` method as each `Node` requires an *id*, and the edges (or in this case streets) connecting the the node to the depot and the depot to the node (i.e., respectively `nd_edge` and `dn_edge`).

> **NOTE** It is very important to note that each edge (or street in this case) needs to know which is its inverse and the user is supposed to make this assignment!

> Given *i* a generic edge going from node *a* to node *b*, the inverse is the edge going from *b* to *a*, and, in some cases, it may have a different saving and cost value.

Now that we have created our own customised nodes and edges instances, we can proceed instantiating the `ClarkeWrightSavings` algorithm:
``` python
solver = cws.ClarkeWrightSavings(nodes=customers, edges=streets)
```
As you can see, we passed the set of customers as nodes, and the set of streets as edges.

We are now ready to define the configuration of parameters and run the algorithm. For doing that, the `CWSConfiguration` class is instantiated, and the function `__call__` of the `solver` is called. We will go later into more details for each single parameter.
``` python
config = cws.CWSConfiguration()
solution, cost = solver.__call__(config)
```
As you can see, the method `__call__` returns a tuple, where the first element is the list of routes, and the second one the cost of the returned.

#### Configuration parameters
In the previous example, the default configuration was used. There is although the possibility to define a different configuration that affects the behaviour of the algorithm. The default `CWSConfiguration` class is reported below:
``` python
config = cws.CWSConfiguration(
    biased = True,
    biasedfunc = cws.biased_randomisation,
    reverse = True,
    metaheuristic = True,
    start = None,
    maxiter = 1000,
    maxnoimp = 500,
    maxcost = float("inf"),
    minroutes = float("-inf"),
)
```
The parameters which is possible to change are the following:
-   **biased**: If True a biased randomisation in the selection of elements from the savings list is used, otherwise not (for further information on the biased randomisation take a look at *Grasas, A., Juan, A. A., Faulin, J., De Armas, J., & Ramalhinho, H. (2017). Biased randomization of heuristics using skewed probability distributions: a survey and some applications. Computers & Industrial Engineering, 110, 216-228.*).
-   **biasedfunc**: The probabilistic function used to carry out the biased randomisation. The default function is a quasi-geometric distribution
``` python 
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
```




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
