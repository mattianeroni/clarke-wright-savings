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
