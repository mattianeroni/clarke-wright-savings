import cws
import random
import math
import itertools

def distance (city1, city2):
    return int(math.sqrt(math.pow(city1[0] - city2[0], 2) + math.pow(city1[1] - city2[1], 2)))


def random_customer (id):
    return Customer(id, (random.randint(0, 100), random.randint(0, 100)))


def get_streets (customers):
    streets = []
    for i, j in itertools.combinations(customers, 2):
        saving = i.nd_edge.cost + j.dn_edge.cost - distance(i.city, j.city)
        cost = distance(i.city, j.city)
        s = Street(i, j, saving, cost)
        s_inverse = Street(j, i, saving, cost)
        s.inverse, s_inverse.inverse = s_inverse, s
        streets.append(s)
    return tuple(streets)


depot = (0, 0)


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


customers = tuple(random_customer(i) for i in range(20))
streets = get_streets(customers)



if  __name__ == "__main__":
    print("Program...", end="")
    config = cws.CWSConfiguration(
        biased = True,
        reverse = True,
        metaheuristic = True,
        start = None,
        maxiter = 1000,
        maxnoimp = 500,
        maxcost = float("inf"),
        minroutes = 5,
    )
    solver = cws.ClarkeWrightSavings(nodes=customers, edges=streets)
    sol, cost = solver.__call__(config)
    print("done")

    for route in sol:
        print(route)
