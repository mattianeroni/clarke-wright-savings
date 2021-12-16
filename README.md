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
where origin is the `Customer` of origin, dest the `Customer` of destination, saving the respective saving value, and cost the respective cost value.
