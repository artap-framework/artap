from abc import *


class Individual(metaclass=ABCMeta):
    """
       Collects information about one point in design space.
    """

    def __init__(self, vector: list):
        self.vector = vector.copy()
        self.costs = []
        self.is_evaluated = False

    def __repr__(self):
        """ :return: [vector[p1, p2, ... pn]; costs[c1, c2, ... cn]] """

        string = "vector: ["
        for i, number in enumerate(self.vector):
            string += str(number)
            if i < len(self.vector)-1:
                string += ", "
        string = string[:len(string) - 1]
        string += "]"

        string += "; costs:["
        for i, number in enumerate(self.costs):
            string += str(number)
            if i < len(self.costs)-1:
                string += ", "
        string += "]"

        return string

    def sync(self, individual):
        self.vector = individual.vector
        self.costs = individual.costs
        self.is_evaluated = individual.is_evaluated

    # deprecated
    # def to_list(self):
    #     params = [self.vector, self.costs]
    #     # flatten list
    #     out = [val for sublist in params for val in sublist]
    #     # front_number
    #     if self.front_number is None:
    #         out.append(0)
    #     else:
    #         out.append(self.front_number)
    #     # crowding_distance
    #     if self.crowding_distance is None:
    #         out.append(0)
    #     else:
    #         out.append(self.crowding_distance)
    #     # feasible
    #     if self.feasible is None:
    #         out.append(0)
    #     else:
    #         out.append(self.feasible)
    #     if self.depends_on is None:
    #         out.append(-1)
    #     else:
    #         out.append(self.depends_on)
    #     out.append(self.modified_param)
    #     # dominates
    #     dominates = []
    #     out.append(dominates)
    #     # gradient
    #     out.append(self.gradient)
    #     return out
