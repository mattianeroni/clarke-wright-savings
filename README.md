## Clarke & Wright Savings 
*A small Python package that provides all the instruments to quickly implement your own Clarke &amp; Wright Savings heuristic algorithm*

-----------------------------------------------------------------

#### End users
This repository is supposed to be useful for people who have to quickly implement the Clarke &amp; Wright Savings (CWS) algorithm or a similar version inspired by it.

#### Structure 
The main elements are:
- the main `ClarkeWrightSavings` class representing the algorithm instance;
- the `CWSConfiguration` class representing a particular configuration of parameters;
- the `Edge` and `Node` classes from which the respective new implementations have to inherit.

#### Usage 
Let's suppose we want to implement the CWS to a classsic Vehicle Routing Problem (VRP). In this case, our nodes will be the customers to visit, and the edges will be the streets connecting customers to each other.

So, first, let's go to import the CWS package.
```
import cws
```
